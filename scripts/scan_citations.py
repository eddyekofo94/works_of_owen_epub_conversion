#!/usr/bin/env python3
"""
scan_citations.py — Comprehensive inline citation audit tool.

Scans all volume intermediate JSON files, finds every instance of Owen's
abbreviated patristic and classical citations (lib., cap., epist., serm.,
orat., tract., homil., haer., dial., adv., etc.) and produces a
categorized report showing:

  - Total citations found
  - Already-resolved citations (matching a BODY_TRANSLATIONS entry nearby)
  - Unresolved citations, grouped by volume and author
  - Self-reference citations (Owen citing his own works)
  - Statistics by abbreviation type

Usage:
    python3 scripts/scan_citations.py              # all volumes
    python3 scripts/scan_citations.py --vol 1      # volume 1 only
    python3 scripts/scan_citations.py --unresolved # only show unresolved
    python3 scripts/scan_citations.py --csv        # CSV output
"""

import argparse
import csv
import glob
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from patristic_refs import (
    PATRISTIC_CITATION_RE, SELF_REF_PATTERNS,
    _strip_tags, _find_author_in_context, _find_work_in_context,
    AUTHOR_ABBREV_MAP, build_citation_note, WORK_MAP, is_bible_citation_ref
)
from translation_db import BODY_TRANSLATIONS


def load_volume(vol_num) -> dict | None:
    from shared import get_volume_dir
    base = os.path.join(get_volume_dir(vol_num), 'intermediate')
    path = os.path.join(base, f'volume_{vol_num}.json')
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def scan_volume(vol_num: int, data: dict) -> list[dict]:
    """Return a list of citation hit records for one volume."""
    hits = []
    for ch in data.get('chapters', []):
        cid = ch.get('cid', '')
        text = ch.get('raw_text', '')
        for m in PATRISTIC_CITATION_RE.finditer(text):
            cite_str = m.group(0).strip()
            ctx_start = max(0, m.start() - 120)
            ctx_end = min(len(text), m.end() + 80)
            context_before = text[ctx_start:m.start()].replace('\n', ' ')
            context_after = text[m.end():ctx_end].replace('\n', ' ')
            full_context = text[ctx_start:ctx_end].replace('\n', ' ')

            # Combine before/after context with a separator
            combined_context = context_before + " | " + context_after

            # Check if it looks like a Bible citation matched by mistake
            if is_bible_citation_ref(cite_str, combined_context):
                continue

            # Already resolved: a BODY_TRANSLATIONS phrase overlaps this window
            already_resolved = any(
                phrase in full_context
                for phrase in BODY_TRANSLATIONS
                if len(phrase) > 8
            )
            
            # If not in BODY_TRANSLATIONS, check if the two-tier patristic fallback can resolve it
            if not already_resolved:
                if build_citation_note(cite_str, combined_context) is not None:
                    already_resolved = True

            # Self-reference: Owen citing his own work
            is_self_ref = bool(SELF_REF_PATTERNS.search(context_before))

            author_key = _find_author_in_context(combined_context)
            author_name = AUTHOR_ABBREV_MAP.get(author_key, '') if author_key else ''
            work_data = _find_work_in_context(combined_context, author_key)
            if work_data is None and author_key:
                abbrev_m = re.match(r'^\(?\s*([a-z]+)\.', cite_str.lower())
                if abbrev_m:
                    cite_abbrev = abbrev_m.group(1).rstrip('o')
                    work_data = WORK_MAP.get((author_key, cite_abbrev))

            work_title = work_data.get('full_title', '') if work_data else ''

            hits.append({
                'vol': vol_num,
                'cid': cid,
                'cite': cite_str,
                'abbrev': m.group('abbrev').lower(),
                'context_before': context_before[-100:].strip(),
                'context_after': context_after[:60].strip(),
                'already_resolved': already_resolved,
                'is_self_ref': is_self_ref,
                'author_key': author_key or '',
                'author_name': author_name,
                'work_title': work_title,
            })
    return hits


