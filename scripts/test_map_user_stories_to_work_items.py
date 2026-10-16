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
_catalog_file_for_type = mod._catalog_file_for_type

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
    titles = [r.get("Title") or r.get("Title 3") or r.get("Title 2") or r.get("Title 1") or "" for r in mapped]
    assert "Should not appear" not in titles
    epics = [r for r in mapped if r["Work Item Type"] == "Epic"]
    feats = [r for r in mapped if r["Work Item Type"] == "Feature"]
    assert len(epics) == 1
    assert epics[0]["ID"] == "E1"
    assert epics[0].get("Title 1") == "B2B Direct Service" or epics[0].get("Title") == "B2B Direct Service"
    assert len(feats) == 1
    assert feats[0]["ID"] == "F1"
    stories = [r for r in mapped if r["Work Item Type"] == "User Story"]
    assert all((s.get("ID") or "") == "" for s in stories)
    assert [r["Work Item Type"] for r in mapped][:4] == ["Workshop", "Epic", "Feature", "User Story"]
    assert log[0]["status"] == "matched"
    assert log[1]["status"] == "unmatched"


def test_catalog_file_filter_respects_config() -> None:
    cfg = {
        "catalog_epic_json": "custom-epic.json",
        "catalog_feature_json": "custom-feature.json",
        "workshop_catalog_json": "custom-workshop.json",
    }
    assert _catalog_file_for_type("Epic", "custom-epic.json", cfg)
    assert not _catalog_file_for_type("Epic", "epic.json", cfg)
    assert _catalog_file_for_type("Feature", "custom-feature.json", cfg)
    assert not _catalog_file_for_type("Feature", "feature.json", cfg)


def test_hierarchy_epic_feature_stories_order() -> None:
    rows = [
        _row("User Story", "Story for feature A"),
        _row("User Story", "Story for feature B"),
    ]
    buckets = {
        "Epic": [_cand("E1", "Epic Alpha"), _cand("E2", "Epic Beta")],
        "Feature": [
            _cand("F1", "Feature Alpha One", parent="E1"),
            _cand("F2", "Feature Beta One", parent="E2"),
        ],
        "Workshop": [],
    }
    # Force match titles
    rows[0]["Description"] = "Story for feature Alpha One capability"
    rows[1]["Description"] = "Story for feature Beta One capability"
    mapped, _ = map_stories(rows, buckets, THRESHOLD, MARGIN)
    types = [r["Work Item Type"] for r in mapped]
    assert types == ["Epic", "Feature", "User Story", "Epic", "Feature", "User Story"]
    assert mapped[2].get("ID") == ""
    assert mapped[5].get("ID") == ""


def test_duplicate_feature_titles_still_map() -> None:
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
    assert log[0]["status"] == "matched"
    assert log[0]["featureId"] in {"F1", "F2"}
    story = next(r for r in mapped if r["Work Item Type"] == "User Story")
    assert (story.get("ID") or "") == ""
    assert log[0]["featureId"] in {"F1", "F2"}


def main() -> int:
    tests = [
        test_title_score_ignores_numbering,
        test_story_maps_to_existing_feature_and_parent_epic,
        test_map_stories_writes_catalog_epic_and_feature_rows,
        test_hierarchy_epic_feature_stories_order,
        test_catalog_file_filter_respects_config,
        test_duplicate_feature_titles_still_map,
    ]
    for fn in tests:
        fn()
        print(f"ok {fn.__name__}")
    print("map_user_stories_to_work_items tests OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
