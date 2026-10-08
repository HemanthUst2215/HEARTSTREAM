"""Load and index all work items from JSON files under artifacts/work-items/."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_SKIP_NAME_PARTS = ("manifest", "schema-profile", "validation-report")


def load_work_items_from_directory(work_items_dir: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    seen_ids: set[int] = set()
    if not work_items_dir.is_dir():
        return items

    for path in sorted(work_items_dir.glob("*.json")):
        if path.name.startswith(".") or any(p in path.name for p in _SKIP_NAME_PARTS):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        work_items = data.get("workItems")
        if not isinstance(work_items, list):
            continue
        source_file = (data.get("meta") or {}).get("sourceFile") or str(path)
        for wi in work_items:
            if not isinstance(wi, dict) or wi.get("workItemId") is None:
                continue
            wid = int(wi["workItemId"])
            if wid in seen_ids:
                continue
            seen_ids.add(wid)
            entry = dict(wi)
            entry["_indexSourceJson"] = str(path)
            entry["_indexSourceCsv"] = source_file
            items.append(entry)
    return items


def build_item_index(items: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    return {int(w["workItemId"]): w for w in items}


def build_parent_title_index(items: list[dict[str, Any]]) -> dict[int, str]:
    by_id: dict[int, str] = {}
    for wi in items:
        wid = wi.get("workItemId")
        if wid is not None:
            by_id[int(wid)] = (wi.get("title") or wi.get("displayTitle") or "").strip()
    return by_id


def work_item_description_text(wi: dict[str, Any]) -> str:
    desc = wi.get("description") or {}
    if isinstance(desc, dict):
        return " ".join(str(desc.get(k) or "") for k in ("plainText", "summary")).strip()
    return str(desc or "")


def work_item_search_text(
    wi: dict[str, Any], parent_titles: dict[int, str]
) -> str:
    parts: list[str] = []
    for key in ("title", "displayTitle", "workItemCode", "workItemType"):
        v = wi.get(key)
        if v:
            parts.append(str(v))
    parts.append(work_item_description_text(wi))
    area = wi.get("areaPath") or {}
    if isinstance(area, dict) and area.get("raw"):
        parts.append(str(area["raw"]))
    parent = wi.get("parent") or {}
    if isinstance(parent, dict):
        pid = parent.get("workItemId")
        if pid is not None:
            pt = parent_titles.get(int(pid))
            if pt:
                parts.append(pt)
    return " ".join(p for p in parts if p)


def _ancestor_chain(
    wi: dict[str, Any], by_id: dict[int, dict[str, Any]], max_depth: int = 6
) -> list[dict[str, Any]]:
    chain = [wi]
    cur = wi
    for _ in range(max_depth):
        parent = cur.get("parent") or {}
        pid = parent.get("workItemId") if isinstance(parent, dict) else None
        if pid is None or int(pid) not in by_id:
            break
        cur = by_id[int(pid)]
        chain.append(cur)
    return chain


def epic_and_feature_labels(
    wi: dict[str, Any], by_id: dict[int, dict[str, Any]]
) -> tuple[str, str]:
    """Epic = nearest Epic ancestor-or-self; Feature = nearest Feature ancestor-or-self."""
    chain = _ancestor_chain(wi, by_id)
    epic = ""
    feature = ""
    for node in chain:
        wtype = (node.get("workItemType") or "").strip().lower()
        title = (node.get("title") or "").strip()
        if not feature and wtype == "feature":
            feature = title
        if not epic and wtype == "epic":
            epic = title
    if not feature and (wi.get("workItemType") or "").strip().lower() == "workshop":
        feature = (wi.get("title") or "").strip()
    return epic, feature
