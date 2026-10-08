#!/usr/bin/env python3
"""Map generated user stories to Epic / Feature / Workshop IDs.

Used only by `/generate-user-stories-from-transcript` (work-item-mapping-agent).
Reads artifacts/work-items/*.json. Writes one public Excel (stories + IDs) and an internal JSON mapping log. INVEST stays a separate CSV.
Does not change Title, Description, Acceptance Criteria, or other source cells.

Do not invent Epic/Feature titles from the transcript. Match each User Story
to existing Features in artifacts/work-items JSON, then write those catalog
Epic and Feature rows into the workbook with their ADO IDs. Fill story
Catalog Epic/Feature/Workshop IDs go in the rulebook `ID` column only — no extra EPIC ID / FEATURE ID columns.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import zipfile
from difflib import SequenceMatcher
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from collections import defaultdict
from typing import Any
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ado_user_story_csv_layout import excel_safe_cell  # noqa: E402

STOPWORDS = frozenset(
    """
    a an the and or to of for in on at as is are was were be been being
    with without from by this that these those it its their they we i
    need so that user story via vs etc also only when after before
    """.split()
)
# Too common in this catalog to count as a unique Feature match by themselves.
WEAK_MATCH_TOKENS = STOPWORDS | frozenset(
    "partner data sales order management customer record create sync available "
    "user crm process integration processing".split()
)
TOKEN_RE = re.compile(r"[a-z0-9]+", re.I)
# Never add these to the public Excel; catalog IDs use the rulebook `ID` column.
DROP_COLUMNS = ("EPIC ID", "FEATURE ID", "WORKSHOP ID")
# Transcript-authored Epic/Feature rows are discarded; catalog matches are written instead.
SKIP_AUTHORING_TYPES = frozenset({"Epic", "Feature"})
SKIP_JSON_NAMES = {
    "manifest",
    "schema-profile",
    "validation-report",
}


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text or "") if t.lower() not in STOPWORDS and len(t) > 1]


def token_overlap(query: set[str], candidate: set[str]) -> set[str]:
    """Exact tokens plus prefix morphology (create/creation, sync/synchronization)."""
    hit: set[str] = set(query & candidate)
    for q in query:
        if q in hit:
            continue
        for c in candidate:
            shorter, longer = (q, c) if len(q) <= len(c) else (c, q)
            if len(shorter) >= 4 and longer.startswith(shorter):
                hit.add(q)
                break
    return hit


def normalize_title(title: str) -> str:
    """Strip numbering prefixes so catalog '4. Foo' matches generated '1. Foo'."""
    t = (title or "").lower().replace("&", " and ")
    t = re.sub(r"^#\d+:\s*", "", t)
    t = re.sub(r"^[\d.#]+(?:\.\d+)*\s*", "", t)
    t = re.sub(r"^[a-z]\d*[.)]\s*", "", t)
    t = re.sub(r"[^a-z0-9\s]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def title_score(query: str, candidate: str) -> float:
    """0–100 title similarity. Generic: numbering-agnostic, no domain phrases."""
    q, c = normalize_title(query), normalize_title(candidate)
    if not q or not c:
        return 0.0
    if q == c:
        return 100.0
    if len(q) >= 12 and q in c:
        return min(100.0, 88.0 + 12.0 * len(q) / max(len(c), 1))
    if len(c) >= 12 and c in q:
        return min(100.0, 88.0 + 12.0 * len(c) / max(len(q), 1))
    seq = SequenceMatcher(None, q, c).ratio() * 100.0
    qt, ct = set(tokenize(q)), set(tokenize(c))
    if not qt or not ct:
        return seq
    overlap = token_overlap(qt, ct)
    jacc = 100.0 * len(overlap) / len(qt | ct)
    cov = 100.0 * len(overlap) / len(qt)
    if len(overlap) < 2 and seq < 70.0:
        return round(max(seq * 0.5, jacc * 0.4), 1)
    blended = max(seq, 0.4 * jacc + 0.6 * cov)
    if len(qt) <= 6 and len(overlap) >= 2 and cov >= 65.0:
        blended = max(blended, 70.0 + 0.15 * cov)
    return round(blended, 1)


def load_yaml_mapping(config_path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError:
        return {}
    if not config_path.is_file():
        return {}
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return data.get("work_item_mapping") or {}


def load_work_items(work_items_dir: Path) -> dict[str, list[dict[str, Any]]]:
    buckets: dict[str, list[dict[str, Any]]] = {"Epic": [], "Feature": [], "Workshop": []}
    seen: set[tuple[str, str]] = set()
    if not work_items_dir.is_dir():
        return buckets
    for path in sorted(work_items_dir.glob("*.json")):
        stem = path.stem.lower()
        if any(skip in stem for skip in SKIP_JSON_NAMES):
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        items = payload.get("workItems") if isinstance(payload, dict) else None
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            wit = (item.get("workItemType") or "").strip()
            if wit not in buckets:
                continue
            wid = str(item.get("workItemId") or item.get("source", {}).get("id") or "").strip()
            if not wid:
                continue
            key = (wit, wid)
            if key in seen:
                continue
            seen.add(key)
            title = item.get("title") or item.get("displayTitle") or ""
            desc = ""
            description = item.get("description")
            if isinstance(description, dict):
                desc = description.get("plainText") or description.get("summary") or ""
            elif isinstance(description, str):
                desc = description
            parent = item.get("parent") or {}
            parent_id = parent.get("workItemId") if isinstance(parent, dict) else None
            buckets[wit].append(
                {
                    "id": wid,
                    "title": title,
                    "description": desc,
                    "parent_id": str(parent_id) if parent_id not in (None, "") else "",
                    "source_file": path.name,
                }
            )
    return buckets


def pick_strong(
    scores: list[tuple[float, dict[str, Any]]],
    threshold: float,
    margin: float,
) -> tuple[dict[str, Any] | None, str]:
    if not scores:
        return None, "no_candidates"
    scores.sort(key=lambda x: x[0], reverse=True)
    top_score, top = scores[0]
    if top_score < threshold:
        return None, f"below_threshold ({top_score:.1f} < {threshold})"
    if len(scores) > 1:
        second = scores[1][0]
        if (top_score - second) < margin:
            return None, f"ambiguous ({top_score:.1f} vs {second:.1f}, margin {margin})"
    return top, f"strong ({top_score:.1f})"


def pick_strong_unique_title(
    scores: list[tuple[float, dict[str, Any]]],
    threshold: float,
    margin: float,
) -> tuple[dict[str, Any] | None, str]:
    """Ignore Features that share a normalized title across multiple catalog IDs."""
    by_core: dict[str, list[tuple[float, dict[str, Any]]]] = defaultdict(list)
    for score, cand in scores:
        by_core[normalize_title(cand.get("title") or "")].append((score, cand))
    unique: list[tuple[float, dict[str, Any]]] = []
    for core, group in by_core.items():
        if not core:
            continue
        ids = {c["id"] for _s, c in group}
        if len(ids) == 1:
            unique.append(max(group, key=lambda x: x[0]))
    if not unique:
        return None, "no_unique_catalog_title"
    return pick_strong(unique, threshold, margin)


def score_titles(query_title: str, candidates: list[dict[str, Any]]) -> list[tuple[float, dict[str, Any]]]:
    return [(title_score(query_title, c.get("title") or ""), c) for c in candidates]


def story_blob(row: dict[str, str]) -> str:
    return " ".join(
        [
            row.get("Title") or "",
            row.get("Description") or "",
            row.get("Acceptance Criteria") or "",
        ]
    ).strip()


def _content_tokens(title: str) -> set[str]:
    return {t for t in tokenize(normalize_title(title)) if t not in WEAK_MATCH_TOKENS and len(t) > 3}


def feature_is_relevant_to_story(feat_title: str, story_title: str) -> bool:
    """Keep only catalog Features whose distinctive title terms appear in the story title."""
    core = normalize_title(feat_title)
    st = normalize_title(story_title)
    if not core or not st:
        return False
    if core == st or (len(core) >= 12 and core in st):
        return True
    words = [w for w in core.split() if w not in WEAK_MATCH_TOKENS and len(w) > 3]
    if len(words) >= 2:
        for i in range(len(words) - 1):
            if f"{words[i]} {words[i + 1]}" in st:
                return True
    feat_strong = _content_tokens(feat_title)
    story_toks = set(tokenize(st))
    if feat_strong and feat_strong <= token_overlap(feat_strong, story_toks):
        return True
    return False


def score_story_to_catalog_feature(story_title: str, blob: str, feature: dict[str, Any]) -> float:
    feat_title = feature.get("title") or ""
    if not feature_is_relevant_to_story(feat_title, story_title):
        return 0.0
    base = title_score(feat_title, story_title)
    core = normalize_title(feat_title)
    words = [w for w in core.split() if w not in STOPWORDS and len(w) > 3]
    st = story_title.lower()
    if len(words) >= 2:
        hits = sum(1 for i in range(len(words) - 1) if f"{words[i]} {words[i + 1]}" in st)
        if hits:
            base = min(100.0, base + 18.0 * hits)
    return round(base, 1)


def resolve_story_to_existing(
    story_title: str,
    blob: str,
    buckets: dict[str, list[dict[str, Any]]],
    threshold: float,
    margin: float,
) -> dict[str, Any]:
    """Map a User Story to an existing Feature whose parent Epic is in the catalog.

    Both IDs are filled only when the Feature winner is strong/unique and that
    parent Epic exists. No new Epic/Feature is created.
    """
    features = buckets.get("Feature") or []
    epic_by_id = {e["id"]: e for e in (buckets.get("Epic") or [])}
    feat_scores = [(score_story_to_catalog_feature(story_title, blob, f), f) for f in features]
    feature, feat_why = pick_strong_unique_title(feat_scores, threshold, margin)
    empty: dict[str, Any] = {
        "epic_id": "",
        "feature_id": "",
        "feature": feature,
        "epic": None,
        "feat_scores": feat_scores,
        "epic_scores": [],
        "feat_why": feat_why,
        "epic_why": "skipped",
        "pair": "unmatched",
    }
    if not feature:
        empty["pair"] = "no_feature"
        empty["epic_why"] = "skipped (no unique catalog feature)"
        return empty
    parent = str(feature.get("parent_id") or "")
    epic = epic_by_id.get(parent)
    if not epic:
        empty["pair"] = "feature_without_epic"
        empty["feat_why"] = f"{feat_why}; withheld (parent epic not in catalog)"
        empty["epic_why"] = f"parent {parent or '(none)'} not in epic.json"
        return empty
    return {
        "epic_id": str(epic["id"]),
        "feature_id": str(feature["id"]),
        "feature": feature,
        "epic": epic,
        "feat_scores": feat_scores,
        "epic_scores": [(100.0, epic)],
        "feat_why": feat_why,
        "epic_why": f"parent of feature {feature['id']}",
        "pair": "matched",
    }


def _row_keys(rows: list[dict[str, str]]) -> list[str]:
    keys: list[str] = []
    if rows:
        keys.extend(k for k in rows[0].keys() if k not in DROP_COLUMNS)
    if "ID" not in keys:
        keys.insert(0, "ID")
    return keys


def catalog_item_row(keys: list[str], wit: str, item: dict[str, Any]) -> dict[str, str]:
    """Existing catalog Epic/Feature as an ADO row, ID populated from JSON."""
    out = {k: "" for k in keys}
    out["Work Item Type"] = wit
    out["ID"] = str(item.get("id") or "")
    out["Title"] = item.get("title") or ""
    out["Description"] = item.get("description") or ""
    return out


def map_stories(
    rows: list[dict[str, str]],
    buckets: dict[str, list[dict[str, Any]]],
    threshold: float,
    margin: float,
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    keys = _row_keys(rows)
    workshops: list[dict[str, str]] = []
    stories: list[dict[str, str]] = []
    trailing: list[dict[str, str]] = []
    log_entries: list[dict[str, Any]] = []
    workshop_pick: dict[str, Any] | None = None
    workshop_scores: list[tuple[float, dict[str, Any]]] = []
    workshop_why = "no_csv_workshop"
    last_workshop_title = ""
    matched_features: dict[str, dict[str, Any]] = {}
    matched_epics: dict[str, dict[str, Any]] = {}

    for idx, row in enumerate(rows):
        wit = (row.get("Work Item Type") or "").strip()
        if wit in SKIP_AUTHORING_TYPES:
            continue
        out = {k: row.get(k) or "" for k in keys}
        title = row.get("Title") or ""

        if wit == "Workshop":
            last_workshop_title = title
            workshop_scores = score_titles(title, buckets.get("Workshop") or [])
            workshop_pick, workshop_why = pick_strong(workshop_scores, threshold, margin)
            if workshop_pick:
                out["ID"] = workshop_pick["id"]
            workshops.append(out)
            continue
        if wit != "User Story":
            trailing.append(out)
            continue

        pair = resolve_story_to_existing(title, story_blob(row), buckets, threshold, margin)
        feature_id = pair["feature_id"] if pair["pair"] == "matched" else ""
        epic_id = pair["epic_id"] if pair["pair"] == "matched" else ""
        workshop_id = workshop_pick["id"] if workshop_pick else ""
        if pair["pair"] == "matched" and pair["feature"] and pair["epic"]:
            matched_features[feature_id] = pair["feature"]
            matched_epics[epic_id] = pair["epic"]

        cat_feat_scores = pair["feat_scores"]
        feature = pair["feature"]
        epic = pair["epic"]
        log_entries.append(
            {
                "csvRow": idx + 2,
                "title": title,
                "status": "matched" if pair["pair"] == "matched" else "unmatched",
                "pair": pair["pair"],
                "catalogFeatureTitle": feature["title"] if feature else "",
                "catalogEpicTitle": epic["title"] if epic else "",
                "epicId": epic_id,
                "featureId": feature_id,
                "workshopId": workshop_id,
                "feature": {
                    "id": feature_id,
                    "title": feature["title"] if feature else "",
                    "score": round(cat_feat_scores[0][0], 1) if cat_feat_scores else 0,
                    "rationale": pair["feat_why"],
                },
                "epic": {
                    "id": epic_id,
                    "title": epic["title"] if epic else "",
                    "score": 100.0 if epic_id else 0,
                    "rationale": pair["epic_why"],
                },
                "workshop": {
                    "id": workshop_id,
                    "title": workshop_pick["title"] if workshop_pick else last_workshop_title,
                    "score": round(workshop_scores[0][0], 1) if workshop_scores else 0,
                    "rationale": workshop_why,
                },
            }
        )
        stories.append(out)

    epic_rows = [
        catalog_item_row(keys, "Epic", e)
        for e in sorted(matched_epics.values(), key=lambda x: (x.get("title") or "", x.get("id") or ""))
    ]
    feature_rows = [
        catalog_item_row(keys, "Feature", f)
        for f in sorted(
            matched_features.values(),
            key=lambda x: (x.get("parent_id") or "", x.get("title") or "", x.get("id") or ""),
        )
    ]
    mapped = workshops + epic_rows + feature_rows + stories + trailing
    return mapped, log_entries


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    """Internal only — not a public deliverable."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({h: excel_safe_cell(row.get(h) or "") for h in headers})


