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

---

## Issue Details

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
