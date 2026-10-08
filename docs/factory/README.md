# Factory docs

## Pipeline phases (operator)

Step-by-step operator guides (agents, subagents, artifacts, refuse/STOP, human gates). Validated against `.cursor/commands/`. Where the flow starts, human gates, and what each command does:

1. [Intake and planning](pipeline-phases/01-intake-and-planning.md) — recordings, Figma, BRD, stories, plan **Approved**
2. [Implement API and UI](pipeline-phases/02-implement-api-and-ui.md) — `/implement-api` → `/implement-ui`
3. [Test case write and execution](pipeline-phases/03-test-cases-and-execution.md) — `/expand-test-coverage` → human package → `/run-tests`
4. [Evals, review, and summary](pipeline-phases/04-eval-review-and-summary.md) — `/run-eval` → `/close-eval-gaps` → `/review-changes` → `/validate-kpi-metrics` → `/application-summary`
5. [Fix issue](pipeline-phases/05-fix-issue.md) — reactive `/fix-issue` (not on the sprint spine)

## Other factory docs

- [playwright-automation-mvp-plan.md](playwright-automation-mvp-plan.md) — AI-assisted Playwright test automation MVP (codegen agent, CI integration, future self-heal/coverage agents).
- [agent-regulatory-body-and-ops-hub.md](agent-regulatory-body-and-ops-hub.md) — Agent Cards, telemetry, drift detection, and Factory Ops Hub design.
- [external-platform-observability.md](external-platform-observability.md) — External platforms for live tracking, monitoring, and observability (Langfuse, OTel, Datadog, etc.).
- [lineage-map.md](lineage-map.md) — keep / generalize / drop ledger for source factories.
- [CURSOR-FLOW.md](../../CURSOR-FLOW.md) — Cursor operator map.
- [CLAUDE-FLOW.md](../../CLAUDE-FLOW.md) — Claude Code operator map.
