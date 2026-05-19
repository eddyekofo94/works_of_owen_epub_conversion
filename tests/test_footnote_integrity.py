r"""test_footnote_integrity.py — Footnote round-trip completeness.

Footnotes are the scholarly backbone of Owen's work.  A missing or broken
footnote may silently drop a patristic citation or a scripture reference
that Owen explicitly placed there.

These tests verify the complete footnote pipeline:
  PDF → intermediate JSON ([f\d+] markers) → EPUB endnotes.xhtml (anchors)

All tests are EPUB-scanning tests: they require a built EPUB on disk and
use the same skip/parametrize convention as the other test files.

    OWEN_REGRESSION_VOLUMES=1,2 pytest tests/test_footnote_integrity.py
"""

from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.parent


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


def _intermediate_path(volume: int) -> Path:
    return BASE_DIR / "volumes" / f"v{volume}" / "intermediate" / f"volume_{volume}.json"


def _load_epub_files(volume: int) -> dict[str, str]:
    """Return {name: decoded_text} for all XHTML files in the EPUB."""
    ep = _epub_path(volume)
    if not ep.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {ep}")
    files: dict[str, str] = {}
    with zipfile.ZipFile(ep) as zf:
        for name in zf.namelist():
            if name.endswith(".xhtml"):
                files[name] = zf.read(name).decode("utf-8", errors="replace")
    return files


VOLUMES = _requested_volumes()

# Matches endnote aside elements: <aside ... id="fnN">...</aside>
ENDNOTE_ASIDE_RE = re.compile(
    r'<aside\b[^>]+\bid="(?P<id>fn\d+)"[^>]*>.*?</aside>',
    re.S,
)
# Matches noteref links in chapter files: href="endnotes.xhtml#fnN"
NOTEREF_RE = re.compile(
    r'<a\b[^>]+class="noteref"[^>]*\bhref="(?P<href>[^"]+)"[^>]*>',
)
# Fragment anchor in noteref href — e.g. endnotes.xhtml#fn5  → fn5
NOTEREF_FRAG_RE = re.compile(r"#(fn\d+)$")


# ===========================================================================
# Tests
# ===========================================================================

@pytest.mark.parametrize("volume", VOLUMES)
def test_endnotes_file_exists_in_epub(volume: int):
    """Every EPUB must have an endnotes.xhtml file (or none at all if the
    volume genuinely has no footnotes — checked in a separate test)."""
    ep = _epub_path(volume)
    if not ep.exists():
        pytest.skip(f"EPUB for volume {volume} not found")
    with zipfile.ZipFile(ep) as zf:
        names = set(zf.namelist())
    # endnotes.xhtml may be at EPUB/endnotes.xhtml
    has_endnotes = any("endnotes.xhtml" in n for n in names)
    # If there are noterefs in the chapter files, the endnotes file MUST exist
    files = _load_epub_files(volume)
    chapter_html = "\n".join(
        v for k, v in files.items() if k.startswith("EPUB/ch")
    )
    has_noterefs = bool(NOTEREF_RE.search(chapter_html))

    if has_noterefs:
        assert has_endnotes, (
            f"Volume {volume}: chapter files contain noteref links but "
            "endnotes.xhtml is missing from the EPUB."
        )


