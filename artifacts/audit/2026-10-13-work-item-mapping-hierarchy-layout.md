# Audit — Epic → Feature → User Stories Excel hierarchy

**Date:** 2026-10-13

## What

Changed public Excel layout from “all Epics, then all Features, then all User Stories (with Feature ID on each story)” to **nested hierarchy**: Epic → Feature 1 → its User Stories → Feature 2 → its User Stories → next Epic. User Story `ID` is always blank.

## Why

Operator requested ADO-style grouping matching workshop Excel flow (Epic1, Features under it, stories under each Feature).

## How

- `scripts/map-user-stories-to-work-items.py`: `_build_epic_feature_story_hierarchy`, `stories_by_feature` grouping.
- Rulebook `generation.row_order.hierarchy` + `id_column` rules updated.
- Agents/skills/commands/rule `32-catalog-only-work-item-mapping.mdc` aligned.
- Regenerated `artifacts/intake/2026-10-13-user-stories-from-transcript.xlsx`.

## Validation

- `python scripts/test_map_user_stories_to_work_items.py` — PASS
- Spot-check Excel: Epic 67461 → Feature 67492 → User Stories (blank ID) → Feature 67493 → …
