# Pull Request — {{TITLE}}

> From `/pr-assist`. Trace to stories, AC, and audit evidence.

| Field | Value |
|-------|-------|
| **Branch** | {{feature-branch}} |
| **Target** | {{main / develop}} |
| **Sprint / SP refs** | {{ids}} |
| **Commands completed** | {{implement-api → … → review-changes}} |
| **Audit** | `artifacts/audit/{{latest}}.md` |

## Summary

{{2–4 sentences: what and why}}

## Type of change

- [ ] Feature
- [ ] Bug fix (`/fix-issue` — link issue log)
- [ ] Refactor / cleanup
- [ ] Infra / CI
- [ ] Docs only

## Changes by area

| Area | Files / modules | Notes |
|------|-----------------|-------|
| API | | |
| UI | | |
| Tests | | |
| Migrations | forward-only: yes/no | |
| Contracts | OpenAPI synced: yes/no | |

## Test plan

| Suite | Command | Result | Evidence |
|-------|---------|--------|----------|
| Unit (API) | | pass/fail | |
| Unit (UI) | | | |
| E2E | `npm run test:e2e` | | `artifacts/e2e-test-results-*.md` |
| BR coverage | | PASS required | `docs/test-cases-br-coverage.md` |
| Security | SAST/SCA | | |

## Screenshots / demos

(if UI change)

## Breaking changes

- [ ] None
- [ ] API breaking — consumer notified: 
- [ ] Migration required — runbook: 

## Checklist

- [ ] Plan was **Approved** (if execute-phase work)
- [ ] No secrets in diff
- [ ] Harness progress updated
- [ ] CODEOWNERS gates respected

## Related artifacts

| Artifact | Path |
|----------|------|
| Issue log | `artifacts/issues/…` |
| KPI validation | `docs/quality/kpi-validations/…` |
| Application summary | |

**Output path:** Used as PR body via `gh pr create`; draft stored in `artifacts/pr/{{date}}-{{slug}}.md`
