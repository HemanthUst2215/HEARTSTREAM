# Audit: SOW.json feature mapping (replace epic/feature catalogs)

## What

Transcript user-story public Excel now maps Features from `artifacts/work-items/SOW.json` only. No Epic rows; Feature `ID` blank; Annexure ID1 = SOW minutes; Title 2 = `<minutes> - <topic>`.

## Why

Operator requested SOW-driven features with annexure display instead of ADO epic.json / feature.json.

## How

- Script: `scripts/map-user-stories-to-sow-features.py`
- Config: `work_item_mapping.feature_source: sow_json`
- Updated rulebook, agents, skills, command, rule `32-catalog-only-work-item-mapping.mdc`
- Regenerated `2026-10-13-marketing-ws03-user-stories-from-transcript.xlsx` (12/13 matched)

## Validation

- `test_map_user_stories_to_sow.py` OK
- Legacy `map-user-stories-to-work-items.py` retained as `legacy_map_script` for `feature_source: ado_catalog` if needed

## Next command

Re-run `/generate-user-stories-from-transcript` or remap with `--rows-json` for prerequisite-based SOW matching.
