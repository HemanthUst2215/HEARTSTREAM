# Harness Progress

| Field | Value |
|-------|-------|
| **Updated** | 2026-10-13 |
| **Last command** | `/generate-user-stories-from-transcript` |

## Pipeline

| Stage | Status |
|-------|--------|
| Factory installed | **Done** |
| `/generate-user-stories-from-transcript` | **Done** (`artifacts/intake/2026-10-13-user-stories-from-transcript.xlsx`, INVEST `artifacts/intake/2026-10-13-invest-scorecard.csv`; source Sales CE R2R workshop docx; audit `2026-10-13-generate-user-stories-from-transcript-sales-ce-r2r-workshop.md`) |
| `/generate-brd` | Pending |
| `/generate-test-cases-from-user-stories` | **Done** (`artifacts/intake/2026-10-13-msd-e2e-test-cases.xlsx`; 5 processes / 10 cases / 41 steps; source `Finance User Stories- Workshop -WS-02.xlsx`; audit `2026-10-13-generate-test-cases-from-user-stories-finance-ws02.md`) |
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