@pytest.mark.parametrize("volume", VOLUMES)
def test_every_noteref_href_resolves_to_an_endnote_anchor(volume: int):
    """
    Every <a class="noteref" href="endnotes.xhtml#fnN"> in a chapter file
    must have a matching <aside id="fnN"> in endnotes.xhtml.

    A missing anchor means the reader clicks the footnote number and lands
    on a broken link — or Apple Books silently drops the link.
    """
    files = _load_epub_files(volume)

    # Collect all defined endnote IDs
    endnotes_html = next(
        (v for k, v in files.items() if "endnotes.xhtml" in k), ""
    )
    defined_ids: set[str] = set(ENDNOTE_ASIDE_RE.findall(endnotes_html))
    # ENDNOTE_ASIDE_RE uses a named group — re.findall returns the group string
    defined_ids = {m.group("id") for m in ENDNOTE_ASIDE_RE.finditer(endnotes_html)}

    if not defined_ids and not any(
        NOTEREF_RE.search(v) for k, v in files.items() if k.startswith("EPUB/ch")
    ):
        pytest.skip(f"Volume {volume} has no footnotes — nothing to check.")

    # Collect all noteref targets from chapter files
    broken: list[str] = []
    for name, html in sorted(files.items()):
        if not name.startswith("EPUB/ch"):
            continue
        for m in NOTEREF_RE.finditer(html):
            href = m.group("href")
            frag_m = NOTEREF_FRAG_RE.search(href)
            if not frag_m:
                broken.append(f"{name}: unexpected noteref href format {href!r}")
                continue
            fn_id = frag_m.group(1)
            if fn_id not in defined_ids:
                broken.append(f"{name}: noteref #{fn_id} has no matching endnote aside")

    assert not broken, (
        f"Volume {volume}: {len(broken)} broken noteref link(s):\n"
        + "\n".join(f"  {b}" for b in broken[:20])
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_every_endnote_has_a_back_link_noteref(volume: int):
    """
    Every <aside id="fnN"> in endnotes.xhtml must be referenced by at least
    one noteref in a chapter file.  An orphan endnote is unreachable content.
    """
    files = _load_epub_files(volume)

    endnotes_html = next(
        (v for k, v in files.items() if "endnotes.xhtml" in k), ""
    )
    if not endnotes_html:
        pytest.skip(f"Volume {volume} has no endnotes.xhtml")

    defined_ids = {m.group("id") for m in ENDNOTE_ASIDE_RE.finditer(endnotes_html)}

    # Collect all referenced IDs from chapter files
    referenced_ids: set[str] = set()
    for name, html in files.items():
        if not name.startswith("EPUB/ch"):
            continue
        for m in NOTEREF_RE.finditer(html):
            frag_m = NOTEREF_FRAG_RE.search(m.group("href"))
            if frag_m:
                referenced_ids.add(frag_m.group(1))

    orphans = sorted(defined_ids - referenced_ids)
    assert not orphans, (
        f"Volume {volume}: {len(orphans)} endnote(s) have no noteref "
        f"in any chapter file: {orphans[:20]}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_endnote_ids_are_sequential_and_start_at_one(volume: int):
    """
    Endnote IDs must form a gapless sequence fn1, fn2, fn3, …
    A gap means a footnote was silently dropped during extraction or rendering.
    """
    files = _load_epub_files(volume)
    endnotes_html = next(
        (v for k, v in files.items() if "endnotes.xhtml" in k), ""
    )
    if not endnotes_html:
        pytest.skip(f"Volume {volume} has no endnotes.xhtml")

    numbers = sorted(
        int(m.group("id")[2:])   # strip "fn" prefix
        for m in ENDNOTE_ASIDE_RE.finditer(endnotes_html)
    )
    if not numbers:
        pytest.skip(f"Volume {volume} endnotes.xhtml has no aside elements")

    expected = list(range(1, numbers[-1] + 1))
    missing = sorted(set(expected) - set(numbers))

    assert not missing, (
        f"Volume {volume}: footnote sequence has gaps — missing fn numbers: "
        f"{missing[:20]}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_endnote_text_is_free_of_extraction_artifacts(volume: int):
    """
    Endnote text must not contain pipeline-internal markers or AGES boilerplate.
    A footnote with '[f12]' literally in it, or with 'Books For The Ages',
    means the extraction stage garbled the note content.
    """
    files = _load_epub_files(volume)
    endnotes_html = next(
        (v for k, v in files.items() if "endnotes.xhtml" in k), ""
    )
    if not endnotes_html:
        pytest.skip(f"Volume {volume} has no endnotes.xhtml")

    # Strip tags to get plain text of all endnotes
    text = re.sub(r"<[^>]+>", " ", endnotes_html)
    text = re.sub(r"\s+", " ", text)

    failures: list[str] = []

    # Literal footnote markers
    literal_fn = re.findall(r"\[f\d+\]", text)
    if literal_fn:
        failures.append(f"Literal [fN] markers found: {literal_fn[:5]}")

    # Pipeline tokens
    for tok in ["[[CHAPTER]]", "[[BLOCKQUOTE]]", "[[PART]]"]:
        if tok in text:
            failures.append(f"Pipeline token {tok!r} found in endnotes")

    # AGES boilerplate
    for phrase in ["Books For The Ages", "AGES Software", "JOHN OWEN COLLECTION"]:
        if phrase.lower() in text.lower():
            failures.append(f"AGES boilerplate {phrase!r} found in endnotes")

    assert not failures, (
        f"Volume {volume} endnote artifacts:\n"
        + "\n".join(f"  {f}" for f in failures)
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_noteref_count_matches_endnote_count(volume: int):
    """
    The number of noteref links across all chapter files must equal the number
    of endnote asides.  A mismatch means noterefs were injected or endnotes
    were duplicated during rendering.
    """
    files = _load_epub_files(volume)
    endnotes_html = next(
        (v for k, v in files.items() if "endnotes.xhtml" in k), ""
    )
    if not endnotes_html:
        pytest.skip(f"Volume {volume} has no endnotes.xhtml")

    endnote_count = len(list(ENDNOTE_ASIDE_RE.finditer(endnotes_html)))
    noteref_count = sum(
        len(NOTEREF_RE.findall(html))
        for name, html in files.items()
        if name.startswith("EPUB/ch")
    )

    assert endnote_count == noteref_count, (
        f"Volume {volume}: {noteref_count} noteref link(s) in chapter files "
        f"but {endnote_count} endnote aside(s) in endnotes.xhtml. "
        f"Delta: {abs(endnote_count - noteref_count)}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_intermediate_footnote_count_matches_epub_endnote_count(volume: int):
    """
    The footnote map in the intermediate JSON must produce the same number of
    endnotes in the EPUB.  A discrepancy means the render stage silently
    dropped or duplicated footnotes.

    Requires both the intermediate JSON and a built EPUB.
    """
    inter_path = _intermediate_path(volume)
    if not inter_path.exists():
        pytest.skip(f"Intermediate JSON for volume {volume} not found at {inter_path}")

    data = json.loads(inter_path.read_text(encoding="utf-8"))
    # Collect all footnote keys across all chapters
    json_fn_numbers: set[int] = set()
    for chapter in data.get("chapters", []):
        for key in chapter.get("footnotes", {}).keys():
            try:
                json_fn_numbers.add(int(key))
            except (ValueError, TypeError):
                pass

    if not json_fn_numbers:
        pytest.skip(f"Volume {volume} intermediate JSON has no footnotes")

    files = _load_epub_files(volume)
    endnotes_html = next(
        (v for k, v in files.items() if "endnotes.xhtml" in k), ""
    )
    epub_fn_numbers = {
        int(m.group("id")[2:])
        for m in ENDNOTE_ASIDE_RE.finditer(endnotes_html)
    }

    missing_in_epub = sorted(json_fn_numbers - epub_fn_numbers)
    extra_in_epub = sorted(epub_fn_numbers - json_fn_numbers)

    errors: list[str] = []
    if missing_in_epub:
        errors.append(
            f"Footnotes in JSON but missing from EPUB: {missing_in_epub[:10]}"
        )
    if extra_in_epub:
        errors.append(
            f"Endnotes in EPUB with no JSON source: {extra_in_epub[:10]}"
        )

    assert not errors, (
        f"Volume {volume} footnote count mismatch:\n"
        + "\n".join(f"  {e}" for e in errors)
    )
