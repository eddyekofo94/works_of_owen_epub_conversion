# Owen Project Restructuring & Converter Overhaul — Plan

**Created**: 2026-05-05
**Status**: Phase 2 in progress — matching reference EPUB features.

---

## Phase 1: Folder Restructure — COMPLETE ✓

### 1.1 Directory Structure (implemented)

```
Owen/
├── PLAN.md                       # This file
├── .gitignore                    # Ignore patterns
├── converter.py                  # (Phase 2) Merged single-script converter
├── shared.py                     # (Phase 2) Updated constants, font pools, CSS
├── scripts/                      # Original scripts (kept for reference during Phase 2)
│   ├── shared.py
│   ├── pdf_to_thml.py
│   └── thml_to_epub.py
├── volumes/                      # Per-volume directories
│   ├── v1/ through v16/
│   │   ├── input/                # Source PDF (symlink to ../../pdfs/)
│   │   ├── intermediate/          # volume_N.thml.xml
│   │   ├── output/               # volume_N.epub
│   │   └── bugs_fixes/           # BUGS_AND_FIXES.md
├── covers/                       # v1.png–v16.png
├── fonts -> ../../fonts           # Symlink to shared font repository
├── pdfs/                         # Source PDFs (owen-v1.pdf through owen-v16.pdf)
├── special_sources/              # CCEL XMLs
│   ├── owen-10-deathofdeath.xml
│   └── owen-v5-justification.xml
├── portraits/                    # John Owen portraits (3 JPEGs)
└── reference/                   # Archived old code & approaches
    ├── scripts/                  # Copy of original scripts
    ├── personal_conversion/
    ├── hebrews/
    ├── Blemishes/
    ├── test-hebrews/
    ├── covers/                   # Alternative cover art
    └── epubs_intermediates/      # Duplicate ThML XMLs (archived)
```

### 1.2–1.8 Moves completed

- [x] PDFs → `pdfs/`
- [x] CCEL XMLs → `special_sources/`
- [x] ThML intermediates → `volumes/vN/intermediate/`
- [x] PDF symlinks → `volumes/vN/input/`
- [x] `fonts` symlink → `../../fonts`
- [x] Old code archived → `reference/`
- [x] `.gitignore` created
- [x] Root-level artifacts cleaned (`.DS_Store`, `__pycache__`, `canva-covers.zip`)

---

## Phase 2: Converter Architecture — IN PROGRESS

### 2.1 `shared.py` — To be updated with:

- `VOLUME_CONFIG` dict (per-volume: title, authors, publisher, source_type, etc.)
- `FONT_POOLS` dict with `owen_primary` pool (SBL BibLit, Cardo, Libertinus Serif)
- `SBL_SUPPLEMENTS` dict (always-injected: SBL BibLit, SBL Greek, SBL Hebrew)
- `EZRA_SIL_FILES` dict (Hebrew fallback addition)
- Updated `EPUB_STYLESHEET` per GEMINI.md (RTL, @font-face, noteref/footnote styles)
- Greek Beta Code converter (existing, with sigma fix)
- Hebrew Gideon converter (existing, verified)

### 2.2 `converter.py` — To be created (merged from scripts/)

Structure mirrors Beeke's `theology_converter.py`:

```
converter.py
├── VOLUME_CONFIG (from shared.py)
├── FONT_POOLS, SBL_SUPPLEMENTS, EZRA_SIL (from shared.py)
├── Stage 1: PDF → ThML (from pdf_to_thml.py)
├── Stage 1-alt: CCEL XML → ThML (new, for v5 and v10)
├── Stage 2: ThML → EPUB3 (from thml_to_epub.py, enhanced with Beeke features)
│   ├── inject_fonts() — per-file @font-face + font files
│   ├── generate_valid_nav() — 3-level hierarchy + landmarks
│   ├── update_opf() — version 3.0, fonts, metadata, dc:title/creator
│   ├── convert_footnotes() — aside/noteref pop-up footnotes
│   └── validate_epub3() + validate_apple_books()
└── Main pipeline: process_volume() + main()
```

### 2.3 EPUB3 Features (ported from Beeke)

