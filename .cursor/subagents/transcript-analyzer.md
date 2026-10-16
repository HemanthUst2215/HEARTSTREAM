## Purpose
Raw transcript → cited facts, conflicts, quotes.

## Parent
requirements-agent

## Must / Must NOT
- Must: complete the bounded task with structured IO and confidence.
- Must NOT: Do not resolve conflicts or invent FR/BR.

## Inputs
- transcript_paths
- Optional `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json` — when supplied by parent, interpret facts using prerequisite terminology and scope boundaries (do not add requirements from prerequisites alone)

## Outputs
- artifacts/intake/<date>-intake-notes.md (facts section)
- Confidence: high | medium | low
- Unresolved assumptions list

## Failure modes
Incomplete input → partial result with explicit gaps.

## Quality gate
No unsourced requirements; conflicts listed not resolved.

## Ask-backs
Register Open DQ for parent if unclear. Do not invent. Do not STOP the parent except human gates.

## Loop
Plan → Act → Observe → Reflect (max 3).
