# work-item-reference-matcher

## Purpose
Match generated stories to work items for legacy **user-stories.csv** pipelines (IDF + fuzzy). **Not** the Phase 5 mapper for transcript intake.

## Parent
business-analyst-agent (legacy CSV pipeline only)

## Must / Must NOT
- Must: For `/generate-user-stories-from-transcript`, defer to **work-item-mapping-agent** / `scripts/map-user-stories-to-work-items.py` — `epic.json` + `feature.json` only, generic config thresholds (rule `32-catalog-only-work-item-mapping.mdc`). Do not run a retired `/generate-user-story` pipeline or duplicate mapping in this subagent.
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