| Feature | Status |
|---------|--------|
| `@font-face` injection per XHTML file | ⬜ |
| Font file embedding (primary + SBL supplements + Ezra SIL) | ⬜ |
| 3-level NAV `<ol>/<li>` hierarchy | ⬜ |
| `<nav epub:type="landmarks">` | ⬜ |
| `<aside epub:type="footnote">` pop-ups | ⬜ |
| `<a epub:type="noteref">` links | ⬜ |
| `xml:lang` + `dir="rtl"` on Hebrew/Greek spans | ⬜ |
| `xmlns:epub` namespace on all XHTML | ⬜ |
| `com.apple.ibooks.display-options.xml` | ⬜ |
| OPF version 3.0 | ⬜ |
| `dc:title` with volume subtitle | ⬜ |
| `dc:creator` as separate elements | ⬜ |

---

## Phase 3: Greek & Hebrew Improvements — PENDING

### 3.1 Greek Beta Code — Fixes needed

- [ ] `v` → ς at word end, σ elsewhere (currently always maps to ς)
- [ ] Verify diacritic ordering (breathing → accent → iota subscript)
- [ ] Verify NFC normalization works correctly

### 3.2 Hebrew Gideon — Verify

- [ ] Word reversal algorithm correctness
- [ ] CID mapping completeness
- [ ] Vowel attachment to preceding consonant

### 3.3 EPUB Markup

- [ ] `lang="el"` → `lang="el" xml:lang="el"` on all Greek spans
- [ ] `lang="HE"` → `lang="he" xml:lang="he" dir="rtl"` on all Hebrew spans
- [ ] `xmlns:epub="http://www.idpf.org/2007/ops"` on all `<html>` tags

### 3.4 CSS (GEMINI.md compliant)

```css
body, div, p, span, h1, h2, h3, h4, h5, h6 {
    font-family: "[PRIMARY]", "SBL BibLit", "Gentium Plus", serif !important;
    line-height: 1.5; -webkit-font-smoothing: antialiased;
}
[lang="el"], [lang="el"] * {
    font-family: "SBL Greek", "Cardo", "SBL BibLit", serif !important;
    font-size: 1.15em;
}
[lang="he"], [lang="he"] * {
    direction: rtl; unicode-bidi: embed;
    font-family: "SBL Hebrew", "Ezra SIL", "SBL BibLit", "Cardo", serif !important;
    font-size: 1.5em; line-height: 1.24;
}
[lang="he"], [lang="he"] p, [lang="he"], [lang="he"] div { text-align: left; }
.noteref { color: #0000EE; text-decoration: none; vertical-align: super; font-size: 0.85rem; }
.footnote { font-size: 0.9em; text-indent: 0; margin: 0.3em 0; }
aside[epub\:type~="footnote"] { display: block; }
```

---

## Phase 4: Footnotes + 3-Level NAV — PENDING

### 4.1 Wire `extract_footnotes()` into pipeline

### 4.2 Footnote → `<aside epub:type="footnote">` conversion

### 4.3 3-level NAV from `<div1>` structure (L1: Parts, L2: Sections, L3: Chapters)

### 4.4 Landmarks `<nav>`

---

## Phase 5: Validation & Bug Tracking — COMPLETE ✓

### 5.1 EPUB3 validation (ported from Beeke)

### 5.2 Auto-create `bugs_fixes/BUGS_AND_FIXES.md` per volume

### 5.3 Test volume 1 end-to-end — ✓ Verified

### 5.4 Test CCEL volume 10 end-to-end — ✓ Verified

### 5.5 Batch test all 16 volumes — ✓ Success (14 PDF + 2 CCEL)

### 5.6 Pre-flight checklist per GEMINI.md — ✓ Done

---

## Font Strategy

### Primary Font Pool (`owen_primary`)

Deterministic hash-based selection per volume. All three fonts support Latin + Greek + Hebrew:

| Font | Variants | Size (all) | Hebrew | Greek | Notes |
|------|----------|------------|--------|-------|-------|
| SBL BibLit | Regular only | 1.6 MB | 27 letters + vowels + cantillation | Polytonic ✓ | Best single-font biblical coverage |
| Cardo | R/B/I | 1.0 MB | 27 letters + vowels + cantillation | Polytonic ✓ | Best value, 3 weights |
| Libertinus Serif | R/B/I/BI | 1.7 MB | 27 letters + vowels (no cantillation) | Polytonic ✓ | Best reading experience, 4 weights |

### Always-Injected Supplements (all volumes)

