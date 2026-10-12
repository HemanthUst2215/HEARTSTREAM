# MSD test-case rows JSON (input to `msd_test_case_xlsx.py write`)

> Agents produce this file; **never** hand-author the Excel. Keys under each case/step are **role names** from the rulebook (`columns.register.roles`). The writer maps roles → header labels.

## Path

`artifacts/intake/<YYYY-MM-DD>-msd-test-case-rows.json`

## Write command

```bash
python scripts/msd_test_case_xlsx.py write \
  --json artifacts/intake/<YYYY-MM-DD>-msd-test-case-rows.json \
  --out artifacts/intake/<YYYY-MM-DD>-msd-e2e-test-cases.xlsx
python scripts/validate-msd-test-case-xlsx.py --xlsx artifacts/intake/<YYYY-MM-DD>-msd-e2e-test-cases.xlsx
```

## Shape

Coverage and ISV sheets are **derived by the writer**. Do not include them here.

```json
{
  "meta": {
    "source_excel": "<user-story workbook path>",
    "project_label": "<from config or rulebook fallback>"
  },
  "cases": [
    {
      "scenario_id": 1,
      "business_process": "<grouping name from stories, not invented>",
      "test_case_id": "<from id_patterns.test_case_id>",
      "test_case_title": "<short headline>",
      "test_type": "<allowed test_types value>",
      "priority": "<allowed priority value>",
      "preconditions": "<cited setup only>",
      "source_flow": "<source workbook + story IDs>",
      "coverage_focus": "<one-line synthesis>",
      "provenance": {
        "behavior_id": "TC-<id>",
        "source_path": "<user-story excel>",
        "source_locator": "<sheet/row or story ID>",
        "confidence": "derived"
      },
      "steps": [
        {
          "step_number": 1,
          "detailed_test_step": "<imperative action cited from AC/need>",
          "step_owner": "<role from story or named actor>",
          "application_isv": "<cited Dynamics/integration token(s)>",
          "test_data": "<cited values or empty>",
          "expected_result": "<observable outcome>"
        }
      ]
    }
  ]
}
```
