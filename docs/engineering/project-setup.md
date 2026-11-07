# 本地工程设置

仓库知识入口是 [memory/INDEX.md](../../memory/INDEX.md)。本目录独立于
`causal-memory-main` 等参考包；源码 Git 发布不携带其他项目的记忆。

## 生成配置

Python 3.10+，准备一个可执行的 CM 服务，然后在仓库根运行：

```text
python scripts/setup_project_memory.py --cm-command <服务可执行文件绝对路径>
python scripts/check_project_memory.py
```

脚本生成忽略的 `.mcp.json`、`.codex/config.toml` 和
`.causal-memory/runtime.json`。所有 DB 和 CodeGraph 根路径都是绝对路径；
不依赖宿主当前目录，不创建索引，不导入记忆，不安装 hooks。
配置相同时可重复执行；遇到不同的已有配置会停止，须明确合并，不能盲覆盖。
移动仓库后也须重新核对路径、更新本机配置，不能沿用旧 DB 指向。

服务可以使用已有安装；该二进制不是本 fork 已构建产物。
研究截点和服务 SHA-256 分别登记。未来升级须先验证兼容性与迁移范围。
生成配置明确清空可选 LLM/embedding 配置，避免从用户配置继承其他项目
的服务密钥；默认按当前二进制的无外部模型能力运行。需要语义检索时
另行配置并验证提供方，不把关键词召回描述成嵌入检索。

## 核对实际客户端

- Codex 只加载可信项目的 `.codex/config.toml`。在本目录启动/重新打开
  客户端，核对 `causal_memory` 的有效 DB、args、cwd；保留其他项目的绑定。
- Claude 使用项目 `.mcp.json`，按客户端实际启用状态核验。客户端若要求
  初次接受项目 MCP 配置，应在它的原生界面完成；生成文件不是启用证明。
- 当前已经打开的 XCS 会话不会因新增目录配置而热切换；不得向旧连接写入
  新项目知识。独立 stdio 连接可验证新配置，但不能冒充既有宿主已经重连。
- 核验配置时只输出必要字段。不要直接展示完整 `mcp get --json`，其中可能
  含用户配置合并而来的凭据。
- CM CLI 始终使用 `--db <本根/.causal-memory/causal.db>`，不得回落到默认库。
- CodeGraph 的配置使用 `serve --mcp --path <本根>`。本次未初始化索引；
  进入逆向阶段前可由用户明确运行 `codegraph init`，随后核验范围与查询。

运行一次有界的 `search_memory`，再按
[CM 工作流](../../memory/workflows/causal-memory.md) 核验 recall 与写入回执。
正常事实写入在已授权范围内进行；批量抽取、`.cm` 快照与同步不自动执行。

## 可移植性与验证

Git 中只保存生成器、仓库记忆、规则与校验工具。本机数据库不会随 clone
同步，因此换机器仍需生成配置及初始化独立项目库。CM 数据迁移另立明确任务。
`check_project_memory.py` 核验入口文件、相对链接目标、分区边界、大小预算
和运行数据误入 Git；它不证明语义完整性，也不检查 Markdown 标题锚点。

官方配置依据（本次读取）：
[Codex MCP](https://developers.openai.com/codex/mcp/)（现重定向至
[官方 MCP 指南](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)）。
其中明确项目可信要求，以及 stdio 的 `command/args/env/cwd` 配置。
