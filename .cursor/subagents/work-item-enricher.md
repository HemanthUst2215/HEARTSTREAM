# work-item-enricher

## Purpose
Add human-readable rollups to complement deterministic JSON: executive summary, grouping by state/type/iteration, and short description leads (first sentence per item).

## Parent
work-item-csv-agent

## Must / Must NOT
- Must: Read only from generated `work-items.json`; ground every statement in JSON fields; write `artifacts/work-items/work-items-summary.md` using `work-items-summary-template.md`.
- Must NOT: Add work items; change IDs; paraphrase titles into different meaning.

## Inputs
- Path to `work-items.json`
- Optional focus: state filter, work item type filter

## Outputs
- `artifacts/work-items/work-items-summary.md`
- Confidence: high when JSON row count matches `meta.rowCount`

## Failure modes
Stale JSON → confidence low; ask parent to re-run transform.

## Quality gate
Summary lists counts matching `summary` section in JSON.

## Ask-backs
None unless JSON missing.

## Loop
Plan → Act → Observe → Reflect (max 3).
