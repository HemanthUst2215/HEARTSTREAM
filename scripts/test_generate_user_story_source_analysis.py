#!/usr/bin/env python3
"""Tests for scripts/generate_user_story_source_analysis.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_user_story_source_analysis.py"
CONTRACT = ROOT / ".cursor" / "templates" / "user-story-source-analysis-contract.yaml"
SOW = ROOT / "artifacts" / "work-items" / "SOW.json"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def _minimal_analysis(side: str) -> dict:
    story = {
        "story_key": f"{side}-US-2",
        "user_story_id": "",
        "user_story_title": "Partner onboarding",
        "feature_name": "70 - External Analytics Data Ingestion & Unification",
        "match_type": "Exact Match",
        "derived_sources": ["Transcript"],
        "source_references": [
            {
                "source_type": "Transcript",
                "locator": "line 1",
                "excerpt": "partner onboarding",
            }
        ],
        "why_generated": "Stated in workshop discussion.",
        "why_mapped_to_feature": "Topic aligns with SOW BPM row.",
        "supporting_business_context": "Marketing workshop scope.",
        "coverage_assessment": "Fully Supported",
        "confidence_score": "0.92",
        "recommended_action": "Accept",
    }
    return {
        "schema_version": "1.0",
        "kind": "user-story-source-analysis",
        "side": side,
        "status": "Draft — Pending Method Review",
        "assumption_id": "ASSUMPTION-USHTML-001",
        "inputs": {
            "user_story_csv": f"{side}.csv",
            "unified_knowledge_base": "kb.json",
        },
        "executive_summary": {
            "total_user_stories": 1,
            "exact_matches": 1,
            "partial_matches": 0,
            "no_matches": 0,
            "fully_supported_stories": 1,
            "overall_traceability_score": "100",
        },
        "stories": [story],
        "feature_traceability_matrix": [
            {
                "feature_name": story["feature_name"],
                "mapped_user_stories": ["Partner onboarding"],
                "coverage_percent": 100,
                "missing_requirements": [],
                "requirements_not_in_stories": [],
            }
        ],
        "source_coverage_summary": {
            "transcript_percent": 100,
            "mom_percent": 0,
            "preread_percent": 0,
            "feature_list_percent": 100,
        },
        "coverage_gap_analysis": {
            "feature_requirements_not_in_stories": [],
            "source_requirements_not_captured": [],
            "unmapped_user_stories": [],
            "missing_business_scenarios": [],
        },
        "open_items": ["ASSUMPTION-USHTML-001 pending method review."],
    }


def test_allocate_run_json() -> None:
    proc = _run("allocate-run", "--date", "2099-01-01", "--slug", "fixture", "--json")
    assert proc.returncode == 0, proc.stderr
    paths = json.loads(proc.stdout)
    assert "public_manual_html" in paths
    assert "public_ai_html" in paths
    assert "manual-user-story-analysis" in paths["public_manual_html"]


def test_prepare_kb_and_validate_render() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tdir = Path(tmp)
        transcript = tdir / "t.txt"
        transcript.write_text("We discussed partner onboarding.\n", encoding="utf-8")
        kb_out = tdir / "kb-index.json"
        proc = _run(
            "prepare-kb",
            "--transcript",
            str(transcript),
            "--mom",
            str(transcript),
            "--preread",
            str(transcript),
            "--sow-json",
            str(SOW),
            "--out",
            str(kb_out),
        )
        assert proc.returncode == 0, proc.stderr
        data = json.loads(kb_out.read_text(encoding="utf-8"))
        assert data["kind"] == "source-kb-index"
        assert data["feature_list_rows"]

        analysis_path = tdir / "analysis.json"
        analysis_path.write_text(
            json.dumps(_minimal_analysis("manual"), indent=2), encoding="utf-8"
        )
        proc = _run("validate", "--analysis", str(analysis_path), "--contract", str(CONTRACT))
        assert proc.returncode == 0, proc.stdout + proc.stderr

        html_path = tdir / "manual-user-story-analysis.html"
        json_path = tdir / "manual-user-story-analysis.json"
        proc = _run(
            "render",
            "--analysis",
            str(analysis_path),
            "--html",
            str(html_path),
            "--json",
            str(json_path),
            "--contract",
            str(CONTRACT),
        )
        assert proc.returncode == 0, proc.stderr
        html = html_path.read_text(encoding="utf-8")
        assert "Executive summary" in html
        assert "manual user story analysis" in html.lower()


def test_validate_ushtml_match_001_no_match_with_refs_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        analysis_path = Path(tmp) / "bad.json"
        doc = _minimal_analysis("manual")
        doc["stories"][0]["match_type"] = "No Match"
        analysis_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        proc = _run("validate", "--analysis", str(analysis_path), "--contract", str(CONTRACT))
        assert proc.returncode != 0
        assert "USHTML-MATCH-001" in proc.stdout + proc.stderr


def test_validate_ushtml_feat_001_csv_row_reason_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        analysis_path = Path(tmp) / "bad.json"
        doc = _minimal_analysis("manual")
        doc["stories"][0]["why_mapped_to_feature"] = "Nearest preceding Feature row in CSV."
        analysis_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        proc = _run("validate", "--analysis", str(analysis_path), "--contract", str(CONTRACT))
        assert proc.returncode != 0
        assert "USHTML-FEAT-001" in proc.stdout + proc.stderr


def test_validate_ushtml_match_001_partial_without_refs_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        analysis_path = Path(tmp) / "bad.json"
        doc = _minimal_analysis("manual")
        doc["stories"][0]["source_references"] = [
            {"source_type": "Transcript", "locator": "n/a", "excerpt": "No Supporting Evidence Found"}
        ]
        doc["stories"][0]["derived_sources"] = []
        analysis_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        proc = _run("validate", "--analysis", str(analysis_path), "--contract", str(CONTRACT))
        assert proc.returncode != 0
        assert "USHTML-MATCH-001" in proc.stdout + proc.stderr
