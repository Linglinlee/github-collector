# GitHub API 使用指南

## 概述

GitHub API 是 RESTful API，用于与GitHub平台进行交互。本Skill使用GitHub REST API v3。

## 基础URL

```
https://api.github.com
```

## 认证方式

### 方式1: 无认证（有限制）
- 每小时最多60次请求
- 适用于简单的搜索和查询

### 方式2: Token认证（推荐）
```bash
# 在请求头中添加
Authorization: token YOUR_GITHUB_TOKEN
```

## 主要端点

### 搜索仓库
```
GET /search/repositories?q={query}&sort={sort}&order={order}&per_page={limit}
```

**参数说明**:
- `q`: 搜索关键词，支持高级语法如 `language:python stars:>1000`
- `sort`: 排序字段（stars/forks/updated）
- `order`: 排序方向（asc/desc）
- `per_page`: 每页结果数（1-100）

**响应示例**:
```json
{
  "total_count": 1000,
  "incomplete_results": false,
  "items": [
    {
      "id": 123,
      "name": "repo-name",
      "full_name": "owner/repo-name",
      "description": "Repository description",
      "html_url": "https://github.com/owner/repo-name",
      "stargazers_count": 1000,
      "forks_count": 100,
      "language": "Python",
      "created_at": "2020-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

### 获取仓库信息
```
GET /repos/{owner}/{repo}
```

**响应示例**:
```json
{
  "id": 123,
  "name": "repo-name",
  "full_name": "owner/repo-name",
  "description": "Repository description",
  "html_url": "https://github.com/owner/repo-name",
  "stargazers_count": 1000,
  "forks_count": 100,
  "watchers_count": 100,
  "language": "Python",
  "languages_url": "https://api.github.com/repos/owner/repo-name/languages",
  "created_at": "2020-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "pushed_at": "2023-01-01T00:00:00Z",
  "size": 10000,
  "open_issues_count": 10,
  "topics": ["machine-learning", "python"],
  "license": {
    "name": "MIT License"
  }
}
```

### 获取语言统计
```
GET /repos/{owner}/{repo}/languages
```

**响应示例**:
```json
{
  "Python": 50000,
  "JavaScript": 10000,
  "HTML": 5000
}
```

### 获取贡献者列表
```
GET /repos/{owner}/{repo}/contributors
```

**响应示例**:
```json
[
  {
    "login": "username",
    "id": 123,
    "avatar_url": "https://avatars.githubusercontent.com/u/123?v=4",
    "html_url": "https://github.com/username",
    "contributions": 100
  }
]
```

## 高级搜索语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `language:` | 按编程语言筛选 | `language:python` |
| `stars:` | 按星标数筛选 | `stars:>1000` |
| `forks:` | 按fork数筛选 | `forks:>=100` |
| `created:` | 按创建时间筛选 | `created:>2020-01-01` |
| `pushed:` | 按最后推送时间筛选 | `pushed:>2023-01-01` |
| `user:` | 按用户筛选 | `user:torvalds` |
| `org:` | 按组织筛选 | `org:microsoft` |
| `topic:` | 按主题筛选 | `topic:machine-learning` |

## 错误处理

### 常见HTTP状态码

| 状态码 | 含义 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | 正常处理响应 |
| 401 | 未授权 | 检查Token是否有效 |
| 403 | 禁止访问 | 可能超出API限制 |
| 404 | 未找到 | 检查仓库是否存在 |
| 422 | 验证失败 | 检查请求参数 |
| 500 | 服务器错误 | 稍后重试 |

### 速率限制响应头

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 58
X-RateLimit-Reset: 1640995200
```

## 最佳实践

1. **使用Token认证**: 提高请求限制，避免被限流
2. **处理分页**: 大量结果需要处理分页
3. **缓存结果**: 避免重复请求相同数据
4. **错误重试**: 实现指数退避重试机制
5. **遵守规范**: 遵循GitHub API使用条款
