#!/usr/bin/env python3
"""Canonical ADO user-story CSV layout: write helpers + structural validation.

All `/generate-user-stories-from-transcript` CSV output must be written through
`write_csv()` and pass `validate_structure()` (also invoked by validate-user-story-csv.py).
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

USER_STORY_RE = re.compile(
    r"^As an?\s+.+\s*,?\s*I need to\s+.+\s*,?\s*so that\s+.+",
    re.IGNORECASE | re.DOTALL,
)

# Monotonic section order (rulebook ado_export_layout.row_order)
SECTION_RANK: dict[str, int] = {
    "Workshop": 0,
    "Epic": 1,
    "Feature": 2,
    "Test Case": 3,
    "User Story": 3,
    "Task": 4,
    "Issue": 5,
    "Risk": 6,
}

TEST_CASE_HEAD_RE = re.compile(
    r"^Transcript:\s*\S.+\n"
    r"Epic:\s*(?P<epic>\d+)\s*\|\s*\S.+\n"
    r"Feature:\s*(?P<feature>\d+)\s*\|\s*\S.+\n"
    r"Steps:\n"
    r"(?:\d+\.\s+\S.*\n?)+",
    re.MULTILINE,
)

# Transcript authoring does not create Epic/Feature rows; those IDs come from work-items JSON.
HIERARCHY_BEFORE_STORIES = frozenset({"Workshop"})

# ASCII hyphen bullets (Excel/ADO-friendly); do not use Unicode U+2022 (•).
AC_BULLET_PREFIX = "- "


def headers_from_rulebook(rulebook: dict[str, Any]) -> list[str]:
    cols = rulebook.get("csv", {}).get("column_order")
    if not cols:
        raise ValueError("rulebook csv.column_order missing")
    return list(cols)


def blank_row(headers: list[str]) -> dict[str, str]:
    return {h: "" for h in headers}


def ac_bullet_lines(ac: str) -> list[str]:
    return [ln.strip() for ln in ac.splitlines() if ln.strip().startswith(AC_BULLET_PREFIX)]


def acceptance_criteria_cell(*bullets: str) -> str:
    """One ASCII `- ` bullet per line (required when len(bullets) > 1)."""
    return "\n".join(f"{AC_BULLET_PREFIX}{b.strip()}" for b in bullets if b.strip())


def issue_description_cell(risk: str, impact: str, mitigation: str) -> str:
    return f"Risk: {risk.strip()}\nImpact: {impact.strip()}\nMitigation: {mitigation.strip()}"


# Characters that Excel (and some other spreadsheet tools) treat as a formula
# trigger when they are the first character of a CSV cell. A cell like
# "- Partner record is not created..." gets parsed as `-Partner` minus
# something and renders as `#NAME?` once opened in Excel. RFC4180 quoting
# alone does not prevent this -- Excel re-applies its own formula detection
# to the *unquoted* cell content after parsing the CSV. Prefixing such cells
# with a single space neutralizes the trigger while staying fully readable
# (the validator strips leading whitespace before checking the "- " bullet
# prefix, and ADO/plain-text consumers render the content unchanged).
EXCEL_FORMULA_TRIGGER_CHARS = ("=", "+", "-", "@")


def excel_safe_cell(value: str) -> str:
    """Prefix a cell value with a single space if it would be mis-parsed as
    an Excel formula (leading =, +, -, or @). No-op for empty/other values.
    """
    if value and value[0] in EXCEL_FORMULA_TRIGGER_CHARS:
        return f" {value}"
    return value


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    """RFC4180 CSV with quoted fields that contain newlines or commas.

    Cell values are passed through `excel_safe_cell()` so that bullet lists
    (Acceptance Criteria `- ` bullets) and any other field beginning with a
    formula-trigger character do not render as `#NAME?` when opened in Excel.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    for row in rows:
        missing = set(headers) - set(row.keys())
        if missing:
            raise ValueError(f"row missing columns: {sorted(missing)}")
    safe_rows = [{k: excel_safe_cell(v) for k, v in row.items()} for row in rows]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=headers,
            lineterminator="\n",
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        writer.writerows(safe_rows)


