#!/usr/bin/env python3
"""Audit CSS integrity in an Owen EPUB3 file.

Checks:
  1. Class mismatch — classes used in XHTML but not defined in CSS (error),
     and classes defined in CSS but never used (warning).
  2. Font-face integrity — @font-face url targets exist, embedded fonts have
     @font-face rules, and font-family references are resolvable.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared import _get_font_name_records

# Web-safe / universally available font families that don't need @font-face
WEB_SAFE_FONTS = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy",
    "system-ui", "ui-serif", "ui-sans-serif", "ui-monospace",
    "Arial", "Helvetica", "Times", "Times New Roman", "Georgia",
    "Courier", "Courier New", "Verdana", "Trebuchet MS",
    "Palatino", "Palatino Linotype", "Book Antiqua",
    "Garamond", "Baskerville", "Hoefler Text",
}

FONT_FACE_ALIASES = {
    # "Owen Title" is a deliberate CSS alias over the embedded Baskervville face.
    "Owen Title": {"Baskervville"},
}


def parse_css_classes(css: str) -> set[str]:
    """Extract all class names defined in CSS selectors.

    Handles grouped selectors (.a, .b { }), ignores pseudo-classes,
    pseudo-elements, and @-rule blocks.
    """
    classes: set[str] = set()
    # Remove @font-face, @media, @page, etc. blocks (nested braces)
    cleaned = re.sub(r'@[a-zA-Z-]+\s*[^{]*\{(?:[^{}]*\{[^}]*\})*[^}]*\}', '', css)
    # Find class selectors: .classname (not followed by another letter/digit/hyphen that's part of a longer name)
    for m in re.finditer(r'\.([a-zA-Z_][\w-]*)', cleaned):
        classes.add(m.group(1))
    return classes


def extract_xhtml_classes(zf: zipfile.ZipFile, xhtml_files: list[str]) -> Counter[str]:
    """Count every class attribute value used across all XHTML files."""
    counts: Counter[str] = Counter()
    for fn in xhtml_files:
        if fn not in zf.namelist():
            continue
        content = zf.read(fn).decode('utf-8', 'replace')
        for m in re.finditer(r'class="([^"]*)"', content):
            for cls in m.group(1).split():
                if cls:
                    counts[cls] += 1
    return counts


def parse_font_faces(css: str) -> list[dict[str, str]]:
    """Extract @font-face blocks as (font-family, url) pairs."""
    faces: list[dict[str, str]] = []
    for m in re.finditer(r'@font-face\s*\{([^}]+)\}', css, re.S):
        block = m.group(1)
        family_match = re.search(r'font-family\s*:\s*["\']?([^"\';\n]+)["\']?\s*;', block)
        src_match = re.search(r'url\(\s*["\']?([^)"\']+)["\']?\s*\)', block)
        if family_match:
            faces.append({
                "font_family": family_match.group(1).strip(),
                "url": src_match.group(1).strip() if src_match else "",
            })
    return faces


def extract_font_family_references(css: str) -> set[str]:
    """Extract all font-family values from non-@font-face rules."""
    families: set[str] = set()
    # Remove @font-face blocks first
    cleaned = re.sub(r'@font-face\s*\{[^}]+\}', '', css, flags=re.S)
    for m in re.finditer(r'font-family\s*:\s*([^;]+);', cleaned):
        value = m.group(1).strip()
        # Parse comma-separated list
        for part in value.split(','):
            part = part.strip().strip("'\"")
            # Strip !important and skip artifacts
            part = part.replace('!important', '').strip()
            if part and part not in ('important', ''):
                families.add(part)
    return families


def run_audit(epub_path: Path) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    info: dict[str, Any] = {}

    if not epub_path.exists():
        return {
            "status": "fail",
            "errors": [{"code": "missing_epub", "message": "EPUB file does not exist"}],
            "warnings": [],
            "info": {},
        }

    with zipfile.ZipFile(epub_path) as zf:
        # Find CSS files
        css_files = [n for n in zf.namelist() if n.endswith('.css')]
        info["css_file_count"] = len(css_files)

        if not css_files:
            return {
                "status": "warn",
                "errors": [],
                "warnings": [{"code": "no_css_files", "message": "No CSS files found in EPUB"}],
                "info": info,
            }

        # Combine all CSS
        all_css = ""
        for cf in css_files:
            all_css += zf.read(cf).decode('utf-8', 'replace') + "\n"

        # ── 1. Class mismatch ───────────────────────────────────────────
        css_classes = parse_css_classes(all_css)
        info["css_classes_defined"] = len(css_classes)

        # Get XHTML files from manifest
        xhtml_files: list[str] = []
        try:
            container = zf.read("META-INF/container.xml").decode('utf-8')
            opf_match = re.search(r'full-path="([^"]+)"', container)
            if opf_match:
                opf_path = opf_match.group(1)
                opf_dir = posixpath.dirname(opf_path)
                opf = zf.read(opf_path).decode('utf-8')
                for m in re.finditer(r'<item[^>]+href="([^"]+)"[^>]*media-type="application/xhtml\+xml"', opf):
                    href = m.group(1)
                    xhtml_files.append(posixpath.normpath(posixpath.join(opf_dir, href)).lstrip("./"))
                # Also catch nav property items
                for m in re.finditer(r'<item[^>]+properties="[^"]*nav[^"]*"[^>]*href="([^"]+)"', opf):
                    href = m.group(1)
                    full = posixpath.normpath(posixpath.join(opf_dir, href)).lstrip("./")
                    if full not in xhtml_files:
                        xhtml_files.append(full)
        except Exception:
            # Fallback: grab all .xhtml files
            xhtml_files = [n for n in zf.namelist() if n.endswith('.xhtml')]

        xhtml_classes = extract_xhtml_classes(zf, xhtml_files)
        info["xhtml_classes_used"] = len(xhtml_classes)
        info["xhtml_files_scanned"] = len(xhtml_files)

        # Undefined: used in XHTML, not in CSS
        undefined = sorted(xhtml_classes.keys() - css_classes)
        for cls in undefined:
            errors.append({
                "code": "undefined_class",
                "message": f"Class '.{cls}' used in XHTML but not defined in CSS",
                "class": cls,
                "usage_count": xhtml_classes[cls],
            })

        # Orphan: defined in CSS, never used
        orphan = sorted(css_classes - xhtml_classes.keys())
        for cls in orphan:
            warnings.append({
                "code": "orphan_class",
                "message": f"Class '.{cls}' defined in CSS but never used in XHTML",
                "class": cls,
            })

        # ── 2. Font-face integrity ──────────────────────────────────────
        font_faces = parse_font_faces(all_css)
        info["font_face_count"] = len(font_faces)

        # Map: font_family -> list of urls
        font_face_map: dict[str, list[str]] = {}
        for ff in font_faces:
            font_face_map.setdefault(ff["font_family"], []).append(ff["url"])

        # Embedded font files
        embedded_fonts = {n for n in zf.namelist() if n.endswith(('.ttf', '.otf', '.woff', '.woff2'))}
        info["embedded_font_count"] = len(embedded_fonts)

        # Check @font-face urls point to real files
        for ff in font_faces:
            if not ff["url"]:
                continue
            # Resolve relative to CSS file location
            css_dir = posixpath.dirname(css_files[0]) if css_files else ""
            resolved = posixpath.normpath(posixpath.join(css_dir, ff["url"]))
            if resolved not in embedded_fonts:
                errors.append({
                    "code": "missing_font_file",
                    "message": f"@font-face '{ff['font_family']}' references missing file '{ff['url']}'",
                    "font_family": ff["font_family"],
                    "url": ff["url"],
                })
                continue
            if resolved.endswith(('.ttf', '.otf')):
                try:
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix=Path(resolved).suffix) as tmp:
                        tmp.write(zf.read(resolved))
                        tmp.flush()
                        records = _get_font_name_records(tmp.name)
                    family_values = {
                        records.get("preferred_family", ""),
                        records.get("family", ""),
                    }
                    allowed = {ff["font_family"]} | FONT_FACE_ALIASES.get(ff["font_family"], set())
                    if not (allowed & family_values):
                        warnings.append({
                            "code": "font_family_metadata_mismatch",
                            "message": (
                                f"@font-face family '{ff['font_family']}' does not match embedded "
                                f"font metadata family values {sorted(v for v in family_values if v)}"
                            ),
                            "font_family": ff["font_family"],
                            "file": resolved,
                            "metadata": records,
                        })
                except Exception as exc:
                    warnings.append({
                        "code": "font_metadata_unreadable",
                        "message": f"Could not read font metadata for '{resolved}': {exc}",
                        "file": resolved,
                    })

        # Check embedded fonts have @font-face
        font_face_urls = set()
        for urls in font_face_map.values():
            for url in urls:
                css_dir = posixpath.dirname(css_files[0]) if css_files else ""
                resolved = posixpath.normpath(posixpath.join(css_dir, url))
                font_face_urls.add(resolved)

        for font_file in sorted(embedded_fonts):
            if font_file not in font_face_urls:
                warnings.append({
                    "code": "orphan_font_file",
                    "message": f"Embedded font '{font_file}' has no matching @font-face rule",
                    "file": font_file,
                })

        # Check font-family references in regular rules
        referenced_families = extract_font_family_references(all_css)
        for family in sorted(referenced_families):
            if family in font_face_map:
                continue
            if family in WEB_SAFE_FONTS:
                continue
            warnings.append({
                "code": "undefined_font_family",
                "message": f"Font family '{family}' used in CSS but has no @font-face and is not web-safe",
                "font_family": family,
            })

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {
        "epub": str(epub_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "info": info,
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# CSS Audit: {Path(result['epub']).name}",
        "",
        f"- Status: **{result['status'].upper()}**",
        f"- Errors: {result['error_count']}",
        f"- Warnings: {result['warning_count']}",
        "",
    ]

    info = result.get("info", {})
    lines.extend([
        "## Summary",
        "",
        f"- CSS files: {info.get('css_file_count', 0)}",
        f"- CSS classes defined: {info.get('css_classes_defined', 0)}",
        f"- XHTML classes used: {info.get('xhtml_classes_used', 0)}",
        f"- XHTML files scanned: {info.get('xhtml_files_scanned', 0)}",
        f"- @font-face rules: {info.get('font_face_count', 0)}",
        f"- Embedded fonts: {info.get('embedded_font_count', 0)}",
        "",
    ])

    if result["errors"]:
        lines.extend(["## Errors", ""])
        for item in result["errors"]:
            detail = item.get("class", item.get("font_family", item.get("file", "")))
            count = item.get("usage_count", "")
            suffix = f" ({count} uses)" if count else ""
            lines.append(f"- `{item['code']}`: {item['message']}{suffix}")
        lines.append("")

    if result["warnings"]:
        lines.extend(["## Warnings", ""])
        for item in result["warnings"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit CSS integrity in an Owen EPUB3 file")
    parser.add_argument("epub", type=Path, help="Path to .epub file")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Directory for JSON/Markdown reports",
    )
    args = parser.parse_args(argv)

    result = run_audit(args.epub)

    # Determine output directory
    out_dir = args.out_dir
    if out_dir is None:
        parts = args.epub.parts
        for i, part in enumerate(parts):
            if part == "volumes" and i + 3 < len(parts):
                vol_dir = Path(*parts[: i + 2])
                if parts[i + 2] == "output":
                    out_dir = vol_dir / "bugs_fixes"
                    break
        if out_dir is None:
            out_dir = Path("qa/reports")

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.epub.stem
    json_path = out_dir / f"{stem}_css_audit.json"
    md_path = out_dir / f"{stem}_css_audit.md"

    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(result), encoding="utf-8")

    print(render_markdown(result))
    print(f"Reports written:\n- {json_path}\n- {md_path}")

    if result["error_count"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
