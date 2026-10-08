# Execution options

After the sprint or governed plan is **Approved**, run the locked execute spine.

## Option A — Manual

```
/implement-api → /implement-ui → /expand-test-coverage → [human: test-package Approved] → /run-tests → /run-eval → /review-changes → /application-summary
```

Skip `/implement-api` or `/implement-ui` only when the approved plan has no work in that layer (record skip in audit).

## Option B — Batch

```
/deliver-sprint
```

Orchestrator runs the same spine. **STOP** after `/expand-test-coverage` Pending Approval. Resume `/run-tests` after human Approved.

## Surgical (not a second style)

```
/apply-requirements   # cited BR/story IDs only
/review-changes
```