def print_report(all_hits: list[dict], unresolved_only: bool = False) -> None:
    from collections import Counter

    total = len(all_hits)
    resolved = [h for h in all_hits if h['already_resolved']]
    self_refs = [h for h in all_hits if h['is_self_ref'] and not h['already_resolved']]
    unresolved = [h for h in all_hits
                  if not h['already_resolved'] and not h['is_self_ref']]
    with_author = [h for h in unresolved if h['author_key']]
    without_author = [h for h in unresolved if not h['author_key']]

    print("=" * 70)
    print("COMPREHENSIVE INLINE CITATION AUDIT — JOHN OWEN WORKS")
    print("=" * 70)
    print(f"  Total citation instances:     {total}")
    print(f"  Already resolved:             {len(resolved)}  "
          f"({100 * len(resolved) // max(total, 1)}%)")
    print(f"  Self-references (Owen):       {len(self_refs)}")
    print(f"  Unresolved — author found:    {len(with_author)}")
    print(f"  Unresolved — no author:       {len(without_author)}")
    print()

    abbrev_counts = Counter(h['abbrev'] for h in all_hits)
    print("By abbreviation type:")
    for abbrev, count in abbrev_counts.most_common():
        print(f"    {abbrev}.:  {count}")
    print()

    vol_counts = Counter(h['vol'] for h in unresolved)
    print("Unresolved by volume:")
    for vol, count in sorted(vol_counts.items()):
        print(f"    v{vol}:  {count}")
    print()

    if unresolved_only:
        hits_to_show = unresolved
    else:
        hits_to_show = all_hits

    print("-" * 70)
    print("CITATION DETAILS:")
    print("-" * 70)
    current_vol = None
    for h in hits_to_show:
        if h['vol'] != current_vol:
            current_vol = h['vol']
            print(f"\n{'━' * 60}")
            print(f"  VOLUME {h['vol']}")
            print(f"{'━' * 60}")
        status = (
            "[RESOLVED]   " if h['already_resolved']
            else "[SELF-REF]   " if h['is_self_ref']
            else f"[{h['author_name'] or 'UNKNOWN'}]"
        )
        print(f"\n  {h['cid']}  {status}")
        print(f"    CITE:  {h['cite']!r}")
        if h['work_title']:
            print(f"    WORK:  {h['work_title']}")
        ctx = h['context_before'][-80:] + '«' + h['cite'] + '»' + h['context_after'][:40]
        print(f"    CTX:   ...{ctx.strip()}...")


def write_csv(all_hits: list[dict], path: str) -> None:
    fieldnames = ['vol', 'cid', 'cite', 'abbrev', 'already_resolved',
                  'is_self_ref', 'author_name', 'work_title', 'context_before']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_hits)
    print(f"CSV written to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan Owen citations")
    parser.add_argument('--vol', type=int, help="Scan specific volume only")
    parser.add_argument('--unresolved', action='store_true',
                        help="Only show unresolved citations")
    parser.add_argument('--csv', metavar='FILE', help="Write results to CSV file")
    args = parser.parse_args()

    all_hits = []
    if args.vol:
        volumes = [args.vol]
    else:
        base = os.path.join(_ROOT, 'volumes')
        vol_dirs = sorted(glob.glob(os.path.join(base, 'v*')))
        volumes = []
        for d in vol_dirs:
            name = os.path.basename(d)
            if name[1:].isdigit():
                volumes.append(int(name[1:]))
        volumes.sort()

    for vol_num in volumes:
        data = load_volume(vol_num)
        if data is None:
            continue
        hits = scan_volume(vol_num, data)
        all_hits.extend(hits)
        print(f"v{vol_num}: {len(hits)} citations", flush=True)

    print()
    if args.csv:
        write_csv(all_hits, args.csv)
    else:
        print_report(all_hits, unresolved_only=args.unresolved)


if __name__ == '__main__':
    main()
