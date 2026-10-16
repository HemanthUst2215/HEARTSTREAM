# Audit: /generate-html-for-user-stories (marketing-ws03)

## What
Independent source-traceability HTML reports for CRM manual workshop stories (44 US) and AI-generated marketing WS03 stories (14 US).

## Why
Operator requested validation against transcript, MoM, pre-read, and SOW features without manual-vs-AI comparison.

## How
- `allocate-run` slug `marketing-ws03` (2026-10-16)
- Intake-safety exit 0 on xlsx + normalized `.txt` extracts (transcript, mom, preread). Raw MoM PDF exit 1 (card-number-shaped PII hits on PDF text extraction); pipeline used `artifacts/intake/.pipeline/2026-10-16-marketing-ws03-mom.txt` sourced from operator MoM PDF.
- `prepare-kb` → unified KB (prerequisite KB + corpus chunks + SOW features)
- `prepare-stories` + traceability analysis + `validate`/`render` per side
- Runner: `artifacts/evaluation/.pipeline/2026-10-16-marketing-ws03-run-source-analysis.py`

## Inputs
| Role | Path |
|------|------|
| Manual | `CRM - Workshop Stories.xlsx` → `.pipeline/2026-10-16-marketing-ws03-manual.csv` |
| AI | `artifacts/intake/2026-10-13-marketing-ws03-user-stories-from-transcript.xlsx` → `.pipeline/2026-10-16-marketing-ws03-generated.csv` |
| Transcript | `artifacts/intake/2026-10-13-marketing-ws03-transcript.txt` (from operator docx) |
| MoM | `artifacts/intake/.pipeline/2026-10-16-marketing-ws03-mom.txt` |
| Pre-read | `artifacts/intake/.pipeline/2026-10-13-marketing-ws03-prerequisite.txt` |
| Features | `artifacts/work-items/SOW.json` |

## Validation
- [x] Output-path gate CLEAR
- [x] Both analysis JSON `validate` PASS
- [x] Both HTML via `render` only
- [x] No manual-vs-AI pairing artifacts

## Open Items
- `ASSUMPTION-USHTML-001` — method review (lexical grounding thresholds in runner).
- MoM PDF waiver for full-binary scan if operators require scanning PDF directly.

## Next command
Review public HTML/JSON under `artifacts/evaluation/2026-10-16-*-user-story-analysis-marketing-ws03.*`
