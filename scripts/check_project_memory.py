#!/usr/bin/env python3
"""Read-only routes, partition registry, size budgets and Git hygiene checks."""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    warnings: list[str] = []
    policy = json.loads((root / "memory/policy.json").read_text(encoding="utf-8"))
    for name in policy["required"]:
        if not (root / name).is_file():
            errors.append(f"Missing required file: {name}")
    documents = [root / "AGENTS.md", root / "CLAUDE.md"]
    documents += sorted((root / "memory").rglob("*.md"))
    documents += sorted((root / "docs/engineering").rglob("*.md"))
    for doc in documents:
        if not doc.is_file():
            continue
        text = doc.read_text(encoding="utf-8-sig")
        for link in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
            link = link.strip().strip("<>")
            parsed = urlsplit(link)
            if parsed.scheme or not parsed.path:
                continue
            target = (doc.parent / unquote(parsed.path)).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                errors.append(f"Outside-repository route: {doc.relative_to(root)} -> {link}")
                continue
            if not target.exists():
                errors.append(f"Broken route: {doc.relative_to(root)} -> {link}")
    for budget in policy["soft_budgets"]:
        for path in sorted(root.glob(budget["glob"])):
            size = path.stat().st_size
            lines = len(path.read_text(encoding="utf-8-sig").splitlines())
            if size > budget["max_bytes"] or lines > budget["max_lines"]:
                warnings.append(f"Soft budget exceeded: {path.relative_to(root)} ({lines} lines, {size} bytes)")
    registry = json.loads((root / "memory/causal-memory-blocks.json").read_text(encoding="utf-8"))
    ids: set[str] = set()
    for block in registry["blocks"]:
        name = block["id"]
        if name in ids or block["key_prefix"] != name + ".":
            errors.append(f"Duplicate block or invalid key prefix: {name}")
        if not block.get("includes") or not block.get("excludes"):
            errors.append(f"Block missing inclusion/exclusion boundary: {name}")
        ids.add(name)
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode("utf-8").split("\0")
    for path in tracked:
        if path in {".mcp.json", ".codex/config.toml"} or path.startswith(
                (".causal-memory/", ".codegraph/", ".cm/")):
            errors.append(f"Local runtime/config tracked by Git: {path}")
    print(json.dumps({"status": "failed" if errors else "passed", "documents": len(documents),
                      "blocks": len(ids), "errors": errors, "warnings": warnings,
                      "limits": "File targets only; no heading, semantic coverage or runtime validation"},
                     ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
