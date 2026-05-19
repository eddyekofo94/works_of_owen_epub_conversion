"""test_epub_structure.py — XHTML structure and navigation correctness.

These tests verify the structural integrity of the produced EPUB files:
  - Heading hierarchy matches the Owen design (treatise title, chapter, sub)
  - Language tags are correct on Greek / Hebrew spans
  - Navigation is complete and Apple Books compatible
  - CSS classes used in XHTML are defined in main.css
  - No empty paragraph elements
  - No raw Markdown or pipeline artifacts in text nodes

All tests are EPUB-scanning tests; they skip if the EPUB is not on disk.

    OWEN_REGRESSION_VOLUMES=1,2 pytest tests/test_epub_structure.py
"""

from __future__ import annotations

import os
import re
import zipfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.parent

# Apple Books navigation entry limit (characters).
# Entries longer than this are truncated in the Books TOC sidebar.
APPLE_BOOKS_NAV_MAX_CHARS = 100


def _requested_volumes() -> list[int]:
    raw = os.environ.get("OWEN_REGRESSION_VOLUMES", "1").strip()
    if raw.lower() == "all":
        return [
            int(path.name[1:])
            for path in sorted((BASE_DIR / "volumes").glob("v[0-9]*"))
            if (path / "output" / f"volume_{path.name[1:]}.epub").exists()
        ]
    return [int(part) for part in raw.replace(",", " ").split() if part]


def _epub_path(volume: int) -> Path:
    return BASE_DIR / "volumes" / f"v{volume}" / "output" / f"volume_{volume}.epub"


def _load_epub(volume: int) -> dict[str, str]:
    ep = _epub_path(volume)
    if not ep.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {ep}")
    files: dict[str, str] = {}
    with zipfile.ZipFile(ep) as zf:
        for name in zf.namelist():
            if name.endswith((".xhtml", ".css", ".opf", ".ncx")):
                files[name] = zf.read(name).decode("utf-8", errors="replace")
    return files


VOLUMES = _requested_volumes()


# ===========================================================================
# Heading hierarchy
# ===========================================================================

