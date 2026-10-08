# Audit: map stories to relevant catalog Epic/Feature rows

**Date:** 2026-10-08  
**Command:** `/generate-user-stories-from-transcript` (mapping)

## What
Public Excel now contains only **catalog** Epic and Feature rows that uniquely match generated User Stories, with existing ADO IDs. Transcript-invented Epic/Feature titles are not written.

## Why
Operator: write relevant existing Epics and Features from work-items JSON (with IDs), not new ones from the transcript.

## How
- Match User Story title to unique catalog Feature titles (`pick_strong_unique_title`).
- Require distinctive Feature terms in the story title (`feature_is_relevant_to_story`).
- Insert matched Epic + Feature rows (`ID` = `workItemId`) before User Stories.
- Duplicate Feature titles across Epics stay unmatched.

## Validation
- `python scripts/test_map_user_stories_to_work_items.py` PASS
- Mapper: 3/29 stories matched; 1 catalog Epic + 2 catalog Features written
- Public file: `artifacts/intake/2026-10-08-user-stories-from-transcript.xlsx`

## Open items
- Duplicate catalog titles (e.g. multiple “Partner Onboarding & Enablement”) cannot be auto-assigned.
- Stories whose titles do not share distinctive Feature terms stay unmatched (IDs blank).

## Next command
Use the Excel, then `/plan-governed-stories` or `/plan-sprint`.
