# CM 检索、记录与纠正

## 身份与 preflight

1. 首次使用或服务重启后，核对实际启用的客户端配置、进程工作目录与
   `CAUSAL_MEMORY_DB`，必须指向此根目录 `.causal-memory/causal.db`。
   文件存在不证明当前会话已经换库；从其他工程继续的会话仍可能连旧库。
2. 重要设计、实现、业务解释或配置前，记下单元开始时间，执行一次
   `search_memory(query, limit=5, max_tokens=2500)`。中文问题包含业务词
   和文件/符号等技术标识。不为机械续作重复检索。
3. 在 checkpoint 留 recall ID、运行时、命中/未命中、实际采用的至多
   五个 source ID、适用性与排除理由；回查实际源码、文档或配置。
   返回超过五项时仍只采用五项，不能宣称已修复服务的全局 top-K。
4. 进入编辑/运行前用核验器检查实际注册与精确查询回执：

```text
python scripts/check_cm_receipts.py preflight --config .mcp.json --since <ISO时间含时区> --runtime <服务及合同> --query <完整原查询>
```

Codex 使用 `.codex/config.toml` 或经核对的有效注册；Python 3.10 解析
TOML 需要已有 `tomli`，Python 3.11+ 使用标准库。JSON 不需额外依赖。
检查配置文件不是对宿主热加载的证明。MCP 不可用或误绑时暂停依赖它的编辑；
已授权的独立配置修复可由已核验的 bootstrap 单元完成。

## 记录与分类

稳定事实用 `record_fact`；真实行动及可复用观察用 `record_decision`。
不机械配对，不把进度、设计愿望或“文件已写”记录为成功经验。
事实 value / 决策 context 首行按 [登记表](../causal-memory-blocks.json) 标注：

```text
cm_meta={"block":"cm.workflow","related_blocks":[],"classification_status":"assigned","registry_version":1}
```

元数据目前是文本约定，不能提供原生过滤或隔离。正文保留来源、版本、
适用应用与运行时。`task_tag` 是主题，`scope` 是 API 原生范围，不能替代分区。
新 fact key 用分区前缀与稳定语义名，不用日期。归属未知留待校准。
`confidence_source` 只能取 `temporal/rule/llm_inferred/user_feedback`。
写后回读 ID、正文元数据和有效状态，并检查同范围重复/冲突候选。

执行状态 `pending/implemented/verified/blocked/superseded` 与证据
`code_verified/runtime_verified/output_verified/inferred/not_run/blocked`
分别记录。人工确认不证明实现运行正确，测试定义不证明测试通过。

## 纠正与闭环

纠正先列旧 fact/decision ID，选择 `supersedes`、`retains_with_scope`
或 `invalidates`。先写并回读替代记录，再软失效已推翻的范围；保留历史。
`replace_same_key` 仅覆盖同 key 同 scope；不据此宣称实现全局单值约束。
未完成的纠正留 checkpoint。中断或未知回执先只读回查 DB 和工作树，不盲重试。

```text
python scripts/check_cm_receipts.py closure --config .mcp.json --recall-id <本单元最新ID> --fact <实际新ID>
python scripts/check_cm_receipts.py closure --config .mcp.json --recall-id <本单元最新ID> --no-new-knowledge <具体理由>
```

支持多个 `--fact` / `--decision` / `--retired-decision`。closure 证明回执
存在和状态符合要求，不能替代语义对应、正确写入次序与业务验收。
检查器只读 DB，最近成功 preflight 的关联存入忽略的本机目录；若并行任务
更新它，重新核验本任务精确查询再 closure，不冒用别的任务回执。

真实未决二选一才用 `counterfactual_query`；高风险难回退操作才用
`intervention_query`。不补造已经决定的备选。
`remember/distill/extract/judge/reasoning`、批量迁移、快照和 CM 同步
需明确授权；自动整理与隐式 LLM 调用不属于日常记录。

DB 只读检查用 SQLite `mode=ro`；查询 MCP 本身可能写审计或统计。
外层 Git 提交按 [交付流程](delivery.md)，不自动提交 `.cm` 或数据库。
