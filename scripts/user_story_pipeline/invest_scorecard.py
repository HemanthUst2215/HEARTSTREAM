"""INVEST scorecard evaluation (rule-aligned heuristics; same dimensions as invest-scorecard-evaluator)."""
from __future__ import annotations

import re
from typing import Any

GWT_RE = re.compile(r"\b(given|when|then)\b", re.I)
SO_THAT_RE = re.compile(r"\bso that\b", re.I)
USER_STORY_RE = re.compile(
    r"\bas an?\s+.+\s+i want\b", re.I | re.DOTALL
)


def _score_independent(story: dict[str, Any]) -> tuple[int, str]:
    text = " ".join(
        [
            story.get("description") or "",
            story.get("acceptanceCriteria") or "",
        ]
    ).lower()
    blockers = sum(
        1
        for w in ("depends on", "blocked by", "after story", "requires us-", "must complete")
        if w in text
    )
    score = max(1, min(10, 9 - blockers * 2))
    note = "Coupling phrases reduce independence." if blockers else "No strong coupling detected."
    return score, note


def _score_negotiable(story: dict[str, Any]) -> tuple[int, str]:
    desc = story.get("description") or ""
    ac = story.get("acceptanceCriteria") or ""
    if len(desc) > 80 and (" or " in desc.lower() or "option" in desc.lower()):
        return 8, "Outcome described with room for implementation choices."
    if len(ac) > 40:
        return 7, "AC present; detail level allows negotiation on how."
    return 5, "Add outcome-level detail; avoid prescribing UI-only solution."


def _score_valuable(story: dict[str, Any]) -> tuple[int, str]:
    desc = story.get("description") or ""
    if SO_THAT_RE.search(desc) or "benefit" in desc.lower():
        return 9, "Benefit / so-that present."
    if USER_STORY_RE.search(desc):
        return 7, "User story form present; clarify benefit."
    return 4, "State who benefits and why."


def _score_estimable(story: dict[str, Any]) -> tuple[int, str]:
    text = (story.get("description") or "") + " " + (story.get("acceptanceCriteria") or "")
    signals = sum(
        1
        for pat in (r"\d+", r"\bapi\b", r"\bscreen\b", r"\bfield\b", r"\brule\b", r"\bvalidation\b")
        if re.search(pat, text, re.I)
    )
    score = max(3, min(10, 4 + signals))
    return score, "Concrete scope signals help estimation."


def _score_small(story: dict[str, Any]) -> tuple[int, str]:
    ac = story.get("acceptanceCriteria") or ""
    words = len(ac.split())
    if words <= 120:
        return 8, "AC length suggests sprint-sized slice."
    if words <= 250:
        return 6, "Consider splitting; AC is long."
    return 3, "Likely too large for one story."


def _score_testable(story: dict[str, Any]) -> tuple[int, str]:
    ac = story.get("acceptanceCriteria") or ""
    if GWT_RE.search(ac):
        return 9, "Given/When/Then style AC."
    if len(ac) > 30 and ("must" in ac.lower() or "should" in ac.lower()):
        return 7, "Testable statements present."
    return 4, "Add observable Given/When/Then criteria."


def evaluate_invest(story: dict[str, Any]) -> dict[str, Any]:
    dims = [
        ("Independent", _score_independent),
        ("Negotiable", _score_negotiable),
        ("Valuable", _score_valuable),
        ("Estimable", _score_estimable),
        ("Small", _score_small),
        ("Testable", _score_testable),
    ]
    scores: dict[str, int] = {}
    notes: list[str] = []
    for name, fn in dims:
        s, note = fn(story)
        scores[name] = s
        if s < 7:
            notes.append(f"{name}: {note}")
    overall = round(sum(scores.values()) / len(scores), 1)
    invest_status = "Pass" if overall >= 7.0 and min(scores.values()) >= 5 else "Needs Refinement"
    recommendations = "; ".join(notes) if notes else "Meets INVEST thresholds."
    return {
        "userStoryId": story.get("userStoryId") or story.get("UserStoryID") or "",
        "title": story.get("title") or "",
        "independentScore": scores["Independent"],
        "negotiableScore": scores["Negotiable"],
        "valuableScore": scores["Valuable"],
        "estimableScore": scores["Estimable"],
        "smallScore": scores["Small"],
        "testableScore": scores["Testable"],
        "overallScore": overall,
        "investStatus": invest_status,
        "recommendations": recommendations,
    }


def evaluate_all(stories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [evaluate_invest(s) for s in stories]