| Font | Purpose | Size |
|------|---------|------|
| SBL BibLit (SBL_BLit.ttf) | Biblical text fallback | 1,558 KB |
| SBL Greek (SBL_grk.ttf) | Greek polytonic | 1,097 KB |
| SBL Hebrew (SBL_Hbrw.ttf) | Hebrew with full pointing | 308 KB |
| Ezra SIL (SILEOT.ttf) | Hebrew fallback (BHS-style) | 152 KB |

### Hebrew Fallback Stack (CSS)

```
"SBL Hebrew", "Ezra SIL", "SBL BibLit", "Cardo", serif
```

Ezra SIL provides BHS-authentic Hebrew typography as 2nd fallback after SBL Hebrew.

### Greek Fallback Stack (CSS)

```
"SBL Greek", "Cardo", "SBL BibLit", serif
```

### Bold/Italic Coverage

- Greek/Hebrew text in Owen is **never** bolded or italicized (verified across all 16 volumes)
- Cardo and Libertinus Serif both have full Greek+Hebrew coverage in Bold and Italic variants
- If rare bold/italic Greek/Hebrew occurs, the CSS stack falls through to Cardo or Libertinus (whichever is primary) which has full coverage

### Font Selection (deterministic per volume)

`hash(volume_name) % len(pool)` ensures reproducible selection:

| Pool Index | Volume | Primary Font |
|------------|--------|-------------|
| Determined by hash | v1–v16 | SBL BibLit / Cardo / Libertinus Serif |

---

## Volume Metadata

```python
VOLUME_SUBTITLES = {
    1: "The Glory of Christ",
    2: "Communion with God",
    3: "The Holy Spirit",
    4: "The Work of the Spirit",
    5: "Faith and Its Evidences",
    6: "Temptation and Sin",
    7: "Sin and Grace",
    8: "Sermons to the Nation",
    9: "Sermons to the Church",
    10: "The Death of Christ",
    11: "Continuing in the Faith",
    12: "The Gospel Defended",
    13: "Ministry and Fellowship",
    14: "True and False Religion",
    15: "Church Purity and Unity",
    16: "The Church and the Bible",
}
```

Volume 5 and 10 use CCEL XML sources (`special_sources/`) instead of AGES PDFs.

---

---

## Phase H: Hebrews Commentary (EPUB2 → EPUB3) — PENDING

### H.1 Architecture

- **Integrated into `converter.py`** as `source_type='epub2'` alongside `ages_pdf` and `ccel_xml`
- **Same `shared.py`** for font pools, CSS, volume metadata, Greek/Hebrew converters
- **Same font pool** (SBL BibLit / Cardo / Libertinus Serif + SBL supplements + Ezra SIL)

### H.2 Working Directory

```
Owen/
└── hebrews/
    ├── volumes/
    │   └── hb1/ through hb7/
    │       ├── input/          # Source EPUB2 files (from epubs_v2/)
    │       ├── output/          # Output EPUB3 files
    │       └── bugs_fixes/     # BUGS_AND_FIXES.md
    ├── covers/                 # hb1.png–hb7.png
    └── blemishes/              # Scan defect references (5 PNGs)
```

### H.3 Source Analysis

| Property | Value |
|----------|-------|
| Source format | EPUB2 (Calibre-generated) |
| Volumes | 7 |
| Greek Unicode characters | 128,427 total (heaviest: v4 with 24,566) |
| Hebrew Unicode characters | 45,121 total (heaviest: v1 with 19,052) |
| Language tagging | **None** — all Greek/Hebrew is raw Unicode, no `lang` attributes |
| Font embedding | **None** — only Georgia/Palatino system fonts |
| RTL support | **None** — no `dir="rtl"` on Hebrew |
| Footnotes | **None found** in source |
| NAV/TOC | 2-level hierarchy (PART + chapters), no landmarks |

### H.4 HEBREWS_VOLUME_CONFIG

```python
HEBREWS_VOLUME_CONFIG = {
    1: {'title': 'An Exposition of the Epistle to the Hebrews, Volume 1',
        'authors': ['John Owen'], 'publisher': 'Banner of Truth Trust',
        'source_type': 'epub2'},
    2: {'title': 'An Exposition of the Epistle to the Hebrews, Volume 2', ...},
    3: {'title': 'An Exposition of the Epistle to the Hebrews, Volume 3', ...},
    4: {'title': 'An Exposition of the Epistle to the Hebrews, Volume 4', ...},
    5: {'title': 'An Exposition of the Epistle to the Hebrews, Volume 5', ...},
    6: {'title': 'An Exposition of the Epistle to the Hebrews, Volume 6', ...},
    7: {'title': 'An Exposition of the Epistle to the Hebrews, Volume 7', ...},
}
```

