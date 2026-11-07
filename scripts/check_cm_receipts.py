#!/usr/bin/env python3
"""Check CM identity and receipts using read-only SQLite (Python 3.10+).

This checks mechanical evidence, not relevance, source interpretation or causal
validity. It never retrieves memories, edits the database or installs a hook.
A successful preflight saves a local pointer for closure under .causal-memory/.
Adapted from the user's XCS tools/check_cm_receipts.py for this independent fork.
"""

from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import sys
try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10: use an existing TOML backport if available.
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        tomllib = None


class CheckError(ValueError):
    """A required receipt or identity check failed."""


def timestamp(value: str) -> int:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CheckError("--since must be an ISO timestamp with a timezone") from exc
    if parsed.tzinfo is None:
        raise CheckError("--since requires an explicit timezone")
    return int(parsed.timestamp())


def project_db(project: Path) -> Path:
    return project.resolve() / ".causal-memory" / "causal.db"


def connect(project: Path) -> sqlite3.Connection:
    db = project_db(project)
    if not db.is_file():
        raise CheckError("Project .causal-memory/causal.db is missing")
    connection = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    return connection


def check_registration(config: Path, project: Path, server: str) -> None:
    """Read only the selected server's DB path; never echo config contents."""
    if config.suffix.lower() == ".toml" and tomllib is None:
        raise CheckError("TOML configuration requires Python 3.11+ or the tomli backport")
    try:
        source = config.read_text(encoding="utf-8-sig")
        data = tomllib.loads(source) if config.suffix.lower() == ".toml" else json.loads(source)
        servers = dict(data.get("mcp_servers", data.get("mcpServers", {})))
        # Claude's per-project registrations override top-level registrations.
        for path, settings in data.get("projects", {}).items():
            if Path(path).resolve() == project.resolve():
                servers.update(settings.get("mcpServers", {}))
        registration = servers[server]
        if registration.get("enabled") is False or registration.get("disabled") is True:
            raise CheckError("Selected CM server is disabled")
        configured = Path(registration["env"]["CAUSAL_MEMORY_DB"]).expanduser()
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        # Parser exception messages may contain configuration source text.
        raise CheckError("Cannot verify the selected server's CAUSAL_MEMORY_DB registration") from exc
    if not configured.is_absolute():
        raise CheckError("CAUSAL_MEMORY_DB must be absolute; process cwd is not assumed")
    if configured.resolve() != project_db(project).resolve():
        raise CheckError("Selected CM server does not point to the project database")


def preflight(project: Path, config: Path, server: str, query: str,
              since: str, runtime: str, limit: int = 5) -> dict:
    if not query.strip() or not runtime.strip():
        raise CheckError("Query and applicable runtime/contract must be explicit")
    if limit < 1 or limit > 5:
        raise CheckError("The review budget must be between 1 and 5")
    lower_bound = timestamp(since)
    check_registration(config, project, server)
    with closing(connect(project)) as connection:
        row = connection.execute(
            "SELECT id, created_at, result_count FROM recall_audit "
            "WHERE query = ? AND created_at >= ? ORDER BY id DESC LIMIT 1",
            (query, lower_bound),
        ).fetchone()
    if row is None:
        raise CheckError("No matching project recall receipt since this decision unit began")
    warnings = []
    if row["result_count"] > limit:
        warnings.append(
            "Combined recall exceeds the review budget; select at most "
            f"{limit} relevant sources across layers, not the first {limit} per layer"
        )
    return {
        "check": "identity-and-recall",
        "status": "verified",
        "db": ".causal-memory/causal.db",
        "recall_id": row["id"],
        "recalled_at": datetime.fromtimestamp(row["created_at"], timezone.utc).isoformat(),
        "runtime": runtime,
        "returned_count": row["result_count"],
        "review_budget": limit,
        "warnings": warnings,
        "semantic_review": "Required: record hit/no-hit and check selected sources against the applicable contract before acting",
    }


