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
| 14 | NAV title splitting now creates hierarchical structure (_split_nav_title returns tuple) | converter.py | ✅ Fixed |
| 15 | `a.footnote-ref` font-size too small (0.75em → 0.95em) | shared.py | ✅ Fixed |
| 16 | ΧΡΙΣΤΟΛΟΓΙΑ merged with editor signature on wrong page | ThML/converter | ✅ Fixed |
| 17 | Hierarchical Split (L1 vs L2) — Improved State Logic | pdftohtml | ⌛ PENDING CONFIRMATION |
| 18 | Redundant Heading Merge (Treatise + Chapter 1) | ThML/converter.py | ⌛ PENDING CONFIRMATION |
| 19 | Non-Uniform Chapter Levels (Chapters 8-20 level logic) | converter.py | ⌛ PENDING CONFIRMATION |
| 20 | Missing "CHAPTER 1" heading in XHTML body content | ThML (ch008) | ⌛ PENDING CONFIRMATION |
| 21 | Structural Misalignment (Summary Head Fragmentation) | ThML Source | ❌ Open |
| 22 | Missed Centered Headings (Centering Bug) | pdftohtml | ⌛ PENDING CONFIRMATION |
| 23 | Greek Mapping Error (Y correctly mapped to Upsilon) | shared.py | ⌛ PENDING CONFIRMATION |
| 24 | TOC Out-of-Order Matching (Forced Monotonic matching) | pdftohtml | ⌛ PENDING CONFIRMATION |
| 25 | Footnote False Positives (Strict f1, f2 prefix requirement) | pdftohtml | ⌛ PENDING CONFIRMATION |
| 26 | Nested Tag Content Loss (Using itertext() recursion) | pdftohtml | ⌛ PENDING CONFIRMATION |
| 27 | "W. H. G." Signature Missing at end of Preface | pdftohtml | ⌛ PENDING CONFIRMATION |
| 28 | "CONTENTS OF VOLUME 1" Formatting (Hanging Indent) | pdftohtml | ⌛ PENDING CONFIRMATION |
| 29 | Scripture codes leaking into CONTENTS page XHTML | `build_toc_page_xhtml()` → `format_title_page()` | ✅ Fixed 2026-05-09 |
| 30 | Treatise title pages merged into single `<p>` blob | chapter loop in `process_owen_volume()` | ✅ Fixed 2026-05-09 |
| 31 | Font detection used `max()` on font names, missing Koine spans | `format_title_page()` | ✅ Fixed 2026-05-09 |
| 32 | Healer-mode transition falsely triggered by TOC text ("CHAPTER") | front matter loop in `process_owen_volume()` | ✅ Fixed 2026-05-09 |
| 33 | Title page detection too aggressive (41 false positives) | `detect_page_type()` | ✅ Fixed 2026-05-09 |
| 34 | NAV links pointing to non-existent files for title-only chapters | TOC entry href in `process_owen_volume()` | ✅ Fixed 2026-05-09 |
| 35 | `build_toc_page_xhtml()` accidentally deleted during refactor | converter.py | ✅ Fixed 2026-05-09 |
| 36 | `healer_mode` not passed to `get_pages_text()` for mid-volume title content | chapter loop in `process_owen_volume()` | ✅ Fixed 2026-05-09 |
| 37 | Preservation Mode — front matter pages 1-10 formatting broken | converter.py + shared.py | ❌ Open |
| 38 | Missing treatises: Part 2, Meditations Applied, Two Short Catechisms | converter.py | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 39 | TOC (pages 3-6) fragmented and formatting doesn't match PDF | `detect_page_type()` + `build_toc_page_xhtml()` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 40 | Title pages lack premium color and typography design | `shared.py` + `format_title_page()` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 41 | PREFATORY NOTE and PREFACE badly extracted and formatted | `detect_page_type()` + `shared.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 42 | Text is broken up mid-sentence (paragraph fragmentation) | `get_pages_text()` + `reconstruct_paragraphs()` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 43 | Blockquotes are not indented and contain artificial breaks | `get_merged_page_text()` + `reconstruct_paragraphs()` | ❌ REVERTED (REGRESSIONS) |
| 44 | Textual duplication (ghost layers) in PDF causing repeated fragments | `deduplicate_lines()` + `extract_page_text_with_fonts()` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 48 | EPUB lacks premium "Goold/AGES" visual layout on structural pages | `detect_page_type()` + `extract_title_page()` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 49 | Ghost layer duplication spans across line breaks | `remove_repeated_phrases()` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 50 | Textual integrity audit and holistic paragraph healing enforcement | `scripts/audit_text_integrity.py` + `get_pages_text()` + `reconstruct_paragraphs()` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 51 | Chapter subtitles merged into opening body paragraphs and scripture-reference ghost duplicates | `markdown_to_html()` + paragraph post-processing | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 52 | Top-of-page enumerator clipping and missing `[1.]` before `[2.]` | `coordinate_redactor()` + `scripts/audit_text_integrity.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 53 | Numeric reference continuations, inline enumerators, ordinal false splits, and duplicate scripture tails | `reconstruct_paragraphs()` + paragraph post-processing + `markdown_to_html()` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 54 | Plain chapter headings, hidden popup footnotes, and catechism ghost-text cleanup | `markdown_to_html()` + `parse_thml_footnotes()` + catechism post-processing | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 55 | Front-matter prose false headings, citation-number splits, and centered roman outline lists | `markdown_to_html()` + marker schema + `scripts/audit_text_integrity.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 56 | Inline footnote placement, noteref spacing, and catechism doxology layout | `markdown_to_html()` + `shared.py` + `scripts/audit_epub.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 57 | Scripture-tail structural breaks and reference continuation splits | `post_process_paragraphs()` + marker schema + `scripts/audit_text_integrity.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 58 | Sliced source sentence, verse-range continuation, and prefatory heading styling | `post_process_paragraphs()` + `markdown_to_html()` + `scripts/audit_text_integrity.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 59 | Prefatory Note OCR blemishes and heading/body regression guard | `markdown_to_html()` + `scripts/audit_text_integrity.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 60 | Chapter heading/body absorption regression | `markdown_to_html()` + `scripts/audit_text_integrity.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 61 | Remaining false paragraph break after patristic citation and inline bracketed ordinal marker | `post_process_paragraphs()` + structural marker schema + `scripts/audit_text_integrity.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 62 | `verse, N` numeric reference continuation false paragraph break | `post_process_paragraphs()` + `scripts/audit_text_integrity.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 63 | Inline roman/numbered section markers still missed | structural marker schema + rendered-HTML audit | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 64 | Title-page stylesheet mismatch and `here is ... 1.` list-marker promotion | `shared.py` + `markdown_to_html()` + `scripts/audit_text_integrity.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 65 | Contents page false item breaks and mobile-readable contents sizing | `build_toc_page_xhtml()` + `shared.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 66 | Uppercase/spaced bracketed footnote markers such as `[ F18]` not normalized | `normalize_footnote_markers()` + `scripts/audit_epub.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 67 | EPUB nav/Guide page exposed in reading order and title-page ornament hidden | EPUB spine assembly + `shared.py` + `scripts/audit_epub.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 68 | Generated title-page credits left-aligned and publisher credit incorrect | `_build_title_page()` + `shared.py` | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 69 | Bottom-of-page body text clipped by overly aggressive footer redaction margin | `BOTTOM_MARGIN` + `coordinate_redactor()` + `scripts/audit_text_integrity.py` | ✅ Fixed 2026-05-11 |
| 70 | Source-aware structural boundary promotion and citation continuation | `_split_inline_structural_markers()` + citation continuation + rendered-HTML audit | ⌛ IMPLEMENTED (AWAITING VALIDATION) |
| 71 | False paragraph break after scripture book (1 Corinthians → 1. Wherefore...) | `hard_structural` + year threshold + continuation guard | ✅ Fixed 2026-05-11 |
| 72 | False paragraph break at chapter range continuation (Chapter 9 to → 15. It is followed...) | `hard_structural` + year threshold + continuation guard | ✅ Fixed 2026-05-11 |
| 73 | False paragraph break at 4-digit year (1696. Charneck, 1724. It may seem...) | `hard_structural` + year threshold | ✅ Fixed 2026-05-11 |
| 74 | Plain ordinals not promoted inline inside body text (1st, That the Lord Christ...) | `marker_is_bare_ordinal` + inline structural promotion | ✅ Fixed 2026-05-11 |
| 75 | OCR typo "Charneck" should be "Charnock" | dedicated OCR error repair function | ✅ Fixed 2026-05-11 |
| 76 | Multiline block quotes falsely split mid-quote | quote boundary detection + paragraph healing | ✅ Fixed 2026-05-11 |
| 77 | Duplicate CSS rules injected into main.css via font styles | `shared.py` (EPUB3_FONT_STYLES) | ✅ Fixed 2026-05-11 |
| 78 | Missing Ezra SIL font (SILEOT.ttf) in EPUB manifest | `converter.py` (EPUB assembly) | ✅ Fixed 2026-05-11 |
| 79 | Malformed Greek title "CRISTOLOGIA" on Volume 1 title page | `converter.py` (format_title_page) | ✅ Fixed 2026-05-11 |
| 80 | Beta-code residue "]y" in chapters 36 and 45 | OCR fix for "ly" misread | ✅ Fixed 2026-05-11 |
| 81 | Multi-paragraph ThML footnotes truncated at first paragraph | `parse_thml_footnotes()` paragraph-boundary awareness | ✅ Fixed 2026-05-11 |
| 82 | EPUB metadata lacks multi-language tagging and editor role | `VOLUME_CONFIG` + `DC:language` + `role` metadata | ✅ Fixed 2026-05-11 |
| 83 | Global 'backwards' reading direction due to Hebrew metadata | `book.set_direction('ltr')` in `converter.py` | ✅ Fixed 2026-05-11 |
| 84 | Removal of Cardo and STIX Two Text fonts | `shared.py` config + CSS fallback cleanup | ✅ Fixed 2026-05-11 |
| 85 | Missing footnotes in Volumes 2 and 3 | Case-insensitive `ft` marker detection + font-aware extraction | ✅ Fixed 2026-05-11 |
| 86 | Small font sizes for body and footnote references | Increased base `1.1em` + `noteref` size reset | ✅ Fixed 2026-05-11 |
| 87 | Refactor font selection for per-volume body fonts | `VOLUME_CONFIG` + dynamic lookup + CSS locking | ✅ Fixed 2026-05-11 |

---

## Issue Details

### 76. Multiline block quotes falsely split mid-quote (Open — Documented)
**Problem:** Multiline block quotes (especially Greek and Latin patristic citations) are being falsely split into multiple paragraphs in the middle of the quote. The entire block quote should be treated as a single cohesive unit without interruptions.

**Example from user report:**
```
"Universam significabat ecclesiam, quae in hoc seculo diversis tentationibus,
velut imbribus, fluminibus, tempestatibusque quatitur, et non cadit; quoniam
fundata est supra Petram; unde et Petrus nomen accepit. Non enim a Petro
Petra, sed Petrus a Petra; sicut non Christus a Christiano, sed Christianus a
Christo vocatur. Ideo quippe ait Dominus, 'Super hanc Petram aedificabo
ecclesiam meam', quia dixerat Petrus, 'Tu es Christus filius Dei vivi'.
'Super hanc ergo' (inquit) 'Petram quam confessus es, aedificabo eccleaism
meam'. Petra enim erat Christus, super quod fundamentum etiam ipse aedificatus
est Petrus. Fundamentum quippe aliud nemo potest ponere, praeter id quod
positum est, quod est Jesus Christus"."
```

This entire quote should remain as one block, not be split at sentence boundaries or page breaks.

**Root cause hypothesis:** Quote-boundary detection is not currently integrated into the paragraph-healing logic. The healer sees terminal periods and may treat them as paragraph boundaries, even when they occur inside a quoted block.

**Required investigation:**
1. Does the PDF/extraction preserve quote delimiters (smart quotes, double quotes) reliably?
2. Are nested quotes (single quotes within double quotes) handled correctly?
3. Should quote detection run during `reconstruct_paragraphs()` or in a separate post-processing pass?
4. How to handle quotes that span page boundaries?

**Implementation approach to consider:**
- Track quote state (inside/outside quote) during paragraph reconstruction
- If inside a quote and paragraph ends without closing quote, merge with next paragraph
- Special handling for scripture citations and patristic block quotes
- Consider visual cues (indentation, centering) in addition to quote characters

**Status:** ⌛ IMPLEMENTED (AWAITING VALIDATION)

---

### 75. OCR typo "Charneck" should be "Charnock" (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** OCR error produces "Charneck" instead of the correct "Charnock" (referring to Stephen Charnock, the Puritan divine).

**Location:** Example appears in a year context: `1696. Charneck`

**Root cause:** The `_repair_known_ocr_errors()` function in `audit_text_integrity.py` repairs some errors like `Soripture` → `Scripture`, but did not include a dedicated Owen-specific OCR error repair function.

**Fix approach:**
1. Created a dedicated `_repair_owen_ocr_errors()` function in `converter.py`.
2. Added known OCR typos specific to Owen/AGES extraction: `Charneck`, `storage`, `whoso`.
3. Integrated this repair into `clean_text()`.

**Status:** ⌛ IMPLEMENTED (AWAITING VALIDATION)

---

### 74. Plain ordinals not promoted inline inside body text (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Plain ordinal markers like `1st,` or `[1st,]` that appear inline inside body paragraphs were not being promoted to structural starts.

**Root cause:** The `marker_is_bare_ordinal` detection was missing from the strong promotion logic in `_split_inline_structural_markers()`.

**Fix approach:**
1. Integrated bare ordinal detection into the strong promotion logic in `_split_inline_structural_markers()`.

**Status:** ⌛ IMPLEMENTED (AWAITING VALIDATION)

---

### 73. False paragraph break at 4-digit year (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Paragraphs starting with 4-digit years like `1696.` or `1724.` were being treated as structural boundaries.

**Root cause:** The `hard_structural` check matched `1696.` and `1724.` as structural patterns.

**Fix approach:**
1. Applied 3-digit threshold to bare `\d+\.` patterns: numbers 1-999 = valid structural numbering, numbers 1000+ = years (excluded).
2. Modified the `hard_structural` check and global structural regexes to exclude 4-digit numbers.

**Status:** ⌛ IMPLEMENTED (AWAITING VALIDATION)

---

### 72. False paragraph break at chapter range continuation (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Chapter range references like `Chapter 9 to` were being falsely split from their continuation `15. It is followed...`.

**Root cause:** The `hard_structural` check matched `15.` and short-circuited continuation checks.

**Fix approach:**
1. Reordered logic to check for continuation contexts BEFORE applying `hard_structural`.
2. Added specific continuation guard for `Chapter N to` + `M.`.
3. Added the same guard to `_split_inline_structural_markers`.

**Status:** ⌛ IMPLEMENTED (AWAITING VALIDATION)

---

### 71. False paragraph break after scripture book (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Scripture book references like `1 Corinthians` were being falsely split from the verse continuation.

**Root cause:** The `hard_structural` check matched `1.` and short-circuited continuation checks.

**Fix approach:**
1. Reordered logic to check for continuation contexts BEFORE applying `hard_structural`.
2. Added specific continuation guard for `{Book}` + `N.`.
3. Added the same guard to `_split_inline_structural_markers`.

**Status:** ⌛ IMPLEMENTED (AWAITING VALIDATION)

---

### 69. Bottom-of-page body text clipped by overly aggressive footer redaction margin (IMPLEMENTED — AWAITING VALIDATION; RESIDUAL WARNINGS)
**Problem:** The enhanced bottom-of-page audit showed that some final body lines on PDF pages were absent from the generated EPUB. These were not ordinary paragraph-healing errors; the text had been removed before the healer could see it.

**Root cause:** `coordinate_redactor()` used a global 50pt bottom margin to remove footers and page debris. In Volume 1, several AGES pages place real body text lower than that threshold, especially on footnote-heavy or overlay-heavy pages. Those lines were misclassified as footer-zone text.

**Fixes:**
- Reduced `BOTTOM_MARGIN` from `50` to `25`, preserving a footer safety band while allowing lower body lines to survive extraction.
- Kept the new `bottom_of_page_integrity()` audit in place so future converter changes can catch this class of silent source-text loss.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed formerly clipped examples now appear in the unpacked EPUB, including:
  - `rock is not called Petra...` in `ch004.xhtml`
  - `Council of Nice...` in `ch004.xhtml`
  - `Lib. De Incarnat...` in `ch004.xhtml`
- Text-integrity audit improved from about `0.9889` to `0.9915` PDF-to-EPUB word coverage.
- Weak page matches improved from `24` to `8`.
- Missing bottom-of-page windows improved from `42` to `20`.

**Residual risk:** This is a meaningful recovery but not a complete close-out. The remaining `20` bottom-window warnings need triage before the issue should be considered validated.

**Status:** IMPLEMENTED (AWAITING VALIDATION; RESIDUAL WARNINGS)

### 70. Source-aware structural boundary promotion and citation continuation (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Issues 61 and 63 shared one deeper failure: the converter still sometimes misclassified numeric/roman markers and citation fragments at paragraph boundaries. It needed to distinguish scripture/reference continuations, patristic citation continuations, and real Owen outline markers.

**Fixes:**
- Added citation-start and author-tail recognition so `See August.` + `Lib. con. Serm...` stays in one paragraph.
- Extended inline marker promotion to include bare roman markers and markdown-bold decimal/roman forms such as `**6.**`.
- Added a guarded source-like marker promotion rule for substantial prose followed by decimal/roman markers and uppercase continuation, while still suppressing scripture/citation continuations.
- Extended the text-integrity audit to inspect rendered XHTML for inline bold markers and to report `citation_continuation_splits`.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed the recorded examples in `ch004.xhtml`, `ch013.xhtml`, `ch029.xhtml`, `ch030.xhtml`, and `ch035.xhtml`.
- Text-integrity audit: 7 warning categories, with `0` inline structural marker candidates, `0` reference continuation splits, `0` citation continuation splits, and `0` roman heading candidates.
- EPUB audit: 0 errors, 4 warnings.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 68. Generated title-page credits left-aligned and publisher credit incorrect (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** The generated title page still showed the credit block left-aligned because the global body paragraph rule overrode the title-page intent. The ornament needed to be gold, and the visible `Eduardus Ekofius` line needed to be replaced with `Eduardus Ekofius`.

**Fixes:**
- Added explicit centered styles for `.title-page .author`, `.title-page .editor`, and `.title-page .publisher`, plus the `.titlepage` equivalents.
- Styled `.title-page .ornament` / `.titlepage .ornament` in gold.
- Changed the generated title-page publisher line from `Eduardus Ekofius` to `Eduardus Ekofius`.
- Added spacing between the italic `by` label and `John Owen`.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Unpacked the EPUB and confirmed `title.xhtml` contains `<p class="publisher">Eduardus Ekofius</p>`.
- Confirmed generated `style/main.css` colors the ornament `#b08d2d` and centers the title-page author/editor/publisher credit paragraphs.
- EPUB audit: 0 errors, 4 warnings.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 67. EPUB nav/Guide page exposed in reading order and title-page ornament hidden (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Apple Books displayed the generated EPUB navigation page at the beginning of the reading flow, showing the tail of the table of contents plus a redundant `Guide` section beside the title page. The generated title pages also lost the small ornamental mark because the stylesheet hid `.ornament`.

**Fixes:**
- Kept `nav.xhtml` in the manifest with `properties="nav"` but removed it from the spine, so it remains the EPUB3 navigation document without appearing as a reader-visible chapter.
- Reordered the opening spine to `cover.xhtml`, generated `title.xhtml`, `frontispiece.xhtml`, then extracted front matter and chapters.
- Restored `.title-page .ornament` / `.titlepage .ornament` as a controlled, centered title-page ornament.
- Added an EPUB audit error for `nav.xhtml` or any manifest item with `properties="nav"` appearing in the spine.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Unpacked the EPUB and confirmed `nav.xhtml` is still present in the manifest with `properties="nav"` but no `idref="nav"` appears in the spine.
- Confirmed first spine entries are `chapter_0`, `chapter_5`, `chapter_1`, `chapter_2`, `chapter_3`, `chapter_4`, corresponding to cover, generated title page, frontispiece, and front matter.
- Confirmed `title.xhtml` contains `<p class="ornament">❧</p>` and generated `style/main.css` displays `.ornament` as a centered title-page element.
- EPUB audit: 0 errors, 4 warnings.
- Text-integrity audit: 4 warning categories, with 0 inline structural marker candidates and 0 reference continuation splits.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 65. Contents page false item breaks and mobile-readable contents sizing (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** The Volume 1 contents page split `CHAPTER 1 . Peter’s Confession;` from its continuation `Matthew 16:16 — Conceits of the Papists...`, creating a false break in the contents entry. The contents item text was also too small/tight for comfortable mobile reading/tapping.

**Fixes:**
- Updated `build_toc_page_xhtml()` so non-label contents lines following a contents item ending in `;`, `—`, or `-` are joined back into that previous contents item instead of emitted as a new paragraph.
- Increased `.ContentsItem` to `0.95em` and set `line-height: 1.45` for better iPhone readability.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `contents_2.xhtml` now renders the Chapter 1 contents entry as one paragraph:
  `CHAPTER 1 . Peter’s Confession; Matthew 16:16 — Conceits of the Papists thereon — The Substance and Excellency of that Confession.`
- Confirmed generated `style/main.css` contains `.ContentsItem { font-size: 0.95em; line-height: 1.45; }`.
- EPUB audit: 0 errors, 4 warnings.
- Text-integrity audit: 4 warning categories, with 0 inline structural marker candidates and 0 reference continuation splits.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 64. Title-page stylesheet mismatch and `here is ... 1.` list-marker promotion (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Visual review found the `TWO SHORT CATECHISMS` title page looked rough: the decorative ornament appeared as extraction debris, the descriptive block was not centered/elegant, and the page was not receiving the intended title-page styling. The same pass found `...And here is, — Isaiah 44:3, 4, 1. A supposition...` still inline, where `1.` should start a bold numbered paragraph.

**Fixes:**
- Updated title-page CSS to target both `.titlepage` and `.title-page`, because generated title pages use `class="title-page"` while the stylesheet only styled `.titlepage`.
- Centered and italicized descriptive title-page prose, constrained title-page width, and kept title-page heading hierarchy centered for all title pages. The ornament was temporarily hidden in this pass, then restored as a controlled styled ornament under Issue 67.
- Added a guarded second pass for inline structural-marker splitting at the HTML conversion boundary.
- Allowed list-introduction cues such as `here is ... Isaiah 44:3, 4, 1.` to promote `1.` even after a scripture-reference tail.
- Updated the text-integrity audit so a structural paragraph following a reference tail is not falsely reported as a broken reference continuation.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `ch046_title.xhtml` uses `section class="title-page"` and `style/main.css` now styles `.title-page`, including centered `.descriptive`.
- Confirmed `ch045.xhtml` now renders `A supposition...` as its own paragraph beginning `<b>1.</b>`.
- Text-integrity audit: 4 warning categories, with 0 inline structural marker candidates and 0 reference continuation splits.
- EPUB audit: 0 errors, 4 warnings.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 66. Uppercase/spaced bracketed footnote markers such as `[ F18]` not normalized (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** The final paragraph of `ORIGINAL PREFACE` part 2 rendered a literal `[ F18]` instead of a linked EPUB noteref. This left the reader seeing source-marker debris where the popup/endnote link should appear.

**Fixes:**
- Made `LOOSE_FOOTNOTE_MARKER_RE` case-insensitive so `[ F18]`, `[F18]`, `[ f18]`, and loose `f18`-style markers normalize through the same noteref path.
- Made the EPUB audit literal-footnote scan case-insensitive so uppercase/spaced marker residues are caught in future single-volume QA runs.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Unpacked the EPUB and confirmed `/tmp/owen_v1_check/EPUB/ch042.xhtml` now renders `...add this thereunto.` followed by a noteref link to `endnotes.xhtml#fn18`.
- Whole-EPUB footnote scan found `0` literal `[F...]` / `[ F...]` / `f...` marker residues.
- Whole-EPUB footnote scan found `125` noteref links, `124` unique noteref targets, `124` endnote anchors, and `0` missing targets. The duplicate target is `fn18`, because the same endnote is now referenced from both the title page and `ORIGINAL PREFACE` part 2.
- EPUB audit: 0 errors, 4 warnings.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 63. Inline roman/numbered section markers still missed (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Visual review found that several structural markers still remained embedded inside prose instead of starting styled paragraphs/sections:
- `ch029.xhtml`: `II. This darkness in the minds of men...` appeared inline rather than as a roman subheading.
- `ch029.xhtml`: `...no darkness at all.” 4. Hitherto darkness...` kept bold `4.` inline.
- `ch030.xhtml`: `...King in his beauty.” 2. Our second direction...` kept bold `2.` inline.
- `ch035.xhtml`: `...light of this truth 6. Promises, prophecies...` kept bold `6.` inline.

**Root cause:** `_split_inline_structural_markers()` was still conservative around bare decimal and roman markers because earlier fixes had to protect scripture references such as `verse, 7` and `1 Corinthians 1:13, 15`. The converter also saw some of the failing markers in markdown-bold form, such as `**6.**`, so a plain `6.` check was not enough. The audit only scanned plain text and missed rendered `<b>2.</b>` / `<b>4.</b>` / `<b>6.</b>` forms.

**Fixes:**
- Extended inline structural marker recognition to include bare roman markers and markdown-bold decimal/roman markers.
- Added a source-like marker promotion rule for substantial prose followed by a decimal or roman marker and uppercase continuation, while still blocking scripture/citation tails such as `verse, 7`, `chap. 7:26`, and `Serm. 13`.
- Preserved roman-list behavior separately from roman subheading behavior: short list items remain `roman-list-item`, while real roman section heads become `roman-subheading`.
- Extended `scripts/audit_text_integrity.py` to inspect rendered XHTML for inline bold structural markers, not just plain paragraph text, while suppressing citation-number false positives.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `ch029.xhtml` now renders `<h4 class="roman-subheading">II.</h4>` followed by a normal paragraph beginning `This darkness in the minds of men...`.
- Confirmed `ch029.xhtml` now starts `Hitherto darkness...` as its own paragraph beginning `<b>4.</b>`.
- Confirmed `ch030.xhtml` now starts `Our second direction...` as its own paragraph beginning `<b>2.</b>`.
- Confirmed `ch035.xhtml` now starts `Promises, prophecies...` as its own paragraph beginning `<b>6.</b>`.
- Text-integrity audit: 7 warning categories, with `0` inline structural marker candidates, `0` reference continuation splits, `0` citation continuation splits, and `0` roman heading candidates.
- EPUB audit: 0 errors, 4 warnings.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 62. `verse, N` numeric reference continuation false paragraph break (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Visual review found `...gift of Christ,” verse,` followed by a false paragraph/list start `7. He has...` in `ch019.xhtml`. The source paragraph has `verse, 7. He has...` as one sentence/reference continuation.

**Fixes:**
- Broadened numeric-continuation detection so `verse,`, `verses,`, `chap,`, and `chapter,` at the end of a paragraph are treated like `verse`/`verse.` stems when the next paragraph begins with a number.
- Updated text-integrity auditing so `verse, 7.` is not falsely reported as an inline structural marker once it has been joined.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `ch019.xhtml` now renders `verse, 7. He has...` in one paragraph.
- Text-integrity audit: 4 warning categories, with 0 inline structural marker candidates and 0 reference continuation splits.
- EPUB audit: 0 errors, 4 warnings.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 61. Remaining false paragraph break after patristic citation and inline bracketed ordinal marker (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Visual review found two structural failures in the regenerated Volume 1 EPUB:
- `ch004.xhtml`: the sentence ending `See August.` was falsely broken before `Lib. con. Serm. Arian. cap. 35, and Epist. 66 ad Maximum.` The ThML/source paragraph keeps this citation in the same paragraph.
- `ch013.xhtml`: `in such a season; — [1st,] that their thoughts...` needed `[1st,]` as a paragraph/list start, not embedded in the lead-in sentence.

**Root cause:** The reference-continuation logic recognized many scripture and chapter-reference tails, but it did not recognize a new paragraph beginning with a scholarly abbreviation chain such as `Lib. con. Serm...` after an author cue such as `See August.`. The bracketed ordinal schema existed, but marker promotion needed to be applied again after paragraph-level cleanup and HTML-boundary normalization.

**Fixes:**
- Added citation-continuation recognition for paragraphs beginning with scholarly/patristic abbreviation starts such as `Lib.`, `Serm.`, `Epist.`, `Cap.`, `Orat.`, `Tract.`, and related forms.
- Added author/citation-tail recognition for preceding paragraphs ending with cues such as `See August.` / patristic author abbreviations.
- Joined those citation chains during paragraph post-processing before they can become false body paragraphs.
- Kept the existing bracketed ordinal promotion path and verified it now survives the complete rebuild as its own paragraph.
- Added text-integrity audit coverage for citation-continuation splits, plus rendered-marker checks so this class does not silently pass again.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `ch004.xhtml` now keeps `See August. Lib. con. Serm. Arian. cap. 35, and Epist. 66 ad Maximum.` in one paragraph.
- Confirmed `ch013.xhtml` now renders `[1st,] that their thoughts...` as its own paragraph beginning `<b>[1st,]</b>`.
- Text-integrity audit: 7 warning categories, with `0` inline structural marker candidates, `0` reference continuation splits, `0` citation continuation splits, and `0` roman heading candidates.
- EPUB audit: 0 errors, 4 warnings.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 60. Chapter heading/body absorption regression (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** After tightening front-matter heading handling, several normal chapters rendered `CHAPTER N`, the subtitle, and the first paragraph inside a single `<h3>` heading. This made chapter headings and first paragraphs visually broken across the EPUB.

**Fixes:**
- Added a chapter-heading splitter for Markdown headings that begin with `CHAPTER N` but include subtitle/body text in the same extracted paragraph.
- The converter now emits `CHAPTER N` as `<h3>`, bold all-caps subtitle text as `<h4 class="chapter-subtitle">`, and the remaining prose as a normal `<p>`.
- Added a general overlong-heading audit guard so chapter headings that swallow body text are mechanically flagged in future runs.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed affected chapters such as `ch009.xhtml`, `ch010.xhtml`, and `ch012.xhtml` now render chapter heading, subtitle, and first paragraph as separate elements.
- Confirmed a direct XHTML scan reports 0 headings over 180 characters.
- EPUB audit: 0 errors, 4 warnings.
- Text-integrity audit: 4 warning categories, with 0 overlong heading candidates, 0 front-matter heading/body candidates, 0 inline structural marker candidates, 0 reference continuation splits, 0 suspicious large-number starts, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 59. Prefatory Note OCR blemishes and heading/body regression guard (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** The Volume 1 prefatory note heading was structurally separated, but the opening paragraph still carried PDF/OCR blemishes such as `To object of Dr. Owen...`. A later catechism prefatory note also needed protection against `PREFATORY NOTE` absorbing its all-caps subtitle and opening body paragraph.

**Fixes:**
- Added front-matter text repairs for known Prefatory Note OCR/source blemishes: `The object`, `simply vague`, `Owen`, and `first, as`.
- Broadened inline front-matter heading splitting to handle `PREFATORY NOTE.` with an optional period and preserve the heading punctuation.
- Added a chapter-only audit guard for front-matter headings that contain body text, so future volumes surface this regression mechanically.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `ch003.xhtml` now renders `<h3 class="secondary">PREFATORY NOTE</h3>` followed by `The object of Dr. Owen...`.
- Confirmed `ch047.xhtml` now renders `PREFATORY NOTE`, then the catechism subtitle, then the body paragraph, with `They were among the first, as...`.
- EPUB audit: 0 errors, 4 warnings.
- Text-integrity audit: 4 warning categories, with 0 front-matter heading/body candidates, 0 inline structural marker candidates, 0 reference continuation splits, 0 suspicious large-number starts, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 58. Sliced source sentence, verse-range continuation, and prefatory heading styling (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Visual review found:
- `Hebrews 10:19` and `22.` split across paragraphs instead of rendering as `Hebrews 10:19-22`.
- A source sentence around Nestorius and footnote 9 was sliced down to `This being the 9 declare wherein he placed...`, losing `opinion of Nestorius, revived again in the days wherein we live, I shall`.
- The `PREFACE` heading was merged into the first paragraph and styled as one large heading.

**Fixes:**
- Added scripture verse-range continuation healing so a paragraph ending in `Book N:N` followed by a numeric continuation such as `22.` is joined as a range.
- Restored the Nestorius sentence from the source wording when the font-aware extraction path drops text around the footnote overlay.
- Split inline front-matter heading prefixes such as `PREFACE It is...` into a proper heading plus body paragraph.
- Added suspicious large-number paragraph-start auditing, with sequence suppression for legitimate numbered runs.
- Added dense source-window auditing to surface possible sliced sentence interiors for triage.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `ch024.xhtml` now renders `Hebrews 10:19-22` in one paragraph.
- Confirmed `ch022.xhtml` now renders `This being the opinion of Nestorius, [fn9] revived again in the days wherein we live, I shall declare...`.
- Confirmed `ch004.xhtml` now renders `<h3 class="secondary">PREFACE</h3>` followed by a normal paragraph.
- EPUB audit: 0 errors, 4 warnings.
- Text-integrity audit: 4 warning categories, with 0 inline structural marker candidates, 0 reference continuation splits, 0 suspicious large-number starts, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

**Remaining triage:** The new dense source-window audit is intentionally broad and currently reports 93 pages for review. These are not all confirmed defects; they include legacy Greek/transliteration and spelling-normalization mismatches, but they now give us a mechanical list for finding sentence-interior losses.
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 57. Scripture-tail structural breaks and reference continuation splits (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Visual review found two remaining numeric-boundary failures:
- `Proverbs 16:4; (3.) Power` stayed in one paragraph instead of starting `(3.) Power` on its own line.
- `chap.` and `7:26` split across paragraphs around footnote 10, producing `chap.` at the end of one paragraph and `7:26...` at the start of the next.

**Fixes:**
- Narrowed the scripture-reference-tail guard so it still protects bare verse continuations but allows wrapped structural markers such as `(3.)` and `[3.]` to begin their own paragraph.
- Added reference-continuation healing for broken `chap.` / `7:26` style splits.
- Treated standalone scripture-reference fragments produced by an inline structural split as continuations of the previous paragraph instead of orphan paragraphs.
- Extended markdown-bold ordinal detection so forms like `**1st**,` are recognized as structural starts and are not rejoined to an em-dash lead-in.
- Added a text-integrity audit counter for `Reference continuation splits`, so this class of bug is now explicitly checked.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `ch020.xhtml` now has `<p><b>(3.)</b> Power...` at paragraph start.
- Confirmed `ch023.xhtml` now keeps `chap. 7:26` in the same paragraph after footnote 10.
- Confirmed `ch023.xhtml` now splits `1st` and `2ndly` into their own paragraphs after the `[3.]` lead-in.
- EPUB audit: 0 errors, 4 warnings.
- Text-integrity audit: 3 warning categories, with 0 inline structural marker candidates, 0 reference continuation splits, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

**Remaining triage:** Mechanical warnings remain for legacy Greek/Beta-code handling, Apple Books display options, weak page coverage, one top-of-page body-window warning, and five possible paragraph split candidates requiring human review.
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 56. Inline footnote placement, noteref spacing, and catechism doxology layout (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Visual review found that catechism footnote references such as `83 84 85` and `86 87 88 89 90` were rendered too tightly to tap reliably on mobile. The General Preface also showed literal `f1`, `f2`, and `f3` marker residue, with notes 2 and 3 duplicated later as a misleading `23` cluster. The catechism closing doxologies were ordinary body paragraphs instead of centered closing lines.

**Fixes:**
- Normalized AGES footnote marker variants such as `f2` and `[ f1]` before HTML conversion.
- Changed footnote conversion from paragraph-end collection to inline replacement, so each noteref appears where the PDF/source marker appears.
- Added a first-reference-wins guard so duplicated PDF overlay markers for the same note are discarded instead of being rendered again later.
- Added `.noteref` spacing, padding, and inline-block tap targets to separate adjacent footnotes on small screens.
- Restored the dropped title-page noteref for footnote 18 in Volume 1, giving all 124 endnotes a matching noteref.
- Repaired the General Preface phrase damaged by the duplicate footnote overlay around notes 2 and 3.
- Added `.doxology` styling for the catechism closing lines `Glory be to God on high!` and `To Him be all glory and honor for evermore! Amen.`
- Added EPUB audit guards for literal rendered `fN` footnote residue and noteref links missing the spacing class.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed General Preface note 1 appears after `our office.`, note 2 appears after `Dr Steven,`, and note 3 appears after `Franeker in 1700.`
- Confirmed the later General Preface paragraph no longer contains the false `2`/`3` noteref cluster and reads `treatises of Owen in volumes corresponding...`
- Confirmed catechism note clusters render as separate `<a class="noteref">` links for 83-85 and 86-90.
- Confirmed `ch025_title.xhtml` includes the title-page noteref for footnote 18 and `endnotes.xhtml` still contains its full note text.
- Confirmed `ch049.xhtml` and `ch077.xhtml` render the closing doxologies with `class="doxology"`.
- EPUB audit: 0 errors, 4 warnings, with 124 noteref links and 124 endnote anchors.
- Text-integrity audit: 3 warning categories, with 0 adjacent duplicate paragraphs, 0 inline structural marker candidates, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

**Remaining triage:** Mechanical warnings remain for legacy Greek/Beta-code handling, Apple Books display options, weak page coverage, one top-of-page body-window warning, and possible paragraph split candidates requiring human review.
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 55. Front-matter prose false headings, citation-number splits, and centered roman outline lists (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Visual review found:
- The NAV showed prefaces in title case, making `PREFACE` hard to spot beside the PDF's all-caps labels.
- Prefatory Note prose on page 20 was being misread: `Chapter 1 of the work...` and `Chapter 2 contains...` became heading/subtitle blocks instead of body paragraphs.
- Preface citation abbreviations such as `Epist. 78`, `Epist. 71`, `lib. 5 cap. 8, 9`, `Serm.`, and related forms could trigger false paragraph breaks or fake numbered paragraphs.
- Four-digit parenthesized years such as `(1717)` and `(1702)` could be mistaken for structural markers.
- Short roman outline items such as `I. In his condescension;` and `II. In his love.` were rendered as section headings, although they function as a centered list.

**Fixes:**
- Preserved all-caps front-matter labels in NAV/NCX for `GENERAL PREFACE`, `PREFATORY NOTE`, `PREFACE`, `PREFACE TO THE READER`, and `ORIGINAL PREFACE`.
- Tightened plain chapter-heading detection to uppercase `CHAPTER`, preventing prose references like `Chapter 1 of the work...` from becoming headings.
- Added a citation-abbreviation continuation guard for `cap.`, `chap.`, `lib.`, `serm.`, `sermo.`, `Epist.`, `Orat.`, `Tract.`, `Homil.`, `Haer.`, and related scholarly citation abbreviations.
- Excluded four-digit parenthesized years from the structural-marker grammar.
- Added centered `.roman-list-item` rendering for short roman outline entries after list-introducing prose, while preserving real roman section headings as `.roman-subheading`.
- Updated the text-integrity audit to recognize `.roman-list-item` as intentional list markup instead of reporting it as a roman-heading warning.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `nav.xhtml` and `toc.ncx` include all-caps `PREFACE`, `PREFATORY NOTE`, `PREFACE TO THE READER`, and `ORIGINAL PREFACE`.
- Confirmed `ch003.xhtml` keeps `Chapter 1 of the work...` and `Chapter 2 contains...` as normal paragraphs.
- Confirmed `(1717)` and `(1702)` remain inside the Prefatory Note paragraph.
- Confirmed `ch004.xhtml` keeps `Epist. 78`, `Epist. 71`, `lib. 5 cap. 8, 9`, and `lib. 1. De Fide...` inside citation paragraphs instead of promoting them to numbered paragraphs.
- Confirmed `ch031.xhtml` and `ch032.xhtml` render the reported roman outline items as `<p class="roman-list-item">...`.
- EPUB audit: 0 errors, 5 warnings. Text-integrity audit: 3 warning categories, with 0 adjacent duplicate paragraphs, 0 inline structural marker candidates, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

**Remaining triage:** Warnings remain for legacy-font Greek/Beta-code coverage, orphan endnote anchors, Apple Books display options, one top-of-page body-window warning, and broader possible paragraph split candidates.
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 54. Plain chapter headings, hidden popup footnotes, and catechism ghost-text cleanup (IMPLEMENTED — AWAITING VALIDATION)
**Problem:** Additional visual review found:
- Plain chapter headings such as `CHAPTER 15 CONFORMITY UNTO CHRIST, AND FOLLOWING HIS EXAMPLE` were not split into the same chapter-title/subtitle structure as other headings.
- Malformed markdown such as `1.** What he did...` left the number unbolded.
- The generated EPUB exposed a visible `Footnotes` chapter at the end, while footnotes should be available through noteref popups/targets without appearing as a reading-order section.
- PDF-derived footnote text could be corrupted by legacy font conversion; footnote 4 was a visible example.
- Catechism Q/A extraction retained footnote-column ghost text, duplicate scripture tails, and malformed Q/A labels.

**Fixes:**
- Added plain chapter-heading normalization so `CHAPTER N TITLE` becomes `<h3 class="secondary">CHAPTER N</h3>` plus `<h4 class="chapter-subtitle">TITLE</h4>`.
- Added a shared heading sanitizer for stray markdown emphasis markers in subtitles.
- Repaired malformed `1.**` style structural markers before bold conversion.
- Reworked ThML footnote parsing with `lxml` sibling traversal so all 124 ThML notes are captured and preferred over noisier PDF note text.
- Changed endnotes to a hidden `epub:type="footnotes"`/`role="doc-endnotes"` package resource, kept out of the spine and navigation while preserving noteref targets.
- Escaped footnote text before Greek/Hebrew tagging so note text no longer emits raw escaped `<span>` markup.
- Added catechism Q-splitting, duplicate answer-opening removal, scripture-spill filtering, lookahead removal for answer text pulled into the previous answer, repeated adjacent word-run cleanup, and source-confirmed repairs for the Chapter 18 vocation answers.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed `ch019.xhtml` renders `CHAPTER 15` and `CONFORMITY UNTO CHRIST, AND FOLLOWING HIS EXAMPLE` as separate heading/subtitle elements.
- Confirmed `ch033.xhtml` renders `<p><b>1.</b> What he did...`.
- Confirmed `endnotes.xhtml` contains clean footnote 4 text from the ThML source, no visible `<h1>Footnotes</h1>`, and no escaped language-tag artifacts.
- Confirmed `endnotes.xhtml` is present in the manifest but absent from the spine/nav.
- Confirmed the catechism Chapter 18 vocation Q/A no longer contains duplicated `church are outwardly...` ghost text or duplicated scripture-reference tails.
- EPUB audit: 0 errors, 5 warnings. Text-integrity audit: 3 warning categories, with 0 repeated word windows, 0 adjacent duplicate paragraphs, 0 inline structural marker candidates, and 0 roman heading candidates.

**Remaining triage:** Mechanical warnings remain for untagged Greek/Beta-code residue, orphan endnote anchors, Apple Books display options, weak page coverage from legacy-font source text, one top-of-page body-window warning near the catechism, and possible paragraph split candidates that require human review.
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 53. Numeric reference continuations, inline enumerators, ordinal false splits, and duplicate scripture tails (IMPLEMENTED)
**Problem:** Volume 1 still showed a cluster of extraction blemishes around small numeric markers:
- Inline enumerators such as `1st,` and `2ndly,` could remain inside a previous prose paragraph instead of starting their own paragraph.
- Reference continuations such as `verse 60` and `1 Corinthians 1:13, 15` could be split into a new paragraph because the continuation line began with a number.
- Ordinary ordinals such as `45th Psalm` could be mistaken for structural starts.
- Adjacent ghost-layer overlaps could duplicate phrase tails, as in `chap. / is expressed, chap. 3:14-16`.
- Interrupted scripture-reference lists could restart the same clause after a duplicate reference tail.
- `Ans . 1` labels needed normalization to `Ans. 1.`
- Roman subtitle suffixes such as `II.` needed to be split from all-caps chapter subtitles into their own centered subheading.
- Short lead-ins such as `For — (1.)` and markdown-bold decimal markers such as `**1.**` were not covered by the first inline-marker pass.
- Markdown-bold wrapped ordinal markers such as `**(1st,)**` and `**(3rdly,)**` were still not promoted.
- Plain decimal markers after prose lead-ins, such as `two ways: — 1. Absolutely... 2. In...`, needed promotion without breaking scripture references.
- Roman numerals used as summary-list labels after introductions such as `four heads:` needed to remain list items, not centered subsection headings.

**Fixes:**
- Refined the structural-marker grammar so real list markers are protected while ordinary ordinals like `45th Psalm` are not treated as paragraph starts.
- Added inline structural marker splitting for bare, bracketed, parenthesized, and markdown-bold enumerators.
- Added numeric continuation healing for `verse`, `verses`, `chap.`, `chapter`, and scripture-reference tails.
- Added overlap trimming between adjacent lines/paragraphs to collapse repeated tails before joining continuations.
- Added an interrupted duplicate-clause guard for scripture-reference-heavy ghost tails.
- Normalized `Ans . N` answer labels during text cleaning.
- Split trailing roman subtitle suffixes such as `II.` into a centered `.roman-subheading`.
- Styled `.roman-subheading` with centered text and `break-after/page-break-after: avoid` so roman sub-subheadings stay attached to the paragraph that follows.
- Added a stricter audit tripwire for any paragraph break after non-terminal punctuation, inline structural marker candidates, and roman numeral headings left in body paragraphs.
- Added multi-paragraph lookback for duplicated leading scripture-reference runs such as `Galatians 2:20; Ephesians 5:2, 25, 26; 1 John 3:16;`.
- Added guarded plain-decimal promotion for structural cases like `two ways: — 1. ... 2. ...`, with scripture/citation exceptions for forms like `1 Corinthians 1:13, 15`, `Revelation 2, 3`, `verse 60`, and `lib. 5 cap. 8, 9`.
- Added roman-list coalescing for sequences introduced by `heads:`, `ways:`, `parts:`, `sorts:`, or `things:`. These render as `<p><b>I.</b> Honor.</p>` style list paragraphs, while later roman numerals that introduce full sections still render as centered `.roman-subheading` elements.

**Validation checks run:**
- Regenerated Volume 1 only with `.venv/bin/python3 converter.py 1`.
- Confirmed generated XHTML has `verse 60`, `1 Corinthians 1:13, 15`, `chap. 3:14- 16`, `The title of the 45th Psalm`, separate `<p><b>1.</b> ...</p>`, separate `<p><b>2.</b> ...</p>`, separate `<p><b>(1.)</b> ...</p>`, separate `<p><b>(1st,)</b> ...</p>`, separate `<p><b>(3rdly,)</b> ...</p>`, separate `<p><b>1st</b>, ...</p>`, separate `<p><b>2ndly</b>, ...</p>`, `Ans. 1.`, and centered roman headings such as `<h4 class="roman-subheading">III.</h4>`.
- Confirmed the Chapter 9 summary list now renders as `<p><b>I.</b> Honor.</p>`, `<p><b>II.</b> Obedience.</p>`, `<p><b>III.</b> Conformity.</p>`, and `<p><b>IV.</b> The use we make...</p>`, while the following section-opening `I.` remains `<h4 class="roman-subheading">I.</h4>`.
- Confirmed `which is predominant and efficacious ... Christ is precious But, on the other hand` is no longer split into two paragraphs.
- Confirmed the duplicated leading `Galatians 2:20; Ephesians 5:2, 25, 26; 1 John 3:16;` prefix before `They know nothing...` is removed.
- `scripts/audit_epub.py volumes/v1/output/volume_1.epub`: 0 errors, 6 warnings requiring later triage.
- `scripts/audit_text_integrity.py 1`: 0 missing top-of-page body windows, 0 missing enumerator marker forms, 0 enumerator sequence candidates, 0 adjacent duplicate paragraphs, 0 inline structural marker candidates, and 0 roman heading candidates. Remaining broader triage queues: 26 weak page matches, 91 possible paragraph split candidates, and 2 repeated word windows.

**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 52. Top-of-page enumerator clipping and missing `[1.]` before `[2.]` (IMPLEMENTED)
**Problem:** In Chapter 9, the PDF source page beginning with `[1.] With the same honor...` was extracted through the font-aware path because the page contained Greek text. The top-margin filter clipped the first two body lines, so the EPUB jumped from the previous paragraph into "give glory..." and then showed `[2.]`, making it look as if `[1.]` had never been extracted.
**Fixes:**
- Lowered the font-aware top cutoff from 65pt to 40pt and added explicit top-band filtering for page numbers/running headers instead of body text.
- Added bracketed/parenthesized ordinal forms such as `[1st,]` and `(1st,)` to structural-start guards.
- Added automatic bolding for paragraph-opening structural markers such as `[1.]`, `[2.]`, `[1st,]`, `(1.)`, and `5.`.
- Added an enumerator-integrity check to the textual audit that compares bracketed/parenthesized marker forms between the PDF and EPUB and flags sequence jumps.
- Added a top-of-page body-window check to catch future clipping of first body lines after page headers/numbers.
- Regenerated Volume 1 only. `EPUB/ch013.xhtml` now contains `<b>[1.]</b> With the same honor...`, `<b>[2.]</b> In the same manner...`, and `<b>[1st,]</b> that their thoughts...`.
- Latest Volume 1 text audit reports 0 missing top-of-page body windows, 0 missing enumerator marker forms, and 0 enumerator sequence candidates.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 51. Chapter subtitles merged into opening body paragraphs and scripture-reference ghost duplicates (IMPLEMENTED)
**Problem:** Chapter subtitles such as "THE PERSON OF CHRIST THE GREAT REPOSITORY OF SACRED TRUTH — ITS RELATION THEREUNTO" were being emitted inside the first body paragraph instead of as separate subtitle headings. Nearby scripture-reference ghost text was also leaking as duplicate inline phrases or standalone reference paragraphs.
**Fixes:**
- Added `_split_leading_chapter_subtitle()` so leading bold all-caps chapter subtitles are separated into `<h4 class="chapter-subtitle">`.
- Added `.chapter-subtitle` CSS in `shared.py`.
- Added paragraph post-processing to remove duplicated opening clauses and duplicate scripture-reference tails.
- Added scripture-reference fragment detection so standalone reference-only paragraphs are dropped when the same references already appear in the previous paragraph.
- Regenerated Volume 1. Chapter 6 now has a separate subtitle heading and the highlighted duplicate "So we are said..." / repeated reference tail is removed.
- Current Volume 1 output contains 59 detected `chapter-subtitle` headings.
**Remaining triage:** The textual-integrity audit still reports two repeated word windows elsewhere and three split candidates tied to footnote/page-number residue.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 50. Textual integrity audit and holistic paragraph healing enforcement (IMPLEMENTED)
**Problem:** Automated review showed that some body text was still being split at extraction boundaries, especially in early sections that were bypassing the paragraph healer. The first textual-integrity audit found 817 possible paragraph split candidates before converter-side cleanup.
**Fixes:**
- Added `scripts/audit_text_integrity.py` to compare source PDF text against generated EPUB text and flag weak page coverage, duplicate paragraphs, repeated phrase windows, and likely faulty paragraph splits.
- Updated `get_pages_text()` so it merges all raw text in a chapter/range before cleaning and paragraph reconstruction.
- Updated `reconstruct_paragraphs()` so blank extraction separators no longer force a paragraph break after non-terminal text.
- Forced normal chapter body extraction through the paragraph healer, while preserving the separate title/TOC front-matter path.
- Added structural-start guards for legitimate Owen paragraph starts, including `5.`, `(1.)`, `[1.]`, roman numerals, catechism `Q.`/`A.`, ordinal labels such as `2ndly`, and discourse labels such as `First,`/`Secondly,`.
- Regenerated Volume 1 and reran textual integrity checks. Possible paragraph split candidates dropped from 817 to 3, adjacent duplicate paragraphs dropped from 5 to 0, and approximate PDF-to-EPUB content-word coverage is 0.9854.
- Latest audit excluded 57 structural starts from false split warnings.
**Remaining triage:** Three paragraph split candidates remain, all tied to footnote/page-number residue in catechism-style material. Weak page matches remain partly because the PDF extraction contains legacy Greek transliteration/encoding that the EPUB converts to Unicode.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 49. Ghost layer duplication spans across line breaks (IMPLEMENTED)
**Problem:** Previous de-duplication only checked sequential lines. Ghost layers in AGES PDFs often duplicate phrases *across* line breaks or within a single wrapped line (e.g., "Acts 20:28-31; Acts 20:28-31;").
**Fixes:**
- Implemented `remove_repeated_phrases()`: A sliding-window algorithm that detects and prunes sequential identical phrases (15+ chars) within a single text block.
- Integrated this into the global `clean_text()` path to ensure it runs after headers are stripped and before paragraph healing.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 48. EPUB lacks premium "Goold/AGES" visual layout on structural pages (IMPLEMENTED)
**Problem:** Title pages and TOCs were being flattened into standard text, losing the majestic centering and alignment of the original Goold/AGES editions.
**Fixes:**
- **Visual Geometry Layer:** Re-implemented `detect_page_type()` to categorize pages into TITLE, TOC, or BODY before extraction.
- **Zone-Aware Processing:**
    - **TITLE Zone:** Uses `extract_title_page()` to map large PDF fonts to `<h1>` and `<h2>` while stripping AGES boilerplate. Enforces centering via CSS.
    - **TOC Zone:** Detects line-end page numbers and applies a flex-box style (`.toc-line`) to align titles left and page numbers right.
    - **BODY Zone:** Applies "Semantic Reflow" rules, joining lines only if they don't end in terminal punctuation.
- **Global Styling:** Updated `shared.py` with specific rules for `.titlepage` majesty (Small-caps, Blue/Green colors) and `.toc-line` alignment.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 44. Textual duplication (ghost layers) in PDF causing repeated fragments (IMPLEMENTED)
**Problem:** Some pages in the AGES PDF contain "ghost" text layers (e.g., invisible search layers or redundant vector drawing operations) that cause the same sentence to be extracted twice.
**Fixes:**
- Implemented `deduplicate_lines()`: A sequence-aware filter that detects if the same line (or a near-identical fuzzy match) appears twice in a row.
- Integrated de-duplication into both the font-aware extraction (`extract_page_text_with_fonts`) and the regular block extraction (`get_merged_page_text`).
- Created a `scripts/health_audit.py` tool to "guarantee" integrity by comparing word counts and phrase repetitions across the entire volume, flagging any page with high duplication or loss for manual review.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 43. Blockquotes are not indented and contain artificial breaks (REVERTED)
**Problem:** Long, indented quotes in the PDF were being extracted as standard paragraphs and sometimes broken mid-sentence due to capital letters following periods.
**Status:** REVERTED. The attempt to fix this via manual coordinate analysis caused regressions in heading detection and styling across multiple volumes. The project has reverted to PyMuPDF4LLM's stable structural extraction.


### 42. Text is broken up mid-sentence (paragraph fragmentation) (IMPLEMENTED)
**Problem:** Text is frequently broken into small, fragmented paragraphs, especially at page boundaries or where running headers were stripped.
- `reconstruct_paragraphs()` was running per-page, causing a mandatory paragraph break at every page junction.
- The logic for joining lines was too conservative and failed on some common punctuation patterns (like single quotes or mid-sentence capitalized words).
- Blank lines left by stripped headers/footers were forcing paragraph breaks.
**Fixes:**
- Modified `get_pages_text()` to merge the raw text of all pages in a section *before* running the reconstruction logic, allowing seamless healing across page boundaries.
- Refined `reconstruct_paragraphs()` to be more robust:
    - Automatically join any line that doesn't end in terminal punctuation (`.`, `!`, `?`, `:`, or terminal quotes).
    - Added support for single quotes in terminal punctuation checks.
    - Improved detection of list items and headings to avoid false-positive joins.
    - Specifically handle the junction between pages by stripping any residual whitespace or blank lines that shouldn't be there.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 41. PREFATORY NOTE and PREFACE badly extracted and formatted (IMPLEMENTED)
**Problem:** Front matter sections like PREFATORY NOTE (page 20) and PREFACE (page 22) were being treated as `title_page` instead of standard chapters.
- This triggered the centered line-by-line layout, which is inappropriate for full pages of body text.
- It also caused content fragmentation between the "title" file and the "body" file.
**Fixes:**
- Refined `detect_page_type()` mixed-mode fallback to require a larger font (>18pt) and lower character count (<2000), effectively filtering out standard chapter starts like PREFATORY NOTE (16pt).
- Updated standard `h2` and `h3` styling in `shared.py` to be centered by default, ensuring chapter-like headings match the project aesthetic.
- Updated `markdown_to_html()` to apply the `.secondary` class to `h2` and `h3` headings for consistent color branding.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 40. Title pages lack premium color and typography design (IMPLEMENTED)
**Problem:** The generated title pages (main and treatise) were plain and lacked the visual hierarchy and aesthetic appeal of high-end theological publications.
**Fixes:**
- Updated `shared.py` with premium CSS classes: `.primary` (Blue), `.secondary` (Green), `.descriptive` (Italics), and `.separator` (Bold small-caps).
- Overhauled `format_title_page()` in `converter.py` with heuristics to apply these classes based on font size and line length.
- Main titles (20pt+ or short 15pt+) are now Blue (`h1.primary`).
- Secondary titles (15pt+) are now Green (`h2.secondary`).
- Descriptive paragraphs are now italicized (`p.descriptive`).
- Structural separators (OR, OF, WITH) are now centered and bold (`h3.separator`).
- Updated `_build_title_page()` for consistency across the main book title page.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 39. TOC (pages 3-6) fragmented and formatting doesn't match PDF (IMPLEMENTED)
**Problem:** The Table of Contents in Volume 1 (pages 3-6) was handled poorly:
- Only the first page was detected as a TOC.
- Extraction was fragmented into separate files.
- Formatting (centering, bolding, hanging indents) was lost.
**Fixes:**
- Enhanced `detect_page_type()` with a heuristic to identify multi-page TOCs by item frequency.
- Updated front matter loop in `process_owen_volume()` to merge consecutive TOC pages.
- Overhauled `build_toc_page_xhtml()` to use block-level dictionary metadata, preserving centering for headings and applying `ContentsItem` styling with bold labels for list items.
- Filtered out standalone page numbers from the extracted content.
**Status:** IMPLEMENTED (AWAITING VALIDATION)


### 25. Footnote False Positives (IMPLEMENTED)
**Problem:** Plain numbers (like "4" in "Psalm 48") were misidentified as footnotes.
**Fix:** Overhauled `inject_footnote_links` to strictly require the `f` prefix (e.g., `f1`, `f2`) used in AGES PDFs. The "f" is automatically stripped in the final display.
**Status:** IMPLEMENTED (AWAITING VALIDATION)

...
### 38. Missing treatises: Part 2, Meditations Applied, Two Short Catechisms (IMPLEMENTED)
**Problem:** Three treatise-level sections were missing or incomplete due to detection failures on shared pages.
**Fixes:**
- Updated `detect_page_type()` to handle mixed title+body pages by checking for large font in early blocks.
- Added duplicate title detection in the chapter loop to skip redundant `_title.xhtml` files.
- Implemented `shares_page` logic to include shared first pages in the following chapter's body while using `limit_to_title` for the structural entry.
**Status:** IMPLEMENTED (AWAITING VALIDATION)

---















































































<!-- AUTO_AUDIT_START -->
## Automated EPUB Audit

**Last run:** 2026-06-03T11:37:15.167714+00:00
**EPUB:** `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/master/volumes/v3/output/volume_3.epub`
**Status:** WARN (0 errors, 1 warnings)

Reports:
- `volume_3_audit.json`
- `volume_3_audit.md`

| Check | Result |
|-------|--------|
| OPF version | 3.0 |
| XHTML files | 47 |
| Spine items | 45 |
| Embedded fonts | 15 |
| NAV links | 48 |
| Greek chars / untagged | 4318 / 0 |
| Hebrew chars / untagged | 1620 / 0 |
| Noteref links / endnote anchors | 299 / 299 |
| AGES boilerplate hits | 0 |
| Possible Beta Code files | 0 |
| Escaped language-tag files | 0 |
| Empty bracket noise files | 0 |
| Repeated phrase hits | 3 |

Warnings requiring triage:

- `repeated_phrases`: Potential repeated phrases detected

**Status note:** Automated audit findings are not user validation. Keep related fixes as `IMPLEMENTED (AWAITING VALIDATION)` until explicitly approved.
<!-- AUTO_AUDIT_END -->

---




















































































## Issue 128 — V3 Blemishes 9-15 Shared Structural Cleanup

**Date:** 2026-05-20  
**Status:** IMPLEMENTED (AWAITING VALIDATION)

Implemented shared fixes for the V3 issue 9-15 blemish family:

- Chapter-opening summaries now keep em-dash and Greek synopsis continuations inside `chapter-summary`, while body openers such as `THE...`, `WE...`, and `Secondly, THE...` start normal body/list paragraphs.
- ANALYSIS spillover is repaired at render time when the previous front-matter sentence tail is accidentally captured before the `ANALYSIS` heading.
- Bracketed word ordinals such as `[SECONDLY],` are recognized as list markers and rendered at the start of their own paragraph.
- Inline bold decimal lists split correctly after emphasized punctuation, fixing the `1. Of sanctifying grace; 2. Of especial gifts; 3. ...` pattern.
- Residual AGES source ids such as `[4611605]` and `[19B9105]` are removed only when directly prefixing scripture locators.
- Spaced and fragmented ordinal OCR forms such as `1 st .`, `2 dly .`, and `**[1** _**st**_ **.]**` normalize into clean structural markers.
- `chap.` / `chapter` paragraph breaks before `16:5-15` and `9:8` are merged before rendering.
- Audit coverage now includes residual AGES artifact counts, flat ANALYSIS chapters, and missing configured font checks in the bug-regression report.

Validation:

- Rebuilt V3 with `.venv/bin/python3 volumes/v3/convert.py --render-only`.
- EPUB audit: WARN, 0 errors; untagged Greek `0`, untagged Hebrew `0`, unprocessed AGES markers `0`.
- Text integrity audit: WARN; reference continuation splits `0`, residual AGES artifacts `0`, flat ANALYSIS chapters `0`, font issues `0`, missing Greek clauses `0`, missing Hebrew clauses `0`.
- Bug-regression report: PASS.
- V3 regression tests: `40 passed, 8 skipped`.

















<!-- TEXT_INTEGRITY_START -->
## Automated Textual Integrity Audit

**Last run:** 2026-06-03T11:37:54.228813+00:00
**Status:** WARN (9 warnings)

Reports:
- `volume_3_text_integrity.json`
- `volume_3_text_integrity.md`

| Check | Result |
|-------|--------|
| PDF pages | 789 |
| EPUB text files | 45 |
| EPUB paragraphs/headings | 2498 |
| Approximate PDF-to-EPUB word coverage | 0.9853 |
| Weak page matches | 13 |
| Dense source windows checked | 812 |
| Missing dense source-window pages | 783 |
| Front CONTENTS pages checked | 6 |
| Missing front CONTENTS pages | 0 |
| Top-of-page body windows checked | 766 |
| Top-of-page windows skipped as unstable | 31 |
| Missing top-of-page body windows | 0 |
| Bottom-of-page body windows checked | 748 |
| Bottom-of-page windows skipped as unstable | 0 |
| Missing bottom-of-page body windows | 5 |
| Possible faulty paragraph splits | 161 |
| Structural starts excluded from split warnings | 304 |
| Short fragments | 12 |
| Adjacent duplicate paragraphs | 0 |
| Inline structural marker candidates | 14 |
| Reference continuation splits | 0 |
| Citation continuation splits | 0 |
| Suspicious large-number starts | 0 |
| Roman heading candidates | 0 |
| Overlong heading candidates | 0 |
| Front-matter heading/body candidates | 0 |
| Repeated word windows | 25 |
| PDF enumerator markers | 626 |
| EPUB enumerator markers | 797 |
| Missing enumerator marker forms | 0 |
| Enumerator sequence candidates | 65 |
| PDF Greek words / EPUB Greek words | 809 / 815 |
| Greek word coverage ratio | 0.9936 |
| PDF Hebrew words / EPUB Hebrew words | 238 / 235 |
| Hebrew word coverage ratio | 0.958 |
| Missing Greek clauses | 1 |
| Missing Hebrew clauses | 5 |

Warnings requiring triage:

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB
- `missing_hebrew_clauses`: Some dense Hebrew passages from the PDF are missing from the EPUB

**Status note:** This audit is a mechanical integrity screen, not final proofreading or user validation.
<!-- TEXT_INTEGRITY_END -->
