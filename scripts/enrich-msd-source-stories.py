#!/usr/bin/env python3
"""Merge supplemental requirement sources into msd-source-stories.json.

Supplements the primary User Story Excel with:
  - consultant_story_excel (functional-consultant workbook, same bind keys)
  - clarification_paths (plain text / docx-extracted snippets, attached per group)
  - workshop_prerequisite_kb (JSON from workshop-prerequisite-analysis)
  - transcript_path (optional workshop transcript for locator-backed excerpts)

Does not invent requirements — only merges cited rows and attaches operator-supplied text.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from msd_test_case_xlsx import extract_stories  # noqa: E402
from msd_test_case_xlsx_layout import load_rulebook  # noqa: E402


def _norm_title(title: str) -> str:
    t = re.sub(r"\s+", " ", (title or "").strip().lower())
    return re.sub(r"[^\w\s]", "", t)


def _merge_story(primary: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    out = dict(primary)
    out["story_sources"] = list(
        dict.fromkeys(
            (primary.get("story_sources") or ["primary"])
            + (extra.get("story_sources") or ["consultant"])
        )
    )
    for field in ("description", "acceptance_criteria"):
        a = str(primary.get(field) or "").strip()
        b = str(extra.get(field) or "").strip()
        if b and b not in a:
            out[field] = (a + "\n\n[Consultant story]\n" + b).strip() if a else b
    if extra.get("id") and not out.get("id"):
        out["consultant_story_id"] = extra.get("id")
    out["supplemental_locators"] = list(
        dict.fromkeys(
            (primary.get("supplemental_locators") or [])
            + [extra.get("source_locator")]
        )
    )
    return out


def merge_consultant_stories(
    primary_payload: dict[str, Any],
    consultant_payload: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    notes: list[str] = []
    by_title: dict[str, dict[str, Any]] = {}
    for s in consultant_payload.get("stories") or []:
        key = _norm_title(str(s.get("title") or ""))
        if key:
            s = dict(s)
            s["story_sources"] = ["consultant"]
            by_title[key] = s

    merged: list[dict[str, Any]] = []
    matched = 0
    for p in primary_payload.get("stories") or []:
        key = _norm_title(str(p.get("title") or ""))
        extra = by_title.pop(key, None)
        if extra:
            merged.append(_merge_story(p, extra))
            matched += 1
        else:
            merged.append(p)

    for key, extra in by_title.items():
        notes.append(f"Consultant-only story (no primary match): {extra.get('title')}")
        extra["story_sources"] = ["consultant"]
        merged.append(extra)

    out = dict(primary_payload)
    out["stories"] = merged
    out["consultant_merge"] = {
        "matched_by_title": matched,
        "consultant_only_count": len(by_title),
    }
    return out, notes


def attach_clarifications(
    payload: dict[str, Any],
    clarification_blobs: list[tuple[str, str]],
) -> dict[str, Any]:
    """Attach global clarification text; groups can filter in the extractor."""
    out = dict(payload)
    out["clarifications"] = [
        {"source_path": path, "text": text.strip()}
        for path, text in clarification_blobs
        if text.strip()
    ]
    return out


def attach_workshop_kb(payload: dict[str, Any], kb_path: Path) -> dict[str, Any]:
    out = dict(payload)
    if kb_path.is_file():
        out["workshop_prerequisite_kb"] = json.loads(kb_path.read_text(encoding="utf-8"))
        out["workshop_prerequisite_kb_path"] = str(kb_path)
    return out


def attach_transcript_ref(payload: dict[str, Any], transcript_path: Path) -> dict[str, Any]:
    out = dict(payload)
    if transcript_path.is_file():
        out["transcript_path"] = str(transcript_path)
        # Keep excerpt cap — full transcript is loaded by agents with locators.
        text = transcript_path.read_text(encoding="utf-8", errors="replace")
        out["transcript_char_count"] = len(text)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Enrich MSD source-stories JSON with supplemental inputs.")
    parser.add_argument("--in", dest="input_json", required=True, help="Primary extract-stories JSON")
    parser.add_argument("--out", required=True, help="Enriched output JSON")
    parser.add_argument("--consultant-excel", help="Optional consultant User Story Excel")
    parser.add_argument("--clarification", action="append", default=[], help="Clarification text file(s)")
    parser.add_argument("--workshop-kb", help="Workshop prerequisite knowledge base JSON")
    parser.add_argument("--transcript", help="Workshop transcript path (reference only in JSON)")
    parser.add_argument("--rulebook", default=str(ROOT / "docs" / "intake" / "msd-test-case-rulebook.yaml"))
    parser.add_argument(
        "--source-rulebook",
        default=str(ROOT / "docs" / "intake" / "user-story-csv-rulebook.yaml"),
    )
    args = parser.parse_args()

    payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    merge_notes: list[str] = []
    msd_rb = load_rulebook(Path(args.rulebook))
    src_rb = load_rulebook(Path(args.source_rulebook))

    if args.consultant_excel:
        consultant = extract_stories(Path(args.consultant_excel), src_rb, msd_rb)
        payload, merge_notes = merge_consultant_stories(payload, consultant)

    blobs: list[tuple[str, str]] = []
    for p in args.clarification or []:
        path = Path(p)
        if path.is_file():
            blobs.append((str(path), path.read_text(encoding="utf-8", errors="replace")))
    payload = attach_clarifications(payload, blobs)

    if args.workshop_kb:
        payload = attach_workshop_kb(payload, Path(args.workshop_kb))
    if args.transcript:
        payload = attach_transcript_ref(payload, Path(args.transcript))

    payload["enrichment"] = {
        "consultant_excel": args.consultant_excel,
        "clarification_paths": args.clarification or [],
        "workshop_kb": args.workshop_kb,
        "transcript": args.transcript,
        "merge_notes": merge_notes,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(out), "merge_notes": merge_notes}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