def validate_structure(
    rulebook: dict[str, Any],
    rows: list[dict[str, str]],
    row_offset: int = 2,
) -> tuple[list[str], int]:
    """Return (findings, critical_count)."""
    findings: list[str] = []
    critical = 0

    layout = rulebook.get("ado_export_layout", {})
    us_area_default = (
        rulebook.get("required_fields", {})
        .get("User Story", {})
        .get("area_path_default", "empty")
    )

    types_seen: set[str] = set()
    prev_rank = -1
    story_count = 0
    saw_story = False
    saw_test_case = False
    epic_ids: set[str] = set()
    feature_ids: set[str] = set()
    cited_pairs: list[tuple[int, str, str]] = []

    for i, row in enumerate(rows):
        line = row_offset + i
        wit = (row.get("Work Item Type") or "").strip()
        if not wit:
            findings.append(f"row {line}: missing Work Item Type")
            critical += 1
            continue

        rank = SECTION_RANK.get(wit, 99)
        if rank < prev_rank:
            findings.append(
                f"row {line}: {wit} is out of ADO section order "
                f"(expected Workshop → User Story → Task → Issue → Risk; Epic/Feature are catalog IDs, not new rows)"
            )
            critical += 1
        prev_rank = max(prev_rank, rank)

        if wit == "User Story":
            story_count += 1
            if not saw_story:
                saw_story = True
                if not HIERARCHY_BEFORE_STORIES.issubset(types_seen):
                    missing = sorted(HIERARCHY_BEFORE_STORIES - types_seen)
                    findings.append(
                        f"row {line}: first User Story before hierarchy rows present: missing {missing}"
                    )
                    critical += 1
            area = (row.get("Area Path") or "").strip()
            if us_area_default == "empty" and area:
                findings.append(
                    f"row {line}: User Story Area Path must be empty (ADO export convention)"
                )
                critical += 1
            ac = row.get("Acceptance Criteria") or ""
            if ac and "\u2022" in ac:
                findings.append(
                    f"row {line}: Acceptance Criteria must use ASCII '- ' bullets, not Unicode • (U+2022)"
                )
                critical += 1
            bullet_lines = ac_bullet_lines(ac)
            if ac and not bullet_lines:
                findings.append(
                    f"row {line}: Acceptance Criteria must use lines starting with '- ' (hyphen + space)"
                )
                critical += 1
            else:
                for ac_line in ac.splitlines():
                    if ac_line.count(AC_BULLET_PREFIX) > 1:
                        findings.append(
                            f"row {line}: Acceptance Criteria must use one '- ' bullet per line, not multiple on one line"
                        )
                        critical += 1
                        break
                if len(bullet_lines) >= 2 and len(ac.splitlines()) < 2:
                    findings.append(
                        f"row {line}: Acceptance Criteria must use one '- ' bullet per line, not a single line"
                    )
                    critical += 1

        if wit in ("Issue", "Risk"):
            ac = (row.get("Acceptance Criteria") or "").strip()
            if ac:
                findings.append(f"row {line}: {wit} must have empty Acceptance Criteria")
                critical += 1
            desc = row.get("Description") or ""
            for label in ("Risk:", "Impact:", "Mitigation:"):
                if label not in desc:
                    findings.append(f"row {line}: {wit} Description must include {label}")
                    critical += 1

        if wit == "Workshop":
            area = (row.get("Area Path") or "").strip()
            if layout.get("workshop_row") and not area:
                findings.append(f"row {line}: Workshop should include Area Path when known")
                # warning only — not critical

        if wit == "Epic":
            epic_id = (row.get("ID") or "").strip()
            if epic_id:
                epic_ids.add(epic_id)
        if wit == "Feature":
            feature_id = (row.get("ID") or "").strip()
            if feature_id:
                feature_ids.add(feature_id)

        if wit == "Test Case":
            if not saw_test_case:
                saw_test_case = True
                if "Epic" not in types_seen or "Feature" not in types_seen:
                    findings.append(
                        f"row {line}: Test Case before Epic and Feature catalog rows"
                    )
                    critical += 1
            if (row.get("ID") or "").strip():
                findings.append(f"row {line}: Test Case ID must be blank")
                critical += 1
            desc = row.get("Description") or ""
            match = TEST_CASE_HEAD_RE.search(desc.strip())
            if not match:
                findings.append(
                    "row {line}: Test Case Description must be "
                    "Transcript / Epic: <id> | <title> / Feature: <id> | <title> / Steps".format(
                        line=line
                    )
                )
                critical += 1
            else:
                cited_pairs.append((line, match.group("epic"), match.group("feature")))
            ac = row.get("Acceptance Criteria") or ""
            if ac and "\u2022" in ac:
                findings.append(
                    f"row {line}: Acceptance Criteria must use ASCII '- ' bullets, not Unicode • (U+2022)"
                )
                critical += 1
            if not ac_bullet_lines(ac):
                findings.append(
                    f"row {line}: Test Case Acceptance Criteria must use lines starting with '- '"
                )
                critical += 1

        types_seen.add(wit)

    if story_count and "Workshop" not in types_seen:
        findings.append("file: at least one Workshop row required when User Stories are present")
        critical += 1

    if saw_test_case:
        for line, epic_id, feature_id in cited_pairs:
            if epic_id not in epic_ids:
                findings.append(
                    f"row {line}: Test Case Epic {epic_id} is not an Epic row ID in this file"
                )
                critical += 1
            if feature_id not in feature_ids:
                findings.append(
                    f"row {line}: Test Case Feature {feature_id} is not a Feature row ID in this file"
                )
                critical += 1

    return findings, critical


def validate_row_content(
    rulebook: dict[str, Any],
    rows: list[dict[str, str]],
    row_offset: int = 2,
) -> tuple[list[str], int]:
    """Field-level rules (narrative, AC presence)."""
    findings: list[str] = []
    critical = 0
    required_by_type = rulebook.get("required_fields", {})
    allowed_types = set(rulebook.get("work_item_types", {}).get("allowed", []))

    for i, row in enumerate(rows):
        line = row_offset + i
        wit = (row.get("Work Item Type") or "").strip()
        if wit not in allowed_types:
            continue
        for col in required_by_type.get(wit, {}).get("required", []):
            if col == "workshop_governance_columns":
                continue
            if not (row.get(col) or "").strip():
                findings.append(f"row {line} ({wit}): required column '{col}' is empty")
                critical += 1
        if wit == "User Story":
            desc = row.get("Description") or ""
            if not USER_STORY_RE.search(desc):
                findings.append(
                    f"row {line}: User Story Description must match "
                    "'As a <role>, I need to ..., so that ...'"
                )
                critical += 1
    return findings, critical
