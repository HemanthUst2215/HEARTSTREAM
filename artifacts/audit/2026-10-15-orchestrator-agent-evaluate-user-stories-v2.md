# Agent Audit — orchestrator-agent — evaluate-user-stories v2

| Field | Value |
|-------|-------|
| **Date** | 2026-10-15 |
| **Command / Agent** | orchestrator-agent · /evaluate-user-stories (v2 hallucination both sides) |
| **Iteration** | 1 of 3 |
| **Validation** | DoD met; v1 artifacts not overwritten |

## What
- Operator follow-up: score manual-story hallucination as well as generated.
- Routed hallucination-detection-evaluator for all 44 manual User Stories; published a new `-v2` report.

## Why
- v1 comparison row left manual hallucination as “not scored (contract is generated-only).”

## How
- New-run-only allocate-run `marketing-ws03-v2`
- Contract metric `manual_hallucination_rate` added so future runs cannot skip the manual CSV
- No `docs/harness/**` write

## Next command
Review `artifacts/evaluation/2026-10-15-user-story-evaluation-marketing-ws03-v2.html`.

**Output path:** `artifacts/audit/2026-10-15-orchestrator-agent-evaluate-user-stories-v2.md`
