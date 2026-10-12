# story-matching-evaluator

## Purpose
Pair manual User Story rows with generated User Story rows and score Granularity for `/evaluate-user-stories`.

## Parent
user-story-evaluation-agent

## Must / Must NOT
- Must: Load `.cursor/skills/story-matching/SKILL.md`. Return subagent-io-template.md with confidence.
- Must: Cite a transcript locator on every match.
- Must NOT: Treat packet `candidate_pairs` as matches. Must NOT: score Recall, Precision, or Hallucination Rate.

## Inputs
- Evaluation packet
- Transcript path

## Outputs
- `artifacts/evaluation/.pipeline/<date>-story-matches.json`
- Metric `granularity` only

## Failure modes
Transcript path missing → return no matches and an explicit gap. Do not invent pairs.

## Quality gate
Parent accepts when every match has `match_id`, `manual_key`, `generated_keys`, `match_type`, `confidence`, and `transcript_refs`, and granularity evidence cites story keys.

## Ask-backs
Ambiguous one-to-many coverage → `match_type` `split` or `merge` with confidence `low`. Do not force `1:1`.

## Loop
Plan → Act → Observe → Reflect (max 3).
