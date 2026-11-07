# 参考实现取舍

本评估继承 2026-11-07 源码比较的设计结论，并复核 three-tier 的 README
与架构文档。它不是参考引擎的运行测试，也不证明其宣传中的无损或零遗漏。
历史包与新 Git checkout 分别固定身份，不从相同版本号推断内容相同。

| 方法 | 取舍 | 本项目落点 |
|---|---|---|
| 热入口、按需专题、Git 历史 | 采用 | INDEX → 领域/工作流 → 来源与 Git |
| 容量巡检 | 采用并改为软上限 | policy.json + check_project_memory.py |
| 410–460 行、68KB 固定热文档 | 不套用 | 不为满足下限填充上下文；字节不等于 token |
| 规则到代码与测试关联 | 采用设计思路 | 能力卡、代码绑定、证据与变更影响 |
| 固定每百规则/两千行自动分卷 | 暂不采用 | 先按稳定责任和独立验收单元组织 |
| 自动安装 pre-commit、自动整理 | 不启用 | 显式校验命令，无隐式仓库副作用 |
| 正则命中代码守卫 | 仅作线索 | CodeGraph/源码/测试与运行证据分别核验 |

three-tier 来源包：`three-tier-memory-v2.0-universal`，README 标识 v2.0；
关键来源 `three-tier-memory/docs/ARCHITECTURE.md`、
`three-tier-memory/templates/PROJECT_NEURONS.template.json`、
`three-tier-memory/scripts/neuron_audit.py`。它提供可执行规则关联的启发，
正则和子串扫描不等于 AST 依赖闭包或业务正确性证明。

YantrikDB 参考包 core 版本 0.23.4 的既有静态比较，可供后续重新核源：

- `base/types.rs` 的 LinkType、RecordRevision：借鉴类型化关系与修订身份。
- `engine/links.rs` 的 namespace、防环与有效后继约束：借鉴结构校验，
  多客户覆盖要加范围，不能原样照搬全局单后继。
- `engine/lifecycle.rs` 的修订历史与 reason，`base/provenance.rs` 的
  来源类型一致性：减少推断被误写成事实，但不证明来源真实。
- record 与 links 可有部分成功；事务保证须按实际边界验证，不笼统宣称原子。

这些锚点均相对 `crates/yantrikdb-core/src/`。本阶段不复制其内核代码。
后续借鉴顺序是：关系/来源语义 → 修订审计 → 完整查询/导出 → 经实测再选
检索或认知算法；不以更复杂的算法替代人工语义确认。

前期设计已读取的外部参考（本阶段复用其概念，不新增实现承诺）：

- [W3C PROV-O](https://www.w3.org/TR/prov-o/)：来源、活动与修订产生关系。
- [OSLC RM](https://docs.oasis-open-projects.org/oslc-op/rm/v2.1/os/requirements-management-vocab.html)：区分分解、实现、满足和验证。
- [OSLC Configuration Management](https://docs.oasis-open-projects.org/oslc-op/config/v1.0/os/oslc-config-mgt.html)：逻辑身份与配置中的版本解析。
- [Bazel Skyframe](https://bazel.build/reference/skyframe)：显式依赖与增量失效；不把人工知识图当作完整构建图。
- [SLSA Provenance](https://slsa.dev/spec/v1.0/provenance)：制品、来源 commit 与构建输入绑定，不等于业务验收。
