# 独立工程 bootstrap 交接

此文件先作为待发布的交接记录。配置与发布期间的唯一活动游标由发起工程
`cm-external-project-bootstrap-20261107` 持有；发布成功后在这里封存结果。
本记录不启动逆向试点，也不自动转入实现阶段。

## 授权与边界

用户授权在父目录下新建子目录克隆自己的 fork，配置独立 CM、memory
和工作流，并允许提交推送。实际目录是 `causal-memory` 子目录；
研究源基线 `b05d671fc45d1f73c99c36a58f05c0bdd673cb88`。
本阶段不改引擎、不运行 XAPS/Yuto、不导入其他项目 DB、不做 CM 快照同步。

## 当前验证

- 生成项目 `.mcp.json` / `.codex/config.toml`，CodeGraph 显式绑定本根。
- Codex 信任设置只新增本目录；有效项目配置已核验，原 XCS 绑定保持原值。
  新设置不表示既有宿主热切换；Claude 宿主连接尚未验证。
- 独立 stdio MCP initialize/list/search/record 成功，17 tools，目标 DB schema15。
  服务 SHA-256 为 `6d4c040edb060d1c637d8be0b77741c9040462036ba987885f0489db4fd9e1ed`；
  MCP 返回 rmcp/2.2.0 不是产品版本，不能据此与源码版本等同。
- 目标单元开始于 `2026-11-07T16:09:19.487606+00:00`（运行时钟）。
  查询 `cm.workflow 独立项目 初始化 causal-memory memory/INDEX.md 逆向学习`；
  recall 2，无命中、无采用的旧 source ID；当前配置/Git/DB 分别直接核源。
  首个诊断 recall 1 因 stdin 中文编码丢失排除，未作为知识写入依据。
- fact 1 `cm.workflow.project_memory_boundary` 已回读有效、元数据正确，
  无同范围重复/冲突。closure 与 recall 2 对齐通过；无旧记录待纠正。
- 三个脚本语法通过；错库、旧回执、不存在 fact 的负对照均正确拒绝。
  配置生成幂等，遇已有不同配置时保持原文件。上述为配置/工作流运行证据。
- CodeGraph 索引不存在；结构查询、Rust 构建、产品行为测试、性能、知识包
  导出导入及语义替换均 `not_run`。设计方案仍为 proposed。

## 发布

待完成仓库链接/容量检查、staged diff 审阅及授权 Git 提交推送。
DB、配置、探测脚本与日志均在忽略范围，不属于发布内容。

## 下一阶段

从 [逆向试点计划](../../docs/engineering/reverse-pilot.md) 选择首个能力；
获得实施范围后创建新的 checkpoint。先现状映射及人工校准，再根据实测
缺口决定 CM 扩展；XAPS 校准保持在原项目，Yuto 替换验证另行推进。
