"""MSDynamics 365 Business Entity scope catalog (runtime).

Load docs/intake/msd365-business-entity-catalog.json built from Area Paths.xlsx Details sheet.
Do not read the Excel file at transcript runtime.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "docs" / "intake" / "msd365-business-entity-catalog.json"


def _cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def load_catalog(path: Path | None = None) -> dict[str, Any]:
    catalog_path = path or DEFAULT_CATALOG
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("catalog root must be a JSON object")
    return data


def business_entity_set(catalog: dict[str, Any]) -> set[str]:
    entities = catalog.get("business_entities", [])
    return {str(x) for x in entities}


def entry_key(domain: str, application: str, business_entity: str) -> tuple[str, str, str]:
    return (_cell(domain), _cell(application), _cell(business_entity))


def catalog_entry_keys(catalog: dict[str, Any]) -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    for entry in catalog.get("entries", []):
        if not isinstance(entry, dict):
            continue
        keys.add(
            entry_key(
                entry.get("domain", ""),
                entry.get("application", ""),
                entry.get("business_entity", ""),
            )
        )
    return keys


def story_scope_fields(row: dict[str, Any]) -> tuple[str, str, str]:
    """Read scope triple from row JSON (msd365_* keys)."""
    domain = _cell(row.get("msd365_domain"))
    application = _cell(row.get("msd365_application"))
    business_entity = _cell(row.get("msd365_business_entity"))
    return domain, application, business_entity


def story_matches_catalog(
    row: dict[str, Any], catalog: dict[str, Any]
) -> tuple[bool, str]:
    domain, application, business_entity = story_scope_fields(row)
    if not domain and not application and not business_entity:
        return False, "missing msd365_domain / msd365_application / msd365_business_entity"

    allowed_entities = business_entity_set(catalog)
    if business_entity and business_entity not in allowed_entities:
        return (
            False,
            f"business_entity '{business_entity}' is not in the catalog allow-list",
        )

    key = entry_key(domain, application, business_entity)
    if key not in catalog_entry_keys(catalog):
        return (
            False,
            f"no catalog entry for domain='{domain}', application='{application}', "
            f"business_entity='{business_entity or '(empty)'}'",
        )
    return True, ""


def validate_user_story_rows(
    rows: list[dict[str, Any]], catalog: dict[str, Any]
) -> tuple[list[str], int]:
    """Validate User Story rows in ADO row JSON. Returns (findings, critical_count)."""
    findings: list[str] = []
    critical = 0
    for idx, row in enumerate(rows, start=1):
        wit = _cell(row.get("Work Item Type"))
        if wit != "User Story":
            continue
        ok, reason = story_matches_catalog(row, catalog)
        if not ok:
            title = _cell(row.get("Title 3")) or _cell(row.get("Title 1"))
            findings.append(f"row {idx} User Story '{title}': {reason}")
            critical += 1
    return findings, critical
