# work-item-reference-matcher

## Purpose
Match each generated user story to work items in `artifacts/work-items/**/*.json` using IDF-weighted title/description coverage + fuzzy scoring; populate ReferenceWorkItemIds and MatchScores in **user-stories.csv**.

## Parent
business-analyst-agent

## Must / Must NOT
- Must: For `/generate-user-stories-from-transcript`, use **work-item-mapping-agent** / `scripts/map-user-stories-to-work-items.py` (catalog `ID` on Epic/Feature rows). Do not run a retired `/generate-user-story` pipeline.
- Must: Include **all** matches ≥ threshold, sorted by score descending; pipe-delimited IDs and scores.
- Must NOT: Rely on exact title match only; drop valid lower-ranked matches.

## Inputs
- `artifacts/user-stories/.pipeline/stories-draft.json`
- `artifacts/work-items/` JSON exports (epic.json, feature.json, work-items.json, etc.)

## Outputs
- `artifacts/user-stories/user-stories.csv` (includes ReferenceWorkItemIds, MatchScores, Epic, Feature)
- `artifacts/user-stories/invest-scorecard.csv`

## Configuration
- `user_story_pipeline.match_threshold` in `.cursor/config.yaml` (default 50)

## Loop
Plan → Act → Observe → Reflect (max 3).

