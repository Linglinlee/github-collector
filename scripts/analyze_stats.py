#!/usr/bin/env python3
"""
分析GitHub仓库统计信息脚本
分析仓库的代码统计、贡献者信息等
"""

import argparse
import sys
from datetime import datetime

from github_utils import (
    GitHubClient, format_number, parse_repo_string,
    print_error, print_info
)


def analyze_repository(repo_str: str) -> str:
    """
    分析仓库统计信息并返回格式化的Markdown
    
    Args:
        repo_str: 仓库字符串，如 "owner/repo"
        
    Returns:
        Markdown格式的分析报告
    """
    client = GitHubClient()
    
    try:
        owner, repo = parse_repo_string(repo_str)
        print_info(f"正在分析仓库: {owner}/{repo}...")
        
        # 获取基本信息
        repo_info = client.get_repository(owner, repo)
        
        # 获取语言统计
        try:
            languages = client.get_languages(owner, repo)
        except Exception:
            languages = {}
        
        # 获取贡献者信息
        try:
            contributors = client.get_contributors(owner, repo, per_page=10)
        except Exception:
            contributors = []
        
        # 构建Markdown输出
        md_lines = []
        
        name = repo_info.get('full_name', f'{owner}/{repo}')
        md_lines.append(f"# 📊 {name} 统计分析")
        md_lines.append("")
        
        # 总体概览
        md_lines.append("## 📈 总体概览")
        md_lines.append("")
        
        stars = repo_info.get('stargazers_count', 0)
        forks = repo_info.get('forks_count', 0)
        watchers = repo_info.get('watchers_count', 0)
        open_issues = repo_info.get('open_issues_count', 0)
        
        md_lines.append(f"| 指标 | 数值 | 评级 |")
        md_lines.append(f"|------|------|------|")
        
        # 根据星标数评级
        if stars >= 10000:
            star_rating = "🔥🔥🔥 热门"
        elif stars >= 1000:
            star_rating = "🔥🔥 受欢迎"
        elif stars >= 100:
            star_rating = "🔥 有潜力"
        else:
            star_rating = "⭐ 小众"
        
        md_lines.append(f"| ⭐ Stars | {format_number(stars)} | {star_rating} |")
        md_lines.append(f"| 🍴 Forks | {format_number(forks)} | - |")
        md_lines.append(f"| 👀 Watchers | {format_number(watchers)} | - |")
        md_lines.append(f"| 🐛 Open Issues | {format_number(open_issues)} | - |")
        md_lines.append("")
        
        # 代码统计
        md_lines.append("## 💻 代码统计")
        md_lines.append("")
        
        if languages:
            total_bytes = sum(languages.values())
            md_lines.append(f"**总代码量**: {format_number(total_bytes)} 字节")
            md_lines.append("")
            
            md_lines.append("### 语言分布详情")
            md_lines.append("")
            md_lines.append(f"| 语言 | 代码量 | 占比 | 可视化 |")
            md_lines.append(f"|------|--------|------|--------|")
            
            sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
            for lang, bytes_count in sorted_langs[:10]:
                percentage = (bytes_count / total_bytes) * 100
                bar = '█' * int(percentage / 10)
                md_lines.append(f"| {lang} | {format_number(bytes_count)} | {percentage:.1f}% | {bar} |")
            
            md_lines.append("")
            md_lines.append(f"**语言种类数**: {len(languages)}")
            md_lines.append("")
        else:
            md_lines.append("无法获取语言统计信息")
            md_lines.append("")
        
        # 社区活跃度分析
        md_lines.append("## 👥 社区活跃度")
        md_lines.append("")
        
        if contributors:
            md_lines.append(f"**主要贡献者数量**: {len(contributors)}")
            md_lines.append("")
            md_lines.append("### 顶级贡献者")
            md_lines.append("")
            md_lines.append(f"| 排名 | 用户 | 贡献次数 | 头像 |")
            md_lines.append(f"|------|------|----------|------|")
            
            for i, contributor in enumerate(contributors[:5], 1):
                login = contributor.get('login', 'Unknown')
                contributions = contributor.get('contributions', 0)
                avatar_url = contributor.get('avatar_url', '')
                html_url = contributor.get('html_url', '')
                
                # 使用GitHub头像链接
                avatar_md = f"![{login}]({avatar_url}&s=50)" if avatar_url else "-"
                user_link = f"[{login}]({html_url})" if html_url else login
                
                md_lines.append(f"| {i} | {user_link} | {contributions} | {avatar_md} |")
            
            md_lines.append("")
            
            # 计算总贡献
            total_contributions = sum(c.get('contributions', 0) for c in contributors)
            md_lines.append(f"**前{len(contributors)}名贡献者总提交数**: {format_number(total_contributions)}")
            md_lines.append("")
        else:
            md_lines.append("无法获取贡献者信息")
            md_lines.append("")
        
        # Fork比率分析
        if stars > 0:
            fork_ratio = (forks / stars) * 100
            md_lines.append(f"**Fork/Star 比率**: {fork_ratio:.1f}%")
            md_lines.append(f"- 说明: 每100个star中有约{fork_ratio:.0f}个fork")
            md_lines.append("")
        
        # Issue响应率估算
        if open_issues > 0:
            md_lines.append(f"**待处理Issues**: {format_number(open_issues)}")
            md_lines.append("")
        
        # 项目健康度评估
        md_lines.append("## 🏥 项目健康度评估")
        md_lines.append("")
        
        updated_at = repo_info.get('updated_at', '')
        if updated_at:
            update_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            days_since_update = (datetime.now(update_date.tzinfo) - update_date).days
            
            if days_since_update < 7:
                activity_status = "🟢 非常活跃"
            elif days_since_update < 30:
                activity_status = "🟡 活跃"
            elif days_since_update < 90:
                activity_status = "🟠 一般"
            else:
                activity_status = "🔴 不活跃"
            
            md_lines.append(f"- **最近更新**: {days_since_update}天前 ({activity_status})")
        
        archived = repo_info.get('archived', False)
        if archived:
            md_lines.append(f"- **项目状态**: ⚠️ 已归档（不再维护）")
        else:
            md_lines.append(f"- **项目状态**: ✅ 活跃维护中")
        
        fork = repo_info.get('fork', False)
        if fork:
            md_lines.append(f"- **仓库类型**: 🍴 Fork仓库")
        else:
            md_lines.append(f"- **仓库类型**: 📦 原始仓库")
        
        md_lines.append("")
        
        # 总结
        md_lines.append("## 📝 总结")
        md_lines.append("")
        
        # 生成简短总结
        summary_parts = []
        if stars >= 1000:
            summary_parts.append("这是一个受欢迎的项目")
        if forks >= 500:
            summary_parts.append("有较高的fork参与度")
        if contributors and len(contributors) >= 5:
            summary_parts.append("拥有活跃的贡献者社区")
        if languages and len(languages) >= 3:
            summary_parts.append("使用多种编程语言")
        
        if summary_parts:
            md_lines.append("，".join(summary_parts) + "。")
        else:
            md_lines.append("这是一个相对小众的项目，适合特定场景使用。")
        
        md_lines.append("")
        
        return '\n'.join(md_lines)
        
    except Exception as e:
        print_error(str(e))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='分析GitHub仓库统计信息',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python analyze_stats.py --repo "microsoft/vscode"
  python analyze_stats.py --repo "kubernetes/kubernetes"
  python analyze_stats.py --repo "https://github.com/facebook/react"
        '''
    )
    
    parser.add_argument(
        '--repo', '-r',
        required=True,
        help='仓库地址，格式: owner/repo 或 https://github.com/owner/repo'
    )
    
    args = parser.parse_args()
    
    # 执行分析
    result = analyze_repository(args.repo)
    print(result)


if __name__ == '__main__':
    main()