def col_letter(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def write_xlsx(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    """Minimal XLSX (no openpyxl). Shared strings + worksheet."""
    path.parent.mkdir(parents=True, exist_ok=True)
    strings: list[str] = []
    index: dict[str, int] = {}

    def sid(value: str) -> int:
        if value not in index:
            index[value] = len(strings)
            strings.append(value)
        return index[value]

    def cell_xml(ref: str, value: str) -> str:
        i = sid(value)
        return f'<c r="{ref}" t="s"><v>{i}</v></c>'

    sheet_rows = []
    header_cells = "".join(cell_xml(f"{col_letter(i + 1)}1", h) for i, h in enumerate(headers))
    sheet_rows.append(f'<row r="1">{header_cells}</row>')
    for ridx, row in enumerate(rows, start=2):
        cells = "".join(
            cell_xml(f"{col_letter(cidx + 1)}{ridx}", excel_safe_cell(row.get(h) or ""))
            for cidx, h in enumerate(headers)
        )
        sheet_rows.append(f'<row r="{ridx}">{cells}</row>')

    last = f"{col_letter(len(headers))}{len(rows) + 1}"
    sheet = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="A1:{last}"/>'
        "<sheetData>"
        + "".join(sheet_rows)
        + "</sheetData></worksheet>"
    )
    sst_items = "".join(f"<si><t xml:space=\"preserve\">{escape(s)}</t></si>" for s in strings)
    sst = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        f'count="{len(strings)}" uniqueCount="{len(strings)}">{sst_items}</sst>'
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="UserStories" sheetId="1" r:id="rId1"/></sheets></workbook>'
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
        "</Relationships>"
    )
    ctypes = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
        "</Types>"
    )
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ctypes)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/worksheets/sheet1.xml", sheet)
        z.writestr("xl/sharedStrings.xml", sst)
    path.write_bytes(buf.getvalue())


