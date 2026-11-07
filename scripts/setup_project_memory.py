#!/usr/bin/env python3
"""Generate local project MCP bindings; no DB imports, hooks or global edits."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cm-command", type=Path, required=True)
    parser.add_argument("--codegraph-command", default="codegraph")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    binary = args.cm_command.expanduser()
    if not binary.is_absolute() or not binary.is_file():
        parser.error("--cm-command must name an existing absolute executable path")
    binary = binary.resolve()
    db = (root / ".causal-memory/causal.db").as_posix()
    env = {"CAUSAL_MEMORY_DB": db}
    # Codex merges project settings over user settings. Empty optional provider
    # fields prevent accidental inheritance of another project's credentials.
    for name in ("CAUSAL_MEMORY_LLM_API", "CAUSAL_MEMORY_LLM_KEY", "CAUSAL_MEMORY_LLM_MODEL",
                 "CAUSAL_MEMORY_EMBED_API", "CAUSAL_MEMORY_EMBED_KEY", "CAUSAL_MEMORY_EMBED_MODEL",
                 "DEEPSEEK_API_KEY", "OPENAI_API_KEY"):
        env[name] = ""
    cm = {"command": binary.as_posix(), "args": ["--db", db], "env": env}
    graph = {"command": args.codegraph_command,
             "args": ["serve", "--mcp", "--path", root.as_posix()]}
    servers = {"causal_memory": cm, "codegraph": graph}
    json_text = json.dumps({"mcpServers": servers}, indent=2) + "\n"
    toml_lines = ["# Generated local settings; do not commit."]
    for name, server in servers.items():
        toml_lines += [f"\n[mcp_servers.{name}]",
                       f"command = {json.dumps(server['command'])}",
                       f"args = {json.dumps(server['args'])}",
                       f"cwd = {json.dumps(root.as_posix())}"]
        if "env" in server:
            toml_lines += [f"\n[mcp_servers.{name}.env]"]
            toml_lines += [f"{key} = {json.dumps(value)}" for key, value in server["env"].items()]
    outputs = {root / ".mcp.json": json_text,
               root / ".codex/config.toml": "\n".join(toml_lines) + "\n"}
    # Validate all destinations before writing any. Existing custom configs are
    # never overwritten, even if another destination is still missing.
    for path, content in outputs.items():
        if path.exists() and path.read_text(encoding="utf-8-sig") != content:
            parser.error(f"Existing settings differ: {path}; reconcile explicitly")
    source_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    runtime = {"schema": "project-memory-runtime/v1", "project": root.as_posix(),
               "db": db, "service_command": binary.as_posix(),
               "service_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
               "target_source_commit_at_setup": source_commit,
               "source_equals_service": "not_established"}
    (root / ".causal-memory").mkdir(exist_ok=True)
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")
    (root / ".causal-memory/runtime.json").write_text(
        json.dumps(runtime, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "configured", "configs": [str(p.relative_to(root)) for p in outputs],
                      "db_started": False, "index_created": False,
                      "next": "Verify effective client settings and an explicit project-bound MCP call"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
