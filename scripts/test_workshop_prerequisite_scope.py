#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from workshop_prerequisite_scope import (  # noqa: E402
    allowed_scope_ids,
    knowledge_base_has_scope,
    validate_user_story_rows,
)

SAMPLE_KB = {
    "scope": {
        "in_scope_objectives": [
            {"id": "OBJ-001", "statement": "Partner lifecycle in CE", "source_path": "x.docx"}
        ],
        "in_scope_modules": [{"id": "MOD-001", "statement": "Sales CE", "source_path": "x.docx"}],
    }
}


class WorkshopPrerequisiteScopeTests(unittest.TestCase):
    def test_allowed_ids(self) -> None:
        self.assertEqual(allowed_scope_ids(SAMPLE_KB), {"OBJ-001", "MOD-001"})

    def test_valid_story(self) -> None:
        rows = [
            {
                "Work Item Type": "User Story",
                "Title 3": "Sync partner",
                "prerequisite_refs": ["OBJ-001"],
                "transcript_locator": "00:12:00",
                "transcript_source_path": "artifacts/intake/t.txt",
            }
        ]
        findings, critical = validate_user_story_rows(rows, SAMPLE_KB)
        self.assertEqual(critical, 0)
        self.assertEqual(findings, [])

    def test_require_mom_fields(self) -> None:
        rows = [
            {
                "Work Item Type": "User Story",
                "Title 3": "Sync partner",
                "prerequisite_refs": ["OBJ-001"],
                "transcript_locator": "00:12:00",
                "transcript_source_path": "artifacts/intake/t.txt",
            }
        ]
        _, critical = validate_user_story_rows(rows, SAMPLE_KB, require_mom_fields=True)
        self.assertGreater(critical, 0)

        rows[0]["mom_locator"] = "Agenda item 3"
        rows[0]["mom_source_path"] = "artifacts/intake/mom.docx"
        findings, critical = validate_user_story_rows(
            rows, SAMPLE_KB, require_mom_fields=True
        )
        self.assertEqual(critical, 0)
        self.assertEqual(findings, [])

    def test_reject_bad_ref(self) -> None:
        rows = [
            {
                "Work Item Type": "User Story",
                "prerequisite_refs": ["OBJ-999"],
                "transcript_locator": "00:01:00",
                "transcript_source_path": "t.txt",
            }
        ]
        _, critical = validate_user_story_rows(rows, SAMPLE_KB)
        self.assertGreater(critical, 0)

    def test_kb_must_have_scope(self) -> None:
        self.assertFalse(knowledge_base_has_scope({}))
        self.assertTrue(knowledge_base_has_scope(SAMPLE_KB))


if __name__ == "__main__":
    unittest.main()
