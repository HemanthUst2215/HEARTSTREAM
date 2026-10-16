# Audit: USHTML-MATCH-001

## What
Aligned Match type with source_references for `/generate-html-for-user-stories`.

## Rule
- **No Match** only when no supporting excerpt (placeholder only).
- **Partial / Exact** when at least one supporting reference exists (Exact when lexical best ≥ 0.35 in mechanical runner; analyzer uses full-story substantiation).

## How
- Contract, command, skill, subagent, report template updated.
- `scripts/generate_user_story_source_analysis.py`: `has_supporting_refs`, `match_type_from_evidence`, validate gate.
- Marketing runner updated; tests added.

## Validation
- `pytest scripts/test_generate_user_story_source_analysis.py`

## Next command
Re-run `/generate-html-for-user-stories` or marketing pipeline runner for refreshed HTML.