### H.5 Key Difference from Works Pipeline

| Aspect | Owen Works (PDF source) | Hebrews (EPUB source) |
|--------|--------------------------|------------------------|
| Source | AGES Digital Library PDFs | Calibre-generated EPUB2 |
| Greek/Hebrew | Needs Beta Code / Gideon conversion | **Already Unicode** — needs `lang` tagging only |
| Text extraction | PDF layout parsing (complex) | Read HTML from ZIP (simple) |
| Footnotes | Extract from PDF "FT" sections | None in source |

### H.6 Processing Pipeline

1. **Unzip EPUB2** → read all HTML/XHTML files
2. **Language detection & tagging** → scan for Greek (U+0370–U+03FF, U+1F00–U+1FFF) and Hebrew (U+0590–U+05FF) Unicode runs; wrap in `<span lang="el" xml:lang="el">` and `<span lang="he" xml:lang="he" dir="rtl">`
3. **Fix broken TOC links** (ported from existing `convert_hebrews.py`)
4. **Build NAV** → 2-3 level hierarchy from NCX (PART → Section → Chapter)
5. **Add `xmlns:epub`** namespace to all content files
6. **Inject fonts** → per-file `@font-face` + font files (shared pool)
7. **Inject CSS** → GEMINI.md-compliant stylesheet with Greek/Hebrew rules
8. **Add landmarks `<nav>`** → `toc` + `bodymatter`
9. **Add `com.apple.ibooks.display-options.xml`**
10. **Update OPF** → version 3.0, fonts, metadata, `dc:title`/`dc:creator`
11. **Repackage as EPUB3**

### H.7 GEMINI.md Compliance Checklist (Hebrews)

| # | Feature | Status |
|---|---------|--------|
| 1 | Pop-up Footnotes | ⬜ (N/A — no footnotes in source) |
| 2 | Hierarchical Navigation | ⬜ (currently flat) |
| 3 | Landmarks Navigation | ⬜ |
| 4 | Font Injection | ⬜ |
| 5 | Specified Fonts | ⬜ |
| 6 | Greek Tagging | ⬜ (128K chars untagged) |
| 7 | Hebrew Tagging | ⬜ (45K chars untagged, no RTL) |
| 8 | RTL CSS Fix | ⬜ |
| 9 | xmlns:epub | ⬜ (content chapters missing) |
| 10 | Valid XML | ⬜ |

### H.8 Blemishes

The `blemishes/` folder contains 5 PNG images documenting scan defects. These are reference-only and will be noted in `bugs_fixes/BUGS_AND_FIXES.md` but not processed by the converter.

### H.9 Execution

```bash
# Process Hebrews volumes:
python3 converter.py --hebrews

# Process a single Hebrews volume:
python3 converter.py --hebrews 3
```

*Last updated: 2026-05-14*

---

## Phase 2: Converter Build — IN PROGRESS

### 2.1–2.5 Complete ✓

- `shared.py`: VOLUME_CONFIG, HEBREWS_VOLUME_CONFIG, FONT_POOLS, EPUB_STYLESHEET, font injection CSS
- `converter.py`: Unified pipeline (PDF→ThML→EPUB3 + EPUB2→EPUB3)
- Fixed: Font `@font-face` injected into CSS (not inline per-XHTML)
- Fixed: NCX fallback written to EPUB
- Fixed: Deterministic font selection (md5 hash instead of Python hash)
- Fixed: `lang="EL"` → `lang="el" xml:lang="el"`, `lang="HE"` → `lang="he" xml:lang="he" dir="rtl"`

### 2.9 Volume 1 Test — Gaps vs Reference EPUB

Compared against `reference/example/volume_1.epub`. Key gaps:

| Feature | Reference | Current | Status |
|---------|-----------|---------|--------|
| Portrait/Frontispiece page | `frontispiece.xhtml` with portrait | Missing | **TODO** |
| Footnotes (pop-up) | 124 `<aside epub:type="endnote">` + cross-chapter `<a epub:type="noteref">` links | None | **TODO** |
| Cover page format | Simple `<img>` cover | ebooklib default | Match reference |
| NAV heading | `<h2>` with volume title | `<h1>Table of Contents</h1>` | Match reference |
| NAV page-list | `<nav epub:type="page-list" hidden>` with footnote anchors | Missing | **TODO** (after footnotes) |
| Spine order | nav → frontispiece → title → chapters | nav → title → chapters | Add frontispiece |
| CSS | frontispiece, fn-link, endnote styles | Missing these | **TODO** |
| dc:creator | Has `id="creator"` | Missing `id` | Minor fix |

