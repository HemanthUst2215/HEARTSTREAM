# work-item-hierarchy-matcher

## Purpose
Score User Story rows against **existing** Epic and Feature records in `epic.json` and `feature.json` only. Generic similarity — no domain-specific hint tables or hardcoded epic IDs.

## Parent
work-item-mapping-agent

## Must / Must NOT
- Must: Use `scripts/map-user-stories-to-work-items.py` as the scoring source of truth.
- Must: Require score ≥ `strong_threshold` and apply `winner_margin` + `max_related_features` from config.
- Must: Emit matched Epic/Feature header rows with catalog `ID` only.
- Must: Keep User Story `ID` blank; nest stories under the matched Feature row(s) in Epic → Feature → User Stories order.
- Must NOT: Create new Epics/Features; map Workshop items as Features; mutate story fields; invent IDs.

## Inputs
- Source CSV path
- `artifacts/work-items/epic.json`, `artifacts/work-items/feature.json`
- `.cursor/config.yaml` → `work_item_mapping`

## Outputs (via parent / script)
- One public Excel
- Internal mapping log JSON

## Loop
Plan → Act → Observe → Reflect (max 3).
