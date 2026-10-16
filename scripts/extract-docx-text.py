#!/usr/bin/env python3
"""Extract plain text from a .docx file (paragraphs only).

Usage:
  python scripts/extract-docx-text.py path/to/file.docx --out artifacts/intake/.pipeline/prerequisite.txt
"""
from __future__ import annotations

import argparse
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract_paragraphs(docx_path: Path) -> str:
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    lines: list[str] = []
    for p in root.iter(f"{W_NS}p"):
        parts: list[str] = []
        for t in p.iter(f"{W_NS}t"):
            if t.text:
                parts.append(t.text)
        line = "".join(parts).strip()
        if line:
            lines.append(line)
    return "\n".join(lines) + ("\n" if lines else "")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if not args.docx.is_file():
        print(f"FAIL: file not found: {args.docx}", file=sys.stderr)
        sys.exit(1)
    try:
        text = extract_paragraphs(args.docx)
    except (KeyError, zipfile.BadZipFile) as exc:
        print(f"FAIL: could not read docx: {exc}", file=sys.stderr)
        sys.exit(1)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"Wrote {args.out} ({len(text)} chars)")


if __name__ == "__main__":
    main()
