#!/usr/bin/env python3
"""Map user stories to existing catalog Epic/Feature IDs (no new Epic/Feature rows)."""
from __future__ import annotations

from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
mod = SourceFileLoader(
    "map_user_stories_to_work_items",
    str(ROOT / "scripts" / "map-user-stories-to-work-items.py"),
).load_module()
map_stories = mod.map_stories
resolve_story_to_existing = mod.resolve_story_to_existing
title_score = mod.title_score

THRESHOLD = 62.0
MARGIN = 8.0


def _cand(wid: str, title: str, parent: str = "") -> dict:
    return {"id": wid, "title": title, "parent_id": parent, "description": ""}


def _row(wit: str, title: str, desc: str = "") -> dict[str, str]:
    return {"Work Item Type": wit, "Title": title, "Description": desc, "Acceptance Criteria": ""}


def test_title_score_ignores_numbering() -> None:
    assert title_score("Install Base Management", "4. Install Base Management") == 100.0


def test_story_maps_to_existing_feature_and_parent_epic() -> None:
    buckets = {
        "Epic": [_cand("100", "03. B2B Direct Service")],
        "Feature": [_cand("200", "4. Install Base Management", parent="100")],
        "Workshop": [],
    }
    ok = resolve_story_to_existing(
        "Create install base record on delivery",
        "Create install base record on delivery for serialized hardware",
        buckets,
        THRESHOLD,
        MARGIN,
    )
    assert ok["pair"] == "matched"
    assert ok["feature_id"] == "200"
    assert ok["epic_id"] == "100"

    no_parent = resolve_story_to_existing(
        "Create install base record on delivery",
        "Create install base record on delivery",
        {
            "Epic": [],
            "Feature": [_cand("200", "4. Install Base Management", parent="100")],
            "Workshop": [],
        },
        THRESHOLD,
        MARGIN,
    )
    assert no_parent["pair"] == "feature_without_epic"
    assert no_parent["feature_id"] == ""
    assert no_parent["epic_id"] == ""


def test_map_stories_writes_catalog_epic_and_feature_rows() -> None:
    rows = [
        _row("Workshop", "Sales Workshop"),
        _row("Epic", "Should not appear"),
        _row("Feature", "Should not appear"),
        _row("User Story", "Create install base record on delivery for serialized hardware"),
        _row("User Story", "Unrelated story about quoting discounts"),
    ]
    buckets = {
        "Epic": [_cand("E1", "B2B Direct Service")],
        "Feature": [_cand("F1", "Install Base Management", parent="E1")],
        "Workshop": [_cand("W1", "Sales Workshop")],
    }
    mapped, log = map_stories(rows, buckets, THRESHOLD, MARGIN)
    titles = [r["Title"] for r in mapped]
    assert "Should not appear" not in titles
    epics = [r for r in mapped if r["Work Item Type"] == "Epic"]
    feats = [r for r in mapped if r["Work Item Type"] == "Feature"]
    assert len(epics) == 1
    assert epics[0]["ID"] == "E1"
    assert epics[0]["Title"] == "B2B Direct Service"
    assert "EPIC ID" not in epics[0]
    assert "FEATURE ID" not in epics[0]
    assert len(feats) == 1
    assert feats[0]["ID"] == "F1"
    assert feats[0]["Title"] == "Install Base Management"
    stories = [r for r in mapped if r["Work Item Type"] == "User Story"]
    assert "FEATURE ID" not in stories[0]
    assert "EPIC ID" not in stories[0]
    assert stories[0].get("ID") == ""
    assert [r["Work Item Type"] for r in mapped][:4] == ["Workshop", "Epic", "Feature", "User Story"]
    assert log[0]["status"] == "matched"
    assert log[1]["status"] == "unmatched"


def test_ambiguous_duplicate_features_stay_blank() -> None:
    rows = [_row("User Story", "Onboard the partner and enable selling")]
    buckets = {
        "Epic": [_cand("E1", "Reseller"), _cand("E2", "Retail")],
        "Feature": [
            _cand("F1", "Partner Onboarding & Enablement", parent="E1"),
            _cand("F2", "Partner Onboarding & Enablement", parent="E2"),
        ],
        "Workshop": [],
    }
    mapped, log = map_stories(rows, buckets, THRESHOLD, MARGIN)
    assert "FEATURE ID" not in mapped[0]
    assert "EPIC ID" not in mapped[0]
    assert log[0]["pair"] == "no_feature"
    assert "no_unique_catalog_title" in log[0]["feature"]["rationale"]


def main() -> int:
    tests = [
        test_title_score_ignores_numbering,
        test_story_maps_to_existing_feature_and_parent_epic,
        test_map_stories_writes_catalog_epic_and_feature_rows,
        test_ambiguous_duplicate_features_stay_blank,
    ]
    for fn in tests:
        fn()
        print(f"ok {fn.__name__}")
    print("map_user_stories_to_work_items tests OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
