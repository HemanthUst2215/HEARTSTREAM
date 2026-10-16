# Transcript → user story extraction (Marketing WS-03)

| Field | Value |
|-------|-------|
| Transcript | `artifacts/intake/2026-10-16-transcript.txt` |
| MoM | `artifacts/intake/.pipeline/2026-10-16-marketing-ws03-mom.txt` |
| Prerequisite KB | `artifacts/intake/2026-10-16-workshop-prerequisite-knowledge-base.json` |
| Iteration | 1 |
| Date | 2026-10-16 |

## Session notes

- Workshop title referenced **Lead to Opportunity**; facilitators clarified **Customer Insights = marketing** (transcript 5:18–9:05). MoM topic 1 records stakeholder confusion and need for clearer Marketing / Customer Insights communications.
- Session focused on **external analytics ingestion & unification** (WS-CE-01) with segmentation and profile demos per transcript and MoM topics 2–4, 7–9.

## Out of scope / excluded (prerequisite)

| Transcript locator | Topic | Reason |
|--------------------|-------|--------|
| 10:17–10:23 | Lead assignment through opportunity closure | OOS-001 |

## Open DQ

None for iteration 1.

## Validation

- [x] `validate-user-story-workshop-scope.py` PASS (`--require-mom`)
- [x] `validate-user-story-business-entity-scope.py` PASS
- [x] `validate-user-story-csv.py` PASS
- [x] Work-item mapping: 12/13 matched (`artifacts/intake/.pipeline/2026-10-16-work-item-mapping-log.json`); unmatched: *Identify distributors serving multiple vertical markets* (below SOW token threshold)

## INVEST

Scorecard: `artifacts/intake/2026-10-16-invest-scorecard.csv` — several stories **Needs Refinement** on Testable (score 4); overall scores ≥ 6.8. No Reflect iteration (iteration 1 validator PASS per execution policy).
