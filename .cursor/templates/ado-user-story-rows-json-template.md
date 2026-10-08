# ADO user story rows JSON (input to `ado_user_story_csv.py write`)

> Agents produce this file; **never** hand-author the CSV. Template: one object per CSV row, keys = rulebook `csv.column_order` headers.

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
    "Title": "01. <Workshop name>",
    "Description": "<session scope>",
    "Area Path": "Day 2\\CRM",
    "Start Date": "28-09-2026 08:00"
  },
  {
    "Work Item Type": "User Story",
    "Title": "<short title>",
    "Description": "As a <role>, I need to <need>, so that <benefit>.",
    "Acceptance Criteria": "- <criterion one>\n- <criterion two>"
  },
  {
    "Work Item Type": "Issue",
    "Title": "<issue title>",
    "Description": "Risk: ...\nImpact: ...\nMitigation: ...",
    "Area Path": "Day 2\\CRM"
  }
]
```

Use `acceptance_criteria_cell()` / `issue_description_cell()` from `scripts/ado_user_story_csv_layout.py` when generating strings in code.