def closure(project: Path, decisions: list[int], facts: list[int],
            retired_decisions: list[int], no_new_knowledge: str | None) -> dict:
    any_receipts = bool(decisions or facts or retired_decisions)
    if no_new_knowledge is not None:
        if any_receipts or not no_new_knowledge.strip():
            raise CheckError("A no-new-knowledge reason must be nonempty and cannot accompany receipts")
        return {"check": "closure", "status": "no-new-record",
                "reason": no_new_knowledge, "semantic_review": "Reason requires source review"}
    if not decisions and not facts:
        raise CheckError("Closure requires a successful new record before retiring old knowledge")
    if set(decisions) & set(retired_decisions):
        raise CheckError("A decision cannot be both current and retired")
    with closing(connect(project)) as connection:
        for table, ids, expect_active in (
            ("causal_edges", decisions, True),
            ("agent_facts", facts, True),
            ("causal_edges", retired_decisions, False),
        ):
            for record_id in ids:
                row = connection.execute(
                    f"SELECT valid_to, superseded_by FROM {table} WHERE id = ?", (record_id,)
                ).fetchone()
                if row is None:
                    raise CheckError(f"Missing {table} receipt {record_id}")
                active = row["valid_to"] is None and row["superseded_by"] is None
                if active != expect_active:
                    expected = "active" if expect_active else "retired"
                    raise CheckError(f"{table} receipt {record_id} is not {expected}")
    return {
        "check": "closure", "status": "verified",
        "decisions": decisions, "facts": facts, "retired_decisions": retired_decisions,
        "semantic_review": "Required: verify source cutoff, observed outcome, scope and replacement relationship",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    subparsers = parser.add_subparsers(dest="command", required=True)
    before = subparsers.add_parser("preflight", help="Verify configured DB and a fresh exact-query receipt")
    before.add_argument("--config", type=Path, required=True)
    before.add_argument("--server", default="causal_memory")
    before.add_argument("--query", required=True)
    before.add_argument("--since", required=True, help="Decision-unit start, ISO timestamp with timezone")
    before.add_argument("--runtime", required=True, help="Applicable runtime/contract version")
    before.add_argument("--limit", type=int, default=5)
    after = subparsers.add_parser("closure", help="Verify new records and explicitly retired decisions")
    after.add_argument("--config", type=Path, required=True)
    after.add_argument("--server", default="causal_memory")
    after.add_argument("--recall-id", type=int, required=True)
    after.add_argument("--decision", type=int, action="append", default=[])
    after.add_argument("--fact", type=int, action="append", default=[])
    after.add_argument("--retired-decision", type=int, action="append", default=[])
    after.add_argument("--no-new-knowledge")
    args = parser.parse_args(argv)
    try:
        if args.command == "preflight":
            result = preflight(args.project, args.config, args.server, args.query,
                               args.since, args.runtime, args.limit)
            pointer = {"project": str(args.project.resolve()), "query": args.query,
                       "since": args.since, "runtime": args.runtime,
                       "recall_id": result["recall_id"]}
            path = args.project / ".causal-memory/latest-preflight.json"
            temporary = path.with_suffix(".tmp")
            temporary.write_text(json.dumps(pointer, ensure_ascii=False), encoding="utf-8")
            temporary.replace(path)
        else:
            path = args.project / ".causal-memory/latest-preflight.json"
            try:
                pointer = json.loads(path.read_text(encoding="utf-8"))
                if pointer["project"] != str(args.project.resolve()):
                    raise CheckError("Preflight belongs to another project")
                if pointer["recall_id"] != args.recall_id:
                    raise CheckError("Closure must use the latest successful preflight receipt")
                current = preflight(args.project, args.config, args.server,
                                    pointer["query"], pointer["since"], pointer["runtime"])
                if current["recall_id"] != args.recall_id:
                    raise CheckError("A newer recall exists for this query; revalidate preflight")
            except (OSError, ValueError, KeyError, TypeError) as exc:
                raise CheckError("Missing, stale or mismatched preflight; revalidate the exact unit") from exc
            result = closure(args.project, args.decision, args.fact,
                             args.retired_decision, args.no_new_knowledge)
            result["recall_id"] = args.recall_id
    except CheckError as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False))
        return 1
    except sqlite3.Error:
        print(json.dumps({"status": "failed", "error": "Project CM database unavailable or schema unsupported"}))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