def write_logs(
    json_path: Path,
    source_csv: Path,
    entries: list[dict[str, Any]],
    buckets: dict[str, list[dict[str, Any]]],
    threshold: float,
    margin: float,
) -> None:
    matched = sum(1 for e in entries if e["status"] == "matched")
    unmatched = sum(1 for e in entries if e["status"] == "unmatched")
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceCsv": str(source_csv),
        "threshold": threshold,
        "margin": margin,
        "requireBothEpicAndFeature": True,
        "catalogCounts": {k: len(v) for k, v in buckets.items()},
        "userStoryCount": len(entries),
        "matched": matched,
        "unmatched": unmatched,
        "stories": entries,
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Map user stories to Epic/Feature/Workshop IDs")
    parser.add_argument("--csv", required=True, help="Validated working CSV (internal)")
    parser.add_argument("--work-items-dir", default="artifacts/work-items")
    parser.add_argument("--out-xlsx", required=True, help="Public deliverable: one Excel workbook")
    parser.add_argument("--log-json", required=True, help="Internal mapping log (not Excel)")
    parser.add_argument("--config", default=str(ROOT / ".cursor" / "config.yaml"))
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--margin", type=float, default=None)
    args = parser.parse_args()

    cfg = load_yaml_mapping(Path(args.config))
    threshold = float(args.threshold if args.threshold is not None else cfg.get("strong_threshold", 62))
    margin = float(args.margin if args.margin is not None else cfg.get("winner_margin", 8))

    source = Path(args.csv)
    if not source.is_file():
        print(f"source CSV not found: {source}", file=sys.stderr)
        return 1

    with source.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        source_headers = list(reader.fieldnames or [])
        rows = [{k: (r.get(k) or "") for k in source_headers} for r in reader]

    buckets = load_work_items(Path(args.work_items_dir))
    mapped, log_entries = map_stories(rows, buckets, threshold, margin)
    headers = [h for h in source_headers if h not in DROP_COLUMNS]
    if "ID" not in headers:
        headers.insert(0, "ID")

    write_logs(Path(args.log_json), source, log_entries, buckets, threshold, margin)
    try:
        write_xlsx(Path(args.out_xlsx), headers, mapped)
    except PermissionError:
        fallback = Path(args.log_json).parent / Path(args.out_xlsx).name
        write_xlsx(fallback, headers, mapped)
        print(
            f"WARN: could not overwrite {args.out_xlsx} (file open). Wrote {fallback}. "
            "Close the workbook and re-run mapping.",
            file=sys.stderr,
        )

    us = sum(1 for r in rows if (r.get("Work Item Type") or "").strip() == "User Story")
    if len(log_entries) != us:
        print("FAIL: mapping log count != User Story rows", file=sys.stderr)
        return 1
    print(
        f"mapped {us} user stories; matched {sum(1 for e in log_entries if e['status']=='matched')}; "
        f"unmatched {sum(1 for e in log_entries if e['status']=='unmatched')}; "
        f"catalog epics {sum(1 for r in mapped if (r.get('Work Item Type') or '')=='Epic')}; "
        f"catalog features {sum(1 for r in mapped if (r.get('Work Item Type') or '')=='Feature')}"
    )
    print(f"wrote {args.out_xlsx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
