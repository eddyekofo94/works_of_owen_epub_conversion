Created At: 2026-05-29T22:17:36Z
Completed At: 2026-05-29T22:17:36Z
File Path: `file:///Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/render.py`
Total Lines: 5185
Total Bytes: 232532
Showing lines 2780 to 2830
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
2802:     Intentionally NOT    import re as _re
2803: 
2804:     # Compiled patterns for syllabus introductions (updated to match all trailing punctuation)
2805:     _EXPLICIT_COUNT_RE = _re.compile(
2806:         r'\b(?:I\s+understand\s+)?(?:two|three|four|five|six|seven|'
2807:         r'eight|nine|ten|twofold|threefold|fourfold|\d+)\b.{0,120}'
2808:         r'\b(?:things?|ways?|heads?|accounts?|regards?|parts?|'
2809:         r'sorts?|considerations?|observations?|particulars?|'
2810:         r'respects?|instances?)\b.{0,60}[—\-:,;.]\s*$',
2811:         _re.I,
2812:     )
2813:     _FORMULA_TAIL_RE = _re.compile(
2814:         r'\b(?:these?\s+following|as\s+follows?|following\s+particulars?|'
2815:         r'(?:may|to)\s+be\s+(?:observed|noted|considered|mentioned)|'
2816:         r'I\s+shall\s+(?:observe|note|propose|mention|consider)|'
2817:         r'in\s+particular|are\s+these)\b.{0,60}[—\-:,;.]\s*$',
2818:         _re.I,
2819:     )
2820: 
2821:     _LIST_ITEM_RE = re.compile(
2822:         r'<p class="(list-item|roman-list-item)">(<b>[^<]{1,30}</b>\s*)?(.*?)</p>',
2823:         re.S,
2824:     )
2825: 
2826:     def _plain(frag: str) -> str:
2827:         return _re.sub(r'\s+', ' ', _re.sub(r'<[^>]+>', '', frag)).strip()
2828: 
2829:     def _wc(frag: str) -> int:
2830:         return len(_plain(frag).split())
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
