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
| 15 | Untranslated Latin and Greek quotes | convert.py | ⚠️ IMPLEMENTED (AWAITING VALIDATION) |
| 16 | Chapter 3 summary layout formatting & drape typo | convert.py | ⚠️ IMPLEMENTED (AWAITING VALIDATION) |
| 17 | Chapter 49 summary formatting & CONCENRING typo | convert.py | ⚠️ IMPLEMENTED (AWAITING VALIDATION) |
| 18 | Biographical double-tagging and missing prefatory biographies | render.py, technical_glossary.py, biography_db.py, convert.py | ⚠️ IMPLEMENTED (AWAITING VALIDATION) |



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

### 15. Untranslated Latin and Greek Quotes (Awaiting Validation)
**Problem:** Several large Latin and Greek passages in Chapter 3 (the Seidelius quote, the Hermes Trismegistus/Mercurius quote, the Calicratides quote, and the Seneca quote) and Chapter 49 (quotes by Crellius, Socinus, Rutherford, Smalcius, Schlichting, etc.) were left untranslated. Also, a previous too-broad search-and-replace correction for `remain` -> `veniam` caused cross-contamination, corrupting English occurrences of `remain` across multiple chapters.
**Fix:**
- Added translations for all untranslated passages as `[Translated: “...”]` blocks immediately following the original language runs.
- Targeted the `remain` -> `veniam` replacement specifically to the Latin phrase `delictorum nostrorum remain` -> `delictorum nostrorum veniam`, restoring all English occurrences of `remain` to their correct form.
- Fixed OCR typos: `Cicerco` -> `Cicero`, `sub ape` -> `sub spe`, `ilium` -> `illum`, `putaut` -> `putant`, `Fragm, de Jus. tificat.` -> `Fragm. de Justificat.`, `Pater quam inepte` -> `Patet quam inepte`, `pater denique quam` -> `patet denique quam`, `adversari. orum` -> `adversariorum`, `efiiciens` -> `efficiens`.
- Wrapped translations in lookahead guards `(?!\s*\[Translated:)` to prevent double-translation during Stage 1 and Stage 2 pipeline runs.

