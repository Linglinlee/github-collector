"""
GitHub API 工具函数模块
提供共享的HTTP请求、认证、错误处理等功能
"""

import os
import sys
import time
import requests
from typing import Dict, Any, Optional, List

# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    # 加载当前目录或上级目录的 .env 文件
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()  # 尝试加载默认位置的 .env
except ImportError:
    pass  # 如果未安装 python-dotenv，则跳过


class GitHubAPIError(Exception):
    """GitHub API 错误异常"""
    pass


class RateLimitError(GitHubAPIError):
    """API 速率限制异常"""
    pass


class GitHubClient:
    """GitHub API 客户端"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """
        初始化GitHub客户端
        
        Args:
            token: GitHub Personal Access Token，可选
        """
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Collector-Skill/1.0'
        })
        
        if self.token:
            self.session.headers['Authorization'] = f'token {self.token}'
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        发送HTTP GET请求
        
        Args:
            endpoint: API端点路径
            params: 查询参数
            
        Returns:
            JSON响应数据
            
        Raises:
            RateLimitError: 当达到API速率限制时
            GitHubAPIError: 其他API错误
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            
            # 检查速率限制
            remaining = int(response.headers.get('X-RateLimit-Remaining', 1))
            if remaining == 0:
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                raise RateLimitError(f"API速率限制已用完，重置时间: {reset_time}")
            
            # 处理HTTP错误
            if response.status_code == 401:
                raise GitHubAPIError("认证失败，请检查GitHub Token是否有效")
            elif response.status_code == 403:
                raise GitHubAPIError("访问被拒绝，可能超出API限制或没有权限")
            elif response.status_code == 404:
                raise GitHubAPIError("请求的资源不存在")
            elif response.status_code == 422:
                raise GitHubAPIError(f"请求参数错误: {response.text}")
            elif response.status_code >= 500:
                raise GitHubAPIError("GitHub服务器错误，请稍后重试")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise GitHubAPIError("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise GitHubAPIError("网络连接失败，请检查网络设置")
        except requests.exceptions.RequestException as e:
            raise GitHubAPIError(f"请求失败: {str(e)}")
    
    def search_repositories(self, query: str, sort: str = 'stars', 
                          order: str = 'desc', per_page: int = 10,
                          language: Optional[str] = None) -> Dict[str, Any]:
        """
        搜索GitHub仓库
        
        Args:
            query: 搜索关键词
            sort: 排序方式 (stars/forks/updated)
            order: 排序方向 (asc/desc)
            per_page: 每页结果数
            language: 编程语言筛选
            
        Returns:
            搜索结果字典
        """
        # 构建搜索查询
        search_query = query
        if language:
            search_query += f" language:{language}"
        
        params = {
            'q': search_query,
            'sort': sort,
            'order': order,
            'per_page': min(per_page, 100)  # GitHub限制最大100
        }
        
        return self._make_request('/search/repositories', params)
    
    def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        获取仓库详细信息
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            
        Returns:
            仓库详细信息
        """
        return self._make_request(f'/repos/{owner}/{repo}')
    
    def get_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """
        获取仓库语言统计
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            
        Returns:
            语言及其代码字节数
        """
        return self._make_request(f'/repos/{owner}/{repo}/languages')
    
    def get_contributors(self, owner: str, repo: str, 
                        per_page: int = 10) -> List[Dict[str, Any]]:
        """
        获取仓库贡献者列表
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            per_page: 返回的贡献者数量
            
        Returns:
            贡献者列表
        """
        params = {'per_page': per_page}
        return self._make_request(f'/repos/{owner}/{repo}/contributors', params)


def format_number(num: int) -> str:
    """
    格式化数字显示
    
    Args:
        num: 数字
        
    Returns:
        格式化后的字符串，如 1.2k, 3.5M
    """
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}k"
    else:
        return str(num)


def parse_repo_string(repo_str: str) -> tuple:
    """
    解析仓库字符串
    
    Args:
        repo_str: 仓库字符串，如 "owner/repo" 或 "https://github.com/owner/repo"
        
    Returns:
        (owner, repo) 元组
        
    Raises:
        ValueError: 格式不正确时
    """
    # 处理URL格式
    if 'github.com' in repo_str:
        parts = repo_str.rstrip('/').split('/')
        if len(parts) >= 2:
            return parts[-2], parts[-1]
    
    # 处理 owner/repo 格式
    parts = repo_str.split('/')
    if len(parts) == 2:
        return parts[0], parts[1]
    
    raise ValueError(f"无效的仓库格式: {repo_str}，请使用 'owner/repo' 格式")


def print_error(message: str):
    """打印错误信息到stderr"""
    print(f"❌ 错误: {message}", file=sys.stderr)


def print_success(message: str):
    """打印成功信息"""
    print(f"✅ {message}")


def print_info(message: str):
    """打印信息"""
    print(f"ℹ️  {message}")


def print_warning(message: str):
    """打印警告信息"""
    print(f"⚠️  {message}")
