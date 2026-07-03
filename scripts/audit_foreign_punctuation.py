#!/usr/bin/env python3
"""Audit punctuation and quotation contexts around Greek/Hebrew spans in EPUBs."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any

from audit_epub import (
    HTML_TAG_RE,
    WHITESPACE_RE,
    find_foreign_span_quote_bleeds,
    find_foreign_span_quote_word_glue,
)


SPAN_CONTEXT_RE = re.compile(
    r'(?P<before>.{0,90})(?P<span><span\s+[^>]*lang=["\'](?P<lang>el|he)["\'][^>]*>.*?</span>)(?P<after>.{0,120})',
    re.I | re.S,
)


def html_text(fragment: str) -> str:
    return WHITESPACE_RE.sub(" ", unescape(HTML_TAG_RE.sub("", fragment))).strip()


def classify_context(before: str, span_html: str, after: str) -> tuple[str, str]:
    before_tail = html_text(before)[-60:]
    after_text = html_text(after)[:100]
    span_text = html_text(span_html)

    raw_context = f"{before}{span_html}{after}"
    if find_foreign_span_quote_bleeds(raw_context):
        return "warning", "foreign_span_quote_bleed"
    if find_foreign_span_quote_word_glue(raw_context):
        return "warning", "foreign_span_quote_word_glue"

    if re.search(r'["“]\s*$', before_tail) and re.match(r'^\s*[,;:]', after_text):
        return "review", "quote_opens_outside_span_with_punctuation_after"
    if re.search(r'["“]\s*$', before_tail) and re.match(r'^\s*["”]', after_text):
        return "review", "quote_opens_outside_span_and_closes_after_span"
    if re.search(r'["“]\s*$', before_tail):
        return "review", "quote_opens_outside_span"
    if re.match(r'^\s*["”]', after_text):
        return "review", "quote_closes_after_span"
    if re.match(r'^\s*[,;:]\s+(?=[A-Z])', after_text) and len(span_text) > 1:
        return "info", "foreign_term_followed_by_english_gloss_or_reference"
    if re.match(r'^\s*[—-]\s+', after_text):
        return "info", "foreign_term_followed_by_dash_gloss"
    return "info", "ordinary_foreign_span_context"


def audit_epub(epub_path: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()

    with zipfile.ZipFile(epub_path) as zf:
        for path in sorted(name for name in zf.namelist() if name.endswith(".xhtml")):
            raw = zf.read(path).decode("utf-8", "replace")
            for match in SPAN_CONTEXT_RE.finditer(raw):
                before = match.group("before")
                span_html = match.group("span")
                after = match.group("after")
                severity, code = classify_context(before, span_html, after)
                counts[f"{severity}:{code}"] += 1
                counts[f"severity:{severity}"] += 1
                entries.append({
                    "file": path,
                    "lang": match.group("lang"),
                    "severity": severity,
                    "code": code,
                    "span_text": html_text(span_html),
                    "context": html_text(f"{before}{span_html}{after}")[:260],
                    "html_context": WHITESPACE_RE.sub(" ", f"{before}{span_html}{after}").strip()[:360],
                })

    warnings = [entry for entry in entries if entry["severity"] == "warning"]
    review = [entry for entry in entries if entry["severity"] == "review"]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "epub": str(epub_path),
        "status": "warn" if warnings else "pass",
        "foreign_span_context_count": len(entries),
        "warning_count": len(warnings),
        "review_count": len(review),
        "counts": dict(sorted(counts.items())),
        "warnings": warnings,
        "review_items": review,
        "entries": entries,
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Foreign Punctuation Audit: {Path(result['epub']).name}",
        "",
        f"- Status: **{result['status'].upper()}**",
        f"- Foreign span contexts: {result['foreign_span_context_count']}",
        f"- Warnings: {result['warning_count']}",
        f"- Review-only contexts: {result['review_count']}",
        "",
        "## Counts",
        "",
    ]
    for key, value in result["counts"].items():
        lines.append(f"- `{key}`: {value}")

    def section(title: str, items: list[dict[str, Any]], limit: int | None = None) -> None:
        lines.extend(["", f"## {title}", ""])
        if not items:
            lines.append("None.")
            return
        selected = items if limit is None else items[:limit]
        for item in selected:
            lines.extend([
                f"### {item['file']} — {item['code']}",
                "",
                f"- Language: `{item['lang']}`",
                f"- Span: `{item['span_text']}`",
                f"- Context: {item['context']}",
                "",
            ])
        if limit is not None and len(items) > limit:
            lines.append(f"... {len(items) - limit} additional items omitted from Markdown; see JSON for all entries.")

    section("Warnings", result["warnings"])
    section("Review-Only Contexts", result["review_items"], limit=80)

    return "\n".join(lines).rstrip() + "\n"


def infer_default_epub(volume: str, root: Path) -> Path:
    return root / "volumes" / f"v{volume}" / "output" / f"volume_{volume}.epub"


def infer_default_out_dir(volume: str, root: Path) -> Path:
    return root / "volumes" / f"v{volume}" / "reports"


def write_reports(result: dict[str, Any], out_dir: Path, stem: str) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{stem}_foreign_punctuation.json"
    md_path = out_dir / f"{stem}_foreign_punctuation.md"
    json_path.unlink(missing_ok=True)
    md_path.unlink(missing_ok=True)
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(result), encoding="utf-8")
    return json_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit punctuation around Greek/Hebrew spans in Owen EPUBs")
    parser.add_argument("volume", help="Owen volume number, e.g. 1")
    parser.add_argument("--epub", type=Path, default=None, help="Override EPUB path")
    parser.add_argument("--out-dir", type=Path, default=None, help="Directory for reports")
    args = parser.parse_args(argv)

    root = Path.cwd()
    epub_path = args.epub or infer_default_epub(args.volume, root)
    out_dir = args.out_dir or infer_default_out_dir(args.volume, root)
    if not epub_path.exists():
        print(f"EPUB not found: {epub_path}", file=sys.stderr)
        return 1

    result = audit_epub(epub_path)
    json_path, md_path = write_reports(result, out_dir, f"volume_{args.volume}")
    print(render_markdown(result))
    print(f"Reports written:\n- {json_path}\n- {md_path}")
    return 1 if result["warning_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
