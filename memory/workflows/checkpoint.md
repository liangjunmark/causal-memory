# 单一任务 checkpoint

每个长任务/独立阶段只用一个 `memory/checkpoints/<task>.md`，主执行者
单写。开始先复用已有活动记录；不因压缩重新发现项目或另建并行历史。

```text
Schema: task-checkpoint/v1
Task / phase:
Epoch / revision:
State: active | waiting | paused | blocked | failed | complete
Authorized scope / stop boundary:
Cursor:
Last completed action / evidence:
Pending handle / input:
Last consumed input:
Next action / stop condition:
Read-manifest delta:
CM unit: runtime; query; recall ID; sources/scope; corrections; closure
```

材料决定先记录来源与 `confirmed/proposed/open/superseded`，随后归入
相应合同，checkpoint 只留链接和未决项。完成记录不随普通流程维护改写。
等待必须有真实 handle；复用同一进程，避免重启、短轮询或重复构建。
收到结果先读、分类、记录已消费，再推进游标。

一个授权阶段持续完成配置、必要验证和交接；只因暂停、实质范围选择、
真实阻塞、既定评审门或阶段完成停止。当前游标不是每轮只做一步的限制。
`complete` 要求当前范围无遗漏验证；后续未授权阶段可以是明确的下一入口。
记录授权提交的 hash、分支和实际推送结果；未提交不能写成已发布。
