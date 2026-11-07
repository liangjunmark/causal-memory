# 需求到确认发布

工程流程是当前人工操作规程；自动图校验、说明书生成和发布门禁仍是提案。

| 阶段 | 可审阅产物 | 离开条件 |
|---|---|---|
| 需求 / 逆向观察 | 场景或固定源码截点，as_is 与 to_be | 来源、范围、未知项明确 |
| 澄清 | B/F 规则、行为、正反例和问题 | 阻断实现的语义已裁定 |
| 逐层设计 | R/C/A/D、接口、替换边界 | 接受的合同与建议可区分 |
| 实现 | Git 分支差异、代码绑定、样例 | 实现义务有落点 |
| 测试 / 评审 | 精确命令、输入/配置/代码摘要与结果 | 约定检查通过，缺口显式列出 |
| 业务确认 | 场景输出与确认依据 | 用户确认的是哪个版本可定位 |
| 发布 / 部署 | Git commit、制品摘要、知识视图 manifest | 相同基线，发布权限已具备 |
| 反馈 | 运行观察、缺陷/变更单、CM 经验 | 进入下一次可追溯修订 |

## 每次变更

- CM preflight → 代码/合同核源 → 明确路径的 Git 变更 → 最窄必要验证。
- Bootstrap 文档/脚本检查：`python scripts/check_project_memory.py`，
  `git diff --check`；修改配置另验 MCP 连接与项目 DB。
- Rust 改动按实际 crate/测试选择最窄 `cargo test -p ... <filter>`；
  Python binding 使用其工具链。不要为文档配置改变重跑整个 Rust workspace。
- 源码、测试存在、实际运行通过、业务确认是不同证据。远端 CI 未运行或
  尚未返回时写 `not_run/pending`，不能用本地静态检查替代。
- `git status` 后显式 `git add <paths>`，审阅 staged diff，遵从已有授权
  commit/push；不顺带发布 DB、`.cm`、配置凭据、索引、其他项目改动。
- 提交消息可用 `Capability:` / `Rule:` / `Evidence:` trailers 关联对象；
  不为追溯机械地给每个函数加注释。测试断言和符号绑定优先。
- 发布批准后才创建 tag、release 或部署；提交推送代码不等于业务发布。

覆盖修改保留旧合同与适用范围，范围内替代用 `overrides/supersedes`；
扩展用 `extends/specializes`，检查冲突和继承条件，避免改写全局历史。
代码变更使受影响的验证变为 `needs_revalidation`，不自动判历史观察错误。
