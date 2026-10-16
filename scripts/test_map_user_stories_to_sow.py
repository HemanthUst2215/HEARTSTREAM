#!/usr/bin/env python3
from __future__ import annotations

import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
mod = SourceFileLoader(
    "map_sow",
    str(ROOT / "scripts" / "map-user-stories-to-sow-features.py"),
).load_module()

SOW = ROOT / "artifacts" / "work-items" / "SOW.json"


class SowMappingTests(unittest.TestCase):
    def test_load_sow_feature_shape(self) -> None:
        features = mod.load_sow(SOW)
        self.assertEqual(len(features), 6)
        first = features[0]
        self.assertEqual(first["title"], "70 - External Analytics Data Ingestion & Unification")
        self.assertEqual(first["annexure_minutes"], "70")
        self.assertEqual(first["workshop_code"], "WS-CE-01")

    def test_sow_feature_row_annexure(self) -> None:
        features = mod.load_sow(SOW)
        keys = ["ID", "Work Item Type", "Title 2", "Description", "Annexure ID1"]
        row = mod.sow_feature_row(keys, features[0])
        self.assertEqual(row["ID"], "")
        self.assertEqual(row["Annexure ID1"], "70")

    def test_map_by_prerequisite_ref(self) -> None:
        features = mod.load_sow(SOW)
        csv_rows = [
            {
                "Work Item Type": "Workshop",
                "Title 1": "Marketing WS",
                "Title 3": "",
                "ID": "",
                "Description": "",
            },
            {
                "Work Item Type": "User Story",
                "Title 3": "Connect CRM data",
                "Description": "As a steward, I need to connect CRM, so that audiences align.",
                "Acceptance Criteria": "- One criterion.",
                "ID": "",
            },
        ]
        prereq = {"Connect CRM data": ["OBJ-001"]}
        _, logs = mod.map_stories_to_sow(csv_rows, features, prereq, 62, 8, 3)
        self.assertEqual(logs[0]["status"], "matched")


if __name__ == "__main__":
    unittest.main()
