# github-collector
## GitHub 情报专家
检查环境（需 Python 3 + requests 库）
注册指令与资源
💡 前提条件：
✅ 已安装 Python 3.6+
✅ 已安装 requests 库（pip install requests）
🔵（可选）在.env文件里配置 GITHUB_TOKEN 环境变量，提升 API 限额至 5000次/小时
### 🛠️ github-collector 是什么？
github-collector 是一个兼容 Claude Code、Qoder 等 Agent 框架的 Skill，目标只有一个：
**让 Agent 像 开源项目分析师 一样，高效、智能地从 GitHub 获取所需信息。**
它不做"低效的手动翻页"，而是聚焦任务驱动的 智能采集与分析：
- "帮我找最近热门的 Python 文档处理库"
- "分析一下 microsoft/vscode 的社区贡献情况"
- "把搜索结果导出成 CSV，我要在 Excel 里分析"
Agent 接到指令后，会自动：
✅ 智能决策：判断是否需要 GitHub Token 提升限额
✅ 执行策略：调用 REST API / 处理分页 / 聚合多维度数据
✅ 精准定位：使用高级搜索语法（language:、stars:>1000 等）
✅ 结构化解析：将原始 JSON 转为易读的 Markdown 报告
✅ 多格式导出：支持 Markdown / CSV / JSON 多种输出
## 三层架构设计，只为"懂 GitHub"
github-collector 遵循 Skill 三层设计范式：
### ✅ 元信息层（Metadata Layer）
声明能力边界：支持 search/info/stats 三种任务类型、Markdown 输出格式、依赖 python3 + requests
### ✅ 指令层（Instruction Layer）
定义原子操作：
- search —— 智能搜索仓库（支持语言筛选、多维度排序）
- info —— 获取仓库详情（描述、统计、时间线、许可证）
- stats —— 深度分析（代码语言分布、贡献者排名、健康度评估）
### ✅ 资源层（Resource Layer）
scripts/：封装 GitHubClient 核心类（认证、请求、错误处理、格式化）
- github_utils.py —— 共享工具函数（229行）
- search_repos.py —— 搜索 CLI 工具（148行）
- get_repo_info.py —— 详情查询工具（177行）
- analyze_stats.py —— 统计分析工具（246行）
reference/：提供 GitHub API 使用指南（端点说明、速率限制、错误码）
assets/：预留静态资源（如示例输出模板）
而这一切，都通过 skill.md 统一调度——Agent 读完就知道："哦，这个 Skill 能帮我搞定 GitHub 项目收集。"
