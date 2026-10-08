# Incremental Change Plan — {{SLICE}}

> From `/apply-requirements`. Surgical, cited-only diffs — no silent semantic changes.

| Field | Value |
|-------|-------|
| **Plan ID** | ACR-{{YYYYMMDD}}-{{slug}} |
| **Date** | {{YYYY-MM-DD}} |
| **Agent** | change-agent |
| **Trigger** | {{BRD delta, AC change, waiver}} |
| **Status** | Draft / Approved / Applied |

## Change summary

- **What changes:** (1 paragraph)
- **Why now:** (cite FR/BR/AC or decision log)
- **Blast radius:** API / UI / data / tests

## Cited requirements

| ID | Statement | source_path | locator |
|----|-----------|-------------|---------|
| BR- | | | |

## File-level plan

| File | Change type | Description | Cited rule |
|------|-------------|-------------|------------|
| | modify | | AC- |

## Test impact

| Existing TC | Update needed | New TC |
|-------------|---------------|--------|
| TC- | yes/no | TC- |

## Rollout

| Step | Action | Rollback |
|------|--------|----------|
| 1 | | |

## Validation

- [ ] behavior-provenance recorded for each change
- [ ] test-cases updated if AC changed
- [ ] BR coverage re-run if cases changed
- [ ] `/review-changes` after apply

**Output path:** `artifacts/sprints/{{date}}-incremental-change-plan.md`
