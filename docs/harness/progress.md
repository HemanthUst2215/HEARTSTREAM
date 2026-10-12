# Harness Progress

| Field | Value |
|-------|-------|
| **Updated** | 2026-10-12 |
| **Last command** | `/generate-user-stories-from-transcript` |

## Pipeline

| Stage | Status |
|-------|--------|
| Factory installed | **Done** |
| `/generate-user-stories-from-transcript` | **Done** (`artifacts/intake/2026-10-12-user-stories-from-transcript.xlsx`, INVEST `artifacts/intake/2026-10-12-invest-scorecard.csv`; audit `2026-10-12-generate-user-stories-from-transcript-gl-workshop.md`) |
| `/generate-brd` | Pending |
| `/generate-test-cases-from-user-stories` | **Done** (`artifacts/intake/2026-10-09-msd-e2e-test-cases.xlsx`; audit `2026-10-09-generate-test-cases-from-user-stories-v2.md`) |
| Plan (`/plan-governed-stories`, `/plan-sprint`, or `/plan-bounded-context`) | Pending |
| `/implement-api` | Pending |
| `/implement-ui` | Pending |
| `/expand-test-coverage` | Pending |
| `/run-tests` | Pending (after test-package Approved) |
| `/run-eval` | Pending |
| `/review-changes` | Pending |
| `/validate-kpi-metrics` | Pending |
| `/application-summary` | Pending |

## Notes

- Only `harness-updater` writes this file.
- Status values: Pending / In progress / Done / Blocked / Skipped (with audit pointer).
- Core catalog is 19 primaries. Cursor: `.cursorrules` + `CURSOR-FLOW.md`. Claude Code: `CLAUDE.md` + `CLAUDE-FLOW.md`. GitHub Copilot: `.github/copilot-instructions.md` + `COPILOT-FLOW.md`.
- Phase-changing commands (rule 10) must call harness-updater. Decisions are append-only.
