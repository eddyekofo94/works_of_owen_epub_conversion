#!/usr/bin/env python3
"""
CCEL enrichment module — LEGACY, NOT ACTIVE.

Both v5 and v10 were migrated to ages_pdf in May 2026 when clean AGES PDFs
became available.  This module is no longer wired into any convert.py.
The legacy CCEL XML files are archived at:
  special_sources/legacy/owen-v5-justification-ccel-legacy.zip
  special_sources/legacy/owen-v10-deathofdeath-ccel-legacy.zip

Original purpose: the intermediate JSON for ccel_xml volumes was derived from
the authoritative CCEL ThML XML in special_sources/.  An earlier extraction
pass dropped every
editorial <note place="foot"> footnote and broke some source paragraphs at
scripture-reference points.  This module repairs both *from the XML itself*
(the source of record), without re-running the lossy pipeline:

  1. Footnotes — parse all <note place="foot" n="N"> elements, restore their
     full text into the JSON ``footnotes`` map, and re-anchor a ``[fN]`` marker
     at the exact position the note occupies in the source paragraph.  Any
     stray/misplaced ``[fN]`` markers already in the body are stripped first so
     only correctly-anchored markers survive.

  2. Paragraph splits — using the XML <p> boundaries as ground truth, merge
     adjacent JSON paragraphs that were a single paragraph in the source.

All matching is done on an ASCII-folded projection of the text (letters/digits
lower-cased, punctuation and Greek/Hebrew dropped, whitespace collapsed) so it
is robust to the Greek OCR variants and punctuation differences between the two
derivations of the same source.
"""

from __future__ import annotations

import re
from pathlib import Path

# div1 ids, in document order, that map 1:1 onto the volume's leading chapters.
# v10: div xxv onward (Scripture index etc.) is excluded.
# v5 was removed from this map when it migrated to ages_pdf (May 2026).
_CCEL_CHAPTER_DIVS = {}


def _localname(el) -> str:
    from lxml import etree
    return etree.QName(el).localname if isinstance(el.tag, str) else ''


def _serialize(el, notes_out: list) -> str:
    """Flatten an element to plain text, replacing foot <note>s with ``[fN]``
    and recording (n, note_text, preceding_text) in ``notes_out``."""
    parts: list[str] = []
    if el.text:
        parts.append(el.text)
    for child in el:
        ln = _localname(child)
        if ln == 'note' and child.get('place') == 'foot':
            n = child.get('n')
            note_text = _serialize(child, [])  # notes never nest foot-notes
            preceding = ''.join(parts)
            notes_out.append((n, note_text.strip(), preceding))
            parts.append(f' [f{n}]')
        elif ln in ('pb', 'br'):
            parts.append(' ')
        else:
            parts.append(_serialize(child, notes_out))
        if child.tail:
            parts.append(child.tail)
    return ''.join(parts)


def _collect_body_paragraphs(div, notes_out: list) -> list[str]:
    """Return the serialized text of every <p class="Body"> under ``div`` in
    document order, accumulating footnotes into ``notes_out``."""
    paras: list[str] = []

    def walk(el):
        for child in el:
            ln = _localname(child)
            if ln == 'note':
                continue  # handled inline by _serialize of the containing block
            if ln == 'p' and child.get('class') == 'Body':
                txt = _serialize(child, notes_out)
                txt = re.sub(r'\s+', ' ', txt).strip()
                if txt:
                    paras.append(txt)
                # do NOT descend — inline notes already handled
            else:
                walk(child)

    walk(div)
    return paras


def _ascii_fold(text: str):
    """Project text to lowercase ASCII letters/digits + single spaces, and
    return (folded_string, index_map) where index_map[i] is the original index
    of folded_string[i]."""
    out = []
    idx = []
    prev_space = True
    for i, ch in enumerate(text):
        if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ('0' <= ch <= '9'):
            out.append(ch.lower())
            idx.append(i)
            prev_space = False
        elif ch.isspace():
            if not prev_space:
                out.append(' ')
                idx.append(i)
                prev_space = True
    s = ''.join(out)
    if s.endswith(' '):
        s = s[:-1]
        idx = idx[:-1]
    return s, idx


