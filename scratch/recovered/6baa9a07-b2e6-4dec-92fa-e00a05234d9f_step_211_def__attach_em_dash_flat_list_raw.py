Created At: 2026-05-29T20:55:06Z
Completed At: 2026-05-29T20:55:06Z
File Path: `file:///Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/render.py`
Total Lines: 5158
Total Bytes: 230969
Showing lines 2770 to 3185
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
2796:       C. Label list            — ALL items have ≤ 3 content words
2797:       D. Short parallel
<truncated 18240 bytes>
 i += 1
3153:             continue
3154: 
3155:         # ── ABSORB: strip </p> from preceding paragraph, append items inline ─
3156:         inline_parts = []
3157:         for mk, ct in item_pairs[:flat_prefix_len]:
3158:             inline_parts.append(((mk or '') + ct).strip())
3159:         inline_text = ' '.join(inline_parts)
3160: 
3161:         # Strip the closing </p> from the preceding paragraph and append inline.
3162:         # Also mark the anchor paragraph so CSS and future passes can identify it
3163:         # as a flat-syllabus host (bold markers are now inline text).
3164:         new_preceding = _re.sub(r'</p>\s*$', ' ' + inline_text + '</p>', preceding, count=1)
3165:         # Add syllabus-anchor class to the opening tag
3166:         if _re.match(r'<p\s+class="([^"]*)"', new_preceding):
3167:             new_preceding = _re.sub(
3168:                 r'<p\s+class="([^"]*)"',
3169:                 lambda m: f'<p class="{m.group(1)} syllabus-anchor"',
3170:                 new_preceding, count=1,
3171:             )
3172:         elif _re.match(r'<p>', new_preceding):
3173:             new_preceding = _re.sub(r'^<p>', '<p class="syllabus-anchor">', new_preceding, count=1)
3174:         out[prev_idx] = new_preceding
3175: 
3176:         # Re-emit any non-flat expansion items as list paragraphs for downstream
3177:         # list processing.  This is what keeps the real scholastic expansion
3178:         # blocky after the introductory flat list is absorbed.
3179:         remaining = run[flat_prefix_len:]
3180:         if remaining:
3181:             out.append(_attach_em_dash_flat_list('\n'.join(remaining)))
3182: 
3183:         # Remove any whitespace tokens between prev_idx and the run we absorbed
3184:         # (they were already included as whitespace parts before the list items).
3185:         i = j
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
