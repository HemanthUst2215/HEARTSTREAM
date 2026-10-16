# ADO user story rows JSON (input to `ado_user_story_csv.py write`)

> Agents produce this file; **never** hand-author the CSV. Template: one object per CSV row, keys = rulebook `columns.stories.order` headers (`csv.column_order` is an alias).

## Path

`artifacts/intake/<YYYY-MM-DD>-user-story-rows.json`

## Write command

```bash
python scripts/ado_user_story_csv.py write \
  --json artifacts/intake/<YYYY-MM-DD>-user-story-rows.json \
  --out artifacts/intake/.pipeline/<YYYY-MM-DD>-user-stories-working.csv
python scripts/validate-user-story-csv.py --csv artifacts/intake/.pipeline/<YYYY-MM-DD>-user-stories-working.csv
```

## Minimal shape (abbreviated)

Do not add Epic/Feature objects here. Mapping writes matched catalog Epic/Feature rows (with IDs) into the public Excel.

```json
[
  {
    "Work Item Type": "Workshop",
    "Title 1": "WS-<id> - <topic summary>",
    "Description": "<session scope>",
    "Area Path": "<Iteration>\\<Area>",
    "State": "In Review"
  },
  {
    "Work Item Type": "User Story",
    "Title 3": "<short title>",
    "Description": "As a <role>, I need to <need>, so that <benefit>.",
    "Acceptance Criteria": "- <criterion one>\n- <criterion two>",
    "State": "New"
  },
  {
    "Work Item Type": "Issue",
    "Title 3": "<issue title>",
    "Description": "Risk: ...\nImpact: ...\nMitigation: ...",
    "Area Path": "<Iteration>\\<Area>"
  }
]
```

Use `acceptance_criteria_cell()` / `issue_description_cell()` from `scripts/ado_user_story_csv_layout.py` when generating strings in code.