def _fold_plain(text: str) -> str:
    s, _ = _ascii_fold(text)
    return s


def parse_ccel_xml(xml_path: str, chapter_div_ids: list[str]):
    """Parse the CCEL XML.  Returns (chapter_paras, chapter_notes) where each is
    a list (one entry per chapter div, in order); chapter_paras[i] is the list
    of source Body paragraphs, chapter_notes[i] is a list of (n, text, preceding)
    for footnotes anchored in that chapter."""
    from lxml import etree
    tree = etree.parse(xml_path)
    root = tree.getroot()

    divs_by_id = {}
    for el in root.iter():
        if _localname(el) == 'div1' and el.get('id') in set(chapter_div_ids):
            divs_by_id[el.get('id')] = el

    chapter_paras = []
    chapter_notes = []
    for div_id in chapter_div_ids:
        div = divs_by_id.get(div_id)
        if div is None:
            chapter_paras.append([])
            chapter_notes.append([])
            continue
        notes: list = []
        paras = _collect_body_paragraphs(div, notes)
        chapter_paras.append(paras)
        chapter_notes.append(notes)
    return chapter_paras, chapter_notes


# ── footnote anchoring ──────────────────────────────────────────────────────

_FN_MARKER_RE = re.compile(r'\s*\[f\d+\]')


def _anchor_footnotes(raw_text: str, notes: list) -> tuple[str, list[str]]:
    """Strip any existing [fN] markers from ``raw_text`` and re-insert one marker
    per note at the position implied by its preceding source text.  Returns
    (new_raw_text, unanchored) where ``unanchored`` lists note numbers whose
    anchor could not be located."""
    text = _FN_MARKER_RE.sub('', raw_text)
    # Build folded projection once; recompute after each insertion (cheap: ≤a few).
    inserts: list[tuple[int, str]] = []  # (orig_index, marker)
    unanchored: list[str] = []
    folded, idx_map = _ascii_fold(text)
    used_ends: list[int] = []
    for n, _note_text, preceding in notes:
        # markers already inserted in the source-serialization leak into the
        # preceding text (e.g. " [f1]"); drop them before folding.
        preceding = _FN_MARKER_RE.sub('', preceding)
        full = _fold_plain(preceding)
        words = full.split()
        if not words:
            unanchored.append(n)
            continue
        # Build candidate anchors as word sequences.  Roman→Arabic conversion and
        # dropped page refs in the JSON derivation mean trailing tokens may not
        # match, so also try trimming 1–2 words off the end.  Prefer the longest
        # (most precise) candidate that resolves to an as-yet-unused position.
        candidates: list[str] = []
        for back in range(0, 3):
            tail = words[:len(words) - back] if back else words
            if len(tail) < 2:
                continue
            for w in range(min(8, len(tail)), 1, -1):
                candidates.append(' '.join(tail[-w:]))
        # de-dup preserving order, longest first
        seen = set()
        ordered = []
        for c in sorted(candidates, key=len, reverse=True):
            if c not in seen:
                seen.add(c)
                ordered.append(c)
        pos = -1
        for anchor in ordered:
            if len(anchor) < 5:
                continue
            search_from = 0
            while True:
                p = folded.find(anchor, search_from)
                if p == -1:
                    break
                end = p + len(anchor)
                if all(abs(end - u) > 1 for u in used_ends):
                    pos = end
                    break
                search_from = p + 1
            if pos != -1:
                break
        if pos == -1:
            unanchored.append(n)
            continue
        used_ends.append(pos)
        orig_index = idx_map[pos - 1] + 1 if pos - 1 < len(idx_map) else len(text)
        inserts.append((orig_index, f' [f{n}]'))
    # apply inserts right-to-left so indices stay valid
    for orig_index, marker in sorted(inserts, key=lambda t: -t[0]):
        text = text[:orig_index] + marker + text[orig_index:]
    text = re.sub(r' +\[f', ' [f', text)
    return text, unanchored