### 16. Chapter 3 Summary Formatting and drape Typo (Awaiting Validation)
**Problem:** Chapter 3's summary was split by the parser, sandwiching a raw paragraph (`MR BIDDLE'S question: —`) between two `[[SUMMARY]]` tokens, which rendered as a broken list block. Also contained the OCR typo `drape` instead of `shape`.
**Fix:** Added a regex correction in `volumes/v12/convert.py` to format the summary under two clean, consecutive `[[SUMMARY]]` markers and corrected `drape` to `shape`.

### 17. Chapter 49 Summary Formatting and CONCENRING Typo (Awaiting Validation)
**Problem:** Chapter 49's summary had a typo `CONCENRING` instead of `CONCERNING` and a stray closing bracket `]` at the end of the text.
**Fix:** Added a regex replacement to correct `CONCENRING` to `CONCERNING` and remove the stray bracket.

### 18. Biographical Double-Tagging and Missing Prefatory Biographies (Awaiting Validation)
**Problem:** Space-separated name suffix overlaps (such as "Andrew Fuller" and "Fuller", or "George Bull" and "Bull") were being double-tagged. When the longer name matched and was replaced with its footnote, the shorter surname prefix/suffix was still matched and tagged on the same word, resulting in overlapping pop-up footnotes (e.g. `Andrew Fuller‡‡`). Additionally, several historical figures mentioned in the Volume 12 Prefatory Note (Estwick, Poole, Cheynell, Moscorovius, Schomann, Pezold, Bossuet, Ménage, Sandius) did not have biographies in the database.
**Fix:**
- Implemented temporary placeholder shielding for both biographical and glossary footnotes during rendering (similar to translation notes). Once a term is matched, it is replaced with a temporary placeholder (e.g. `__BIOG_PH_{n}__` or `__GLOSS_PH_{n}__`), preventing any nested substrings or suffixes from matching subsequently. The placeholders are restored to their full HTML formatting at the end of the scanning phase.
- Added new biographical entries for all missing figures from the Volume 12 Prefatory Note to `scripts/biography_db.py`.
- Mapped short surnames (such as "Beza", "Crellius", "Bull", "Waterland", etc.) directly to their respective biographies in the central database, keeping the original names in Owen's main text intact while ensuring they are correctly tagged.
- Removed the inline main-text name expansion replacements from `volumes/v12/convert.py` to keep Owen's original author names unchanged in the text.

---

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
- **2026-06-03**: Translated untranslated Latin and Greek quotes in Chapter 3 and Chapter 49, fixed remain->veniam cross-contamination regression, corrected Chapter 3 and Chapter 49 summary formatting issues and typos (Awaiting Validation)

---

















<!-- AUTO_AUDIT_START -->
## Automated EPUB Audit

**Last run:** 2026-06-09T06:13:19.429665+00:00
**EPUB:** `volumes/v12/output/volume_12.epub`
**Status:** WARN (0 errors, 3 warnings)

Reports:
- `volume_12_audit.json`
- `volume_12_audit.md`

| Check | Result |
|-------|--------|
| OPF version | 3.0 |
| XHTML files | 63 |
| Spine items | 62 |
| Embedded fonts | 20 |
| NAV links | 64 |
| Greek chars / untagged | 14115 / 0 |
| Hebrew chars / untagged | 1448 / 0 |
| Noteref links / endnote anchors | 1084 / 1086 |
| AGES boilerplate hits | 0 |
| Possible Beta Code files | 1 |
| Escaped language-tag files | 0 |
| Empty bracket noise files | 0 |
| Repeated phrase hits | 2 |

Warnings requiring triage:

- `possible_beta_code_residue`: Possible Beta Code residue detected
- `repeated_phrases`: Potential repeated phrases detected
- `orphan_endnotes`: Some endnote anchors have no matching noteref

**Status note:** Automated audit findings are not user validation. Keep related fixes as `IMPLEMENTED (AWAITING VALIDATION)` until explicitly approved.
<!-- AUTO_AUDIT_END -->

---












<!-- TEXT_INTEGRITY_START -->
## Automated Textual Integrity Audit

**Last run:** 2026-06-09T06:14:04.763095+00:00
**Status:** WARN (13 warnings)

Reports:
- `volume_12_text_integrity.json`
- `volume_12_text_integrity.md`

| Check | Result |
|-------|--------|
| PDF pages | 822 |
| EPUB text files | 61 |
| EPUB paragraphs/headings | 3611 |
| Approximate PDF-to-EPUB word coverage | 0.9991 |
| Weak page matches | 0 |
| Dense source windows checked | 32888 |
| Missing dense source-window pages | 40 |
| Front CONTENTS pages checked | 3 |
| Missing front CONTENTS pages | 1 |
| Top-of-page body windows checked | 793 |
| Top-of-page windows skipped as unstable | 47 |
| Missing top-of-page body windows | 3 |
| Bottom-of-page body windows checked | 740 |
| Bottom-of-page windows skipped as unstable | 0 |
| Missing bottom-of-page body windows | 13 |
| Possible faulty paragraph splits | 40 |
| Structural starts excluded from split warnings | 441 |
| Short fragments | 53 |
| Adjacent duplicate paragraphs | 0 |
| Inline structural marker candidates | 3 |
| Reference continuation splits | 0 |
| Citation continuation splits | 0 |
| Suspicious large-number starts | 4 |
| Roman heading candidates | 0 |
| Overlong heading candidates | 0 |
| Front-matter heading/body candidates | 0 |
| Repeated word windows | 25 |
| PDF enumerator markers | 450 |
| EPUB enumerator markers | 460 |
| Missing enumerator marker forms | 1 |
| Enumerator sequence candidates | 1 |
| PDF Greek words / EPUB Greek words | 2593 / 2593 |
| Greek word coverage ratio | 0.9992 |
| PDF Hebrew words / EPUB Hebrew words | 222 / 221 |
| Hebrew word coverage ratio | 0.9955 |
| Missing Greek clauses | 0 |
| Missing Hebrew clauses | 0 |

Warnings requiring triage:

- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

**Status note:** This audit is a mechanical integrity screen, not final proofreading or user validation.
<!-- TEXT_INTEGRITY_END -->
