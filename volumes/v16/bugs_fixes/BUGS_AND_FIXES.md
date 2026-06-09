# Bugs and Fixes — John Owen Works (v1–v16)

## Issues Identified from Reference EPUB Comparison

| # | Issue | Location | Status |
|---|-------|----------|--------|
| 1 | Portrait image exists in `portraits/` but never wired into converter | converter.py | ✅ Fixed |
| 2 | Footnotes not extracted — fnref links not converted to noteref, no endnotes chapter | converter.py | ✅ Fixed |
| 3 | NAV structure missing `<h2>` with volume title and `role="doc-toc"` | generate_nav_xhtml() | ✅ Fixed |
| 4 | Spine order wrong — missing frontispiece between nav and chapter 1 | update_opf_for_epub3() | ✅ Fixed |
| 5 | Cover.xhtml format mismatch — CSS link vs simple `<img>` reference | fix_cover_xhtml() | ✅ Fixed |
| 6 | Missing `id="creator"` in OPF dc:creator | update_opf_for_epub3() | ✅ Fixed |
| 7 | Portrait always same for all volumes | find_portrait() | ✅ Fixed |
| 8 | Portrait not in OPF manifest (EPUB3 validation failure) | process_owen_volume() | ✅ Fixed |
| 9 | Title page doesn't match reference EPUB design | process_owen_volume() | ✅ Fixed |
| 10 | NAV titles not split (e.g., "TREATISE CHAPTER 1" on one line) | _split_nav_title() | ✅ Fixed |
| 11 | CSS not aligned with reference EPUB (title page, footnotes, font-smoothing) | shared.py | ✅ Fixed |
| 12 | `.noteref` color mismatch (`#0066cc` vs `#0000EE`) | shared.py | ✅ Fixed |
| 13 | Duplicate `.footnote` CSS rules | shared.py | ✅ Fixed |
| 14 | Structural Misalignment (Summary Head Fragmentation) | ThML Source | Obsolete (using ages_pdf) |
| 15 | Reference year 136. split into outline list item and separated from quote | post_extract_hook | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 16 | Flat list layout bug (first list item split, anchor sentence stuck in previous paragraph) | regex_replacements / post_extract_hook | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 17 | Hybrid flat/block list split (list item 4 swallowing subsequent prose and becoming block) | owen_lists.py / text_cleaner.py | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 18 | List item 5 split and rendered as block instead of following previous flattened run | owen_lists.py | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 19 | Pastors list items (4.) and (5.) rendered as flat instead of block in Chapter 5 | post_extract_hook | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 20 | Sequential continuation absorption skips subsequent nested lists in consecutive list runs | owen_lists.py | ⌛ IMPLEMENTED (AWAITING VALIDATION) |



---

## Issue Details

### 1. Portrait Not Wired (Fixed)
**Fix:** Added `find_portrait(workspace, vol_num)` and `generate_frontispiece_xhtml()`.

### 2. Footnotes Not Extracted (Fixed)
**Fix:** Added `_build_endnotes_chapter()` and fnref→noteref conversion in `_elem_to_html()`.

### 3–6. NAV, Spine, Cover, id="creator" (Fixed)
See previous sessions.

### 7. Portrait Always Same for All Volumes (Fixed)
**Problem:** `find_portrait()` always returned `protrait1.jpeg` — all 16 Owen volumes + 7 Hebrews volumes got the same portrait.
**Fix:** Changed `find_portrait()` to accept `vol_num` parameter and use `hashlib.md5(f'owen-v{vol_num}')` for deterministic but varied selection from all 3 portraits in `portraits/`.

### 8. Portrait Not in OPF Manifest (Fixed)
**Problem:** Portrait image physically copied into EPUB during post-processing but never declared in OPF manifest. EPUB validators flag this.
**Fix:** Added portrait as `epub.EpubItem(uid='portrait-img', ...)` with proper MIME type before writing EPUB.

