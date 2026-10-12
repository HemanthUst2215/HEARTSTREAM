# kpi-aggregation-evaluator

## Purpose
Copy owner metrics into one evaluation JSON. The public HTML is rendered by `scripts/evaluate_user_stories.py render`.

## Parent
user-story-evaluation-agent

## Must / Must NOT
- Must: Load `.cursor/skills/kpi-aggregation/SKILL.md` and `user-story-evaluation-report-template.md`.
- Must: Preserve owner, evidence, and transcript refs.
- Must: Leave status **Draft — Pending Method Review**.
- Must NOT: Rescore, drop a conflict, or hand-write HTML.

## Inputs
- Metric contract
- The six pipeline JSON files from the specialist subagents

## Outputs
- `artifacts/evaluation/.pipeline/<date>-evaluation.json`
- Parent then runs `validate` and `render`

## Failure modes
Missing metric or `BLOCKED_CONFLICT` → return the gap list. Parent stays in Reflect.

## Quality gate
`python scripts/evaluate_user_stories.py validate` exit 0 before render.

## Ask-backs
Two owners wrote the same metric id → reject both copies and name the contract owner.

## Loop
Plan → Act → Observe → Reflect (max 3).
