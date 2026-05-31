Created At: 2026-05-29T20:56:12Z
Completed At: 2026-05-29T20:56:12Z
File Path: `file:///Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/render.py`
Total Lines: 5158
Total Bytes: 230969
Showing lines 2770 to 2795
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
2770: # (15+ words) is preserved.
2771: _EM_DASH_FLAT_HARD_CAP = 12
2772: 
2773: #: Upper word limit used in the "3+ short parallel phrases" signal (D).
2774: _EM_DASH_FLAT_SHORT_PHRASE = 9  # Raised from 7→9 (Bug #6): Signal D fires for 3+ items all ≤9 words
2775: 
2776: 
2777: def _attach_em_dash_flat_list(html: str) -> str:
2778:     """Absorb short list prefixes into a preceding paragraph ending in em-dash.
2779: 
2780:     Owen frequently introduces a flat enumeration with a sentence ending in "—",
2781:     e.g. "I shall briefly observe four things therein: —", followed by list items
2782:     that are labels or short phrases.  These must render inline, not as a block.
2783: 
2784:     The function uses multi-signal detection to distinguish flat enumerations from
2785:     proper scholastic-anchor block lists (which also follow "—" paragraphs).  It
2786:     intentionally works on the valid prefix of a run, not the whole run, because
2787:     Owen often gives a flat summary list and then immediately starts expanding the
2788:     first item with the same marker family.
2789: 
2790:     HARD VETO
2791:       Any item with > _EM_DASH_FLAT_HARD_CAP (8) content words → block, full stop.
2792: 
2793:     POSITIVE SIGNALS (any one is sufficient to trigger flattening):
2794:       A. Grammar continuation  — any non-final item ends with ";" or ","
2795:       B. Grammar continuation  — any item ends with " and" or " or" (word boundary)
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
