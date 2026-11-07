# 当前事实

- 本仓库是 `https://github.com/liangjunmark/causal-memory` 的独立 Git 克隆。
  Bootstrap 研究截点为 `b05d671fc45d1f73c99c36a58f05c0bdd673cb88`。
- `Cargo.toml` 定义 Rust workspace，源码包版本为 0.10.0。
  默认成员是 `crates/causal-memory` 与 `crates/causal-memory-cli`；
  Python binding 位于 `crates/causal-memory-py`，须区分其构建环境。
- 唯一活动知识库为本仓库根 `.causal-memory/causal.db`。DB、WAL、
  生成的客户端配置、运行清单和 CodeGraph 索引均为本机文件，不提交。
- [setup](../../scripts/setup_project_memory.py) 生成项目配置，不安装二进制。
  `.causal-memory/runtime.json` 保存实际服务路径、摘要和研究源码截点。
  安装的服务版本不由本仓库 Cargo 版本证明。
- 本阶段只配置工程记忆与工作流。六层追溯、原生分区、知识包裁剪、
  发布自动化均为设计提案；不能把存在说明文件当作这些功能已实现。
