#!/usr/bin/env python3
"""Regression tests for MSD365 business entity scope catalog and validation."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from msd365_business_entity_scope import (  # noqa: E402
    load_catalog,
    story_matches_catalog,
    validate_user_story_rows,
)

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "docs" / "intake" / "msd365-business-entity-catalog.json"


class Msd365BusinessEntityScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog(CATALOG_PATH)

    def test_catalog_has_121_entries(self) -> None:
        self.assertEqual(self.catalog["entry_count"], 121)
        self.assertEqual(len(self.catalog["entries"]), 121)

    def test_empty_business_entity_rows_present(self) -> None:
        empty = [e for e in self.catalog["entries"] if not e["business_entity"]]
        self.assertEqual(len(empty), 11)

    def test_valid_finance_gl_story(self) -> None:
        row = {
            "Work Item Type": "User Story",
            "Title 3": "Post journal",
            "msd365_domain": "Finance",
            "msd365_application": "Record to Report",
            "msd365_business_entity": "General Ledger",
        }
        ok, _ = story_matches_catalog(row, self.catalog)
        self.assertTrue(ok)

    def test_reject_unknown_business_entity(self) -> None:
        row = {
            "Work Item Type": "User Story",
            "msd365_domain": "Finance",
            "msd365_application": "Record to Report",
            "msd365_business_entity": "Invented Module",
        }
        ok, reason = story_matches_catalog(row, self.catalog)
        self.assertFalse(ok)
        self.assertIn("allow-list", reason)

    def test_isv_empty_entity(self) -> None:
        row = {
            "Work Item Type": "User Story",
            "msd365_domain": "ISV",
            "msd365_application": "Zinfi",
            "msd365_business_entity": "",
        }
        ok, _ = story_matches_catalog(row, self.catalog)
        self.assertTrue(ok)

    def test_validate_skips_workshop(self) -> None:
        rows = [
            {"Work Item Type": "Workshop", "Title 1": "W"},
            {
                "Work Item Type": "User Story",
                "msd365_domain": "CRM",
                "msd365_application": "Sales",
                "msd365_business_entity": "Lead to Opportunity",
            },
        ]
        findings, critical = validate_user_story_rows(rows, self.catalog)
        self.assertEqual(critical, 0)
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
