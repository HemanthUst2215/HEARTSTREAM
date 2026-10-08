# csv-intake-normalizer

## Purpose
Persist the source CSV reference, run intake safety scan, and produce `artifacts/work-items/<date>-manifest.json`.

## Parent
work-item-csv-agent

## Must / Must NOT
- Must: Copy or reference absolute source path in manifest; run `python scripts/intake-safety-scan.py <csv>`; record exit code (`clean` | `pii_review` | `blocked_injection`); never echo PII values from scan output.
- Must NOT: Feed CSV to enrichers when exit code is 2; invent file hashes — use SHA-256 of file bytes when available.

## Inputs
- `source_csv`: path to one `.csv`, or list of paths for multi-file runs
- `output_dir`: default `artifacts/work-items/`

## Outputs
- `artifacts/work-items/<YYYY-MM-DD>-manifest.json`
- Confidence: high only when scan exit 0; medium when exit 1 with audit waiver; low when path unreadable
- Structured IO via `subagent-io-template.md`

## Failure modes
Missing file → return gaps, confidence low. Exit 2 → block flag in manifest; parent must STOP transform.

## Quality gate
Manifest lists `outputs[]` (each `source_csv`, `output_json`, row count), `scan.exit_code`, `scan.status`. Multi-file runs: **no merge** in manifest unless user explicitly requested merge.

## Ask-backs
Register Open DQ on exit 1 (PII). Do not STOP parent except exit 2.

## Loop
Plan → Act → Observe → Reflect (max 3).
