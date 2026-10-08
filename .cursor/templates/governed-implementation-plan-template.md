# Governed Implementation Plan — {{STORY_ID}}

> From `/plan-governed-stories`. Status **Proposed — Pending Approval** until human approves.

| Field | Value |
|-------|-------|
| **Plan ID** | GIP-{{story_id}} |
| **Story ID** | {{SP-xxx}} |
| **`@story_artifact`** | {{path to techno-functional pack}} |
| **Date** | {{YYYY-MM-DD}} |
| **Planner** | planner-agent (mode governed) |
| **Readiness** | Ready / Gated |

## Workspace bindings

| Binding | Value |
|---------|-------|
| `implementation_module_root` | ${modules.api} or ${modules.python} |
| `implementation_frontend_root` | ${modules.ui} |
| `contract_version` | {{OpenAPI semver}} |
| `envelope_policy` | per api-contract-template |
| `artifact_namespace` | {{sprint folder}} |

## Story pack excerpts

| Section | Pointer / summary |
|---------|-------------------|
| DDL | |
| API surface | |
| UI workflow | |
| Wiring sequence | |
| Data tables | |

## Gap register

| ID | Dimension (DDL/API/UI/Wiring/Data) | Status | Question | Owner |
|----|-----------------------------------|--------|----------|-------|
| DQ- | | open/closed | | |

## Command execution flow (locked)

| Step | Command | Status | Runtime bindings | Artifacts expected |
|------|---------|--------|------------------|-------------------|
| 1 | /implement-api | pending/done/blocked | SP, OpenAPI | API code, migrations, test-results |
| 2 | /implement-ui | pending | wiring gate | UI, e2e evidence |
| 3 | /expand-test-coverage | pending | rule_source | cases, BR PASS, test-package Pending Approval |
| 4 | /run-tests | pending | package Approved | scripts, test-results |
| 5 | /run-eval | pending | rule_source | completeness ledger, fix-queue |
| 6 | /review-changes | pending | ledger | review-findings |
| 7 | /validate-kpi-metrics | pending | | kpi-validations |
| 8 | /application-summary | pending | | summary |

Do **not** add `/generate-backend`, `/generate-frontend`, or `/wire-*`.

## Execution log

| Date | Command | Audit path | DoD | Notes |
|------|---------|------------|-----|-------|
| | | `artifacts/audit/…` | met/partial | |

## Approval

| Approver | Date | Status |
|----------|------|--------|
| | | Proposed — Pending Approval / **Approved** |

**Output path:** `.cursor/plans/{{story_id}}-governed-plan.md` or `docs/forward/{{story_id}}-plan.md`

**Next command after Approved:** `/implement-api`
