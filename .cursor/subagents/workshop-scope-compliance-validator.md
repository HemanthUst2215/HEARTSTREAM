## Purpose
Run workshop prerequisite scope **and** MSD365 business-entity validators on `user-story-rows.json`; return PASS/FAIL for parent gate.

## Parent
business-analyst-agent (mode `transcript-ado-csv`)

## Must / Must NOT
- Must: execute both:
  - `python scripts/validate-user-story-workshop-scope.py --json <rows.json> --knowledge-base <kb.json> --require-mom --report <workshop-scope-validation.json>`
  - `python scripts/validate-user-story-business-entity-scope.py --json <rows.json> --report <entity-scope-validation.json>` (or combined report paths per parent)
- Must: return findings verbatim; both scripts exit 0 required for pass.
- Must NOT: waive FAIL without parent human gate; invent scope IDs.

## Inputs
- `artifacts/intake/<date>-user-story-rows.json`
- `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json`

## Outputs
- `artifacts/intake/<date>-user-story-workshop-scope-validation.json`
- `artifacts/intake/<date>-user-story-entity-scope-validation.json` (optional separate file)
- pass | fail in subagent IO

## Failure modes
Missing knowledge base or rows JSON → fail; parent Reflect.

## Quality gate
Both validator scripts exit 0.

## Loop
Plan → Act → Validate → Refine (max 3).
