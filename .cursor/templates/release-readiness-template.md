# Release Readiness — {{RELEASE_ID}}

> Input to release-agent Go/No-Go. GO forbidden with undocumented criticals.

| Field | Value |
|-------|-------|
| **Release** | {{version / train}} |
| **Date** | {{YYYY-MM-DD}} |
| **Environment** | staging → prod |
| **Release owner** | {{human — not agent}} |
| **Recommendation** | GO / NO_GO / CONDITIONAL |

## Scope

| Story / defect | Summary | In release | Verified |
|----------------|---------|------------|----------|
| | | yes/no | |

## Quality gates

| Gate | Required | Status | Evidence |
|------|----------|--------|----------|
| Plan Approved | yes | | |
| `/expand-test-coverage` | yes | | audit |
| `/review-changes` | yes | | code-review artifact |
| `/validate-kpi-metrics` | GO | | kpi-validations |
| BR coverage PASS | yes | | |
| SAST criticals | 0 unwaived | | |
| Open P0 defects | 0 | | issue logs |

## Security and compliance

| Check | Status | Notes |
|-------|--------|-------|
| Threat profile updated | | |
| Secrets scan | | |
| Compliance evidence | | |

## Operational readiness

| Item | Status | Owner |
|------|--------|-------|
| Runbooks updated | | sre-agent |
| SLO dashboards | | |
| Rollback tested | | |
| Canary / ring plan | | `canary-rollout-planner` |

## Risks and mitigations

| Risk | Severity | Mitigation | Accept? |
|------|----------|------------|---------|
| | | | yes/no |

## Conditional GO conditions

(if CONDITIONAL)

1. 

## Sign-off

| Role | Name | Decision | Date |
|------|------|----------|------|
| Release owner | | GO/NO_GO | |
| Security | | | |
| Domain SME | | | |

**Output path:** `docs/release/{{release-id}}-readiness.md`
