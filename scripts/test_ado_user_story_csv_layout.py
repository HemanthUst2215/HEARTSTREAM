#!/usr/bin/env python3
"""Regression tests for ADO CSV layout (run: python scripts/test_ado_user_story_csv_layout.py)."""
from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import yaml

from ado_user_story_csv_layout import (
    acceptance_criteria_cell,
    validate_structure,
    write_csv,
)
from importlib.machinery import SourceFileLoader

_validate = SourceFileLoader(
    "validate_user_story_csv",
    str(ROOT / "scripts" / "validate-user-story-csv.py"),
).load_module()


def test_good_export_passes() -> None:
    csv_path = ROOT / "artifacts/intake/.pipeline/2026-10-08-user-stories-working.csv"
    rb_path = ROOT / "docs/intake/user-story-csv-rulebook.yaml"
    rulebook = _validate.load_rulebook(rb_path)
    headers, rows = _validate.read_csv_rows(csv_path)
    result = _validate.validate(rulebook, headers, rows)
    assert result["status"] == "PASS", result


def test_flat_user_story_with_area_fails() -> None:
    rb_path = ROOT / "docs/intake/user-story-csv-rulebook.yaml"
    rulebook = yaml.safe_load(rb_path.read_text(encoding="utf-8"))
    headers = rulebook["csv"]["column_order"]
    row = {h: "" for h in headers}
    row.update(
        {
            "Work Item Type": "User Story",
            "Title": "Bad layout story",
            "Description": "As a user, I need to do something, so that value is delivered.",
            "Area Path": r"Day 2\CRM",
            "Acceptance Criteria": acceptance_criteria_cell("One", "Two"),
        }
    )
    findings, critical = validate_structure(rulebook, [row])
    assert critical > 0
    assert any("Area Path must be empty" in f for f in findings)


def test_single_line_ac_fails() -> None:
    rb_path = ROOT / "docs/intake/user-story-csv-rulebook.yaml"
    rulebook = yaml.safe_load(rb_path.read_text(encoding="utf-8"))
    headers = rulebook["csv"]["column_order"]

    def hierarchy_prefix() -> list[dict[str, str]]:
        rows = []
        for wit, title in (("Workshop", "01. Test Workshop"),):
            r = {h: "" for h in headers}
            r["Work Item Type"] = wit
            r["Title"] = title
            r["Description"] = "Scope"
            if wit == "Workshop":
                r["Area Path"] = r"Day 2\CRM"
            rows.append(r)
        return rows

    bad = hierarchy_prefix()
    us = {h: "" for h in headers}
    us.update(
        {
            "Work Item Type": "User Story",
            "Title": "Bad AC",
            "Description": "As a user, I need to test AC layout, so that ADO import works.",
            "Acceptance Criteria": "- One - Two on one line",
        }
    )
    bad.append(us)
    findings, critical = validate_structure(rulebook, bad)
    assert critical > 0
    assert any("one '- ' bullet per line" in f for f in findings) or any(
        "multiple on one line" in f for f in findings
    )


def test_traceable_test_case_passes() -> None:
    rb_path = ROOT / "docs/intake/user-story-csv-rulebook.yaml"
    rulebook = yaml.safe_load(rb_path.read_text(encoding="utf-8"))
    headers = rulebook["csv"]["column_order"]

    def row(wit: str, **fields: str) -> dict[str, str]:
        base = {h: "" for h in headers}
        base["Work Item Type"] = wit
        base.update(fields)
        return base

    rows = [
        row("Epic", ID="67476", Title="16. Ecommerce (B2B & B2C)", Description="Catalog epic"),
        row("Feature", ID="67535", Title="Sales Order Approval", Description="Catalog feature"),
        row(
            "Test Case",
            Title="Order waits for approval",
            Description=(
                "Transcript: artifacts/intake/session.txt#00:12:00\n"
                "Epic: 67476 | 16. Ecommerce (B2B & B2C)\n"
                "Feature: 67535 | Sales Order Approval\n"
                "Steps:\n"
                "1. Submit a sales order that the transcript says must be approved"
            ),
            **{"Acceptance Criteria": acceptance_criteria_cell("The order remains pending approval")},
        ),
    ]
    findings, critical = validate_structure(rulebook, rows)
    assert critical == 0, findings
    result = _validate.validate(rulebook, headers, rows)
    assert result["status"] == "PASS", result


def main() -> int:
    test_good_export_passes()
    test_flat_user_story_with_area_fails()
    test_single_line_ac_fails()
    test_traceable_test_case_passes()
    print("ado_user_story_csv_layout tests OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
