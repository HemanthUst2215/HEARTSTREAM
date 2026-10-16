# Audit — User story pipeline generic runtime contract

## What
Hardened the transcript → user story factory for reuse on any workshop/catalog: runtime contract in the rulebook, MSD grouping order aligned to blank User Story IDs, generic bootstrap wording in commands/templates, mapper docstring, config layout flag, and dev-only labeling on `emit-ado-user-story-csv.py`.

## Why
Prior CE/Finance bootstrap artifacts and ID-on-story conventions should not leak into the next transcript run.

## How
- `docs/intake/user-story-csv-rulebook.yaml` — `runtime_contract`, generic provenance locator
- `docs/intake/msd-test-case-rulebook.yaml` — `nearest_preceding_feature_title` before `mapped_feature_id`
- `.cursor/templates/user-story-csv-rulebook-template.yaml` — parity stubs
- `.cursor/config.yaml` — `public_excel_layout: epic_feature_story_hierarchy`
- Agents/skills/commands/factory doc updates (evaluation context, C2.7, bootstrap refusal)
- `scripts/map-user-stories-to-work-items.py` module docstring

## Validation
- `python scripts/test_ado_user_story_csv_layout.py`
- `python scripts/test_map_user_stories_to_work_items.py`
- `python scripts/test_msd_test_case_xlsx_layout.py`

## Open Items
- `scripts/emit-ado-user-story-csv.py` still contains one workshop fixture corpus for regression only (not runtime).
- Historical dated intake/audit files retain run-specific names by design.

## Next command
`/generate-user-stories-from-transcript` with a new `transcript_path` and current catalogs.
