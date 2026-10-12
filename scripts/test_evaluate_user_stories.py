#!/usr/bin/env python3
"""Tests for scripts/evaluate_user_stories.py."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evaluate_user_stories.py"
METRICS = ROOT / ".cursor" / "templates" / "user-story-evaluation-metrics.yaml"

HEADERS = [
    "ID",
    "Work Item Type",
    "Title",
    "Description",
    "Acceptance Criteria",
]


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        for row in rows:
            full = {key: "" for key in HEADERS}
            full.update(row)
            writer.writerow(full)


def _evidence(statement: str) -> list[dict]:
    return [
        {
            "statement": statement,
            "source_path": "transcript.txt",
            "source_locator": "line 1",
            "confidence": "explicit",
            "transcript_refs": [{"locator": "line 1", "excerpt": "partner onboarding"}],
        }
    ]


def _evaluation() -> dict:
    specs = [
        ("recall", "coverage-analysis-evaluator", "ratio", "100% (1/1)", 1.0),
        ("precision", "coverage-analysis-evaluator", "ratio", "100% (1/1)", 1.0),
        ("manual_only_stories", "coverage-analysis-evaluator", "count", "0", 0),
        ("generated_only_stories", "coverage-analysis-evaluator", "split", "0 valid extras, 0 noise", None),
        ("epic_agreement", "epic-feature-mapping-evaluator", "ratio", "100% (1/1)", 1.0),
        ("feature_agreement", "epic-feature-mapping-evaluator", "ratio", "100% (1/1)", 1.0),
        ("title_description_format_compliance", "business-correctness-evaluator", "ratio", "100% (1/1)", 1.0),
        ("role_specificity", "business-correctness-evaluator", "ratio", "100% (1/1)", 1.0),
        ("acceptance_criteria_count", "acceptance-criteria-evaluator", "comparison", "Manual 1 · Generated 1", None),
        ("acceptance_criteria_quality", "acceptance-criteria-evaluator", "score", "80", 80),
        ("negative_boundary_coverage", "acceptance-criteria-evaluator", "ratio", "n/a", None),
        ("granularity", "story-matching-evaluator", "ratio", "100% (1/1)", 1.0),
        ("hallucination_rate", "hallucination-detection-evaluator", "ratio", "0% (0/1)", 0.0),
    ]
    metrics = []
    for metric_id, owner, kind, display, score in specs:
        row = {
            "metric_id": metric_id,
            "owner": owner,
            "kind": kind,
            "display": display,
            "score": score,
            "evidence": _evidence(f"Fixture evidence for {metric_id}."),
        }
        if metric_id == "negative_boundary_coverage":
            row["na"] = True
            row["na_reason"] = "Transcript states no negative or boundary for this fixture."
            row["display"] = "n/a"
        metrics.append(row)
    return {
        "schema_version": "1.0",
        "status": "Draft — Pending Method Review",
        "assumption_id": "ASSUMPTION-USEVAL-001",
        "inputs": {
            "manual_csv": "manual.csv",
            "generated_csv": "generated.csv",
            "transcript_path": "transcript.txt",
        },
        "matches": [
            {
                "match_id": "M-001",
                "manual_key": "manual-US-4",
                "manual_title": "Sync partner after approval",
                "generated_keys": ["generated-US-4"],
                "generated_titles": "Sync partner after approval",
                "match_type": "1:1",
                "confidence": "high",
                "transcript_refs": [{"locator": "line 1", "excerpt": "partner onboarding"}],
            }
        ],
        "manual_only": [],
        "generated_only": [],
        "metrics": metrics,
        "open_items": ["ASSUMPTION-USEVAL-001 pending method review"],
    }


def test_prepare_epic_feature_and_no_recall() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        manual = folder / "manual.csv"
        generated = folder / "generated.csv"
        transcript = folder / "transcript.txt"
        packet_path = folder / "packet.json"
        story = {
            "Title": "Sync partner after approval",
            "Description": (
                "As a CRM solution owner, I need to sync the partner after approval, "
                "so that CRM shows only ready partners."
            ),
            "Acceptance Criteria": "- Partner is absent until approval",
        }
        _write_csv(
            manual,
            [
                {"Work Item Type": "Epic", "ID": "E1", "Title": "Partner lifecycle"},
                {"Work Item Type": "Feature", "ID": "F1", "Title": "Onboarding sync"},
                {"Work Item Type": "User Story", **story},
            ],
        )
        _write_csv(
            generated,
            [
                {"Work Item Type": "Epic", "ID": "E1", "Title": "Partner lifecycle"},
                {"Work Item Type": "Feature", "ID": "F9", "Title": "Different feature"},
                {"Work Item Type": "User Story", "ID": "F9", **story},
            ],
        )
        transcript.write_text("The partner record syncs after onboarding approval.\n", encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "prepare",
                "--manual",
                str(manual),
                "--generated",
                str(generated),
                "--transcript",
                str(transcript),
                "--out",
                str(packet_path),
                "--candidate-jaccard-floor",
                "0.2",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        assert "recall" not in packet
        assert packet["manual_stories"][0]["epic"]["id"] == "E1"
        assert packet["manual_stories"][0]["feature"]["id"] == "F1"
        assert packet["generated_stories"][0]["feature"]["id"] == "F9"
        assert packet["generated_stories"][0]["structural"]["format_ok"] is True
        assert packet["generated_stories"][0]["structural"]["role_specific"] is True
        assert packet["candidate_pairs"]
        assert all(item["status"] == "proposal" for item in packet["candidate_pairs"])


def test_render_and_reject_incomplete() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        evaluation = folder / "evaluation.json"
        html_path = folder / "report.html"
        json_path = folder / "report.json"
        document = _evaluation()
        evaluation.write_text(json.dumps(document), encoding="utf-8")
        ok = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--metrics",
                str(METRICS),
                "render",
                "--evaluation",
                str(evaluation),
                "--html",
                str(html_path),
                "--json",
                str(json_path),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert ok.returncode == 0, ok.stderr
        page = html_path.read_text(encoding="utf-8")
        assert "User story evaluation" in page
        assert "Hallucination Rate" in page
        assert "M-001" in page
        assert "Sync partner after approval" in page

        document["metrics"] = [row for row in document["metrics"] if row["metric_id"] != "recall"]
        evaluation.write_text(json.dumps(document), encoding="utf-8")
        bad = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--metrics",
                str(METRICS),
                "validate",
                "--evaluation",
                str(evaluation),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert bad.returncode == 1
        assert "missing metric: recall" in bad.stdout


def test_allocate_run_never_reuses_public_html() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        ev = folder / "artifacts" / "evaluation"
        pipe = ev / ".pipeline"
        ev.mkdir(parents=True)
        pipe.mkdir(parents=True)
        (ev / "2099-01-01-user-story-evaluation.html").write_text("old", encoding="utf-8")
        sys.path.insert(0, str(ROOT / "scripts"))
        import importlib.util

        spec = importlib.util.spec_from_file_location("eus", SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.ROOT = folder
        paths = mod.allocate_run_paths("2099-01-01")
        assert paths["public_html"].endswith("2099-01-01-user-story-evaluation-v2.html")
        assert paths["packet"].endswith("2099-01-01-evaluation-packet-v2.json")
        assert not Path(paths["public_html"]).exists()


if __name__ == "__main__":
    test_prepare_epic_feature_and_no_recall()
    test_render_and_reject_incomplete()
    test_allocate_run_never_reuses_public_html()
    print("PASS")
