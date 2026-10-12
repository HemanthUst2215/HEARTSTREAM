# User story evaluation report

> Shape of `artifacts/evaluation/.pipeline/<date>-evaluation.json`.
> `scripts/evaluate_user_stories.py render` is the only writer of the HTML.

| Field | Value |
|-------|-------|
| schema_version | `1.0` |
| status | `Draft — Pending Method Review` |
| assumption_id | `ASSUMPTION-USEVAL-001` |
| inputs.manual_csv | path |
| inputs.generated_csv | path |
| inputs.transcript_path | path |

## matches[]
`match_id`, `manual_key`, `manual_title`, `generated_keys`, `generated_titles`, `match_type` (`1:1` \| `split` \| `merge`), `confidence`, `transcript_refs[]` (`locator`, `excerpt`).

## manual_only[]
`story_key`, `title`, `rationale`, `transcript_refs[]`.

## generated_only[]
`story_key`, `title`, `classification` (`valid_extra` \| `noise`), `rationale`, `transcript_refs[]`.

## metrics[]
One object per id in `user-story-evaluation-metrics.yaml`.

| Field | Required |
|-------|----------|
| metric_id | yes |
| owner | contract owner |
| kind | contract kind |
| display | yes, unless `na` |
| score | ratio or score; null allowed for `count`, `comparison`, `split` |
| na / na_reason | together when the formula says na |
| evidence[] | `statement`, `source_path`, `source_locator`, `confidence` |

`render` copies `name` and `formula` from the contract onto each metric before writing HTML.

## open_items[]
Include pending `ASSUMPTION-USEVAL-001` and any `BLOCKED_CONFLICT`.

## comparison[]
Side-by-side rows. `name`, `manual`, `ai`, `better` (`manual` | `ai` | `tie` | empty), `note`.

## conclusion
`headline`, `winner_line`, `reasons[]`, `limit`. The HTML places this section last.

## HTML sections
The script renders: status and input paths, the Manual/AI comparison table, metric cards, evidence, matched stories, manual-only stories, generated-only stories, open items, then the conclusion.
