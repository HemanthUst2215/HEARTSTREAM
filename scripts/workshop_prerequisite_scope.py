"""Workshop prerequisite scope validation for user-story-rows JSON."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def load_knowledge_base(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("knowledge base root must be a JSON object")
    return data


def allowed_scope_ids(knowledge_base: dict[str, Any]) -> set[str]:
    scope = knowledge_base.get("scope", {})
    if not isinstance(scope, dict):
        return set()
    ids: set[str] = set()
    for key in ("in_scope_objectives", "in_scope_modules"):
        items = scope.get(key, [])
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict):
                item_id = _cell(item.get("id"))
                if item_id:
                    ids.add(item_id)
    return ids


def knowledge_base_has_scope(knowledge_base: dict[str, Any]) -> bool:
    scope = knowledge_base.get("scope", {})
    if not isinstance(scope, dict):
        return False
    for key in ("in_scope_objectives", "in_scope_modules"):
        items = scope.get(key, [])
        if isinstance(items, list) and len(items) > 0:
            return True
    return False


def validate_user_story_rows(
    rows: list[dict[str, Any]],
    knowledge_base: dict[str, Any],
    *,
    require_mom_fields: bool = False,
) -> tuple[list[str], int]:
    findings: list[str] = []
    critical = 0

    if not knowledge_base_has_scope(knowledge_base):
        findings.append("knowledge base missing in_scope_objectives or in_scope_modules entries")
        return findings, 1

    allowed = allowed_scope_ids(knowledge_base)

    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            findings.append(f"row {idx}: not an object")
            critical += 1
            continue
        if _cell(row.get("Work Item Type")) != "User Story":
            continue

        title = _cell(row.get("Title 3")) or _cell(row.get("Title 1"))
        refs = row.get("prerequisite_refs")
        if not isinstance(refs, list) or not refs:
            findings.append(
                f"row {idx} User Story '{title}': missing or empty prerequisite_refs"
            )
            critical += 1
        else:
            for ref in refs:
                ref_id = _cell(ref)
                if ref_id not in allowed:
                    findings.append(
                        f"row {idx} User Story '{title}': prerequisite_ref '{ref_id}' "
                        f"not in knowledge base scope IDs"
                    )
                    critical += 1

        if not _cell(row.get("transcript_locator")):
            findings.append(
                f"row {idx} User Story '{title}': missing transcript_locator"
            )
            critical += 1
        if not _cell(row.get("transcript_source_path")):
            findings.append(
                f"row {idx} User Story '{title}': missing transcript_source_path"
            )
            critical += 1

        if require_mom_fields:
            if not _cell(row.get("mom_locator")):
                findings.append(
                    f"row {idx} User Story '{title}': missing mom_locator"
                )
                critical += 1
            if not _cell(row.get("mom_source_path")):
                findings.append(
                    f"row {idx} User Story '{title}': missing mom_source_path"
                )
                critical += 1

    return findings, critical
