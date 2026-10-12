# /expand-test-coverage

## Invocation

`/expand-test-coverage` — transcript requirements matched to catalog Features, then a test-case CSV.

## Objective

Before any test case is written, read the transcript and list requirements. Match those requirements to `artifacts/work-items/epic.json` and `artifacts/work-items/feature.json`. Write test cases only for strong Feature matches whose parent Epic exists. Public output is one CSV. Columns and the Test Case Description shape come from `docs/intake/user-story-csv-rulebook.yaml`.

Traceability on every case: Transcript locator → Epic id → Feature id → Test Case.

## Use Agents

- orchestrator-agent
- quality-agent
- test-agent (mode `from-transcript`)

## Delegate to Subagents

- test-intake-normalizer (intake-safety on the transcript)
- test-case-generator (row JSON + canonical CSV writer)
- audit-trail-writer

## Enforce Rules

00, 07, 09, 10, 22, 31.

## Use Templates / Skills

`audit-trail-template.md`

`.cursor/skills/test-cases-from-transcript/SKILL.md`

Rulebook (column contract, not a template): `docs/intake/user-story-csv-rulebook.yaml`

## Runtime Inputs

### Required

- `transcript_path`
- `artifacts/work-items/epic.json`
- `artifacts/work-items/feature.json`

### Optional

- `output_slug` (filename suffix)

## Command-Specific Hardening

**Intake:** Run `python scripts/intake-safety-scan.py` on the transcript before test-agent. Exit 2 → STOP. Exit 1 → STOP until redaction or waiver.

**Order (hard):**
1. Requirements from the transcript, each with a locator. No cases yet.
2. Match to Feature title and `description.plainText`. Keep a match only at `work_item_mapping.strong_threshold` with `winner_margin`, and only when `parent.workItemId` is in epic.json.
3. test-case-generator writes cases only for those Features.
4. CSV via `scripts/ado_user_story_csv.py write`, then `scripts/validate-user-story-csv.py`. FAIL stays in Refine.

**CSV shape:** Rulebook `csv.column_order` only. Section order: Epic rows, Feature rows, Test Case rows. Test Case Description follows `test_case.description_format`. Acceptance Criteria uses `- ` bullets. Test Case ID blank. Epic and Feature IDs copied from JSON.

**Out of scope:** Test cases for unmatched requirements or Features that were not matched. New columns. Invented Epic or Feature titles. Executable scripts.

## Execution Policy

Plan → Act → Validate → Refine (max 3). Iteration 1 validator PASS → stop.

## Execution flow

| Phase | Role | Artifact |
|-------|------|----------|
| Intake | test-intake-normalizer | scan result in the audit |
| 1 Requirements | test-agent | requirement list with locators (in the audit) |
| 2 Match | test-agent | matched Feature + parent Epic, or unmatched |
| 3 CSV | test-case-generator | `artifacts/intake/<date>-test-cases.csv` |
| 4 Validate | test-case-generator | `artifacts/intake/<date>-test-case-validation.json` |

## Decision logic

- Transcript path missing → refuse.
- epic.json or feature.json missing → refuse.
- Scan exit 2 → refuse.
- No strong Feature match → write Epic/Feature rows only if any matched; otherwise no Test Case rows, and list unmatched requirements. Do not invent a Feature.

## Clarification Protocol

Register Open DQ for a missing transcript or an empty catalog. Do not invent requirements or catalog IDs.

## Artifact persistence

- `artifacts/intake/<date>-test-case-rows.json`
- `artifacts/intake/<date>-test-cases.csv`
- `artifacts/intake/<date>-test-case-validation.json`
- `artifacts/audit/<date>-expand-test-coverage-<task>.md`

## Definition of Done

- [ ] Intake-safety scan exit 0, or exit 1 with recorded waiver
- [ ] Requirements listed from the transcript before cases
- [ ] Every Test Case traces to one transcript locator, one Epic id, and one Feature id
- [ ] Feature id is a strong unique match and its parent Epic is in epic.json
- [ ] No case for an unmatched requirement
- [ ] CSV headers match the rulebook; validator exit 0
- [ ] Audit written

## Next command

```
✅ /expand-test-coverage complete.
**Next command:** Review `artifacts/intake/<date>-test-cases.csv`.
```