---
## Phase 3: pdftohtml Pipeline (ThML-Guided Rebuild) — IN PROGRESS

**Converter**: `converter_pdftohtml.py`
**Output**: `volumes/v{N}/output_pdftohtml/volume_{N}.epub`
**Goal**: All 106 ThML chapters in spine, pdftohtml text where available, ThML fallback, full polish, **3-level NAV structure**.

### 3-Level NAV Structure

The TOC must support 3 nesting levels:

| Level | Content | Examples |
|-------|---------|---------|
| L1 | Treatise titles | "Christologia", "Meditations and Discourses on the Glory of Christ", "Two Short Catechisms" |
| L2 | Chapters / major sections | "CHAPTER 1", "CHAPTER 2", "PREFACE", "GENERAL PREFACE", "CONTENTS OF VOLUME 1" |
| L3 | Subsections | "I.", "II.", "III.", "IV." (Roman numeral chapters) |

**Rules:**
- L3 chapters are always children of the nearest preceding L2 chapter
- L2 chapters are children of the nearest preceding L1 treatise
- Chapters before the first treatise (CONTENTS, PREFACE, etc.) are L2 at root level
- `_split_nav_title()` splits "Christologia — CHAPTER 1" into L1 + L2
- Roman numeral pattern `^[IVXLCDM]+\.?$` → always L3
- `CHAPTER\|BOOK\|PART\|SECTION \d+` → always L2
- `_is_treatise_title_page()` → L1
- Everything else → L2

### Current Architecture

The pdftohtml pipeline uses a partial hybrid approach:
1. **pdftohtml XML** (`pdftohtml -xml -stdout`) for body text extraction with:
   - High-quality Greek (Beta Code → Unicode via `shared.py`)
   - High-quality Hebrew (Gideon → Unicode via `shared.py`)
   - Bold/italic formatting (parsed from `<b>`/`<i>` tags inside `<text>` elements)
   - Position-based flow reconstruction (lines → paragraphs → chapters)
2. **ThML XML** (from pdfminer pipeline) for structural guidance:
   - Endnote text parsed from ThML FOOTNOTES section
   - Fnref markers mapped by chapter title
   - **Broken**: ThML-based chapter filtering drops 43 real chapters (539K chars)

### Implemented Features (as of 2026-05-09)

| Feature | Status | Details |
|---------|--------|---------|
| pdftohtml XML parsing | ✓ | `parse_pdftohtml_xml()` + `_parse_text_element()` |
| Bold/italic extraction | ✓ | `<b>`/`<i>` tags parsed from pdftohtml text elements, propagated via `TextRun.is_bold/is_italic` through `FontSpec` override |
| Greek detection | ✓ | `ENLFEN+Koine-Medium` font → Beta Code → Unicode |
| Hebrew detection | ✓ | `MOLFEN+Gideon-Medium` font → Unicode |
| Noise filtering | ✓ | AGES headers, page numbers, boilerplate removed |
| Flow reconstruction | ✓ | Lines grouped → paragraphs → chapters |
| Chapter detection | ✓ | Centered + bold + keyword detection for headings |
| ThML-based filtering | ✗ BROKEN | Drops 43 real chapters (539K chars); only 31 of 106 ThML chapters get any pdftohtml content |
| All TOC entries L2 | ✓ | All matched chapters at sibling level (no nesting) |
| Endnotes chapter | ✓ | 124 footnotes from ThML FOOTNOTES section |
| Noteref links | ✓ | 10 links via text matching (limited by marker absence in pdftohtml) |
| EPUB3 assembly | ✓ | ebooklib + OPF 3.0 + NAV + NCX |
| Latin detection | ✓ | `detect_latin_spans()` wraps Latin words in `<span lang="la">` |
| Font embedding | ✓ | SBL BibLit, SBL Greek, SBL Hebrew, Ezra SIL |

### GAP ANALYSIS: Missing ThML Chapters

**43 ThML chapters have NO pdftohtml match** (991 paragraphs, 539,375 chars of real content).

