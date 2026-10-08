# Audit: work-item-mapping-agent — Epic+Feature pair gate

**Date:** 2026-10-08  
**Command:** `/generate-user-stories-from-transcript` (mapping remap)  
**Iteration:** 1 of 3  
**Validation:** PASS (pair gate tests; 0 invented IDs)

## What
- Mapper now fills **EPIC ID and FEATURE ID only when both titles strongly match** and the Feature’s catalog parent is that Epic.
- Feature-only hits (including copying Epic from Feature.parent) are withheld.
- Title scoring is generic (numbering stripped, morphology prefix). CSV Feature→Epic bind supports grouped rulebook order.
- Regenerated `artifacts/intake/2026-10-08-user-stories-from-transcript.xlsx`.

## Why
Operator: map only if both (Epic and Feature) are matching. Prior run filled FEATURE 67562 and inferred EPIC 67557 from parent without an Epic title match.

## How
- `scripts/map-user-stories-to-work-items.py` → `resolve_epic_feature_pair`
- Tests: `scripts/test_map_user_stories_to_work_items.py`
- Config: `require_both_epic_and_feature: true`, `strong_threshold: 62`

## Validation
| Check | Result | Evidence |
|-------|--------|----------|
| Unit tests | PASS | `python scripts/test_map_user_stories_to_work_items.py` |
| This catalog | 0/29 paired | Workshop process Epics do not match ADO channel Epics (e.g. “Install Base Management” vs “03. B2B Direct Service”) |
| Pair reasons | 16 no unique CSV feature; 12 neither catalog title; 1 feature_without_epic | mapping log |
| Invented IDs | None | IDs blank unless pair matched |

## Open items
- Catalog Epics are program/channel titles; generated Epics are process titles. Pair gate correctly leaves IDs blank until ADO Epics/Features share those titles (or a human maps them).

## Next command
Use `artifacts/intake/2026-10-08-user-stories-from-transcript.xlsx` (IDs blank where the pair did not match), then `/plan-governed-stories` or `/plan-sprint`.
