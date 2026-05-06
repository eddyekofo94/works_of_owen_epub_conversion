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
- `<p class="publisher">Banner of Truth Trust</p>` — pushed to bottom with `margin-top: auto`
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

### 14. NAV Title Splitting Creates Hierarchy (Fixed)
**Problem:** Combined titles like "A DECLARATION... CHAPTER 1" were on one line with `<br/>`.
**Fix:** `_split_nav_title()` now returns a tuple `(treatise, chapter)`. The TOC-building loop emits two entries at different levels: parent (treatise) at `toc_level` and child (chapter number) at `toc_level + 1`. Also fixed false positive splits when preceded by em-dash.

### 15. Footnote Reference Font Size (Fixed)
**Problem:** `a.footnote-ref` font-size was 0.75em, too small to read comfortably.
**Fix:** Changed to 0.95em in both occurrences in shared.py. Also fixed stale `#0066cc` → `#0000EE`.

### 16. ΧΡΙΣΤΟΛΟΓΙΑ on Wrong Page (Fixed)
**Problem:** In the printed book, "ΧΡΙΣΤΟΛΟΓΙΑ" appears on its own page as the Greek treatise heading. In the ThML extraction (volume_1.thml.xml line 280), it was placed in the same `<p>` as "W. H. G. Edinburgh, August 1850." at the end of ch004 (GENERAL PREFACE).

**Fix:** Modified the ThML source (volumes/v1/intermediate/volume_1.thml.xml):
- Removed Greek word from editor signature paragraph in ch004
- Added `<h2>ΧΡΙΣΤΟΛΟΓΙΑ</h2>` as first heading in ch005 (before h1)

Updated `_build_treatise_title()` in converter.py to detect and render Greek h2 headings.
Added `.treatise-title h2.greek` CSS in shared.py (1.8em, Greek font, letter-spacing).

**Result:** ch005 now renders with Greek heading at top, followed by English "CHRISTOLOGIA" title.

---

## Remaining Work

| Issue | Priority | Notes |
|-------|----------|-------|
| page-list nav for footnotes | Medium | Not yet implemented — requires page-number references in ThML |
| ThML source data gaps | Low | Volumes 2–16 have fewer footnotes paragraphs than fnref links |

---

## History

- **2026-05-05**: Initial bugs identified from reference EPUB comparison
- **2026-05-05**: Fixed portrait, frontispiece, cover format, NAV structure, spine order, id="creator"
- **2026-05-05**: Fixed footnotes — fnref→noteref conversion, endnotes chapter generation
- **2026-05-05**: Fixed portrait randomization, OPF manifest, title page design, NAV title splitting, CSS alignment, noteref color, duplicate footnote rules
- **2026-05-05**: Fixed hierarchical NAV level assignment and XML validity in generate_nav_xhtml()
- **2026-05-05**: Fixed combined treatise/chapter headings in XHTML body content (e.g., Chapter 1 now shows separate H1/H2)
- **2026-05-05**: Fixed incomplete "CONTENTS OF VOLUME 1" page in ThML; reconstructed 20 missing chapter entries by extracting from chapter headings.
- **2026-05-05**: Extracted chapter subtitles from body text and appended them to "CHAPTER X" entries in the NAV menu (e.g., "Chapter 2 - Opposition Made...").
- **2026-05-05**: Removed redundant Roman numeral entries (I., II., etc.) from the NAV menu to provide a cleaner Table of Contents.
- **2026-05-05**: Fixed garbled NAV subtitles like "II. 1St" by improving list-marker filtering (regex) to catch (1st,), (2dly,), etc. in body text.