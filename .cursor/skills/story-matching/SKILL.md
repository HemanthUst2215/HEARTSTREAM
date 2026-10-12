---
name: story-matching
description: >-
  Pair manual user stories with generated user stories for /evaluate-user-stories.
  Use for story-matching-evaluator. Owns Granularity.
---

# Story matching

## Parent
user-story-evaluation-agent

## Inputs
- Evaluation packet (`manual_stories`, `generated_stories`, `candidate_pairs`)
- Transcript text

## Procedure
1. Read every User Story on both sides. `candidate_pairs` are optional retrieval aids. A high Jaccard score is not a match.
2. Match when the generated story and the manual story state the same transcript requirement. Cite the transcript locator on every match.
3. `match_type` is `1:1`, `split` (one manual story covered by several generated stories), or `merge` (several manual stories covered by one generated story).
4. Leave unmatched rows unmatched. Do not force a pair.
5. Score **Granularity**: generated User Story rows that state exactly one capability, divided by generated User Story rows. A stacked "I need to" or a split/merge that fragments one capability is a miss. Cite the story key and the transcript span.

## Output
`artifacts/evaluation/.pipeline/<date>-story-matches.json`

```json
{
  "matches": [],
  "unmatched_manual_keys": [],
  "unmatched_generated_keys": [],
  "metrics": [
    {
      "metric_id": "granularity",
      "owner": "story-matching-evaluator",
      "kind": "ratio",
      "display": "",
      "score": null,
      "evidence": []
    }
  ]
}
```

Each match needs `match_id`, `manual_key`, `manual_title`, `generated_keys`, `generated_titles`, `match_type`, `confidence` (`high` / `medium` / `low`), and `transcript_refs`.

## Do not
- Score Recall, Precision, hallucination, Epic agreement, or acceptance criteria.
- Invent a transcript quote.
