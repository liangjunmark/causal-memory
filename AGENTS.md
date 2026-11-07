# Working in this fork

- First read `memory/INDEX.md`; resume from the named checkpoint instead of
  repeating discovery. User instructions take precedence over repository rules.
- The research target is this Git checkout. The CM service used to work on it
  can be a different binary: record both identities and never equate versions.
- Before substantive design, interpretation, implementation or configuration,
  follow `memory/workflows/causal-memory.md`: verify the actual binding, perform
  one bounded recall, check sources and save the receipt before acting.
- Use only this root's `.causal-memory/causal.db` as the active project memory.
  Never copy another project's database or fall back to a user-wide database.
  Every CLI call carries explicit `--db`; recall itself can write audit data.
- Load `memory/workflows/code-navigation.md` before code discovery. Use an
  existing root CodeGraph index first; fall back explicitly when unavailable.
- Long tasks use one checkpoint under `memory/checkpoints/`; record decisions,
  exact cursor, pending handle and verification limits before a phase change.
- Follow `memory/workflows/delivery.md` for scoped Git changes and checks. Keep
  implementation status separate from code/runtime/output evidence.
- Snapshot, sync, import, restore, batch extraction and `remember`, `distill`,
  `extract`, `judge`, `reasoning` need explicit authorization. Source Git
  commit/push permission does not grant permission to publish CM data.
- Do not install hooks, global skills, automatic cleanup or recurring jobs as
  a side effect. Do not automatically initialize/rebuild CodeGraph indexes.
- Bootstrap authorizes repository/workflow configuration only. Reverse learning,
  engine extensions and reference-library integration remain proposed until
  their implementation scope is approved.
