---
# 元信息层 (Metadata Layer)
name: github-collector
version: 1.0.0
description: 收集和分析GitHub项目的Skill，支持搜索项目、获取仓库信息、分析代码统计等功能
author: Qoder
triggers:
  - github
  - 收集github
  - 搜索仓库
  - 获取项目信息
inputs:
  - query: 搜索关键词或仓库地址
  - action: 操作类型 (search/info/stats)
outputs:
  - format: markdown
  - content: 项目信息/搜索结果/统计分析
dependencies:
  - python3
  - requests库
---

# GitHub项目收集器

## 简介

本Skill用于收集、搜索和分析GitHub上的开源项目，支持以下功能：
- 根据关键词搜索GitHub仓库
- 获取指定仓库的详细信息
- 分析仓库的代码统计和贡献者信息
- 生成项目概览报告

## 指令层 (Instruction Layer)

### 指令1: 搜索仓库 (search)

**功能描述**: 根据关键词搜索GitHub上的公开仓库

**输入参数**:
- `query` (必需): 搜索关键词
- `language` (可选): 编程语言筛选，如 python, javascript
- `sort` (可选): 排序方式，可选 stars/forks/updated，默认 stars
- `limit` (可选): 返回结果数量，默认 10

**调用方式**:
```bash
python scripts/search_repos.py --query "machine learning" --language python --sort stars --limit 10
```

**预期输出**: Markdown格式的仓库列表，包含名称、描述、星标数、fork数等信息

---

### 指令2: 获取仓库信息 (info)

**功能描述**: 获取指定GitHub仓库的详细信息

**输入参数**:
- `repo` (必需): 仓库地址，格式为 "owner/repo"

**调用方式**:
```bash
python scripts/get_repo_info.py --repo "torvalds/linux"
```

**预期输出**: 包含仓库描述、星标数、语言、创建时间、最后更新等详细信息的Markdown文档

---

### 指令3: 分析仓库统计 (stats)

**功能描述**: 分析指定仓库的代码统计信息

**输入参数**:
- `repo` (必需): 仓库地址，格式为 "owner/repo"

**调用方式**:
```bash
python scripts/analyze_stats.py --repo "microsoft/vscode"
```

**预期输出**: 包含代码行数、语言分布、贡献者数量等统计信息的报告

---

## 资源层 (Resource Layer)

### reference/
- [GitHub API使用指南](reference/github_api_guide.md) - GitHub API的详细使用说明和示例
- [搜索结果格式说明](reference/output_format.md) - 输出格式的详细规范

### scripts/
- [search_repos.py](scripts/search_repos.py) - 搜索GitHub仓库的Python脚本
- [get_repo_info.py](scripts/get_repo_info.py) - 获取仓库详细信息的脚本
- [analyze_stats.py](scripts/analyze_stats.py) - 分析仓库统计信息的脚本
- [github_utils.py](scripts/github_utils.py) - 共享工具函数

### assets/
- 暂无静态资源

## 使用示例

### 示例1: 搜索热门的Python机器学习项目
```
触发: 收集github machine learning
参数: language=python, sort=stars, limit=5
```

### 示例2: 获取特定仓库信息
```
触发: 获取项目信息 facebook/react
```

### 示例3: 分析仓库统计
```
触发: 分析github仓库 kubernetes/kubernetes
```

## 注意事项

1. GitHub API有请求频率限制，未认证用户每小时60次请求
2. 建议配置GitHub Token以提高请求限制（每小时5000次）
3. 搜索功能仅支持公开仓库
4. 部分仓库信息可能需要更长时间获取

## 配置说明

如需配置GitHub Token，请设置环境变量：
```bash
export GITHUB_TOKEN="your_github_token_here"
```

或在Windows PowerShell中：
```powershell
$env:GITHUB_TOKEN="your_github_token_here"
```