| Cat | ID | Title | Paras | Chars | Notes |
|-----|----|-------|-------|-------|-------|
| A | ch001 | CONTENTS OF VOLUME 1 | 23 | 2,246 | TOC list with 11 numbered entries |
| A | ch002 | MEDITATIONS AND DISCOURSES ON THE GLORY OF CHRIST. | 19 | 1,839 | Treatise title page |
| A | ch003 | TWO SHORT CATECHISMS. | 30 | 2,174 | Treatise title page |
| A | ch004 | GENERAL PREFACE. | 26 | 28,579 | Editor's preface, major content |
| A | ch005 | CHRISTOLOGIA — A DECLARATION... | 9 | 961 | Treatise title page |
| A | ch006 | PREFATORY NOTE | 6 | 3,910 | Short preface |
| A | ch008 | A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST | 40 | 18,405 | Chapter 1 heading + content |
| B | ch015–016 | I., II. | 7+38 | 40,310 | Christologia subsections |
| B | ch020 | I. | 53 | 44,153 | Major subsection |
| B | ch023 | II. | 26 | 12,453 | Subsection |
| B | ch028–029 | III., IV. | 48+24 | 27,608 | Subsections |
| B | ch034–037 | I.–IV. | 15+30+11+5 | 32,657 | Constitution of Christ's Person |
| B | ch041–042 | I., II. | 18+33 | 38,711 | Present state and condition of Christ |
| B | ch044 | III. | 78 | 60,454 | **Largest missing chapter** |
| C | ch045 | MEDITATIONS AND DISCOURSES — THE GLORY OF CHRIST | 3 | 260 | Treatise divider |
| C | ch046 | PREFATORY NOTE. | 5 | 3,554 | Short preface |
| B | ch054–055 | I., II. | 7+60 | 40,497 | Meditations subsections |
| B | ch058 | II. | 50 | 28,557 | In his love |
| B | ch060 | II. | 29 | 14,471 | His Love as impelling cause |
| B | ch062–063 | I., II. | 9+6 | 10,756 | What he did / suffered |
| B | ch067–069 | I.–III. | 12+5+21 | 17,898 | Divine justice / administration |
| B | ch075–076 | I., II. | 8+23 | 20,706 | Glory of Christ by faith |
| D | ch077 | ORIGINAL PREFACE. | 2 | 1,161 | To The Reader |
| B | ch085–088 | I.–IV. | 18+17+28+55 | 72,255 | Spiritual life / recovery |
| D | ch089 | TWO SHORT CATECHISMS: — PRINCIPLES... | 4 | 514 | Catechism title |
| D | ch090 | PREFATORY NOTE | 2 | 1,541 | Catechism preface |
| D | ch091 | TO MY LOVING NEIGHBORS | 12 | 4,205 | Epistle dedicatory |
| D | ch092 | THE LESSER CATECHISM | 67 | 7,179 | 67 Q&A catechism |
| D | ch093 | THE GREATER CATECHISM CHAPTER 1 | 9 | 1,361 | Catechism chapter |

Categories: A=front matter, B=Roman numeral subsection, C=Meditations front matter, D=Catechism front matter

**Even among the 64 "matched" ThML chapters**, they share only ~31 distinct pdftohtml chapters — many ThML chapters map to the same pdf chapter (e.g., all 15 catechism CHAPTER N entries collapse into 3–4 pdf chapters), causing content loss inside kept chapters.

### POLISH GAP: 7 Features from converter.py not in pdftohtml pipeline

| # | Feature | converter.py | converter_pdftohtml.py | Fix |
|---|---------|-------------|----------------------|-----|
| 1 | `title_case()` on headings | "Contents of Volume 1" | Raw "CONTENTS OF VOLUME 1" | Import and apply from converter.py |
| 2 | `_split_nav_title()` | Splits "Christologia — CHAPTER 1" into 2-level TOC | Single flat title | Import and call during TOC building |
| 3 | Treatise title page detection | `_is_treatise_title_page()` → special rendering | Not detected | Import and use for heading level |
| 4 | Subtitle extraction | `_extract_chapter_subtitle()` from bold first-paragraph text | Not implemented | Import and integrate into chapter XHTML |
| 5 | Heading levels | `<h1>` for treatises, `<h2>` for chapters | All `<h1>` | Use `is_treatise` to set heading level |
| 6 | Roman numeral TOC hiding | I., II., III. in spine but hidden from nav | Skipped entirely from both | Use ThML `skip_toc` logic |
| 7 | Synthetic chapters | N/A (all chapters from ThML) | 43 chapters never generated | Render from ThML via `_build_normal_chapter()` |

