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
| 14 | Structural Misalignment (Summary Head Fragmentation) | ThML Source | ❌ Open |


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

### 14. Structural Misalignment (Open)
**Problem:** Summary lists (e.g., Roman numerals I., II., etc.) are incorrectly promoted to standalone chapters (`div1` tags), fragmenting the logical hierarchy.
**Evidence (v4):**
- ThML splits "The Reason of Faith" Chapter 2 into five units: `ch008` (Chap 2) contains only the introductory sentence, while the outline points `ch009` (I.), `ch010` (II.), `ch011` (III.), and `ch012` (IV.) are promoted to standalone chapters.
- Fragmented heads identified: `ch009`, `ch010`, `ch011`, `ch012`, `ch019`, `ch020`, `ch023`, `ch024`, `ch027`, `ch028`, `ch029`, `ch030`, `ch031`, `ch032`, `ch033`, `ch040`, `ch041`, `ch046`, `ch047`, `ch062`, `ch063`, `ch064`, `ch067`, `ch076`, `ch084`, `ch085`.
**Status:** Pending surgical consolidation and merging of fragmented heads back into parent chapters.

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

### 15. Volume 4 AGES Footnotes, Empty Bracket Noise, and Front CONTENTS Overlap — IMPLEMENTED (AWAITING VALIDATION)

**Problem:** Volume 4 had body noteref links without a working generated endnotes chapter, and rendered scripture citations exposed empty bracket residue such as `[] Ephesians 4:30`. The front-matter audit also found one missing CONTENTS continuation page.

**Fix:** Added a generic AGES back-matter footnote detector that finds the `FOOTNOTES` section or final-page `ftN` markers, removes empty bracket residue after scripture-code cleanup, teaches the EPUB audit/regression gate to fail on visible `[]`, and lets early TOC-like pages be preserved even when the PDF outline also references them.

**Validation status:** IMPLEMENTED (AWAITING VALIDATION). Regenerated Volume 4 only. Current v4 EPUB audit reports 23 noteref links / 23 endnote anchors, 0 empty bracket noise files, and 0 untagged Greek/Hebrew chars. Current v4 text-integrity audit reports 4 front CONTENTS pages checked and 0 missing.

---







<!-- AUTO_AUDIT_START -->
## Automated EPUB Audit

**Last run:** 2026-05-18T00:19:28.408272+00:00
**EPUB:** `volumes/v4/output/volume_4.epub`
**Status:** WARN (0 errors, 3 warnings)

Reports:
- `volume_4_audit.json`
- `volume_4_audit.md`

| Check | Result |
|-------|--------|
| OPF version | 3.0 |
| XHTML files | 72 |
| Spine items | 70 |
| Embedded fonts | 8 |
| NAV links | 70 |
| Greek chars / untagged | 4420 / 23 |
| Hebrew chars / untagged | 687 / 19 |
| Noteref links / endnote anchors | 24 / 23 |
| AGES boilerplate hits | 0 |
| Possible Beta Code files | 0 |
| Escaped language-tag files | 0 |
| Empty bracket noise files | 0 |
| Repeated phrase hits | 10 |

Warnings requiring triage:

- `untagged_greek`: Greek characters appear outside lang='el' context
- `untagged_hebrew`: Hebrew characters appear outside lang='he' context
- `repeated_phrases`: Potential repeated phrases detected

**Status note:** Automated audit findings are not user validation. Keep related fixes as `IMPLEMENTED (AWAITING VALIDATION)` until explicitly approved.
<!-- AUTO_AUDIT_END -->

---






<!-- TEXT_INTEGRITY_START -->
## Automated Textual Integrity Audit

**Last run:** 2026-05-18T00:19:59.030541+00:00
**Status:** WARN (13 warnings)

Reports:
- `volume_4_text_integrity.json`
- `volume_4_text_integrity.md`

| Check | Result |
|-------|--------|
| PDF pages | 653 |
| EPUB text files | 71 |
| EPUB paragraphs/headings | 2410 |
| Approximate PDF-to-EPUB word coverage | 0.9951 |
| Weak page matches | 34 |
| Dense source windows checked | 777 |
| Missing dense source-window pages | 627 |
| Front CONTENTS pages checked | 4 |
| Missing front CONTENTS pages | 0 |
| Top-of-page body windows checked | 624 |
| Top-of-page windows skipped as unstable | 29 |
| Missing top-of-page body windows | 2 |
| Bottom-of-page body windows checked | 607 |
| Bottom-of-page windows skipped as unstable | 17 |
| Missing bottom-of-page body windows | 3 |
| Possible faulty paragraph splits | 22 |
| Structural starts excluded from split warnings | 408 |
| Short fragments | 24 |
| Adjacent duplicate paragraphs | 0 |
| Inline structural marker candidates | 2 |
| Reference continuation splits | 0 |
| Citation continuation splits | 0 |
| Suspicious large-number starts | 0 |
| Roman heading candidates | 30 |
| Overlong heading candidates | 1 |
| Front-matter heading/body candidates | 0 |
| Repeated word windows | 25 |
| PDF enumerator markers | 416 |
| EPUB enumerator markers | 375 |
| Missing enumerator marker forms | 3 |
| Enumerator sequence candidates | 0 |
| PDF Greek words / EPUB Greek words | 786 / 779 |
| Greek word coverage ratio | 0.9817 |
| PDF Hebrew words / EPUB Hebrew words | 111 / 109 |
| Hebrew word coverage ratio | 0.3303 |
| Missing Greek clauses | 42 |
| Missing Hebrew clauses | 17 |

Warnings requiring triage:

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_hebrew_word_coverage`: EPUB Hebrew word coverage against PDF extraction is lower than expected
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB
- `missing_hebrew_clauses`: Some dense Hebrew passages from the PDF are missing from the EPUB

**Status note:** This audit is a mechanical integrity screen, not final proofreading or user validation.
<!-- TEXT_INTEGRITY_END -->
