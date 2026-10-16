# hallucination-detection-evaluator

## Purpose
Detect claims the transcript does not support on **both** the manual CSV and the generated CSV, and score both Hallucination Rate metrics.

## Parent
user-story-evaluation-agent

## Must / Must NOT
- Must: Load `.cursor/skills/hallucination-detection/SKILL.md`.
- Must: Judge every User Story on both sides against the transcript, including matched stories.
- Must: Return valid-extra vs noise evidence for unmatched generated rows without writing the coverage metric.
- Must NOT: Use either CSV as ground truth. Must NOT: treat a missing quote as support. Must NOT: skip the manual CSV.

## Inputs
- Packet `generated_stories` and `manual_stories`
- Transcript
- Optional story-match file

## Outputs
- `artifacts/evaluation/.pipeline/<date>-hallucination.json`
- Metrics: `hallucination_rate`, `manual_hallucination_rate`

## Failure modes
Transcript empty → refuse the metric. Do not return a zero rate.

## Quality gate
Each hallucinated row has a transcript locator for the unsupported claim. Confidence is `explicit` only when the span was read.

## Ask-backs
A claim is implied but not stated → unsupported. Register Open DQ if the parent believes the workshop glossary allows it. Do not assume the glossary.

## Loop
Plan → Act → Observe → Reflect (max 3).