### IMPLEMENTATION PLAN: ThML-Guided Rebuild + 3-Level NAV

Replace the current `filter_chapters_by_thml()` approach with a full guided rebuild.
The ThML drives the chapter list; pdftohtml fills in text where available.

#### Checklist — ordered by dependency

```
[ ] 0. Run full audit on v1 to establish baseline stats
        commands: converter_pdftohtml.py 1
        verify:   chapter count, bold/italic, footnote count, file size

[ ] 1. Parse ThML for authoritative chapter list (skip FOOTNOTES)
        function: parse_thml_chapter_list(vol_num) -> list of {id, title, div1_elem}
        note:     This replaces load_thml_titles() which only returned a set of norm titles
        verify:   106 entries, in correct order

[ ] 2. Import polish functions from converter.py (DO NOT MODIFY converter.py)
        imports:
          - title_case()
          - _split_nav_title()
          - _is_treatise_title_page()
          - _extract_chapter_subtitle()
          - _build_normal_chapter()
          - _build_treatise_title()
          - _elem_to_html()
          - _escape_xml()
        note:     Do NOT copy — import directly (converter.py is in same directory)
        verify:   imported functions work on sample ThML data

[ ] 3. Build hybrid chapter list (replace filter_chapters_by_thml)
        function: build_hybrid_chapters(thml_div1s, pdf_chapters) -> list of Chapter
        algorithm:
          - For each ThML div1 (in order):
            a. Find matching pdf chapter via title_matches_thml() + TITLE_MAP
            b. If matched → use pdf chapter's paragraphs, rename title to ThML title
            c. If unmatched → create SyntheticChapter with ThML HTML body
          - Any pdf chapters not matched are dropped
        note:     Chapter.paragraphs for synthetic chapters will store raw HTML strings
                  instead of Paragraph objects — need a way to distinguish
        verify:   len(result) == 106 (all ThML chapters present)

[ ] 4. Handle SyntheticChapter in EPUB generation
        change:   Chapter class or subclass to carry raw_html for synthetic chapters
        approach: Add `synthetic_html` field to Chapter. If set, use directly in
                  build_chapter_xhtml instead of rendering from Paragraph objects
        verify:   synthetic chapters have correct XHTML in output EPUB

[ ] 5. Apply title_case() to all chapter headings
        location: build_chapter_xhtml() — wrap chapter.title in title_case()
        location: TOC generation loop — wrap clean_t in title_case()
        verify:   "CONTENTS OF VOLUME 1" → "Contents of Volume 1" in nav and body

[ ] 6. Determine TOC level for each chapter (L1/L2/L3)
        logic:
          - _split_nav_title(text) returns (treatise, chapter) → L1 treatise + L2 chapter
          - Roman numeral pattern ^[IVXLCDM]+\.?$ → L3
          - CHAPTER|BOOK|PART|SECTION \d+ → L2
          - _is_treatise_title_page() → L1
          - Everything else → L2
        note:     Store level on chapter object for TOC generation
        verify:   Christologia→L1, CHAPTER 1→L2, I.→L3

[ ] 7. Update generate_nav_xhtml() to handle 3 levels properly
        change:   current code caps at level 3 and prevents jumps >1 level — verify it
                  handles L1→L2→L3→L2→L1 transitions correctly
        test:     "Christologia" L1 → "CHAPTER 1" L2 → "I." L3 → "II." L3 → "CHAPTER 2" L2
        verify:   NAV HTML has valid nesting with no broken <ol>/<li> tags

[ ] 8. Apply treatise title page detection
        location: chapter iteration loop — call _is_treatise_title_page(div1)
          - If true: use _build_treatise_title() for synthetic, or special rendering for pdf
          - Set has_treatise flag for TOC level logic
        verify:   Christologia, Meditations, Catechisms get treatise-style title pages

[ ] 9. Apply subtitle extraction
        location: when building chapter XHTML, call _extract_chapter_subtitle(div1)
          - If subtitle found: append to TOC entry display text
        verify:   chapters with bold first-paragraph text show subtitle in nav

[ ] 10. Apply proper heading levels (<h1>/<h2>) in chapter body
        location: build_chapter_xhtml() — use is_treatise to decide:
          - treatise → <h1>
          - normal → <h2>
        verify:   headings are consistent with ThML pipeline

[ ] 11. Remove old filter code
        functions to remove:
          - load_thml_titles() (replaced by parse_thml_chapter_list)
          - filter_chapters_by_thml() (replaced by build_hybrid_chapters)
          - title_matches_thml() (keep? or inline into build_hybrid_chapters)
          - _normalize_title() (still needed for matching)

[ ] 12. Run full pipeline v1 — verify baseline
        metrics to check:
          - 106 chapters in spine (all ThML chapters present)
          - Bold tags: ~1300 (from pdftohtml) on pdf-sourced chapters
          - ThML polish: title_case on all headings, split nav, treatise detection
          - Footnotes: 124 endnotes, 10 noteref links
          - No regressions on Greek/Hebrew quality
        commands: .venv/bin/python3 converter_pdftohtml.py 1

[ ] 13. Run full pipeline v1 — spot-check 5 chapters
        check:
          - ch001 (synthetic from ThML): CONTENTS OF VOLUME 1 present, title_case applied
          - ch004 (synthetic from ThML): GENERAL PREFACE, 28K chars, proper formatting
          - ch007 (pdf-sourced): PREFACE, bold preserved, Greek text correct
          - ch044 (synthetic from ThML): III., 78 paras, 60K chars
          - ch092 (synthetic from ThML): THE LESSER CATECHISM, 67 Q&A
        verify each: present in spine, correct content, no corruption

[ ] 14. Verify 3-level NAV structure
        check:
          - "Christologia" at L1 with children "CHAPTER 1" (L2), "I." (L3), "II." (L3)
          - "Meditations and Discourses on the Glory of Christ" at L1
          - "PREFACE" at L2 root level
          - "Footnotes" at L1 root level (end)
          - All <ol>/<li> tags properly nested with no broken HTML
        verify: python3 -c "import zipfile; e = zipfile.ZipFile('...'); ..."

[ ] 15. Update output stats in PLAN.md
        metrics:
          - Total chapters (should match ThML: 106)
          - Bold/italic counts
          - NAV depth validation
          - Footnote counts
          - EPUB file size
```

