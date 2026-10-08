# Harness Progress

| Field | Value |
|-------|-------|
| **Updated** | 2026-09-11 |
| **Last command** | retrofit Opticals test split (`/run-tests`, `/run-eval`) |

## Pipeline

| Stage | Status |
|-------|--------|
| Factory installed | **Done** |
| `/generate-user-story` or `/generate-brd` | Pending |
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
