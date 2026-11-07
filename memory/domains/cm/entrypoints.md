# CM 领域入口

产品概览：[README](../../../README.md) / [中文 README](../../../README.zh-CN.md)。
工程入口：[逆向试点计划](../../../docs/engineering/reverse-pilot.md)。

| 主题 | 先定位的源码范围 | 注意 |
|---|---|---|
| 事实写入、去重、替换与恢复 | `crates/causal-memory/src/memory/`、`src/store/` | scope 与业务应用范围不同 |
| 统一检索、召回审计 | `crates/causal-memory/src/memory/` | 描述、源码算法、运行结果分别核验 |
| MCP / CLI 契约 | `crates/causal-memory-cli/src/server/`、`src/lib.rs` | 实际服务可能来自另一构建 |
| Python 调用 | `crates/causal-memory-py/` | 绑定存在不表示该环境已构建 |

目录栏中的简写相对同一 crate；进入代码前按
[导航流程](../../workflows/code-navigation.md) 查具体符号，避免推测接口名称。
首轮只分析事实生命周期或统一检索一个能力，先形成现状证据，再人工确认意图。
