# Audit — Catalog-only work item mapping (every run)

**Date:** 2026-10-12  
**Command / task:** Align agents and governance so `/generate-user-stories-from-transcript` always uses catalog-only generic mapping with no hardcoded domains.

## What

- Added always-on rule `.cursor/rules/32-catalog-only-work-item-mapping.mdc` and registered it in `.cursorrules` and `cursor-factory-governance.mdc`.
- Updated orchestrator spawn/skip criteria: mapping runs every validator-PASS; skip only when configured `epic.json` / `feature.json` lack `workItems[]`.
- Updated `generate-user-stories-from-transcript.md`, `ado-user-story-csv-writer.md`, `work-item-reference-matcher.md`, `transcript-story-extractor.md`.
- Removed dead `pick_strong_unique_title` from `map-user-stories-to-work-items.py`; clarified module docstring; dropped unused import.
- Added unit test `test_catalog_file_filter_respects_config`.

## Why

User requirement: apply catalog-only generic matching on every intake run; agents must stay aligned; no domain/epic/topic hardcoding in code or prompts.

## How

Config-driven paths and thresholds (`work_item_mapping` in `.cursor/config.yaml`); Phase 5 **work-item-mapping-agent** only for Feature `ID`; BA leaves IDs blank until mapper runs.

## Validation

- `python scripts/test_map_user_stories_to_work_items.py` — PASS (5 tests).

## Open Items

- **DQ-GL-CATALOG:** GL workshop stories need real GL Features in ADO → re-export `feature.json` → `/process-work-items-csv` → remap. Until then, generic overlap may match unrelated CRM Features or leave IDs blank.

## Next command

Re-run mapper after catalog refresh, or `/generate-user-stories-from-transcript` on a new transcript with current `epic.json` / `feature.json`.
