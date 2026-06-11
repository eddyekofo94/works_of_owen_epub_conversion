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














<!-- AUTO_AUDIT_START -->
## Automated EPUB Audit

**Last run:** 2026-06-11T23:44:05.447405+00:00
**EPUB:** `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v13/output/volume_13.epub`
**Status:** PASS (0 errors, 0 warnings)

Reports:
- `volume_13_audit.json`
- `volume_13_audit.md`

| Check | Result |
|-------|--------|
| OPF version | 3.0 |
| XHTML files | 86 |
| Spine items | 85 |
| Embedded fonts | 26 |
| NAV links | 87 |
| Greek chars / untagged | 5778 / 0 |
| Hebrew chars / untagged | 87 / 0 |
| Noteref links / endnote anchors | 220 / 220 |
| AGES boilerplate hits | 0 |
| Possible Beta Code files | 0 |
| Escaped language-tag files | 0 |
| Empty bracket noise files | 0 |
| Repeated phrase hits | 0 |

**Status note:** Automated audit findings are not user validation. Keep related fixes as `IMPLEMENTED (AWAITING VALIDATION)` until explicitly approved.
<!-- AUTO_AUDIT_END -->

---













<!-- TEXT_INTEGRITY_START -->
## Automated Textual Integrity Audit

**Last run:** 2026-06-11T23:44:52.540349+00:00
**Status:** WARN (6 warnings)

Reports:
- `volume_13_text_integrity.json`
- `volume_13_text_integrity.md`

| Check | Result |
|-------|--------|
| PDF pages | 749 |
| EPUB text files | 84 |
| EPUB paragraphs/headings | 2253 |
| Approximate PDF-to-EPUB word coverage | 0.9994 |
| Weak page matches | 3 |
| Dense source windows checked | 33423 |
| Missing dense source-window pages | 40 |
| Front CONTENTS pages checked | 0 |
| Missing front CONTENTS pages | 0 |
| Top-of-page body windows checked | 720 |
| Top-of-page windows skipped as unstable | 8 |
| Missing top-of-page body windows | 0 |
| Bottom-of-page body windows checked | 679 |
| Bottom-of-page windows skipped as unstable | 0 |
| Missing bottom-of-page body windows | 0 |
| Possible faulty paragraph splits | 0 |
| Structural starts excluded from split warnings | 111 |
| Short fragments | 37 |
| Adjacent duplicate paragraphs | 0 |
| Inline structural marker candidates | 0 |
| Reference continuation splits | 0 |
| Citation continuation splits | 0 |
| Suspicious large-number starts | 4 |
| Roman heading candidates | 4 |
| Overlong heading candidates | 0 |
| Front-matter heading/body candidates | 0 |
| Repeated word windows | 15 |
| PDF enumerator markers | 80 |
| EPUB enumerator markers | 92 |
| Missing enumerator marker forms | 0 |
| Enumerator sequence candidates | 2 |
| PDF Greek words / EPUB Greek words | 1038 / 1058 |
| Greek word coverage ratio | 1.0 |
| PDF Hebrew words / EPUB Hebrew words | 12 / 12 |
| Hebrew word coverage ratio | 1.0 |
| Missing Greek clauses | 0 |
| Missing Hebrew clauses | 0 |

Warnings requiring triage:

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

**Status note:** This audit is a mechanical integrity screen, not final proofreading or user validation.
<!-- TEXT_INTEGRITY_END -->