# ── paragraph split healing ─────────────────────────────────────────────────

_MARKER_BLOCK_RE = re.compile(r'^\s*\[\[')


def _heal_splits(raw_text: str, source_paras: list[str]) -> tuple[str, int]:
    """Merge adjacent body paragraphs that were one paragraph in the source.
    Returns (new_raw_text, merges_done)."""
    if not source_paras:
        return raw_text, 0
    folded_src = [_fold_plain(p) for p in source_paras]
    blocks = raw_text.split('\n\n')
    merges = 0
    i = 0
    out: list[str] = []
    while i < len(blocks):
        cur = blocks[i]
        # never merge structural-marker blocks ([[CHAPTER]], [[BLOCKQUOTE]], …)
        if _MARKER_BLOCK_RE.match(cur):
            out.append(cur)
            i += 1
            continue
        # greedily absorb following plain blocks if cur+next is contiguous in a
        # single source paragraph
        while i + 1 < len(blocks) and not _MARKER_BLOCK_RE.match(blocks[i + 1]):
            cand = (cur + ' ' + blocks[i + 1]).strip()
            f_cand = _fold_plain(cand)
            if len(f_cand) < 12:
                break
            if any(f_cand in fs for fs in folded_src):
                cur = cand
                merges += 1
                i += 1
            else:
                break
        out.append(cur)
        i += 1
    return '\n\n'.join(out), merges


# ── driver ──────────────────────────────────────────────────────────────────

def enrich_ccel_volume(intermediate: dict, vol_num: int, xml_path: str,
                       verbose: bool = True) -> dict:
    """Enrich a ccel_xml volume's intermediate dict in place and return it."""
    div_ids = _CCEL_CHAPTER_DIVS.get(vol_num)
    if not div_ids:
        raise ValueError(f'No CCEL chapter-div map for volume {vol_num}')
    chapter_paras, chapter_notes = parse_ccel_xml(xml_path, div_ids)

    footnotes: dict = {}
    total_anchored = 0
    total_unanchored: list[str] = []
    total_merges = 0

    chapters = intermediate['chapters']
    n_map = min(len(div_ids), len(chapters))
    for ci in range(n_map):
        ch = chapters[ci]
        notes = chapter_notes[ci]
        paras = chapter_paras[ci]
        raw = ch.get('raw_text', '') or ''

        # 1. footnotes
        for n, note_text, _ in notes:
            footnotes[str(n)] = {'text': note_text, 'source': 'thml'}
        if notes:
            raw, unanchored = _anchor_footnotes(raw, notes)
            total_anchored += len(notes) - len(unanchored)
            total_unanchored += unanchored
        else:
            # strip any stray markers in chapters that have no real notes
            raw = _FN_MARKER_RE.sub('', raw)

        # 2. split healing
        raw, merges = _heal_splits(raw, paras)
        total_merges += merges

        ch['raw_text'] = raw

    intermediate['footnotes'] = footnotes

    if verbose:
        print(f'[ccel_enrich] v{vol_num}: {len(footnotes)} footnotes restored, '
              f'{total_anchored} markers anchored, '
              f'{len(total_unanchored)} unanchored {total_unanchored or ""}, '
              f'{total_merges} paragraph merges')
    return intermediate


def enrich_ccel_post_extract(intermediate: dict, config: dict = None,
                             vol_num: int = None, **kwargs) -> dict:
    """post_extract_hook entrypoint (see shared.run_volume_cli)."""
    config = config or {}
    vol_num = vol_num or intermediate.get('volume')
    ccel_file = config.get('ccel_file')
    if not ccel_file:
        return intermediate
    root = Path(__file__).resolve().parent
    xml_path = root / ccel_file
    if not xml_path.exists():
        print(f'[ccel_enrich] XML not found: {xml_path}; skipping')
        return intermediate
    return enrich_ccel_volume(intermediate, vol_num, str(xml_path))
