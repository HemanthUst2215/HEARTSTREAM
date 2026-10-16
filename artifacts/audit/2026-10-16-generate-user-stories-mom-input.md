# Audit — MoM input for `/generate-user-stories-from-transcript`

## What
Added **Minutes of Meeting (MoM)** as a required runtime input alongside transcript and workshop prerequisites. Updated command, business-analyst-agent, subagents, skills, scope rulebook, validation script, config, and extraction template.

## Why
Workshop user-story generation must cite official minuted decisions and agenda alignment in addition to the spoken transcript and prerequisite scope materials.

## How
- New subagent: `.cursor/subagents/mom-analyzer.md`
- Command/skill/agent wiring for `mom_paths`, docx extract, intake-safety scan, and row JSON fields `mom_locator` / `mom_source_path`
- `validate-user-story-workshop-scope.py --require-mom` enforced via workshop-scope-compliance-validator

## Validation
- `python scripts/test_workshop_prerequisite_scope.py` — PASS (5 tests)

## Open Items
- Existing `artifacts/intake/*-user-story-rows.json` from prior runs lack MoM fields; re-run pipeline with `mom_paths` to pass `--require-mom`.

## Next command
`/generate-user-stories-from-transcript` with `transcript_path`, `mom_paths`, and `prerequisite_paths`.
