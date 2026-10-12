---
name: hallucination-detection
description: >-
  Find generated user-story claims the transcript does not support.
  Use for hallucination-detection-evaluator. Owns Hallucination Rate.
---

# Hallucination detection

## Parent
user-story-evaluation-agent

## Inputs
- Packet `generated_stories` (title, description, acceptance criteria, epic, feature)
- Transcript
- Story-match file when it already exists (a match does not prove every claim is supported)

## Procedure
1. For each generated User Story, list claims in the title, description, acceptance criteria, and preceding Epic/Feature title.
2. A claim is supported only when the transcript states it. Cite `source_locator`.
3. A claim is a hallucination when no transcript span states it. Record the nearest related span, or state that no related span exists, with `source_locator` set to that search note and `confidence` `explicit`.
4. **Hallucination Rate** = generated rows with at least one unsupported claim / generated rows.
5. For each unmatched generated row, say whether the transcript states that requirement (`valid_extra` evidence) or does not (`noise` evidence). Coverage owns the classification. This skill only supplies the evidence.

## Output
`artifacts/evaluation/.pipeline/<date>-hallucination.json` with per-story `claims[]` (`text`, `supported`, `transcript_refs`) and the `hallucination_rate` metric owned by `hallucination-detection-evaluator`.

## Do not
- Treat the manual CSV as ground truth. The transcript is ground truth.
- Mark silence as support.
- Classify the coverage metric. Return evidence coverage can cite.
