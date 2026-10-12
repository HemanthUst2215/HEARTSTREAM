# Agent Audit — /evaluate-user-stories — manual-vs-v2

| Field | Value |
|-------|-------|
| **Date** | 2026-10-08 |
| **Command / Agent** | /evaluate-user-stories |
| **Iteration** | 1 of 3 |
| **Validation** | `evaluate_user_stories.py validate` PASS. HTML rendered. Status Draft — Pending Method Review. |

## What
- Compared manual `WS-68405.csv` (7 User Story rows) with AI `artifacts/intake/2026-10-08-user-stories-from-transcript-v2.xlsx` (29 User Story rows).
- Ground truth: `01. Sales - CE Record to Report UST Led Workshop-20260928-en-US.docx`. Timestamps are taken from the line-broken extract `artifacts/intake/2026-10-08-transcript-v2.txt`, which is the same workshop text.
- Public report: `artifacts/evaluation/2026-10-08-user-story-evaluation.html`
- Public JSON: `artifacts/evaluation/2026-10-08-user-story-evaluation.json`
- Did not regenerate stories. The invocation that named `/generate-user-stories-from-transcript` supplied a manual CSV and an existing AI workbook.

## Why
- Operator named the docx as the transcript, the CSV as manual, and the v2 workbook as AI.

## How
- Intake scan on 2026-10-08 had exit 2 on `WS-68405.csv` line 54 (`override rules`) inside an Issue mitigation sentence. The operator supplied that same file again as the manual baseline. The sentence was treated as data.
- Output-path gate was CLEAR before the report files were written.
- `prepare` wrote `artifacts/evaluation/.pipeline/2026-10-08-evaluation-packet.json`. Proposals were not used as matches.
- Metric owners in the contract scored recall, precision, manual-only, generated-only, epic agreement, feature agreement, format, role specificity, acceptance-criteria count and quality, negative/boundary coverage, granularity, and hallucination rate.
- `render` wrote the HTML.

## Validation
| Check | Result | Evidence |
|-------|--------|----------|
| Inputs complete | Yes | Docx, manual CSV, AI xlsx |
| validate | PASS | exit 0 |
| DoD | Met for a Draft report | HTML + JSON |
| Scope | Held | No product code |

Scores: Recall 71% (5/7). Precision 83% (5/6). Manual-only 2. Generated-only 23 valid extras and 1 noise. Epic agreement 0% (0/5). Feature agreement 0% (0/5). Format 93% (27/29). Role specificity 100% (29/29). Acceptance criteria count manual mean 0.86 versus generated mean 2.72. Acceptance criteria quality 84. Negative/boundary coverage 100% (17/17). Granularity 86% (25/29). Hallucination rate 24% (7/29).

## Behavior provenance
| behavior_id | statement | source | confidence |
|-------------|-----------|--------|------------|
| ASSUMPTION-USEVAL-001 | Ratio formulas used for this report | `.cursor/templates/user-story-evaluation-metrics.yaml` | assumption |
| ASSUMPTION-USEVAL-002 | Role `user`/`users` is not specific | same file | assumption |
| EVAL-001 | Five manual stories match generated stories; two do not | transcript timestamps in the HTML | explicit |

## Open items
- Accept or reject ASSUMPTION-USEVAL-001 before treating scores as accepted.
- Epic and Feature agreement are 0% because of row order and because manual IDs are story ids.
- Manual acceptance-criteria cells are HTML-shifted.
- Partner-created leads: generated-US-29 classified noise from the session close at 3:09:08.

## Next command
Review `artifacts/evaluation/2026-10-08-user-story-evaluation.html`.

**Output path:** `artifacts/audit/2026-10-08-evaluate-user-stories-manual-vs-v2.md`
