# Audit: /generate-html-for-user-stories factory wiring

## What
Added public command `/generate-html-for-user-stories` with skill, subagents, templates, config block, orchestrator route, and `scripts/generate_user_story_source_analysis.py` (allocate-run, prepare-kb, prepare-stories, validate, render).

## Why
Operators need independent HTML traceability reports for manual and AI user stories against transcript, MoM, pre-read, and SOW features — without manual-vs-AI benchmarking.

## How
- Primary: `user-story-evaluation-agent` mode `source-traceability-html` (no new peer primary).
- Subagents: `source-knowledge-base-unifier`, `user-story-source-traceability-analyzer` (run per side).
- Public outputs: versioned `*-manual-user-story-analysis*.html` and `*-ai-user-story-analysis*.html` under `artifacts/evaluation/`.
- Regression: `scripts/test_generate_user_story_source_analysis.py`.

## Validation
- [x] Command DoD documented in `.cursor/commands/generate-html-for-user-stories.md`
- [x] Structural contract YAML + report template
- [x] Tests added for allocate-run, prepare-kb, validate, render

## Open Items
- `ASSUMPTION-USHTML-001` — method acceptance for traceability scoring (human gate, same pattern as USEVAL).

## Next command
Run `/generate-html-for-user-stories` with workshop inputs when ready.
