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

## Phase 5: Validation & Bug Tracking — PENDING

### 5.1 EPUB3 validation (ported from Beeke)

### 5.2 Auto-create `bugs_fixes/BUGS_AND_FIXES.md` per volume

### 5.3 Test volume 1 end-to-end

### 5.4 Test CCEL volume 10 end-to-end

### 5.5 Batch test all 16 volumes

### 5.6 Pre-flight checklist per GEMINI.md

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

### 2.10 Remaining Work

1. **Add portrait/frontispiece page** — portrait at `Owen/portraits/protrait1.jpeg` (724×1086, matches reference)
2. **Wire footnotes into EPUB pipeline** — `extract_footnotes()` exists in Stage 1 but output never reaches Stage 2
   - Store extracted footnotes in ThML XML as `<footnotes>` section
   - Create endnotes chapter (`ch120.xhtml` style) with `<aside epub:type="endnote">` blocks
   - Insert `<a epub:type="noteref" role="doc-noteref">` links at superscript positions in body text
   - Add `page-list` `<nav>` to nav.xhtml with footnote anchors
3. **Add CSS for footnotes and frontispiece** — `.frontispiece`, `.fn-link`, `.footnote-ref`, `aside[epub|type="endnote"]`
4. **Match reference NAV format** — `<h2>` with volume title, `role="doc-toc"`
5. **Fix spine order** — frontispiece between nav and title