---
name: user-story-generation
description: >-
  Transcript or docs to user-stories.csv and invest-scorecard.csv with work-item
  matching. Retired public command `/generate-user-story` — use `/generate-user-stories-from-transcript`.
---

# User story generation

## When to use
- Do not run as a public command. Story authoring + INVEST + mapping live on `/generate-user-stories-from-transcript`.

## Phases
1. **Analyze** — transcript-analyzer → cited facts (no invented FR/BR).
2. **Author** — business-analyst-agent drafts stories into `artifacts/user-stories/.pipeline/stories-draft.json` (schema below).
3. **AC** — gherkin-acceptance-criteria-writer fills `acceptanceCriteria`.
4. **Match + INVEST + CSV** — `python scripts/generate-user-story-outputs.py --out-dir artifacts/user-stories`.

## Draft JSON schema (internal)
```json
{
  "sourceTranscript": "transcript-001",
  "stories": [
    {
      "userStoryId": "US-001",
      "title": "",
      "description": "",
      "acceptanceCriteria": "",
      "priority": "High",
      "epic": "",
      "feature": "",
      "keywords": [],
      "businessContext": ""
    }
  ]
}
```

## Work-item matching
- Index: all `artifacts/work-items/*.json` with `workItems[]`.
- Signals: title, description, AC, epic/feature labels, keywords, businessContext, parent epic titles.
- Scoring: 50% IDF title coverage + 20% description coverage + 20% TF-IDF cosine + 10% title fuzzy (0-100).
- Include every match ≥ `user_story_pipeline.match_threshold` (default 50).

## Outputs (under `artifacts/user-stories/`)
- `user-stories.csv`
- `invest-scorecard.csv`

## Must NOT
- Ship user stories as final JSON/MD/TXT/XLSX
- Merge work-item CSV exports
- Skip pipeline after drafting

