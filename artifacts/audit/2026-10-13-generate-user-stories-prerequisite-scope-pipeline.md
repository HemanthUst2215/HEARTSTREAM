# Audit: Prerequisite scope + MSD365 entity pipeline for user stories

## What

Extended `/generate-user-stories-from-transcript` so workshop **prerequisite document(s)** define scope before transcript extraction. Added rulebook, skill, subagents, validators, and command/agent wiring. User stories require transcript + prerequisite alignment and MSD365 catalog mapping.

## Why

Operator requirement: scope from pre-workshop materials; requirements from transcript only when aligned; closed-world MSD365 business entities; full traceability.

## How

| Component | Path |
|-----------|------|
| Prerequisite rulebook | `docs/intake/workshop-prerequisite-scope-rulebook.yaml` |
| Skill | `.cursor/skills/workshop-prerequisite-analysis/SKILL.md` |
| Subagents | `workshop-prerequisite-analyzer`, `workshop-scope-compliance-validator` |
| Updated | `transcript-story-extractor`, `business-analyst-agent`, command, `user-story-from-transcript` skill |
| Scripts | `extract-docx-text.py`, `validate-user-story-workshop-scope.py`, `workshop_prerequisite_scope.py` |
| Config | `.cursor/config.yaml` → `workshop_prerequisite_scope` |

## Validation

- `python scripts/test_workshop_prerequisite_scope.py` — OK
- `python scripts/test_msd365_business_entity_scope.py` — OK (existing)

## Open Items

- Re-run pipeline with `prerequisite_paths` + transcript to produce knowledge base and scoped rows JSON.

## Next command

`/generate-user-stories-from-transcript` with `prerequisite_paths` and `transcript_path`.
