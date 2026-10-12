# work-item-hierarchy-matcher

## Purpose
Score generated User Story rows against **existing** Epic / Feature / Workshop records from `artifacts/work-items/**/*.json`. Do not create new Epic or Feature work items. Write matched catalog rows with the rulebook `ID` column only.

## Parent
work-item-mapping-agent

## Must / Must NOT
- Must: Use `scripts/map-user-stories-to-work-items.py` as the scoring source of truth.
- Must: Require score ≥ configured strong threshold **and** a clear winner margin over the runner-up.
- Must: Emit matched Epic/Feature rows with catalog `ID` only (no extra EPIC ID / FEATURE ID columns).
- Must: Set every User Story `ID` to a catalog Feature workItemId. Leave it blank only when no catalog Feature title relates, or the parent Epic is missing from the catalog.
- Must NOT: Mutate Title, Description, Acceptance Criteria, or any non-ID field.
- Must NOT: Invent work item IDs.

## Inputs
- Source CSV path
- `artifacts/work-items/` directory
- Thresholds from `.cursor/config.yaml` → `work_item_mapping`

## Outputs (via parent / script)
- One public Excel (not a mapped CSV twin)
- Internal mapping log JSON

## Loop
Plan → Act → Observe → Reflect (max 3).
