# 输出格式说明

本文档详细说明GitHub收集器Skill的各种输出格式规范。

## 1. 搜索结果输出格式

### 文件: search_repos.py

**输出类型**: Markdown

**结构**:
```markdown
# 🔍 GitHub 搜索结果: '{query}'

**找到约 {total_count} 个仓库** | 显示前 {limit} 个

---

## 1. [{full_name}]({html_url})

{description}

⭐ {stars} | 🍴 {forks} | 📝 {language} | 📅 {updated_at}

🏷️  `{topic1}` `{topic2}` ...

---

## 2. [{full_name}]({html_url})
...
```

**字段说明**:
| 字段 | 说明 | 示例 |
|------|------|------|
| full_name | 仓库全名 | "microsoft/vscode" |
| html_url | GitHub链接 | "https://github.com/microsoft/vscode" |
| description | 仓库描述 | "Visual Studio Code" |
| stargazers_count | Star数量 | 150000 |
| forks_count | Fork数量 | 25000 |
| language | 主要语言 | "TypeScript" |
| updated_at | 最后更新 | "2024-01-15" |
| topics | 主题标签 | ["editor", "ide"] |

---

## 2. 仓库信息输出格式

### 文件: get_repo_info.py

**输出类型**: Markdown

**结构**:
```markdown
# 📦 {full_name}

{description}

🔗 **GitHub**: [{html_url}]({html_url})
🌐 **主页**: [{homepage}]({homepage}) (如果有)

## 📊 统计数据

| ⭐ Stars | 🍴 Forks | 👀 Watchers | 🐛 Open Issues |
|----------|----------|-------------|----------------|
| {stars} | {forks} | {watchers} | {open_issues} |

## 📋 基本信息

- **主要语言**: {language}
- **许可证**: {license.name}
- **仓库大小**: {size} MB
- **是否Fork**: 是/否
- **已归档**: 是/否

## 📅 时间信息

- **创建时间**: {created_at}
- **最后更新**: {updated_at}
- **最后推送**: {pushed_at}

## 💻 语言分布

- **{language}**: ████████████░░░░░░░░ 45.2%
...

## 🏷️ 主题标签

`{topic1}` `{topic2}` `{topic3}`

**默认分支**: `{default_branch}`
```

---

## 3. 统计分析输出格式

### 文件: analyze_stats.py

**输出类型**: Markdown

**结构**:
```markdown
# 📊 {full_name} 统计分析

## 📈 总体概览

| 指标 | 数值 | 评级 |
|------|------|------|
| ⭐ Stars | {stars} | 🔥🔥🔥 热门 |
| 🍴 Forks | {forks} | - |
| 👀 Watchers | {watchers} | - |
| 🐛 Open Issues | {open_issues} | - |

## 💻 代码统计

**总代码量**: {total_bytes} 字节

### 语言分布详情

| 语言 | 代码量 | 占比 | 可视化 |
|------|--------|------|--------|
| Python | 50k | 45.0% | ████ |
| JavaScript | 30k | 27.0% | ██ |
...

## 👥 社区活跃度

**主要贡献者数量**: {contributors_count}

### 顶级贡献者

| 排名 | 用户 | 贡献次数 | 头像 |
|------|------|----------|------|
| 1 | [user1](url) | 500 | ![avatar](url) |
...

**Fork/Star 比率**: 15.2%

## 🏥 项目健康度评估

- **最近更新**: 3天前 (🟢 非常活跃)
- **项目状态**: ✅ 活跃维护中
- **仓库类型**: 📦 原始仓库

## 📝 总结

这是一个受欢迎的项目，有较高的fork参与度，拥有活跃的贡献者社区。
```

**评级标准**:
| Star数量 | 评级 |
|----------|------|
| ≥ 10000 | 🔥🔥🔥 热门 |
| ≥ 1000 | 🔥🔥 受欢迎 |
| ≥ 100 | 🔥 有潜力 |
| < 100 | ⭐ 小众 |

**活跃度评级**:
| 天数 | 评级 |
|------|------|
| < 7天 | 🟢 非常活跃 |
| < 30天 | 🟡 活跃 |
| < 90天 | 🟠 一般 |
| ≥ 90天 | 🔴 不活跃 |

---

## 4. 错误输出格式

当发生错误时，脚本会输出到stderr:

```
❌ 错误: {error_message}
```

**常见错误类型**:
- 认证失败: "认证失败，请检查GitHub Token是否有效"
- 速率限制: "API速率限制已用完，重置时间: 1234567890"
- 资源不存在: "请求的资源不存在"
- 网络错误: "网络连接失败，请检查网络设置"

---

## 5. 信息输出格式

脚本执行过程中的信息输出:

```
ℹ️  正在搜索: 'machine learning'...
ℹ️  语言筛选: python
✅ 搜索完成
⚠️  警告: 结果可能不完整
```
