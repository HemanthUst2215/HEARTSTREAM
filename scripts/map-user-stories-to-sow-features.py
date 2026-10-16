#!/usr/bin/env python3
"""Map user stories to SOW.json features (no epic.json / feature.json).

Public Excel layout:
  Workshop → Feature (from SOW) → User Stories (blank ID)

Feature row shape:
  Title 2:  <Annexure ID minutes> - <session topic>
  Description: <session topic>
  ID: (blank)
  Annexure ID1: <Annexure ID minutes>
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from importlib.machinery import SourceFileLoader

_legacy = SourceFileLoader(
    "map_user_stories_to_work_items",
    str(_SCRIPTS / "map-user-stories-to-work-items.py"),
).load_module()
DEFAULT_TITLE_BY_TYPE = _legacy.DEFAULT_TITLE_BY_TYPE
DROP_COLUMNS = _legacy.DROP_COLUMNS
load_story_rulebook = _legacy.load_story_rulebook
load_yaml_mapping = _legacy.load_yaml_mapping
pick_top_feature_matches = _legacy.pick_top_feature_matches
project_label_from_config = _legacy.project_label_from_config
row_title = _legacy.row_title
story_blob = _legacy.story_blob
title_score = _legacy.title_score
write_xlsx = _legacy.write_xlsx

DEFAULT_SOW_JSON = "SOW.json"
OBJ_TO_WORKSHOP = {f"OBJ-00{i}": f"WS-CE-0{i}" for i in range(1, 10)}


def load_sow(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("rows") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        raise ValueError("SOW.json must contain a rows array")
    features: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        topic = str(row.get("BPM") or "").strip()
        workshop_code = str(row.get("Workshop") or "").strip()
        minutes = row.get("Annexure ID")
        if minutes is None or minutes == "":
            continue
        annexure_minutes = str(minutes).strip()
        display_title = f"{annexure_minutes} - {topic}"
        features.append(
            {
                "workshop_code": workshop_code,
                "topic": topic,
                "annexure_minutes": annexure_minutes,
                "title": display_title,
                "description": topic,
            }
        )
    return features


def load_prerequisite_refs(rows_json: Path | None) -> dict[str, list[str]]:
    """Map User Story Title 3 → prerequisite_refs from rows JSON."""
    if not rows_json or not rows_json.is_file():
        return {}
    payload = json.loads(rows_json.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return {}
    out: dict[str, list[str]] = {}
    for item in payload:
        if not isinstance(item, dict):
            continue
        if (item.get("Work Item Type") or "").strip() != "User Story":
            continue
        title = (item.get("Title 3") or "").strip()
        refs = item.get("prerequisite_refs")
        if title and isinstance(refs, list):
            out[title] = [str(r) for r in refs]
    return out


def resolve_sow_feature(
    story_title: str,
    story_text: str,
    features: list[dict[str, Any]],
    prerequisite_refs: list[str],
    threshold: float,
    margin: float,
    max_features: int,
) -> tuple[list[dict[str, Any]], str]:
    if prerequisite_refs:
        codes = {OBJ_TO_WORKSHOP.get(r, "") for r in prerequisite_refs}
        codes.discard("")
        if codes:
            matched = [f for f in features if f.get("workshop_code") in codes]
            if matched:
                return matched[:max_features], "prerequisite_refs→workshop_code"

    scores = [(title_score(story_title, f["title"]), f) for f in features]
    blob_scores = [(title_score(story_text, f["topic"]), f) for f in features]
    combined: dict[str, float] = {}
    feat_by_code: dict[str, dict[str, Any]] = {}
    for f in features:
        code = f.get("workshop_code") or f["title"]
        feat_by_code[code] = f
    for score, f in scores + blob_scores:
        code = f.get("workshop_code") or f["title"]
        combined[code] = max(combined.get(code, 0.0), score)
    ranked = [(combined[k], feat_by_code[k]) for k in combined]
    winners, why = pick_top_feature_matches(ranked, threshold, margin, max_features)
    return [w[0] for w in winners], why


def sow_feature_row(keys: list[str], feature: dict[str, Any]) -> dict[str, str]:
    out = {k: "" for k in keys}
    out["Work Item Type"] = "Feature"
    out["ID"] = ""
    title = feature["title"]
    dest = DEFAULT_TITLE_BY_TYPE.get("Feature", "Title 2")
    if dest in keys:
        out[dest] = title
    out["Description"] = feature.get("description") or feature.get("topic") or ""
    if "Annexure ID1" in keys:
        out["Annexure ID1"] = feature.get("annexure_minutes") or ""
    if "State" in keys and not (out.get("State") or "").strip():
        out["State"] = "New"
    return out


def map_stories_to_sow(
    rows: list[dict[str, str]],
    features: list[dict[str, Any]],
    prereq_by_title: dict[str, list[str]],
    threshold: float,
    margin: float,
    max_features: int,
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    keys = [k for k in (rows[0].keys() if rows else []) if k not in DROP_COLUMNS]
    if "ID" not in keys:
        keys.insert(0, "ID")

    workshops: list[dict[str, str]] = []
    trailing: list[dict[str, str]] = []
    unmatched_stories: list[dict[str, str]] = []
    stories_by_code: dict[str, list[dict[str, str]]] = {}
    log_entries: list[dict[str, Any]] = []

    feature_order = [f.get("workshop_code") or f["title"] for f in features]

    for idx, row in enumerate(rows):
        wit = (row.get("Work Item Type") or "").strip()
        if wit in ("Epic", "Feature"):
            continue
        out = {k: row.get(k) or "" for k in keys}
        title = row_title(row)

        if wit == "Workshop":
            if "Annexure ID1" in out:
                out["Annexure ID1"] = ""
            workshops.append(out)
            continue
        if wit != "User Story":
            trailing.append(out)
            continue

        refs = prereq_by_title.get((row.get("Title 3") or "").strip(), [])
        winners, why = resolve_sow_feature(
            title,
            story_blob(row),
            features,
            refs,
            threshold,
            margin,
            max_features,
        )
        if winners:
            match_details = []
            for feat in winners:
                code = feat.get("workshop_code") or feat["title"]
                story_out = {k: out.get(k) or "" for k in keys}
                story_out["ID"] = ""
                stories_by_code.setdefault(code, []).append(story_out)
                match_details.append(
                    {
                        "sowWorkshopCode": feat.get("workshop_code"),
                        "sowFeatureTitle": feat["title"],
                        "annexureMinutes": feat.get("annexure_minutes"),
                    }
                )
            log_entries.append(
                {
                    "csvRow": idx + 2,
                    "title": title,
                    "status": "matched",
                    "mappingMode": "sow_json",
                    "sowMatches": match_details,
                    "rationale": why,
                }
            )
        else:
            unmatched_stories.append(out)
            log_entries.append(
                {
                    "csvRow": idx + 2,
                    "title": title,
                    "status": "unmatched",
                    "mappingMode": "sow_json",
                    "sowMatches": [],
                    "rationale": why,
                }
            )

    hierarchy: list[dict[str, str]] = []
    for code in feature_order:
        if not stories_by_code.get(code):
            continue
        feat = next((f for f in features if (f.get("workshop_code") or f["title"]) == code), None)
        if not feat:
            continue
        hierarchy.append(sow_feature_row(keys, feat))
        hierarchy.extend(stories_by_code[code])

    mapped = workshops + hierarchy + unmatched_stories + trailing
    return mapped, log_entries


def write_logs(
    json_path: Path,
    source_csv: Path,
    sow_path: Path,
    entries: list[dict[str, Any]],
    feature_count: int,
    threshold: float,
    margin: float,
) -> None:
    matched = sum(1 for e in entries if e["status"] == "matched")
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceCsv": str(source_csv),
        "sowJson": str(sow_path),
        "mappingMode": "sow_feature_story_hierarchy",
        "threshold": threshold,
        "margin": margin,
        "sowFeatureCount": feature_count,
        "userStoryCount": len(entries),
        "matched": matched,
        "unmatched": len(entries) - matched,
        "stories": entries,
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--work-items-dir", default="artifacts/work-items")
    parser.add_argument("--sow-json", default=None, help="SOW.json path (default from config)")
    parser.add_argument("--rows-json", default=None, help="Optional user-story-rows.json for prerequisite_refs")
    parser.add_argument("--out-xlsx", required=True)
    parser.add_argument("--log-json", required=True)
    parser.add_argument("--config", default=str(ROOT / ".cursor" / "config.yaml"))
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--margin", type=float, default=None)
    args = parser.parse_args()

    cfg = load_yaml_mapping(Path(args.config))
    threshold = float(args.threshold if args.threshold is not None else cfg.get("strong_threshold", 62))
    margin = float(args.margin if args.margin is not None else cfg.get("winner_margin", 8))
    max_features = int(cfg.get("max_related_features", 3))

    sow_name = args.sow_json or cfg.get("sow_json", DEFAULT_SOW_JSON)
    sow_path = Path(args.work_items_dir) / sow_name
    if not sow_path.is_file():
        sow_path = ROOT / "artifacts" / "work-items" / sow_name
    if not sow_path.is_file():
        print(f"SOW.json not found: {sow_path}", file=sys.stderr)
        return 1

    features = load_sow(sow_path)
    if not features:
        print("FAIL: no SOW features loaded", file=sys.stderr)
        return 1

    source = Path(args.csv)
    with source.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or [])
        rows = [{k: (r.get(k) or "") for k in headers} for r in reader]

    rows_json = Path(args.rows_json) if args.rows_json else None
    if rows_json is None:
        guess = source.stem.replace("-user-stories-working", "-user-story-rows")
        candidate = ROOT / "artifacts" / "intake" / f"{guess}.json"
        if candidate.is_file():
            rows_json = candidate

    prereq_by_title = load_prerequisite_refs(rows_json)
    mapped, log_entries = map_stories_to_sow(
        rows, features, prereq_by_title, threshold, margin, max_features
    )

    us = sum(1 for r in rows if (r.get("Work Item Type") or "").strip() == "User Story")
    if len(log_entries) != us:
        print("FAIL: mapping log count != User Story rows", file=sys.stderr)
        return 1

    write_logs(Path(args.log_json), source, sow_path, log_entries, len(features), threshold, margin)
    story_rb = load_story_rulebook()
    project_label = project_label_from_config(Path(args.config))
    out_headers = [h for h in headers if h not in DROP_COLUMNS]
    write_xlsx(Path(args.out_xlsx), out_headers, mapped, rulebook=story_rb, project_label=project_label)

    print(
        f"mapped {us} user stories; matched {sum(1 for e in log_entries if e['status']=='matched')}; "
        f"unmatched {sum(1 for e in log_entries if e['status']=='unmatched')}; "
        f"sow features {len(features)}"
    )
    print(f"wrote {args.out_xlsx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
