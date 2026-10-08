#!/usr/bin/env python3
"""Output-path existence gate.

Before any generation command writes artifacts, call this script with the
exact output paths it intends to write. If any path already exists on disk,
the script STOPS (non-zero exit) and reports the conflicting paths so the
calling agent can present a human choice: **new** (write to a
disambiguated path, e.g. a `-v2` / timestamp suffix) or **overwrite**
(explicit human confirmation required before replacing the existing file).

Agents MUST NOT silently overwrite existing artifacts. This gate exists so
every generation command (`/generate-user-stories-from-transcript`,
`/generate-transcript`, `/generate-brd`, `/generate-mom`, etc.) can reuse one
deterministic check instead of hand-rolling file-existence logic.

Usage
-----
    python scripts/output-path-gate.py --check <path1> [<path2> ...]
    python scripts/output-path-gate.py --check <path1> --json

Exit codes
----------
    0  CLEAR      - none of the given paths exist; safe to write.
    2  CONFLICT   - one or more paths already exist; STOP and ask the human
                     "new" vs "overwrite" before writing anything.
    1  USAGE/ERR  - bad arguments.

Human gate (per 09-agent-orchestration.mdc / 10-audit-trail.mdc)
------------------------------------------------------------------
On CONFLICT, the calling agent must ask the human (via AskQuestion or
equivalent) to choose:
  - "new"       -> re-run the command targeting a disambiguated path
                   (e.g. append `-v2`, `-v3`, or a fresh timestamp) and
                   re-check with this gate until CLEAR.
  - "overwrite" -> only after explicit human confirmation, proceed to write
                   over the existing path(s). Record the decision in the
                   command's audit file (`artifacts/audit/...`).
Agents must never choose on the human's behalf.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def check_paths(paths: list[str]) -> dict:
    existing = [p for p in paths if Path(p).exists()]
    missing = [p for p in paths if p not in existing]
    status = "CONFLICT" if existing else "CLEAR"
    return {
        "status": status,
        "existing": existing,
        "clear": missing,
        "checked": paths,
    }


def next_available_path(path: str, suffix_pattern: str = "-v{n}") -> str:
    """Suggest a disambiguated path for the 'new' choice (e.g. foo.csv -> foo-v2.csv)."""
    p = Path(path)
    n = 2
    while True:
        candidate = p.with_name(f"{p.stem}{suffix_pattern.format(n=n)}{p.suffix}")
        if not candidate.exists():
            return str(candidate)
        n += 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", nargs="+", required=True, metavar="PATH", help="Output path(s) the command intends to write.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON only.")
    parser.add_argument("--suggest-new", action="store_true", help="Also suggest disambiguated 'new' paths for conflicts.")
    args = parser.parse_args(argv)

    result = check_paths(args.check)

    if args.suggest_new and result["existing"]:
        result["suggested_new_paths"] = {p: next_available_path(p) for p in result["existing"]}

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["status"] == "CLEAR":
            print("RESULT: CLEAR - no existing output files; safe to proceed.")
        else:
            print("RESULT: CONFLICT - the following output path(s) already exist:")
            for p in result["existing"]:
                print(f"  - {p}")
            print(
                "STOP: ask the human to choose 'new' (write to a disambiguated path) "
                "or 'overwrite' (explicit confirmation required) before writing."
            )
            if "suggested_new_paths" in result:
                print("Suggested new paths:")
                for old, new in result["suggested_new_paths"].items():
                    print(f"  - {old} -> {new}")

    return 2 if result["status"] == "CONFLICT" else 0


if __name__ == "__main__":
    raise SystemExit(main())
