# 项目记忆与软件说明入口

这是本 fork 唯一的仓库知识入口；`/memory` 指此目录。
仓库文件保存可审阅的合同、设计和来源；CM 保存可检索的经验与事实；
CodeGraph 提供代码结构；Git 固定版本。它们各有职责，不相互冒充验证。

## 加载规则

1. 首次进入先读 [事实](global/facts.md) 与 [当前决策](global/decisions.md)。
2. 按下面任务选择入口；链接是路线，不要求递归读取全部文件。
3. 恢复时先读当前指令与指定 checkpoint，只补缺失或变化的上下文。
4. 历史与参考材料按需加载。权威文件仍需读取适用条款；不得因其较长而跳过。

| 任务 | 入口 |
|---|---|
| 配置本地 CM / Codex / Claude | [项目设置](../docs/engineering/project-setup.md) |
| 记忆检索、记录与纠正 | [CM 工作流](workflows/causal-memory.md) |
| 代码定位、调用链与影响范围 | [CodeGraph 工作流](workflows/code-navigation.md) |
| 需求、实现、测试、确认与发布 | [交付工作流](workflows/delivery.md) |
| 长任务恢复 | [Checkpoint 工作流](workflows/checkpoint.md) |
| 本次配置结果与下一步边界 | [Bootstrap 交接](checkpoints/bootstrap-20261107.md) |
| CM 产品现状与逆向试点 | [CM 领域入口](domains/cm/entrypoints.md) |
| 业务实现一体化方案与说明书裁剪 | [设计提案](../docs/engineering/integrated-design.md) |
| three-tier / YantrikDB 借鉴 | [参考评估](../docs/engineering/reference-assessment.md) |

## 维护预算

入口保持简短，按需专题承载细节，Git 保存历史。软预算登记在
[policy.json](policy.json)，由 `python scripts/check_project_memory.py` 报告。
不设置最低行数，不自动归档或删减未决合同，不以行数等同 token 数。
知识条目的来源、范围、修订与验证状态比字数优先。
