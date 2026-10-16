---

name: msd-test-cases-from-user-stories

description: >-

  User Story Excel → MSD E2E test-case workbook using the stored MSD rulebook.

  Business-process E2E depth, precondition alignment, optional consultant/clarification

  inputs. Use for /generate-test-cases-from-user-stories. Never read the bootstrap

  execution-plan Excel at runtime.

---



# MSD test cases from User Story Excel



## Preconditions



1. **MSD rulebook exists:** `docs/intake/msd-test-case-rulebook.yaml` (status Active).

2. **Source story rulebook exists:** `docs/intake/user-story-csv-rulebook.yaml`.

3. If the MSD rulebook is missing, run **one-time bootstrap** only: test-agent mode `rulebook-bootstrap` + `msd-test-case-rulebook-author` with `setup_xlsx`. Persist the rulebook; do not retain the setup workbook as a runtime dependency.

4. **Intake safety** on the User Story Excel: convert `.xlsx` → CSV under `artifacts/intake/.pipeline/`, then `python scripts/intake-safety-scan.py <csv>` — STOP on 2; redact/waive on 1.

5. **Requirement freshness:** When workshop open items were clarified after the initial session (e.g. post 28/09 follow-ups), supply `clarification_paths` and/or re-run `/generate-user-stories-from-transcript` before test generation. Attach consultant `consultant_story_excel` when functional stories exist — extraction notes must show traceability.



## Styling vs case data



- **Styling** (fonts, colors, Excel tables, row heights, column widths) is a **fixed factory contract** in `workbook.styling` and `scripts/msd_test_case_xlsx_layout.py`. Hardcoded styling values are allowed; they are not story content.

- **Case data** (titles, steps, expected results, preconditions, Application / ISV tokens) must come **only** from the User Story Excel and **cited** supplemental sources via extract → enrich → msd-test-case-extractor → `*-msd-test-case-rows.json`. Do not hardcode domain steps or copy bootstrap execution-plan cells.



## Runtime workflow



1. **Load MSD rulebook** — sheets, column roles, ID pattern, case model, **business_process_e2e**, **precondition_step_coherence**, enums, and **styling**. Never open `E2E test execution plan.xlsx` for content or styling at runtime.

2. **user-story-excel-analyzer** — `python scripts/msd_test_case_xlsx.py extract-stories --in <user_story_excel> --out artifacts/intake/<date>-msd-source-stories.json`. Binds columns via rulebook aliases. Attaches nearest Feature / Area Path and stripped `business_process`. Does not author cases.

3. **Optional enrich** — when operator supplies supplements (intake-safety on each untrusted path first):

   `python scripts/enrich-msd-source-stories.py --in artifacts/intake/<date>-msd-source-stories.json --out artifacts/intake/<date>-msd-source-stories-enriched.json [--consultant-excel ...] [--clarification ...] [--workshop-kb ...] [--transcript ...]`

   Use enriched JSON for downstream steps when present.

4. **msd-test-case-business-process-author** — per group, plan E2E paths (trigger → handoffs → outcome); up to `generation.case_model.per_group.max_cases` positive cases when distinct paths are evidenced; decompose AC into steps (`min_steps_positive`).

5. **msd-test-case-extractor** — implement cases from the plan; steps from cited AC/need/clarifications only; exception case only with evidence.

6. **msd-test-case-precondition-aligner** — align Preconditions with Step 1; no unstated active contract / approved onboarding / ISV state.

7. **msd-test-case-xlsx-writer** — persist `artifacts/intake/<date>-msd-test-case-rows.json`, then `python scripts/msd_test_case_xlsx.py write --json <rows.json> --out artifacts/intake/<date>-msd-e2e-test-cases.xlsx`.

8. **msd-test-case-compliance-validator** — `python scripts/validate-msd-test-case-xlsx.py` (includes **precondition coherence** gate). Parent rejects FAIL.



## Output paths



| Artifact | Path |

|----------|------|

| Extraction notes | `artifacts/intake/<YYYY-MM-DD>-msd-test-case-extraction.md` |

| Source stories JSON | `artifacts/intake/<YYYY-MM-DD>-msd-source-stories.json` |

| Enriched stories (optional) | `artifacts/intake/<YYYY-MM-DD>-msd-source-stories-enriched.json` |

| Case rows JSON | `artifacts/intake/<YYYY-MM-DD>-msd-test-case-rows.json` |

| Working register CSV (internal) | `artifacts/intake/.pipeline/<YYYY-MM-DD>-msd-test-cases-working.csv` |

| Validation JSON | `artifacts/intake/<YYYY-MM-DD>-msd-test-case-validation.json` |

| Public Excel | `artifacts/intake/<YYYY-MM-DD>-msd-e2e-test-cases.xlsx` |



## Row rules (summary)



- **Grain:** one register row per step; case-level fields repeated and identical within a Test Case ID.

- **IDs:** `TC{scenario:02d}-{P|N}{seq:02d}` from the rulebook. Scenario ID is the grouping sequence, not copied from ADO.

- **E2E depth:** positive cases ≥ `generation.business_process_e2e.min_steps_positive` with business-process narrative across roles/systems when sources cite them.

- **Preconditions:** must establish every entity/status Step 1 uses (`generation.precondition_step_coherence`).

- **Application / ISV:** tokens **cited** in stories or clarifications. Composite separator from the rulebook.



## Provenance



Each case in extraction notes: `behavior_id`, statement, `source_path` (user-story excel, consultant excel, clarification, transcript), `source_locator`, `confidence`. List consultant-only merges and post-workshop clarifications used.



Silent requirements → `ASSUMPTION-xxx` in notes; do not mark Done with pending blocking assumptions.



## Do not



- Read the bootstrap execution-plan workbook when the rulebook is present.

- Hand-author xlsx or add/remove columns.

- Emit functional-only one-step smoke tests when stories support E2E (register Open DQ instead).

- Invent process names, Dynamics modules, ISVs, SKUs, or failure paths.

- Emit `/expand-test-coverage` markdown catalogs or executable scripts from this skill.


