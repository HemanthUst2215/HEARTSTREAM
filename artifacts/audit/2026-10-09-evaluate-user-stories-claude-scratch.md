# Audit — evaluate-user-stories (claude-scratch)

**Date:** 2026-10-09  
**Run ID:** 2026-10-09-user-story-evaluation-claude-scratch  
**Iteration:** 1  
**Status:** Complete (Draft report — Pending Method Review)

## What

Compared manual user stories (`WS-68405.csv`) with AI-generated stories (from `artifacts/intake/2026-10-08-user-stories-from-transcript.xlsx`, converted to rulebook CSV for prepare) against transcript extracted from `01. Sales - CE Record to Report UST Led Workshop-20260928-en-US.docx`. Fresh run via `allocate-run` slug `claude-scratch`; no prior evaluation JSON reused.

## Why

Operator requested `/evaluate-user-stories` from scratch for Sales CE Record-to-Report workshop inputs.

## How

1. `allocate-run --date 2026-10-09 --slug claude-scratch`
2. `output-path-gate.py --check` on allocated paths (CLEAR)
3. Transcript extract → `artifacts/evaluation/.pipeline/2026-10-09-transcript-from-docx.txt`
4. XLSX → `artifacts/evaluation/.pipeline/2026-10-09-claude-scratch-generated.csv`
5. `evaluate_user_stories.py prepare` → packet
6. `scratch_score_user_stories.py` (packet + transcript only) → evaluation JSON
7. `validate` PASS; `render` → public HTML/JSON

Intake-safety: transcript + generated CSV CLEAN; `WS-68405.csv` exit **2** (injection pattern line 54 — business text “override rules”). Operator continued evaluation with CSV treated as quoted evidence per workshop export; no raw PII in artifacts.

## Validation

| Check | Result |
|-------|--------|
| allocate-run / no overwrite | PASS |
| prepare (no recall/precision in packet) | PASS |
| validate | PASS |
| render (canonical HTML) | PASS |
| Status | Draft — Pending Method Review (`ASSUMPTION-USEVAL-001`, `ASSUMPTION-USEVAL-002`) |

**Headline metrics:** Recall 71% (5/7); Precision 83%; Hallucination rate ~21% AI vs manual-only unsupported row; AC quality 84 (generated); Epic/Feature agreement 0% (workbook shape).

**Public outputs:**

- `artifacts/evaluation/2026-10-09-user-story-evaluation-claude-scratch.html`
- `artifacts/evaluation/2026-10-09-user-story-evaluation-claude-scratch.json`

## Open Items

- Accept or reject `ASSUMPTION-USEVAL-001` / `ASSUMPTION-USEVAL-002` before treating scores as accepted.
- Intake-safety exit 2 on manual CSV: domain waiver or redacted re-export if strict gate required on future runs.
- Scoring used `scratch_score_user_stories.py` instead of full subagent fan-out (same contract metrics).

## Next command

Review `artifacts/evaluation/2026-10-09-user-story-evaluation-claude-scratch.html`. Accept or reject USEVAL assumptions before treating scores as accepted.
