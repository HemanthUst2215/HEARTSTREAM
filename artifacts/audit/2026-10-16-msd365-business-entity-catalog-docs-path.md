# Audit: MSD365 business entity catalog path move

## What
Moved runtime catalog from `artifacts/intake/msd365-business-entity-catalog.json` to `docs/intake/msd365-business-entity-catalog.json`.

## Why
Align catalog with other permanent intake contracts under `docs/intake/` (rulebooks).

## How
- Moved JSON file; updated `DEFAULT_CATALOG` / `DEFAULT_JSON`, `.cursor/config.yaml`, rulebooks, command/skills/agents/subagents/templates, and build script defaults.
- Pipeline CSV bootstrap output remains `artifacts/intake/.pipeline/msd365-business-entity-catalog.csv`.

## Validation
- `python scripts/test_msd365_business_entity_scope.py` — OK (6 tests).

## Open Items
None.

## Next command
Re-bootstrap if needed: `python scripts/build-msd365-business-entity-catalog.py` (writes to `docs/intake/` by default).
