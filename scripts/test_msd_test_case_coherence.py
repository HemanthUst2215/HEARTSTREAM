#!/usr/bin/env python3
"""Tests for msd_test_case_coherence heuristics."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from msd_test_case_coherence import check_case_precondition_coherence  # noqa: E402
from msd_test_case_xlsx_layout import load_rulebook  # noqa: E402


def test_flags_update_without_contract_in_preconditions() -> None:
    rulebook = load_rulebook(ROOT / "docs" / "intake" / "msd-test-case-rulebook.yaml")
    case = {
        "test_case_id": "TC01-P01",
        "test_type": "Positive E2E",
        "preconditions": "User has access to Contract Management.",
        "steps": [
            {
                "detailed_test_step": "User to update the list price on the active contract.",
                "expected_result": "Price updates.",
            }
        ],
    }
    findings = check_case_precondition_coherence(case, rulebook)
    assert any("contract" in f.lower() or "list price" in f.lower() for f in findings)


def test_passes_when_preconditions_establish_contract() -> None:
    rulebook = load_rulebook(ROOT / "docs" / "intake" / "msd-test-case-rulebook.yaml")
    case = {
        "test_case_id": "TC01-P01",
        "test_type": "Positive E2E",
        "preconditions": "An active contract exists with list price configured.",
        "steps": [
            {
                "detailed_test_step": "Update the list price on the active contract.",
                "expected_result": "Price updates.",
            },
            {"detailed_test_step": "Verify downstream quote uses new price."},
            {"detailed_test_step": "Confirm audit trail on contract."},
        ],
    }
    findings = check_case_precondition_coherence(case, rulebook)
    assert not findings


def test_flags_approved_status_without_precondition() -> None:
    rulebook = load_rulebook(ROOT / "docs" / "intake" / "msd-test-case-rulebook.yaml")
    case = {
        "test_case_id": "TC04-P01",
        "test_type": "Positive E2E",
        "preconditions": "Partner user exists in CRM.",
        "steps": [
            {
                "detailed_test_step": "Set the onboarding status to Approved.",
                "expected_result": "Status is Approved.",
            }
        ],
    }
    findings = check_case_precondition_coherence(case, rulebook)
    assert any("approved" in f.lower() or "onboarding" in f.lower() for f in findings)


if __name__ == "__main__":
    test_flags_update_without_contract_in_preconditions()
    test_passes_when_preconditions_establish_contract()
    test_flags_approved_status_without_precondition()
    print("OK")
