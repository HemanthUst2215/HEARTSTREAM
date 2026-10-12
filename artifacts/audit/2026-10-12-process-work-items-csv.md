# Audit: /process-work-items-csv (EPIC.csv + Feature.csv)

**Date:** 2026-10-12  
**Command:** `/process-work-items-csv`  
**Sources:** `EPIC.csv`, `Feature.csv`

## What
Refreshed `artifacts/work-items/epic.json` (17 Epics) and `artifacts/work-items/feature.json` (221 Features) with matching summary markdown. Source CSVs not modified. No merge with `work-items.json`.

## Why
Operator requested `/process-work-items-csv` on kit-root `EPIC.csv` and `Feature.csv` to align catalog JSON with latest ADO exports.

## How
1. Intake safety scan on both CSVs → **CLEAN** (exit 0).
2. Schema profiles → `2026-10-12-schema-profile-epic.json`, `2026-10-12-schema-profile-feature.json`.
3. `scripts/csv-to-work-items-json.py` per file → JSON + summary; validation reports saved as `-epic` / `-feature` stems.
4. Manifest and validation index under `artifacts/work-items/2026-10-12-*`.

## Validation
- EPIC: **PASS** — 17 / 17 / 17; issues `[]`
- Feature: **PASS** — 221 / 221 / 221; issues `[]`

## Open Items
- **DQ-GL-CATALOG** (unchanged): GL workshop stories still need real R2R/GL **Feature** rows in ADO export before strong-match mapping can populate User Story `ID`s. Re-export `Feature.csv` after ADO updates, then re-run this command and mapping.

## Artifacts
- `artifacts/work-items/epic.json`, `epic-summary.md`
- `artifacts/work-items/feature.json`, `feature-summary.md`
- `artifacts/work-items/2026-10-12-manifest.json`
- `artifacts/work-items/2026-10-12-schema-profile.json` (index)
- `artifacts/work-items/2026-10-12-validation-report.json` (index)

## Next command
Re-run user-story mapping after GL Features exist in catalog:

`python scripts/map-user-stories-to-work-items.py --csv artifacts/intake/.pipeline/2026-10-12-user-stories-working.csv --work-items-dir artifacts/work-items --out-xlsx artifacts/intake/2026-10-12-user-stories-from-transcript.xlsx --log-json artifacts/intake/.pipeline/2026-10-12-work-item-mapping-log.json`

Or filter/summarize from `feature.json` by `parent.workItemId`.
