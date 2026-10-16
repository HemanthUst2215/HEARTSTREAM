# Agent Audit — /evaluate-user-stories — marketing-ws03-v2

| Field | Value |
|-------|-------|
| **Date** | 2026-10-15 |
| **Command / Agent** | /evaluate-user-stories · user-story-evaluation-agent |
| **Iteration** | 1 of 3 |
| **Validation** | allocate-run v2, validate PASS, HTML rendered; v1 report not overwritten |

## What
- Follow-up: score hallucination on **both** CSVs (manual 44 + generated 14) against the Marketing WS03 transcript.
- Did not edit `artifacts/evaluation/2026-10-15-user-story-evaluation-marketing-ws03.html`.
- Public v2: `artifacts/evaluation/2026-10-15-user-story-evaluation-marketing-ws03-v2.html`
- Method: added contract metric `manual_hallucination_rate`; hallucination-detection-evaluator now judges both sides.

## Why
- Operator asked to check hallucination in both story sets, not only AI.

## How
- `allocate-run --date 2026-10-15 --slug marketing-ws03` → `-v2`
- Output-path gate CLEAR
- Reused v1 packet, matches, coverage, correctness, AC, epic/feature (unchanged)
- hallucination-detection-evaluator scored 44 manual rows in two batches; merged with v1 generated scores
- `validate` PASS; `render` wrote v2 HTML/JSON only
- Factory updates: metrics YAML, hallucination skill/subagent, command, evaluation agent, `_is_lower_better`, unit test fixture

## Validation
| Check | Result | Evidence |
|-------|--------|----------|
| Prior HTML preserved | PASS | `...-marketing-ws03.html` untouched |
| validate | PASS | evaluation-v2.json |
| `python scripts/test_evaluate_user_stories.py` | PASS | extra metric in fixture |
| Manual hallucination | 100% (44/44) | any-unsupported-claim rule |
| Generated hallucination | 71% (10/14) | unchanged from v1 |
| Core title unsupported (manual) | 17/44 | listed in hallucination-v2 |

## Behavior provenance
| behavior_id | statement | source | confidence |
|-------------|-----------|--------|------------|
| ASSUMPTION-USEVAL-001 | Method now includes Manual Hallucination Rate with the same any-unsupported-claim rule | `.cursor/templates/user-story-evaluation-metrics.yaml` | assumption |

## Open items
- ASSUMPTION-USEVAL-001 still pending method review.
- 100% manual rate is driven by extra AC/description claims plus 17 rows whose core title is not in this transcript.

## Next command
Review `artifacts/evaluation/2026-10-15-user-story-evaluation-marketing-ws03-v2.html`. Accept or reject `ASSUMPTION-USEVAL-001` before treating scores as accepted.

**Output path:** `artifacts/audit/2026-10-15-evaluate-user-stories-marketing-ws03-v2.md`
