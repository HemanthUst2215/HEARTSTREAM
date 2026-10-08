# Code Generation — Do's and Don'ts

> Applies to backend-agent, frontend-agent, change-agent, and all implement commands. Enterprise-grade output only.

| Field | Value |
|-------|-------|
| **Applies to** | `/implement-api`, `/implement-ui`, `/apply-requirements`, `/fix-issue` (Phase 2+) |
| **Enforced by** | scope.yaml, hooks, quality gates, code-review-agent |

## Do

| # | Rule | Evidence expected |
|---|------|-------------------|
| 1 | Match approved plan or cited SP/AC | audit cites plan path |
| 2 | Reuse existing controllers, services, components, hooks | no parallel duplicate types |
| 3 | Cite provenance for business behavior (rule 22) | behavior_id table in audit |
| 4 | Write tests for changed logic | test-results artifact |
| 5 | Use template-owned test structure (`java_test_templates/`, Playwright patterns) | `render_check.py` PASS |
| 11 | Persist template vars; run `tools/templates/render_check.py` on Java | `artifacts/templates/<resource>-vars.yaml` |
| 6 | Centralized error envelope and validation at boundaries | api-contract-template |
| 7 | Forward-only migrations | new Flyway version file |
| 8 | Write audit + update harness on phase change | artifacts/audit |
| 9 | Honor `.cursor/scope.yaml` write allowlists | |
| 10 | Register Open DQ when sources silent — do not invent | DQ-xxx in audit |

## Don't

| # | Rule | Consequence if violated |
|---|------|-------------------------|
| 1 | Invent FR/BR, UI copy, API fields, error semantics | Blocked from Ready |
| 2 | Skip human gates (plan Approved, fix proceed, cutover sign-off) | orchestrator refuse |
| 3 | Commit or log secrets, tokens, PII/PHI | security finding |
| 4 | Skip tests because change "looks small" | review block |
| 5 | Disable JaCoCo or lower coverage floors | quality-agent refuse |
| 6 | Edit applied migrations | data-agent violation |
| 7 | Add public `/generate-backend`, `/generate-frontend`, `/wire-*` commands | catalog-lock eval fail |
| 8 | Script or run tests before `test-cases-br-coverage.md` PASS | test-agent refuse |
| 9 | Self-approve BRD or sprint plan | self-approve-forbidden eval |
| 10 | Paper over API bugs in UI | frontend-agent Must NOT |
| 11 | Rewrite controller style or skip render_check on Java | quality/review Block |

## Ambiguity handling

- Stop on `# AMBIGUITY` in templates — do not guess structure.
- Agent-owned Java only in hybrid_policy slots; agent-owned tests cite `docs/test-cases.md` IDs.
- Max 3 loop iterations; escalate with owners after iteration 3.

**Reference:** `.cursor/rules/30-production-fix-governance.mdc`, `22-behavior-provenance-and-anti-invention.mdc`
