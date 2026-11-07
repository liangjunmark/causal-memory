# CodeGraph 与代码证据

1. 先确认查询根是本 checkout，记录 Git commit 和工作树差异。
2. 有根 `.codegraph/` 时优先 MCP `codegraph_explore`，传明确
   `projectPath`；否则在本根运行 `codegraph explore "路径 符号 问题"`。
3. 使用单一查询字符串，路径加具体符号。已有结果无需再 grep 重读。
4. 未索引时记录 `unavailable`，使用 `rg --files`、`rg -n` 和精确文件读取。
   不查询 XCS 索引来冒充本项目结果，不隐式运行 `codegraph init`。
5. stale、disabled sync 或缺失新文件时，仅回查受影响文件；索引初始化
   或重建是明确维护操作，遵从工具及用户授权。保持单根，不建嵌套索引。

CodeGraph 生成的是结构线索，不能证明业务意图、动态行为或测试通过。
关系绑定保存仓库身份、commit、路径、符号/签名和内容摘要；行号只作导航。
读取代码形成 `as_is`；提出目标合同保存为 `to_be/proposed`，人工确认后
才能作为实现要求。修改代码后重新检查相关绑定与证据是否过期。

本次已生成客户端 CodeGraph 配置，但未创建索引，结构查询尚未验收。
后续明确初始化后再记录索引版本、范围及代表性符号查询结果。
