---
name: business-correctness
description: >-
  Check generated titles, descriptions, and roles against the rulebook and the
  transcript. Use for business-correctness-evaluator. Owns format compliance and role specificity.
---

# Business correctness

## Parent
user-story-evaluation-agent

## Inputs
- Packet `generated_stories` and `structural_summary.generated`
- Rulebook `title_formats.user_story` and `user_story.description_format`
- Transcript and story matches

## Procedure
1. **Title and Description Format Compliance.** Default numerator is `structural_summary.generated.format_ok_count`. Override a row only with evidence that the structural flag misread the rulebook pattern.
2. **Role Specificity.** Default numerator is `role_specific_count`. The generic-role rule is `ASSUMPTION-USEVAL-002` (role text exactly `user` or `users` is not specific). Cite that assumption on the metric.
3. For each match, add a finding when the generated story changes the business outcome stated in the transcript (actor, condition, or result). Those findings are evidence. They do not create an extra metric id.

## Output
`artifacts/evaluation/.pipeline/<date>-business-correctness.json` with metrics `title_description_format_compliance` and `role_specificity`. Owner: `business-correctness-evaluator`.

## Do not
- Invent a role the description does not contain.
- Score acceptance criteria or epic agreement.
