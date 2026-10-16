---
name: hallucination-detection
description: >-
  Find user-story claims the transcript does not support on both the manual
  CSV and the generated CSV. Use for hallucination-detection-evaluator.
  Owns Hallucination Rate (Generated) and Hallucination Rate (Manual).
---

# Hallucination detection

## Parent
user-story-evaluation-agent

## Inputs
- Packet `generated_stories` and `manual_stories` (title, description, acceptance criteria, epic, feature)
- Transcript
- Story-match file when it already exists (a match does not prove every claim is supported)

## Procedure
1. Judge **every** User Story on **both** sides. List claims in the title, description, acceptance criteria, and preceding Epic/Feature title.
2. A claim is supported only when the transcript states it. Cite `source_locator`.
3. A claim is a hallucination when no transcript span states it. Record the nearest related span, or state that no related span exists, with `source_locator` set to that search note and `confidence` `explicit`.
4. **Hallucination Rate (Generated)** = generated rows with at least one unsupported claim / generated rows.
5. **Hallucination Rate (Manual)** = manual rows with at least one unsupported claim / manual rows.
6. For each unmatched generated row, say whether the transcript states that requirement (`valid_extra` evidence) or does not (`noise` evidence). Coverage owns the classification. This skill only supplies the evidence.

## Output
`artifacts/evaluation/.pipeline/<date>-hallucination.json` with per-story `claims[]` (`text`, `supported`, `transcript_refs`) for both `manual_stories` and `generated_stories` (or a `side` field on each story), plus metrics `hallucination_rate` and `manual_hallucination_rate` owned by `hallucination-detection-evaluator`.

## Do not
- Treat either CSV as ground truth. The transcript is ground truth for both sides.
- Skip the manual CSV. Silence is not support.
- Classify the coverage metric. Return evidence coverage can cite.
