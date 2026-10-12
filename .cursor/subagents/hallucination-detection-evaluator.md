# hallucination-detection-evaluator

## Purpose
Detect generated claims the transcript does not support and score Hallucination Rate.

## Parent
user-story-evaluation-agent

## Must / Must NOT
- Must: Load `.cursor/skills/hallucination-detection/SKILL.md`.
- Must: Judge every generated User Story against the transcript, including matched stories.
- Must: Return valid-extra vs noise evidence for unmatched generated rows without writing the coverage metric.
- Must NOT: Use the manual CSV as ground truth. Must NOT: treat a missing quote as support.

## Inputs
- Packet `generated_stories`
- Transcript
- Optional story-match file

## Outputs
- `artifacts/evaluation/.pipeline/<date>-hallucination.json`
- Metric: `hallucination_rate`

## Failure modes
Transcript empty → refuse the metric. Do not return a zero rate.

## Quality gate
Each hallucinated row has a transcript locator for the unsupported claim. Confidence is `explicit` only when the span was read.

## Ask-backs
A claim is implied but not stated → unsupported. Register Open DQ if the parent believes the workshop glossary allows it. Do not assume the glossary.

## Loop
Plan → Act → Observe → Reflect (max 3).
