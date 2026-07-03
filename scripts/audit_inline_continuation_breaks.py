#!/usr/bin/env python3
"""Audit adjacent list-item blocks split after comma/semicolon continuations."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.owen_lists import last_meaningful_visible_char, reader_visible_text


BLOCK_RE = re.compile(
    r'<p\b(?P<attrs>[^>]*)>(?P<inner>.*?)</p>|'
    r'<h[1-6]\b[^>]*>.*?</h[1-6]>|'
    r'<blockquote\b[^>]*>.*?</blockquote>|'
    r'<aside\b[^>]*>.*?</aside>',
    re.S | re.I,
)
CLASS_RE = re.compile(r'\bclass="(?P<classes>[^"]*)"', re.I)
MARKER_RE = re.compile(r'^\s*<strong\b[^>]*>(?P<marker>.*?)</strong>', re.S | re.I)


def is_list_item(attrs: str) -> bool:
    class_match = CLASS_RE.search(attrs)
    if not class_match:
        return False
    classes = set(class_match.group("classes").split())
    return "list-item" in classes or "roman-list-item" in classes


def marker_text(inner: str) -> str:
    marker_match = MARKER_RE.search(inner)
    if not marker_match:
        return ""
    return reader_visible_text(marker_match.group("marker"))


def scan_xhtml(name: str, xhtml: str) -> list[dict]:
    findings = []
    previous = None
    paragraph_index = 0
    for match in BLOCK_RE.finditer(xhtml):
        attrs = match.groupdict().get("attrs") or ""
        inner = match.groupdict().get("inner") or ""
        if not attrs:
            previous = None
            continue
        paragraph_index += 1
        if not is_list_item(attrs):
            previous = None
            continue
        current = {
            "file": name,
            "paragraph_index": paragraph_index,
            "classes": CLASS_RE.search(attrs).group("classes"),
            "marker": marker_text(inner),
            "text": reader_visible_text(inner),
            "last_char": last_meaningful_visible_char(inner),
        }
        if previous and previous["last_char"] in {",", ";"}:
            findings.append(
                {
                    "file": name,
                    "previous_paragraph_index": previous["paragraph_index"],
                    "next_paragraph_index": current["paragraph_index"],
                    "previous_marker": previous["marker"],
                    "next_marker": current["marker"],
                    "previous_last_char": previous["last_char"],
                    "previous_text": previous["text"],
                    "next_text": current["text"],
                }
            )
        previous = current
    return findings


def scan_epub(epub_path: Path) -> list[dict]:
    findings = []
    with zipfile.ZipFile(epub_path) as zf:
        for name in sorted(zf.namelist()):
            if not name.startswith("EPUB/") or not name.endswith(".xhtml"):
                continue
            if name.endswith("endnotes.xhtml") or name.endswith("nav.xhtml"):
                continue
            xhtml = zf.read(name).decode("utf-8", errors="replace")
            findings.extend(scan_xhtml(name, xhtml))
    return findings


def write_reports(volume: int, findings: list[dict], output_dir: Path | None) -> tuple[Path, Path]:
    if output_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_inline_continuation_breaks")
        output_dir = ROOT / "volumes" / f"v{volume}" / "reports" / stamp
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"volume_{volume}_inline_continuation_breaks.json"
    md_path = output_dir / f"volume_{volume}_inline_continuation_breaks.md"
    json_path.unlink(missing_ok=True)
    md_path.unlink(missing_ok=True)

    payload = {
        "volume": volume,
        "finding_count": len(findings),
        "findings": findings,
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        f"# Volume {volume} Inline Continuation Break Audit",
        "",
        f"Finding count: {len(findings)}",
        "",
        "This audit flags adjacent list-item paragraphs where the previous point's last meaningful reader-visible character is comma or semicolon.",
        "",
    ]
    if findings:
        for idx, finding in enumerate(findings, 1):
            lines.extend(
                [
                    f"## {idx}. {finding['file']} p{finding['previous_paragraph_index']} -> p{finding['next_paragraph_index']}",
                    "",
                    f"- Previous marker: `{finding['previous_marker']}`",
                    f"- Next marker: `{finding['next_marker']}`",
                    f"- Previous ending: `{finding['previous_last_char']}`",
                    f"- Previous text: {finding['previous_text']}",
                    f"- Next text: {finding['next_text']}",
                    "",
                ]
            )
    md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("volume", type=int, help="Owen volume number")
    parser.add_argument("--epub", type=Path, help="Path to EPUB; defaults to volumes/vN/output/volume_N.epub")
    parser.add_argument("--output-dir", type=Path, help="Directory for JSON/Markdown reports")
    args = parser.parse_args()

    epub_path = args.epub or ROOT / "volumes" / f"v{args.volume}" / "output" / f"volume_{args.volume}.epub"
    if not epub_path.exists():
        raise SystemExit(f"EPUB not found: {epub_path}")

    findings = scan_epub(epub_path)
    json_path, md_path = write_reports(args.volume, findings, args.output_dir)
    print(f"Inline continuation breaks: {len(findings)}")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
