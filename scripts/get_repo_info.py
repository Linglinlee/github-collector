#!/usr/bin/env python3
"""
获取GitHub仓库详细信息脚本
获取指定仓库的完整信息概览
"""

import argparse
import sys
from datetime import datetime

from github_utils import (
    GitHubClient, format_number, parse_repo_string,
    print_error, print_info
)


def get_repository_info(repo_str: str) -> str:
    """
    获取仓库详细信息并返回格式化的Markdown
    
    Args:
        repo_str: 仓库字符串，如 "owner/repo"
        
    Returns:
        Markdown格式的仓库信息
    """
    client = GitHubClient()
    
    try:
        owner, repo = parse_repo_string(repo_str)
        print_info(f"正在获取仓库信息: {owner}/{repo}...")
        
        # 获取基本信息
        repo_info = client.get_repository(owner, repo)
        
        # 获取语言统计
        try:
            languages = client.get_languages(owner, repo)
        except Exception:
            languages = {}
        
        # 构建Markdown输出
        md_lines = []
        
        # 标题和描述
        name = repo_info.get('full_name', f'{owner}/{repo}')
        description = repo_info.get('description') or '暂无描述'
        url = repo_info.get('html_url', '')
        homepage = repo_info.get('homepage', '')
        
        md_lines.append(f"# 📦 {name}")
        md_lines.append("")
        md_lines.append(f"{description}")
        md_lines.append("")
        
        # 链接
        md_lines.append(f"🔗 **GitHub**: [{url}]({url})")
        if homepage:
            md_lines.append(f"🌐 **主页**: [{homepage}]({homepage})")
        md_lines.append("")
        
        # 统计卡片
        stars = repo_info.get('stargazers_count', 0)
        forks = repo_info.get('forks_count', 0)
        watchers = repo_info.get('watchers_count', 0)
        open_issues = repo_info.get('open_issues_count', 0)
        
        md_lines.append("## 📊 统计数据")
        md_lines.append("")
        md_lines.append(f"| ⭐ Stars | 🍴 Forks | 👀 Watchers | 🐛 Open Issues |")
        md_lines.append(f"|----------|----------|-------------|----------------|")
        md_lines.append(f"| {format_number(stars)} | {format_number(forks)} | {format_number(watchers)} | {format_number(open_issues)} |")
        md_lines.append("")
        
        # 基本信息
        md_lines.append("## 📋 基本信息")
        md_lines.append("")
        
        primary_language = repo_info.get('language') or 'Unknown'
        md_lines.append(f"- **主要语言**: {primary_language}")
        
        license_info = repo_info.get('license')
        if license_info:
            md_lines.append(f"- **许可证**: {license_info.get('name', 'Unknown')}")
        else:
            md_lines.append(f"- **许可证**: 未指定")
        
        size_kb = repo_info.get('size', 0)
        size_mb = size_kb / 1024
        md_lines.append(f"- **仓库大小**: {size_mb:.1f} MB")
        
        is_fork = repo_info.get('fork', False)
        md_lines.append(f"- **是否Fork**: {'是' if is_fork else '否'}")
        
        archived = repo_info.get('archived', False)
        md_lines.append(f"- **已归档**: {'是' if archived else '否'}")
        
        md_lines.append("")
        
        # 时间信息
        md_lines.append("## 📅 时间信息")
        md_lines.append("")
        
        created_at = repo_info.get('created_at', '')[:10]
        updated_at = repo_info.get('updated_at', '')[:10]
        pushed_at = repo_info.get('pushed_at', '')[:10]
        
        md_lines.append(f"- **创建时间**: {created_at}")
        md_lines.append(f"- **最后更新**: {updated_at}")
        md_lines.append(f"- **最后推送**: {pushed_at}")
        md_lines.append("")
        
        # 语言统计
        if languages:
            md_lines.append("## 💻 语言分布")
            md_lines.append("")
            
            total_bytes = sum(languages.values())
            sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
            
            for lang, bytes_count in sorted_langs[:8]:  # 显示前8种语言
                percentage = (bytes_count / total_bytes) * 100
                bar_length = int(percentage / 5)  # 每5%一个方块
                bar = '█' * bar_length + '░' * (20 - bar_length)
                md_lines.append(f"- **{lang}**: {bar} {percentage:.1f}%")
            
            md_lines.append("")
        
        # 主题标签
        topics = repo_info.get('topics', [])
        if topics:
            md_lines.append("## 🏷️ 主题标签")
            md_lines.append("")
            topic_tags = ' '.join([f'`{t}`' for t in topics])
            md_lines.append(topic_tags)
            md_lines.append("")
        
        # 默认分支
        default_branch = repo_info.get('default_branch', 'main')
        md_lines.append(f"**默认分支**: `{default_branch}`")
        md_lines.append("")
        
        return '\n'.join(md_lines)
        
    except Exception as e:
        print_error(str(e))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='获取GitHub仓库详细信息',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python get_repo_info.py --repo "torvalds/linux"
  python get_repo_info.py --repo "microsoft/vscode"
  python get_repo_info.py --repo "https://github.com/facebook/react"
        '''
    )
    
    parser.add_argument(
        '--repo', '-r',
        required=True,
        help='仓库地址，格式: owner/repo 或 https://github.com/owner/repo'
    )
    
    args = parser.parse_args()
    
    # 执行查询
    result = get_repository_info(args.repo)
    print(result)


if __name__ == '__main__':
    main()
