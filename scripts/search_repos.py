#!/usr/bin/env python3
"""
搜索GitHub仓库脚本
根据关键词搜索GitHub上的公开仓库
"""

import argparse
import sys
from typing import Optional

from github_utils import GitHubClient, format_number, print_error, print_info


def search_repositories(query: str, language: Optional[str] = None,
                       sort: str = 'stars', limit: int = 10) -> str:
    """
    搜索GitHub仓库并返回格式化的Markdown结果
    
    Args:
        query: 搜索关键词
        language: 编程语言筛选
        sort: 排序方式
        limit: 返回结果数量
        
    Returns:
        Markdown格式的搜索结果
    """
    client = GitHubClient()
    
    try:
        print_info(f"正在搜索: '{query}'...")
        if language:
            print_info(f"语言筛选: {language}")
        
        result = client.search_repositories(
            query=query,
            language=language,
            sort=sort,
            per_page=limit
        )
        
        total_count = result.get('total_count', 0)
        items = result.get('items', [])
        
        # 构建Markdown输出
        md_lines = []
        md_lines.append(f"# 🔍 GitHub 搜索结果: '{query}'")
        md_lines.append("")
        md_lines.append(f"**找到约 {total_count} 个仓库** | 显示前 {len(items)} 个")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        
        if not items:
            md_lines.append("未找到匹配的仓库。")
            return '\n'.join(md_lines)
        
        for i, repo in enumerate(items, 1):
            name = repo.get('full_name', 'Unknown')
            description = repo.get('description') or '暂无描述'
            url = repo.get('html_url', '')
            stars = repo.get('stargazers_count', 0)
            forks = repo.get('forks_count', 0)
            language_info = repo.get('language') or 'Unknown'
            topics = repo.get('topics', [])
            updated_at = repo.get('updated_at', '')[:10]  # 只取日期部分
            
            md_lines.append(f"## {i}. [{name}]({url})")
            md_lines.append("")
            md_lines.append(f"{description}")
            md_lines.append("")
            
            # 统计信息行
            stats = []
            stats.append(f"⭐ {format_number(stars)}")
            stats.append(f"🍴 {format_number(forks)}")
            stats.append(f"📝 {language_info}")
            stats.append(f"📅 {updated_at}")
            md_lines.append(" | ".join(stats))
            
            # 主题标签
            if topics:
                topic_tags = ' '.join([f'`{t}`' for t in topics[:5]])
                md_lines.append(f"🏷️  {topic_tags}")
            
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        return '\n'.join(md_lines)
        
    except Exception as e:
        print_error(str(e))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='搜索GitHub仓库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python search_repos.py --query "machine learning" --language python
  python search_repos.py --query "react" --sort stars --limit 20
        '''
    )
    
    parser.add_argument(
        '--query', '-q',
        required=True,
        help='搜索关键词'
    )
    
    parser.add_argument(
        '--language', '-l',
        help='编程语言筛选 (如: python, javascript, go)'
    )
    
    parser.add_argument(
        '--sort', '-s',
        choices=['stars', 'forks', 'updated'],
        default='stars',
        help='排序方式 (默认: stars)'
    )
    
    parser.add_argument(
        '--limit', '-n',
        type=int,
        default=10,
        help='返回结果数量 (默认: 10, 最大: 100)'
    )
    
    args = parser.parse_args()
    
    # 执行搜索
    result = search_repositories(
        query=args.query,
        language=args.language,
        sort=args.sort,
        limit=args.limit
    )
    
    print(result)


if __name__ == '__main__':
    main()
