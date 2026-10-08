"""Export user stories and INVEST scorecards to UTF-8 CSV (Excel / Azure DevOps friendly)."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

USER_STORY_COLUMNS = [
    "UserStoryID",
    "Title",
    "Description",
    "AcceptanceCriteria",
    "Priority",
    "ReferenceWorkItemIds",
    "MatchScores",
    "Epic",
    "Feature",
    "SourceTranscript",
]

INVEST_COLUMNS = [
    "UserStoryID",
    "Title",
    "IndependentScore",
    "NegotiableScore",
    "ValuableScore",
    "EstimableScore",
    "SmallScore",
    "TestableScore",
    "OverallScore",
    "InvestStatus",
    "Recommendations",
]


def _story_row(story: dict[str, Any], default_source: str) -> dict[str, str]:
    return {
        "UserStoryID": str(story.get("userStoryId") or story.get("UserStoryID") or ""),
        "Title": str(story.get("title") or ""),
        "Description": str(story.get("description") or ""),
        "AcceptanceCriteria": str(story.get("acceptanceCriteria") or ""),
        "Priority": str(story.get("priority") or "Medium"),
        "ReferenceWorkItemIds": str(
            story.get("referenceWorkItemIds") or story.get("ReferenceWorkItemIds") or ""
        ),
        "MatchScores": str(story.get("matchScores") or story.get("MatchScores") or ""),
        "Epic": str(story.get("epic") or story.get("Epic") or ""),
        "Feature": str(story.get("feature") or story.get("Feature") or ""),
        "SourceTranscript": str(
            story.get("sourceTranscript")
            or story.get("SourceTranscript")
            or default_source
        ),
    }


def _invest_row(row: dict[str, Any]) -> dict[str, str]:
    key_map = {
        "UserStoryID": "userStoryId",
        "Title": "title",
        "IndependentScore": "independentScore",
        "NegotiableScore": "negotiableScore",
        "ValuableScore": "valuableScore",
        "EstimableScore": "estimableScore",
        "SmallScore": "smallScore",
        "TestableScore": "testableScore",
        "OverallScore": "overallScore",
        "InvestStatus": "investStatus",
        "Recommendations": "recommendations",
    }
    return {col: str(row.get(key_map[col], row.get(col, ""))) for col in INVEST_COLUMNS}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\r\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def export_user_stories_csv(
    stories: list[dict[str, Any]],
    path: Path,
    default_source: str = "",
) -> None:
    rows = [_story_row(s, default_source) for s in stories]
    write_csv(path, USER_STORY_COLUMNS, rows)


def export_invest_scorecard_csv(rows: list[dict[str, Any]], path: Path) -> None:
    mapped = [_invest_row(r) for r in rows]
    write_csv(path, INVEST_COLUMNS, mapped)