### Risk Assessment: Importing converter.py Functions

| Risk | Mitigation |
|------|-----------|
| `_build_normal_chapter()` uses `_elem_to_html` which depends on `tag_unicode_ranges()` already defined in converter_pdftohtml.py | Rename converter_pdftohtml's version or use converter.py's version with alias |
| `_build_endnotes_chapter()` in converter.py uses different footnote format than ours | Keep our implementation — don't import converter.py's endnotes |
| `_is_treatise_title_page()` checks "CHRISTOLOGIA" and "DECLARATION" keywords — may need volume-specific tuning | Keep as-is; update if other volumes differ |
| Circular imports if both files import each other | converter_pdftohtml.py imports FROM converter.py (one-way) — safe |
| `_escape_xml()` defined in both files | Use converter.py's version when processing ThML content; ours for pdftohtml content |

### v1 Output Stats (current — pre-rebuild)

| Metric | Value |
|--------|-------|
| Chapters (pre-filter) | 83 |
| Chapters (post-filter) | 60 |
| Missing ThML chapters | 43 (539K chars) |
| Bold tags | 1174 |
| Italic tags | 10 |
| Greek spans | ~2000+ |
| Footnotes | 124 |
| Noteref links | 10 |
| EPUB size | 2348 KB |
| Fonts embedded | SBL BibLit, SBL Greek, SBL Hebrew, Ezra SIL |

### Verification Commands

```bash
# Run pipeline
.venv/bin/python3 converter_pdftohtml.py 1

# Inspect output
.venv/bin/python3 -c "
import zipfile, re
e = zipfile.ZipFile('volumes/v1/output_pdftohtml/volume_1.epub')
for n in e.namelist():
    if n.endswith('.xhtml'):
        c = e.read(n).decode()
        print(f'{n:50s} b={c.count(\"<b>\"):4d} i={c.count(\"<i>\"):4d} fn={c.count(\"noteref\"):3d}')
e.close()
"

# Count chapters in nav
.venv/bin/python3 -c "
import zipfile
e = zipfile.ZipFile('volumes/v1/output_pdftohtml/volume_1.epub')
nav = e.read('EPUB/nav.xhtml').decode()
import re
links = re.findall(r'<a\s+href=\"([^\"]+)\">([^<]+)</a>', nav)
print(f'Nav entries: {len(links)}')
for h, t in links:
    if h.endswith('.xhtml'):
        print(f'  {h:20s} {t[:60]}')
e.close()
"