### 9. Title Page Doesn't Match Reference (Fixed)
**Problem:** Title page was plain — single h1, simple subtitle, no ornament, no decorative rule, no editor line.
**Fix:** Replaced title page XHTML to match reference design:
- `<p class="ornament">❧</p>` — gold ornamental fleuron
- `<h1>The Works of<br/>John Owen</h1>` — split title
- `<hr class="rule"/>` — gold horizontal rule (40%, #8b6914)
- Two `<p class="subtitle">` — volume number + subtitle
- `<p class="author"><span class="by">by</span>John Owen</p>` — italic "by" label
- `<p class="editor">Edited by William H. Goold</p>`
- `<p class="publisher">Eduardus Ekofius</p>` — pushed to bottom with `margin-top: auto`
- Flexbox layout: `display: flex; flex-direction: column; align-items: center; min-height: 90vh`

### 10. NAV Title Splitting (Fixed)
**Problem:** Combined titles like "A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST CHAPTER 1" displayed as one long line in NAV.
**Fix:** Added `_split_nav_title()` regex that detects `TREATISE CHAPTER N` patterns and inserts `<br/>` for line breaks. Only affects NAV; chapter `<h1>` remains unchanged. Applied in `generate_nav_xhtml()` with special handling to not escape `<br/>`.

### 11. CSS Alignment with Reference (Fixed)
**Changes in EPUB_STYLESHEET:**
- Replaced `.title-page` block with reference design (flexbox, ornament, rule, editor, publisher with `margin-top: auto`)
- Added `.title-page .ornament`, `.title-page .rule`, `.title-page .author .by`, `.title-page .editor`
- Added `-webkit-font-smoothing: antialiased` to body rule
- Updated `.frontispiece` with flexbox centering (`display: flex; justify-content: center; min-height: 85vh`)

**Changes in EPUB3_FONT_STYLES:**
- Added `-webkit-font-smoothing: antialiased` and `line-height: 1.65` to body rule
- Added `a.fn-link` rule (color, text-decoration, font-size, margin)
- Added `aside[epub\:type~="endnote"]` rule (margin, padding, text-indent)

### 12. Noteref Color Mismatch (Fixed)
**Problem:** EPUB_STYLESHEET had `.noteref` color `#0066cc` and `.footnote-ref` color `#0066cc`, but reference EPUB and GEMINI.md specify `#0000EE`.
**Fix:** Unified to `#0000EE` in both EPUB_STYLESHEET and EPUB3_FONT_STYLES.

### 13. Duplicate .footnote CSS Rules (Fixed)
**Problem:** Two conflicting `.footnote` rules — one with `margin: 0.3em 0 0.3em 1.5em` and another with `margin: 0.5em 0 0.5em 0`.
**Fix:** Consolidated to single rule: `.footnote { font-size: 0.9em; text-indent: 0; margin: 0.3em 0; }`

---

---

### 14. Structural Misalignment (Obsolete)
**Problem:** Summary lists (e.g., Roman numerals I., II., etc.) are incorrectly promoted to standalone chapters (`div1` tags), fragmenting the logical hierarchy.
**Status:** Obsolete for Volume 16. Volume 16 has been migrated completely to the `ages_pdf` pipeline which does not suffer from CCEL/ThML `div1` fragmentation.

### 15. Reference year 136. split (Implemented - Awaiting Validation)
**Problem:** The citation "See Euseb. Chron. ad an. Christi 136." was split at "136." because of inline structural marker rules. The parser then treated "136." as a list item, causing sequence outline jumps in audits and incorrectly separating it from the blockquote.
**Fix:** Modified the `post_extract_hook` in `volumes/v16/convert.py` to keep the citation in the blockquote and split out the subsequent narrative paragraph using `\n\n`. Restored the year check threshold in `scripts/audit_anomalies.py` back to `1000`.

### 16. Flat list layout bug (Implemented - Awaiting Validation)
**Problem:** In Chapter 1 ("The Subject-Matter of the Church"), the sentence "Hence it appears that there are none excluded..." (the anchor sentence for the second list) was stuck inside the final paragraph of the first list due to a missing paragraph break in the source text extraction. As a result, the first item of the second list began on a new paragraph, preventing it from being flattened inline with its anchor.
**Fix:** Added regex replacements in `volumes/v16/convert.py` to:
- Split the anchor sentence "Hence it appears..." from the preceding paragraph of the first list using `\n\n`.
- Split the items `(1.)` through `(5.)` of the second list into separate paragraphs.
This allows the Stage 2 flat-list flattener to correctly identify both runs as flat syllabi and merge them inline with their respective anchors.

### 17. Hybrid flat/block list split (Implemented - Awaiting Validation)
**Problem:** In Chapter 1, the third list contains items `(1.)` to `(4.)` followed by the main clause of the sentence "It is the duty of every man...". Because this main clause began after an em-dash (`—`), the paragraph healer `reconstruct_paragraphs` and post-processing joined the main clause into item `(4.)`. This made item `(4.)` extremely long (205 words), violating the list flattener cap and causing it to render as a block while items `(1.)` to `(3.)` were flat.
**Fix:** Updated the list flattener in `scripts/owen_lists.py` to safely re-emit non-flattened items, and updated the paragraph healer (`reconstruct_paragraphs` and `_paragraph_needs_text_continuation` in `scripts/text_cleaner.py`) to split paragraphs across trailing em-dashes (`—`) when followed by capitalized prose. This keeps list items within their true semantic boundary and allows the entire list `(1.)` through `(4.)` to be successfully flattened inline.

### 18. List item 5 split and rendered as block (Implemented - Awaiting Validation)
**Problem:** In Chapter 3 ("Of the Polity, Rule, or Discipline of the Church in General"), a list with 5 items had items 1-4 flattened inline while item 5 remained block because it exceeded the word count cap (29 words > 25). Rendering some items inline and others as block creates an inconsistent list style.
**Fix:** Updated the list flattener in `scripts/owen_lists.py` to check the remaining items of a contiguous run. If a prefix is flattened, the remaining items are inspected and only absorbed if they strictly belong to the same list sequence (same marker family type, e.g., `arabic_bare`, and strictly sequential $+1$ value progression). This prevents false positives from swallowing unrelated list groups, while ensuring lists are styled consistently.

### 19. Pastors list items (4.) and (5.) rendered as flat instead of block (Implemented - Awaiting Validation)
**Problem:** In Chapter 5 ("The Especial Duty of Pastors of Churches"), list items `(4.)` and `(5.)` were rendered flat inline because they were originally inlined in the source text, but they should be block paragraphs in this instance.
**Fix:** Added text replacements in `post_extract_hook` in `volumes/v16/convert.py` to insert newlines (`\n\n`) before `(4.)` and `(5.)` to split them into separate block paragraphs.

### 20. Sequential list absorption skips subsequent nested lists (Implemented - Awaiting Validation)
**Problem:** In `_attach_em_dash_flat_list`, when a consecutive run of list items was processed, the loop consumed the entire run in one go by jumping `i = j` even when no prefix was flattened (`flat_prefix_len == 0`). This prevented any subsequent items in that run (like `(5.)` in Chapter 4) from being checked as parent paragraphs for their own sub-lists.
**Fix:** Updated `_attach_em_dash_flat_list` to append the first item and recursively call itself on the remaining items `run_indices[1:]` when `flat_prefix_len == 0`. This allows nested lists to be evaluated and flattened properly.


## Remaining Work

| Issue | Priority | Notes |
|-------|----------|-------|
| page-list nav for footnotes | Medium | Not yet implemented — requires page-number references in ThML |
| ThML source data gaps | Low | Volumes 2–16 have fewer footnotes paragraphs than fnref links |

---

## History

- **2025-05-05**: Initial bugs identified from reference EPUB comparison
- **2025-05-05**: Fixed portrait, frontispiece, cover format, NAV structure, spine order, id="creator"
- **2025-05-05**: Fixed footnotes — fnref→noteref conversion, endnotes chapter generation
- **2025-05-05**: Fixed portrait randomization, OPF manifest, title page design, NAV title splitting, CSS alignment, noteref color, duplicate footnote rules

---






















































<!-- AUTO_AUDIT_START -->
## Automated EPUB Audit

**Last run:** 2026-06-09T21:54:03.888512+00:00
**EPUB:** `volumes/v16/output/volume_16.epub`
**Status:** WARN (0 errors, 1 warnings)

Reports:
- `volume_16_audit.json`
- `volume_16_audit.md`

| Check | Result |
|-------|--------|
| OPF version | 3.0 |
| XHTML files | 84 |
| Spine items | 83 |
| Embedded fonts | 16 |
| NAV links | 85 |
| Greek chars / untagged | 6044 / 0 |
| Hebrew chars / untagged | 1224 / 0 |
| Noteref links / endnote anchors | 257 / 257 |
| AGES boilerplate hits | 0 |
| Possible Beta Code files | 0 |
| Escaped language-tag files | 0 |
| Empty bracket noise files | 0 |
| Repeated phrase hits | 6 |

Warnings requiring triage:

- `repeated_phrases`: Potential repeated phrases detected

**Status note:** Automated audit findings are not user validation. Keep related fixes as `IMPLEMENTED (AWAITING VALIDATION)` until explicitly approved.
<!-- AUTO_AUDIT_END -->

---

























































<!-- TEXT_INTEGRITY_START -->
## Automated Textual Integrity Audit

**Last run:** 2026-06-09T11:41:20.519722+00:00
**Status:** WARN (14 warnings)

Reports:
- `volume_16_text_integrity.json`
- `volume_16_text_integrity.md`

| Check | Result |
|-------|--------|
| PDF pages | 672 |
| EPUB text files | 82 |
| EPUB paragraphs/headings | 2751 |
| Approximate PDF-to-EPUB word coverage | 0.9994 |
| Weak page matches | 1 |
| Dense source windows checked | 27889 |
| Missing dense source-window pages | 40 |
| Front CONTENTS pages checked | 1 |
| Missing front CONTENTS pages | 0 |
| Top-of-page body windows checked | 630 |
| Top-of-page windows skipped as unstable | 34 |
| Missing top-of-page body windows | 3 |
| Bottom-of-page body windows checked | 602 |
| Bottom-of-page windows skipped as unstable | 0 |
| Missing bottom-of-page body windows | 5 |
| Possible faulty paragraph splits | 36 |
| Structural starts excluded from split warnings | 280 |
| Short fragments | 24 |
| Adjacent duplicate paragraphs | 0 |
| Inline structural marker candidates | 6 |
| Reference continuation splits | 0 |
| Citation continuation splits | 0 |
| Suspicious large-number starts | 2 |
| Roman heading candidates | 1 |
| Overlong heading candidates | 1 |
| Front-matter heading/body candidates | 0 |
| Repeated word windows | 25 |
| PDF enumerator markers | 509 |
| EPUB enumerator markers | 520 |
| Missing enumerator marker forms | 0 |
| Enumerator sequence candidates | 2 |
| PDF Greek words / EPUB Greek words | 1020 / 1032 |
| Greek word coverage ratio | 1.0 |
| PDF Hebrew words / EPUB Hebrew words | 268 / 268 |
| Hebrew word coverage ratio | 1.0 |
| Missing Greek clauses | 0 |
| Missing Hebrew clauses | 0 |

Warnings requiring triage:

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py
- `flat_analysis_chapters`: 1 ANALYSIS chapter(s) appear under-structured — fewer outline markers than expected. Check extraction quality for these chapters.

**Status note:** This audit is a mechanical integrity screen, not final proofreading or user validation.
<!-- TEXT_INTEGRITY_END -->
