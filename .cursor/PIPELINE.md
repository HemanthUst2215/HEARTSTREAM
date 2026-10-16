# Canonical pipeline (drop-in)

See [CURSOR-FLOW.md](../CURSOR-FLOW.md). This copy travels with the `.cursor/` drop-in.

**Execute spine (locked):** `/implement-api` → `/implement-ui` → `/expand-test-coverage` → **[human: test-package Approved]** → `/run-tests` → `/run-eval` → `/review-changes` → `/application-summary`

Do not advertise generate-backend / generate-frontend / wire-fe-be as public execute commands. Those jobs are internal steps of implement-*.

Do not advertise public `/write-tech-spec`, `/gap-analysis`, or `/generate-user-story`. User stories come only from `/generate-user-stories-from-transcript`. Gap analysis is an internal step of the plan commands.

Intake: `/generate-user-stories-from-transcript` (transcript → one Excel with IDs, separate INVEST CSV). Then `/generate-test-cases-from-user-stories` (that Excel → MSD E2E test-case workbook via `docs/intake/msd-test-case-rulebook.yaml`).

Satellite (audit only, no harness row): `/evaluate-user-stories` (manual CSV vs AI-generated CSV vs transcript → HTML report). Scores stay Draft — Pending Method Review until `ASSUMPTION-USEVAL-001` is accepted.

Satellite: `/generate-html-for-user-stories` (manual and AI CSVs each validated vs transcript, MoM, pre-read, and SOW features → two HTML reports; no manual-vs-AI comparison). Pending `ASSUMPTION-USHTML-001`.

Quality scorecards: `/validate-kpi-metrics` (quality-agent mode `kpi`).
Figma DS URL: `/figma-to-nextjs`. Bounded context: `/plan-bounded-context`.

**Artifact chain:** implement-api → test-cases + BR coverage PASS + API test-results + audit; implement-ui → test-cases + BR coverage PASS + e2e evidence + audit; expand-test-coverage → test-cases + matrix + BR coverage + test-package Pending Approval; run-tests → scripts + test-results (after Approved); run-eval → completeness ledger + fix-queue; review-changes → review audit (consumes ledger); validate-kpi-metrics → kpi-validations + GO/NO_GO; application-summary → summary + harness.
