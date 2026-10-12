---
name: coverage-analysis
description: >-
  Score recall, precision, manual-only stories, and generated-only valid extras
  versus noise. Use for coverage-analysis-evaluator during /evaluate-user-stories.
---

# Coverage analysis

## Parent
user-story-evaluation-agent

## Inputs
- `story-matches.json`
- `hallucination.json`
- Packet story counts

## Procedure
Use the formulas in `.cursor/templates/user-story-evaluation-metrics.yaml` for:

- `recall`
- `precision`
- `manual_only_stories`
- `generated_only_stories` (`valid_extra` vs `noise`)

Precision denominator is matched generated rows plus noise. Valid extras stay out of that denominator.

A generated-only row is `valid_extra` only when hallucination evidence says the transcript states that requirement. It is `noise` only when hallucination evidence says the transcript does not. If the two files disagree, return `BLOCKED_CONFLICT` for that row and do not pick a class.

List every manual-only and generated-only story with title, rationale, and transcript refs.

## Output
`artifacts/evaluation/.pipeline/<date>-coverage.json` containing the four metrics. `owner` is `coverage-analysis-evaluator`.

## Do not
- Rematch stories.
- Recompute hallucination rate.
- Average a conflict.