@pytest.mark.parametrize("volume", VOLUMES)
def test_chapter_files_have_at_most_two_h1_elements(volume: int):
    """
    Owen chapter files are allowed one OR two h1 elements:
      - Single h1: a normal chapter with a standard chapter-heading.
      - Two h1s: a treatise title page is embedded — h1.primary (treatise)
        plus h1.secondary (chapter number).  Both are valid.
    Front matter files use h2, so zero h1 is also acceptable for those.
    Three or more h1s is always a bug.
    """
    files = _load_epub(volume)
    failures: list[str] = []
    for name, html in sorted(files.items()):
        if not name.startswith("EPUB/ch"):
            continue
        h1s = re.findall(r"<h1\b", html)
        if len(h1s) > 2:
            failures.append(f"{name}: {len(h1s)} h1 elements")

    assert not failures, (
        f"Volume {volume}: chapter files with more than 2 h1 elements:\n"
        + "\n".join(f"  {f}" for f in failures)
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_no_empty_paragraph_elements(volume: int):
    """
    <p></p> and <p>  </p> are rendering artifacts.  Zero tolerance:
    they display as invisible gap-space in most EPUB readers.
    """
    files = _load_epub(volume)
    failures: list[str] = []
    for name, html in sorted(files.items()):
        if not name.endswith(".xhtml"):
            continue
        if re.search(r"<p(?:\s[^>]*)?\s*>\s*</p>", html):
            failures.append(name)

    assert not failures, (
        f"Volume {volume}: files with empty <p> elements: {failures}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_no_raw_markdown_bold_in_xhtml(volume: int):
    """
    '**text**' is Markdown bold syntax.  It must never appear literally in
    the output XHTML — it should have been converted to <b>text</b>.
    """
    files = _load_epub(volume)
    failures: list[str] = []
    for name, html in sorted(files.items()):
        if not name.endswith(".xhtml"):
            continue
        # Strip tags so we only see text node content
        text = re.sub(r"<[^>]+>", " ", html)
        if "**" in text:
            sample = re.search(r".{0,30}\*\*.{0,30}", text)
            snippet = sample.group(0) if sample else "**"
            failures.append(f"{name}: {snippet!r}")

    assert not failures, (
        f"Volume {volume}: raw Markdown bold (**) found in text:\n"
        + "\n".join(f"  {f}" for f in failures[:10])
    )


# ===========================================================================
# Language tags on Greek and Hebrew spans
# ===========================================================================

@pytest.mark.parametrize("volume", VOLUMES)
def test_greek_spans_have_correct_lang_attributes(volume: int):
    """
    Every Greek <span> must carry both lang="el" and xml:lang="el".
    Missing xml:lang breaks XML-namespace-aware EPUB validators.
    """
    files = _load_epub(volume)
    failures: list[str] = []

    GREEK_SPAN_RE = re.compile(r'<span\b([^>]*)>[Ͱ-Ͽἀ-῿]', re.S)

    for name, html in sorted(files.items()):
        if not name.endswith(".xhtml"):
            continue
        for m in GREEK_SPAN_RE.finditer(html):
            attrs = m.group(1)
            if 'lang="el"' not in attrs:
                failures.append(f"{name}: Greek span missing lang=\"el\": {attrs[:80]}")
            if 'xml:lang="el"' not in attrs:
                failures.append(f"{name}: Greek span missing xml:lang=\"el\": {attrs[:80]}")

    assert not failures, (
        f"Volume {volume}: malformed Greek span attributes:\n"
        + "\n".join(f"  {f}" for f in failures[:10])
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_hebrew_spans_have_correct_lang_and_dir_attributes(volume: int):
    """
    Every Hebrew <span> must carry lang="he", xml:lang="he", and dir="rtl".
    Missing dir="rtl" causes Hebrew text to render left-to-right in Apple Books.
    """
    files = _load_epub(volume)
    failures: list[str] = []

    HEBREW_SPAN_RE = re.compile(r'<span\b([^>]*)>[֐-׿]', re.S)

    for name, html in sorted(files.items()):
        if not name.endswith(".xhtml"):
            continue
        for m in HEBREW_SPAN_RE.finditer(html):
            attrs = m.group(1)
            missing = []
            if 'lang="he"' not in attrs:
                missing.append('lang="he"')
            if 'xml:lang="he"' not in attrs:
                missing.append('xml:lang="he"')
            if 'dir="rtl"' not in attrs:
                missing.append('dir="rtl"')
            if missing:
                failures.append(
                    f"{name}: Hebrew span missing {', '.join(missing)}: {attrs[:80]}"
                )

    assert not failures, (
        f"Volume {volume}: malformed Hebrew span attributes:\n"
        + "\n".join(f"  {f}" for f in failures[:10])
    )


# ===========================================================================
# Navigation / TOC
# ===========================================================================

@pytest.mark.parametrize("volume", VOLUMES)
def test_nav_has_no_duplicate_chapter_entries(volume: int):
    """
    Two nav entries pointing to the same href in the reading-order TOC section
    (epub:type="toc") means a chapter was emitted twice during assembly.

    The landmarks section of the nav (epub:type="landmarks") is intentionally
    excluded — it legitimately references files that also appear in the TOC,
    e.g. ch001.xhtml for "Start of Content".
    """
    files = _load_epub(volume)
    nav_html = next(
        (v for k, v in files.items() if "nav.xhtml" in k), ""
    )
    if not nav_html:
        pytest.skip(f"Volume {volume}: nav.xhtml not found")

    # Extract only the reading-order TOC section
    toc_m = re.search(
        r'<nav\b[^>]*epub:type="toc"[^>]*>(.*?)</nav>',
        nav_html,
        re.S,
    )
    if not toc_m:
        pytest.skip(f"Volume {volume}: epub:type=\"toc\" nav section not found")

    toc_html = toc_m.group(1)
    hrefs = re.findall(r'href="([^"#]+\.xhtml)"', toc_html)
    counts: dict[str, int] = {}
    for href in hrefs:
        counts[href] = counts.get(href, 0) + 1

    dupes = {k: v for k, v in counts.items() if v > 1}
    assert not dupes, (
        f"Volume {volume}: duplicate TOC nav entries:\n"
        + "\n".join(f"  {k}: {v} times" for k, v in sorted(dupes.items()))
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_nav_entry_lengths_are_within_apple_books_limit(volume: int):
    """
    Apple Books truncates TOC sidebar entries longer than ~100 characters.
    Flag any nav entries that would be silently cut mid-word.

    Pipeline fix applied: nav_display_title() in shared.py now truncates at
    _NAV_TITLE_MAX_CHARS and appends an ellipsis.  EPUBs built after this fix
    will pass.  Pre-built EPUBs (e.g. V1 on disk) will fail until rebuilt.
    """
    files = _load_epub(volume)
    nav_html = next(
        (v for k, v in files.items() if "nav.xhtml" in k), ""
    )
    if not nav_html:
        pytest.skip(f"Volume {volume}: nav.xhtml not found")

    # Restrict to the TOC section only (landmarks intentionally excluded)
    toc_m = re.search(
        r'<nav\b[^>]*epub:type="toc"[^>]*>(.*?)</nav>', nav_html, re.S
    )
    toc_html = toc_m.group(1) if toc_m else nav_html
    entries = re.findall(r'<a\b[^>]+href="[^"]+"[^>]*>([^<]+)</a>', toc_html)
    overlong = [
        (e.strip(), len(e.strip()))
        for e in entries
        if len(e.strip()) > APPLE_BOOKS_NAV_MAX_CHARS
    ]

    assert not overlong, (
        f"Volume {volume}: {len(overlong)} TOC nav entry/entries exceed "
        f"{APPLE_BOOKS_NAV_MAX_CHARS} chars (Apple Books sidebar truncates them):\n"
        + "\n".join(f"  ({n} chars) {t!r}" for t, n in overlong[:10])
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_all_nav_hrefs_resolve_to_files_in_epub(volume: int):
    """
    Every href in the nav document must point to an existing file inside
    the EPUB.  A broken nav link means Apple Books will show an error
    or silently skip the chapter in the TOC.
    """
    ep = _epub_path(volume)
    if not ep.exists():
        pytest.skip(f"EPUB for volume {volume} not found")

    with zipfile.ZipFile(ep) as zf:
        all_files = set(zf.namelist())
        nav_html = ""
        for name in zf.namelist():
            if "nav.xhtml" in name:
                nav_html = zf.read(name).decode("utf-8", errors="replace")
                nav_dir = name.rsplit("/", 1)[0] + "/"
                break

    if not nav_html:
        pytest.skip(f"Volume {volume}: nav.xhtml not found")

    broken: list[str] = []
    for href in re.findall(r'href="([^"#]+)"', nav_html):
        # Resolve relative to the nav file directory
        full = nav_dir + href
        # Normalise: remove any ../ sequences
        parts = full.split("/")
        resolved: list[str] = []
        for p in parts:
            if p == "..":
                if resolved:
                    resolved.pop()
            elif p != ".":
                resolved.append(p)
        target = "/".join(resolved)
        if target not in all_files:
            broken.append(f"{href!r} -> {target!r} not in EPUB")

    assert not broken, (
        f"Volume {volume}: broken nav hrefs:\n"
        + "\n".join(f"  {b}" for b in broken[:20])
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_nav_chapter_count_is_plausible(volume: int):
    """
    Each volume must have at least 2 chapter nav entries (most have 20–80).
    A count of 0 or 1 means the nav assembly failed catastrophically.
    """
    files = _load_epub(volume)
    nav_html = next(
        (v for k, v in files.items() if "nav.xhtml" in k), ""
    )
    if not nav_html:
        pytest.skip(f"Volume {volume}: nav.xhtml not found")

    # Count entries pointing to chapter files (ch*.xhtml)
    chapter_hrefs = re.findall(r'href="(ch\d+\.xhtml)"', nav_html)
    count = len(chapter_hrefs)

    assert count >= 2, (
        f"Volume {volume}: nav has only {count} chapter entry/entries — "
        "possible nav assembly failure."
    )


# ===========================================================================
# CSS class coverage
# ===========================================================================

@pytest.mark.parametrize("volume", VOLUMES)
def test_html_classes_are_defined_in_main_css(volume: int):
    """
    Every CSS class used in XHTML files should be defined in main.css.
    An undefined class silently has no visual effect — the reader sees
    unstyled text where formatting was intended.

    Known exclusions (renderer-internal or browser-applied):
      - 'greek', 'hebrew' — applied by the language-tagging code, may use
        descendant selectors in CSS rather than direct class rules
      - 'fn-link' — endnote link style, may be covered by an epub:type rule
      - 'cover' — single-use cover image wrapper
      - 'list-item' — intentionally a simple unstyled wrapper in some volumes
    """
    files = _load_epub(volume)
    css = next(
        (v for k, v in files.items() if k.endswith("main.css")), ""
    )
    if not css:
        pytest.skip(f"Volume {volume}: main.css not found")

    # Extract all class names used in XHTML
    used_classes: set[str] = set()
    for name, html in files.items():
        if not name.endswith(".xhtml"):
            continue
        for m in re.finditer(r'class="([^"]+)"', html):
            for cls in m.group(1).split():
                used_classes.add(cls)

    # Extract class selectors defined in CSS (.classname)
    defined_in_css: set[str] = set(re.findall(r"\.([a-zA-Z][-a-zA-Z0-9_]+)", css))

    # Known intentional exclusions
    EXCLUDED = {
        "greek", "hebrew",   # may be targeted via lang= attr selectors
        "fn-link",           # covered by endnote structure rules
        "cover",             # single-use, styled inline or by reader default
        "list-item",         # intentional pass-through in some volumes
        "title-line",        # handled as child selector in .title-page rules
        "contents-section-title",  # volume-specific, checked separately
    }

    undefined = used_classes - defined_in_css - EXCLUDED
    assert not undefined, (
        f"Volume {volume}: CSS classes used in XHTML but not defined in main.css:\n"
        + "\n".join(f"  .{c}" for c in sorted(undefined))
    )


# ===========================================================================
# OPF / spine consistency
# ===========================================================================

@pytest.mark.parametrize("volume", VOLUMES)
def test_all_spine_items_appear_in_nav(volume: int):
    """
    Every readable document in the OPF spine should have a corresponding
    entry in the nav TOC (or be a known non-navigable item like the cover page,
    endnotes, or the nav document itself).

    Non-navigable exceptions:
      - title_*.xhtml (title pages)
      - endnotes.xhtml
      - nav.xhtml itself
      - cover*.xhtml
      - contents_*.xhtml (front-matter TOC pages are usually in the TOC)
    """
    files = _load_epub(volume)
    opf = next((v for k, v in files.items() if k.endswith(".opf")), "")
    nav_html = next((v for k, v in files.items() if "nav.xhtml" in k), "")
    if not opf or not nav_html:
        pytest.skip(f"Volume {volume}: OPF or nav.xhtml not found")

    # Collect spine idrefs → hrefs from OPF.
    # OPF attribute order varies (href may precede or follow id), so parse
    # each <item> element by extracting both attributes independently.
    manifest_href: dict[str, str] = {}
    for item_attrs in re.findall(r'<item\b([^>]+)/>', opf):
        id_m = re.search(r'\bid="([^"]+)"', item_attrs)
        href_m = re.search(r'\bhref="([^"]+)"', item_attrs)
        if id_m and href_m:
            manifest_href[id_m.group(1)] = href_m.group(1)

    spine_hrefs = [
        manifest_href.get(m.group(1), "")
        for m in re.finditer(r'<itemref\b[^>]*\bidref="([^"]+)"', opf)
        if manifest_href.get(m.group(1))  # skip idrefs with no manifest entry
    ]

    # Collect nav hrefs
    nav_hrefs: set[str] = set(re.findall(r'href="([^"#]+\.xhtml)"', nav_html))

    # These file types are legitimately in the spine but not in the reading-
    # order nav TOC (they are navigable by swiping or via landmarks instead).
    NON_NAVIGABLE_RE = re.compile(
        r"^(?:title_|contents_|endnotes|nav|cover|frontispiece)", re.I
    )

    missing: list[str] = []
    for href in spine_hrefs:
        basename = href.rsplit("/", 1)[-1]
        if NON_NAVIGABLE_RE.match(basename):
            continue
        if basename not in {h.rsplit("/", 1)[-1] for h in nav_hrefs}:
            missing.append(basename)

    assert not missing, (
        f"Volume {volume}: spine items not present in nav TOC:\n"
        + "\n".join(f"  {m}" for m in missing[:20])
    )
