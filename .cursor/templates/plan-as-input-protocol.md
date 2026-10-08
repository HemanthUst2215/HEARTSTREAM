# Plan-as-input protocol

Slash commands resolve runtime inputs from **governed plans**, **sprint plans**, **story packs**, and **prior artifacts** before registering remaining gaps.

## Plan types

| Type | Path pattern | Used by |
|------|--------------|---------|
| Per-story governed plan | `.cursor/plans/sprint<N>/<story-id>-governed-implementation-plan.md` | `/implement-api`, `/implement-ui`, quality closeout |
| Sprint unified plan | `.cursor/plans/sprint<N>/sprint<N>-unified-governed-plan.md` | `/compliance-check`, `/sprint-handoff`, `/deliver-sprint` |
| Sprint backlog | `artifacts/sprints/<id>-plan.md` | `/deliver-sprint`, implement-* |
| Story pack | `docs/sprint<N>/userstory/*-techno-functional-pack.md` | `/plan-governed-stories` |

## Invoker minimal prompts

```
/implement-api
@governed_plan: .cursor/plans/sprint3/<story-id>-governed-implementation-plan.md
```

```
/plan-governed-stories
@story_artifact: docs/sprint3/userstory/<pack>.md
```

Optional: `plan_step: <n>` — otherwise first `pending` or `in_progress` row matching the command.

## Resolve-before-ask (mandatory)

When `governed_plan`, `sprint_governed_plan`, or `@story_artifact` is supplied:

1. Load plan, story pack, `docs/sprint<N>/manifest.json`, execution logs, upstream artifact paths.
2. Register Open DQ when §Gap register has **Open** critical items or a required binding is still `TBD` after repo introspection. Do not invent. Critical authz/money/PII/breaking-schema gaps remain a hard-stop (not a clarification round).
3. Never re-ask values present in §Workspace bindings, story pack, manifest, or execution log.
4. Skip Clarification Protocol items answerable from resolved inputs. Do not STOP for a numbered clarification round except human gates.
5. After Definition of Done, update plan execution flow, execution log, and manifest.

## Command execution flow rows (locked)

Governed and sprint plans MUST list execute commands in this order:

1. `/implement-api`
2. `/implement-ui`
3. `/expand-test-coverage` (then human test-package **Approved**)
4. `/run-tests`
5. `/run-eval`
6. `/review-changes`
7. `/application-summary`

Do not emit generate-backend / generate-frontend / wire-fe-be as plan steps.
