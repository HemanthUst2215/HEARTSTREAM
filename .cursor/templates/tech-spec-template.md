# Technical Specification — {{FEATURE_OR_SLICE}}

> From documentation-agent (mode tech-spec) when a plan or implement step needs a spec. Rule 28: context, scope, assumptions, risks, rollout, rollback required. Not a public `/generate-user-story` command.

| Field | Value |
|-------|-------|
| **Spec ID** | TS-{{slug}} |
| **Status** | Draft / Review / Approved |
| **Author** | documentation-agent |
| **Story / SP refs** | {{ids}} |
| **Date** | {{YYYY-MM-DD}} |
| **Related BRD** | {{path or N/A}} |

## Context

- **Problem statement:**
- **Business outcome:** (cite FR/BR)
- **Current state:**
- **Proposed solution summary:**

## Scope

### In scope

-

### Out of scope

-

## Assumptions

| ID | Assumption | Validated | Owner |
|----|------------|-----------|-------|
| ASSUMPTION- | | yes/no | |

## Architecture

### Components affected

| Layer | Component | Change type |
|-------|-----------|-------------|
| API | | new/modify |
| UI | | |
| Data | | |
| Infra | | |

### Sequence / flow

```text
(describe main flow)
```

### API changes

| operationId | Change | Breaking |
|-------------|--------|----------|
| | | yes/no |

### Data model changes

| Entity / table | Change | Migration |
|----------------|--------|-----------|
| | | Flyway V… |

## NFRs

| NFR | Target | Verification |
|-----|--------|--------------|
| Security | | |
| Performance | | |
| Availability | | |
| Observability | logs/traces | |

## Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| | | L/M/H | L/M/H | |

## Rollout plan

| Phase | Action | Success criteria |
|-------|--------|------------------|
| 1 | Feature flag / dark launch | |
| 2 | Limited rollout | |
| 3 | GA | |

## Rollback plan

1. 
2. 
**Data rollback constraints:**

## Test approach

| Layer | Strategy | AC mapping |
|-------|----------|------------|
| Unit | | |
| Integration | | |
| E2E | | |

## Open questions

| DQ ID | Question | Owner | Blocking |
|-------|----------|-------|----------|
| | | | |

## Traceability

| FR/BR/AC | Spec section | Test case |
|----------|--------------|-----------|
| | | TC- |

**Output path:** `docs/specs/{{slug}}-tech-spec.md`
