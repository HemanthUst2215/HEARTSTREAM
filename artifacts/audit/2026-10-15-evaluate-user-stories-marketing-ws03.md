# Agent Audit — /evaluate-user-stories — marketing-ws03

| Field | Value |
|-------|-------|
| **Date** | 2026-10-15 |
| **Command / Agent** | /evaluate-user-stories · user-story-evaluation-agent |
| **Iteration** | 1 of 3 |
| **Validation** | allocate-run, intake-safety CLEAN, validate PASS, HTML rendered |

## What
- New run `2026-10-15-user-story-evaluation-marketing-ws03` (did not edit prior evaluation HTML/JSON).
- Manual: `CRM - Workshop Stories.xlsx` (44 User Stories). AI: `artifacts/intake/2026-10-13-marketing-ws03-user-stories-from-transcript.xlsx` (14 User Stories). Transcript: `Transcript 03. Marketing - 1 - Workshop Meeting Transcript_30.09.2026.docx`.
- Working extracts: `artifacts/evaluation/.pipeline/2026-10-15-marketing-ws03-manual.csv`, `...-generated.csv`, `...-transcript.txt`.
- Public: `artifacts/evaluation/2026-10-15-user-story-evaluation-marketing-ws03.html`

## Why
- Operator `/evaluate-user-stories` comparing CRM workshop stories to the 2026-10-13 marketing WS03 generated workbook, with the 30 Sep 2026 Marketing workshop transcript as ground truth.

## How
- Intake-safety scan exit 0 on transcript extract and both CSVs.
- `allocate-run --date 2026-10-15 --slug marketing-ws03`
- Output-path gate CLEAR on allocated paths
- `prepare` packet (no Recall/Precision scores; 5 Jaccard proposals, ASSUMPTION-USEVAL-003)
- Subagents: story-matching-evaluator, hallucination-detection-evaluator, coverage-analysis-evaluator, business-correctness-evaluator, acceptance-criteria-evaluator, epic-feature-mapping-evaluator, kpi-aggregation-evaluator
- `validate` PASS then `render` (script-owned HTML)

## Validation
| Check | Result | Evidence |
|-------|--------|----------|
| allocate-run | new_run_only | `2026-10-15-user-story-evaluation-marketing-ws03` |
| Output-path gate | CLEAR | allocated paths only |
| Intake-safety | CLEAN (exit 0) | 3 files, 0 injection, 0 PII |
| Packet | no semantic scores | 44 manual / 14 generated; header finding on manual |
| Metric owners | PASS | 13 contract metrics, one owner each |
| validate | PASS | `scripts/evaluate_user_stories.py validate` |
| HTML | script render | `artifacts/evaluation/2026-10-15-user-story-evaluation-marketing-ws03.html` |
| Status | Draft — Pending Method Review | ASSUMPTION-USEVAL-001 pending |
| Harness | not written | command is not a phase change |

## Behavior provenance
| behavior_id | statement | source | confidence |
|-------------|-----------|--------|------------|
| ASSUMPTION-USEVAL-001 | Scoring method for manual vs generated CSVs with transcript as ground truth | `.cursor/templates/user-story-evaluation-metrics.yaml` | assumption |
| ASSUMPTION-USEVAL-002 | Role is specific unless exactly `user`/`users` | role_specificity metric | assumption |
| ASSUMPTION-USEVAL-003 | Jaccard candidate_pairs are proposals, not matches | packet `candidate_note` | assumption |

## Open items
- ASSUMPTION-USEVAL-001 pending method review — do not treat scores as Accepted.
- ASSUMPTION-USEVAL-002 pending on role specificity.
- Open DQ: manual Excel header does not match rulebook `column_order` (`Area Level 2` instead of rulebook columns). Packet indexed 44 User Story rows.
- generated-US-15 and generated-US-19 duplicate the same vertical-trend requirement under Features 38 and 60.
- Feature agreement 0/1: Feature ID `110486` vs blank and hyphen spacing in Feature titles.
- One match (M-001): `manual-US-46` ↔ `generated-US-17`. Recall 2% (1/44). Precision 100% (1/1). 13 valid extras, 0 noise. Hallucination rate 71% (10/14) from extra AC/description claims.

## Next command
Review `artifacts/evaluation/2026-10-15-user-story-evaluation-marketing-ws03.html`. Accept or reject `ASSUMPTION-USEVAL-001` before treating scores as accepted.

**Output path:** `artifacts/audit/2026-10-15-evaluate-user-stories-marketing-ws03.md`
