Created At: 2026-05-29T22:17:07Z
Completed At: 2026-05-29T22:17:07Z
File Path: `file:///Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/render.py`
Total Lines: 5183
Total Bytes: 232377
Showing lines 2780 to 2820
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
2780: def _attach_em_dash_flat_list(html: str) -> str:
2781:     """Absorb short list prefixes into a preceding paragraph ending in em-dash.
2782: 
2783:     Owen frequently introduces a flat enumeration with a sentence ending in "—",
2784:     e.g. "I shall briefly observe four things therein: —", followed by list items
2785:     that are labels or short phrases.  These must render inline, not as a block.
2786: 
2787:     The function uses multi-signal detection to distinguish flat enumerations from
2788:     proper scholastic-anchor block lists (which also follow "—" paragraphs).  It
2789:     intentionally works on the valid prefix of a run, not the whole run, because
2790:     Owen often gives a flat summary list and then immediately starts expanding the
2791:     first item with the same marker family.
2792: 
2793:     HARD VETO
2794:       Any item with > _EM_DASH_FLAT_HARD_CAP (8) content words → block, full stop.
2795: 
2796:     POSITIVE SIGNALS (any one is sufficient to trigger flattening):
2797:       A. Grammar continuation  — any non-final item ends with ";" or ","
2798:       B. Grammar continuation  — any item ends with " and" or " or" (word boundary)
2799:       C. Label list            — ALL items have ≤ 3 content words
2800:       D. Short parallel run    — run has ≥ 3 items AND every item ≤ _EM_DASH_FLAT_SHORT_PHRASE (7) words
2801: 
2802:     Intentionally NOT flattened (left as block for safety):
2803:       • 2-item runs with 4-7 word items and no continuation markers
2804:       • Any run where an item exceeds the hard cap
2805: 
2806:     Called after _attach_colon_introduced_list but before _merge_short_inline_lists
2807:     so that the absorbed items are never seen by Rules A/B.
2808:     """
2809:     import re as _re
2810: 
2811:     _LIST_ITEM_RE = re.compile(
2812:         r'<p class="(list-item|roman-list-item)">(<b>[^<]{1,30}</b>\s*)?(.*?)</p>',
2813:         re.S,
2814:     )
2815: 
2816:     def _plain(frag: str) -> str:
2817:         return _re.sub(r'\s+', ' ', _re.sub(r'<[^>]+>', '', frag)).strip()
2818: 
2819:     def _wc(frag: str) -> int:
2820:         return len(_plain(frag).split())
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
