# Unified Governed Plan — {{PLAN_NAME}}

> From `/plan-governed-stories`. Combines story-level execute rows; status **Proposed — Pending Approval**.

| Field | Value |
|-------|-------|
| **Plan ID** | UGP-{{slug}} |
| **Date** | {{YYYY-MM-DD}} |
| **BRD / story source** | {{path}} |
| **Status** | Proposed — Pending Approval |
| **Planner** | planner-agent (mode governed) |

## Objectives

-

## Story execute table

| Story / SP | AC summary | implement-api | implement-ui | expand-test-coverage | run-tests | run-eval | data/ddl | Open DQ |
|------------|------------|---------------|--------------|----------------------|-----------|----------|----------|---------|
| SP-01 | | yes/no | yes/no | yes | yes | yes | yes/no | DQ- |

## Dependency graph

```text
SP-01 (API) → SP-02 (UI) → SP-03 (tests)
```

## Gap report pointer

`artifacts/sprints/{{slug}}-gap-report.md`

## File ownership (parallel agents)

See `parallel-agent-file-ownership.md` — conflicts → stop, ask, DQ in audit.

## Approval

| Approver | Date | Status |
|----------|------|--------|
| | | Approved / Rejected |

**Next command after Approved:** `/implement-api`

**Output path:** `docs/forward/{{slug}}-unified-plan.md`
