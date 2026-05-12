# PyMuPDF EPUB3 Converter — Architecture Plan

**Created**: 2026-05-09
**Status**: Plan — ready to build

---

## Objective

Replace the legacy `pdftohtml` + `pdfminer` pipeline with a unified PyMuPDF-based EPUB3 converter for John Owen's Works (16 volumes). Produces reflowable, semantically structured EPUB3 output with proper Greek/Hebrew Unicode, Goold footnotes, and 3-level navigation.

---

## Architecture Overview

```
┌───────────────────────────────────────────────────────────────┐
│                      converter.py                             │
├───────────────────────────────────────────────────────────────┤
│  Stage 1: Dual Extraction                                     │
│    ├─ PyMuPDF4LLM (to_markdown) → Markdown text + structure   │
│    └─ Raw PyMuPDF (get_text dict) → font-aware text spans     │
├───────────────────────────────────────────────────────────────┤
│  Stage 2: Font Conversion (Greek / Hebrew)                    │
│    ├─ Koine-Medium  → Beta Code → Unicode Greek (NFC)         │
│    └─ Gideon-Medium → Visual L→R → Unicode Hebrew (RTL)      │
├───────────────────────────────────────────────────────────────┤
│  Stage 3: Semantic Rebuild                                    │
│    ├─ Strip AGES headers, page numbers, boilerplate            │
│    ├─ Rebuild paragraphs, headings, chapters, subsections      │
│    ├─ Map [fN] footnote markers → noteref links                │
│    └─ Extract FTN footnotes section → endnotes                 │
├───────────────────────────────────────────────────────────────┤
│  Stage 4: ThML Footnote Enrichment                            │
│    └─ Parse existing volume_N.thml.xml FOOTNOTES section      │
├───────────────────────────────────────────────────────────────┤
│  Stage 5: EPUB3 Assembly (ebooklib)                            │
│    ├─ Cover / Frontispiece / Title page                        │
│    ├─ Font injection (SBL BibLit / Cardo / Libertinus)         │
│    ├─ CSS from shared.py                                       │
│    ├─ 3-level NAV (L1 treatise → L2 chapter → L3 subsection)  │
│    └─ Endnotes chapter with aside epub:type="endnote"          │
└───────────────────────────────────────────────────────────────┘
```

---

## 1. Dual Extraction Strategy

### Pass 1 — PyMuPDF4LLM (structural skeleton)

```python
pages = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
```

Returns a list of dicts, one per PDF page:
```
{
    'metadata': {'page': N, 'title': '...', 'page_count': 644, ...},
    'toc_items': [...],
    'tables': [...],
    'images': [...],
    'graphics': [...],
    'text': '### THE AGES DIGITAL LIBRARY\n## **JOHN OWEN COLLECTION**\n...',
    'words': [...]
}
```

Provides: heading levels (`#`/`##`/`###`), bold (`**`), italic (`_`), paragraph breaks, page-by-page chunking. Used as the structural skeleton for the EPUB chapters.

### Pass 2 — Raw PyMuPDF (font-aware extraction)

```python
blocks = page.get_text("dict")["blocks"]
for b in blocks:
    if b["type"] == 0:  # text block
        for line in b["lines"]:
            for span in line["spans"]:
                # span keys: font, size, flags, color, text, bbox, origin
```

Each text span carries: font family name, size in points, bold/italic flags, color, bounding box, text content. This is used to detect Koine-Medium and Gideon-Medium fonts for Greek/Hebrew conversion.

### Merge Logic (per page)

| Condition | Source for text |
|-----------|----------------|
| Page has `Koine-Medium` spans | Raw PyMuPDF text (font-converted), structure from 4LLM |
| Page has `Gideon-Medium` spans | Raw PyMuPDF text (font-converted), structure from 4LLM |
| Page has only regular fonts | PyMuPDF4LLM Markdown as-is |

The structure (heading levels, paragraph boundaries, bold/italic) always comes from PyMuPDF4LLM. On Greek/Hebrew pages, the actual character text is replaced with font-converted Unicode from raw PyMuPDF.

---

## 2. Greek/Hebrew Font Processing

### Font → Conversion Mapping

| PDF font(s) | Encoding | Converter | Output |
|-------------|----------|-----------|--------|
| `Koine-Medium`, `ENLFEN+Koine-Medium` | Beta Code | `shared.convert_greek_word()` | NFC Unicode Greek |
| `Gideon-Medium`, `MOLFEN+Gideon-Medium` | Visual L→R | `shared.convert_gideon_hebrew()` | Unicode Hebrew (RTL) |
| All other fonts | Standard | Passthrough | As-is |

### Greek Beta Code Example

PDF text (Koine-Medium font): `o=utov estin he pros ton Patera agousa hosos`
After conversion: `οὗτός ἐστιν ἡ πρὸς τὸν Πατέρα ἄγουσα ὁδός`

### Hebrew Gideon Example

Gideon font encodes Hebrew in visual L→R order with vowel marks. The existing `convert_gideon_hebrew()` handles word reversal and vowel attachment.

### Post-Conversion Tagging

After conversion to Unicode, scan each paragraph for Greek (U+0370–U+03FF, U+1F00–U+1FFF) and Hebrew (U+0590–U+05FF) runs. Wrap in:

```html
<span lang="el" xml:lang="el">Greek text here</span>
<span lang="he" xml:lang="he" dir="rtl">Hebrew text here</span>
```

Merge adjacent identical spans (e.g., `</span><span lang="el" xml:lang="el">` → remove the seam).

---

## 3. Boilerplate Stripping

Remove the following from each page's output (detected by position, content, and font patterns):

| Pattern | Detection method |
|---------|-----------------|
| `THE AGES DIGITAL LIBRARY` | Heading at top of page 1, font=TimesNewRomanPSMT blue |
| `JOHN OWEN COLLECTION` | Heading below AGES line, bold |
| `THE WORKS OF JOHN OWEN` | Running header on subsequent pages (top center, blue) |
| Page numbers (e.g., `2`, `3`, `634`) | Isolated digits, top/bottom of page, small font |
| `Books For The Ages` | Footer line |
| `AGES Software • Albany, OR USA` | Footer line |
| `Version 1.0 © 2000` | Footer line |
| `<271202>` style Strong's links | Bible ref hyperlinks to KJV PDFs (strip link, keep text ref) |

---

## 4. Footnote Pipeline

Three sources work together for complete footnote coverage:

### 4A. Body Markers `[fN]` (from PyMuPDF4LLM Markdown)

129 footnote markers found in v1 body text, formatted as `[f1]`, `[f2]`, ..., `[f129]`.

Detection:
```python
re.findall(r'\[f(\d+)\]', page_text)
```

Action: replace `[f{N}]` → `<a epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fn{N}"><sup>{N}</sup></a>`

### 4B. FT Footnote Content (from PDF FOOTNOTES section)

The last few PDF pages (634+ for v1) contain a `FOOTNOTES` chapter. Each entry has:
- Marker: `FT{N}` at left margin (position `left=38`)
- Text: paragraph(s) of footnote content, with possible Greek (Koine-Medium font)

Example from pdftohtml XML:
```xml
<text top="146" left="38" width="23" height="11" font="17">FT1 </text>
<text top="150" left="61" width="499" height="16" font="13">The Christian Ministry, p. 42-44, by the Rev. Charles Bridges, A.M.</text>
```

### 4C. ThML Footnote Enrichment

Parse existing `volume_{N}.thml.xml` FOOTNOTES section:
```python
<div1 title="FOOTNOTES" id="ch120">
  <p class="Body">
    <a class="fnmarker" data-fn="1"/>
    The Christian Ministry, p. 42-44, by the Rev. Charles Bridges, A.M.
    <a class="fnmarker" data-fn="2"/>
    See his interesting History of the British Churches in the Netherlands.
    ...
  </p>
</div1>
```

ThML text is preferred when available — it already has Unicode Greek, proper paragraph structure, and bold/italic markup.

### Merging Logic

```python
def merge_footnotes(pdf_ft_markers, pdf_ft_texts, thml_ft_texts):
    for fn_num in range(1, max_count):
        entry = {}
        entry['marker_page'] = pdf_ft_markers.get(fn_num)  # PDF page where FT{N} appears
        # ThML text takes priority
        entry['text'] = thml_ft_texts.get(fn_num) or pdf_ft_texts.get(fn_num)
        yield entry
```

### Endnotes XHTML Output

```html
<section epub:type="endnotes" role="doc-endnotes">
  <h1>Footnotes</h1>
  <aside epub:type="endnote" role="doc-endnote" id="fn1">
    <p class="footnote"><a href="#fn1" class="fn-link">1</a> The Christian Ministry...</p>
  </aside>
  <aside epub:type="endnote" role="doc-endnote" id="fn2">
    <p class="footnote"><a href="#fn2" class="fn-link">2</a> See his interesting History...</p>
  </aside>
  ...
</section>
```

---

## 5. Chapter / TOC Hierarchy

### Structural Levels

| Level | Content | Detection |
|-------|---------|-----------|
| L1 | Treatise titles | Keywords: "CHRISTOLOGIA", "MEDITATIONS", "CATECHISMS", "DECLARATION OF", "A VINDICATION" |
| L2 | Chapters / major sections | "CHAPTER \d+", "BOOK \d+", "PART \d+", "SECTION \d+", "PREFACE", "PREFATORY NOTE" |
| L3 | Subsections | Roman numerals: `^[IVXLCDM]+\.?$` |

Uses same logic as current `converter.py`:
- `_split_nav_title()` — splits "Christologia — CHAPTER 1" into L1 + L2
- `_is_treatise_title_page()` — detects treatise title pages
- Roman numeral pattern — always L3

### Per-Volume Navigation

For v1 (example):
```
L1  Christologia
  L2  Prefatory Note
  L2  Preface
  L2  CHAPTER 1
    L3  I.
    L3  II.
    L3  III.
    L3  IV.
  L2  CHAPTER 2
    ...
L1  Meditations and Discourses on the Glory of Christ
  L2  Prefatory Note
  L2  CHAPTER 1
    ...
L1  Two Short Catechisms
  L2  Prefatory Note
  L2  THE LESSER CATECHISM
  L2  THE GREATER CATECHISM
L1  Footnotes
```

### Chapter Dataclass

```python
@dataclass
class Chapter:
    id: str            # e.g. "ch001"
    title: str         # Cleaned, title-cased
    subtitle: str      # From bold first-paragraph text
    body_html: str     # Full XHTML body content
    is_treatise: bool  # True for treatise title pages
    level: int         # 1, 2, or 3 for NAV hierarchy
    page_start: int    # PDF page number (0-based)
    page_end: int      # PDF page number (0-based)
```

---

## 6. BoT Pagination & Reference Format

The Goold edition (1850–53) uses cross-references in this format:
```
—John Owen, Title, section [Vol:Page]
```

These appear as natural text in the source PDF (e.g., "See his Christologia, chap. 4, p. 54 of this volume"). No `[Vol:Page]` bracketed patterns found in v1 body text — references are inline prose. The converter preserves them as-is since they're part of paragraph text.

Banner of Truth (BoT) pagination refers to the page numbering of the printed Goold edition. These page numbers are not embedded as explicit markers in the AGES PDF (no `[1:245]` found in v1). The converter does not need to synthesize them — the reflowable EPUB does not replicate print page numbers.

---

## 7. CCEL Volumes (5 & 10)

Volumes 5 and 10 use CCEL XML sources instead of AGES PDFs:

```python
VOLUME_CONFIG[5] = {'source_type': 'ccel_xml', 'ccel_file': 'special_sources/owen-v5-justification.xml'}
VOLUME_CONFIG[10] = {'source_type': 'ccel_xml', 'ccel_file': 'special_sources/owen-10-deathofdeath.xml'}
```

### CCEL Pipeline Branch

```python
if config['source_type'] == 'ccel_xml':
    chapters = parse_ccel_xml(config['ccel_file'])
    # XML already has Unicode Greek/Hebrew — no font conversion needed
    # Run tag_unicode_ranges() to add lang/xml:lang spans
else:
    # Standard PyMuPDF pipeline
    chapters = extract_pymupdf(pdf_path)
```

CCEL XMLs already contain proper Unicode Greek/Hebrew, paragraph breaks, and heading structure. The converter parses them into the same `Chapter` dataclass and runs the same EPUB assembly code.

---

## 8. EPUB3 Assembly

### Book Structure

```
EPUB/
├── mimetype
├── META-INF/
│   └── container.xml
└── OEBPS/
    ├── content.opf
    ├── nav.xhtml
    ├── toc.ncx
    ├── title.xhtml         # Title page
    ├── frontispiece.xhtml  # Portrait (optional)
    ├── ch001.xhtml         # Chapter 1
    ├── ch002.xhtml         # Chapter 2
    ├── ...
    ├── ch120.xhtml         # Endnotes
    ├── style/
    │   └── main.css
    ├── Fonts/
    │   ├── SBL_BLit.ttf
    │   ├── SBL_grk.ttf
    │   ├── SBL_Hbrw.ttf
    │   └── ... (primary font files)
    └── images/
        ├── cover.png
        └── portrait.jpg
```

### Font Injection (from shared.py)

- Primary font selected deterministically: `select_primary_font(f"owen-v{vol_num}")`
- Always-injected supplements: SBL BibLit, SBL Greek, SBL Hebrew, Ezra SIL
- CSS: `EPUB_STYLESHEET` from `shared.py` for body styling, hierarchy
- `EPUB3_FONT_STYLES` with `@font-face` declarations for per-volume primary font

### NAV Generation

```python
def generate_nav_xhtml(toc_entries, volume_title):
    # 3-level <ol>/<li> nesting
    # L1 → top-level <ol><li>
    # L2 → nested <ol><li> under L1
    # L3 → nested <ol><li> under L2
    # Includes <nav epub:type="toc"> and <nav epub:type="landmarks">
```

### OPF Manifest

```xml
<package version="3.0" xmlns="http://www.idpf.org/2007/opf"
         unique-identifier="book-id">
  <metadata>
    <dc:identifier id="book-id">urn:uuid:{uuid}</dc:identifier>
    <dc:title>The Works of John Owen, Vol. {N} — {subtitle}</dc:title>
    <dc:creator id="creator">John Owen</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>Eduardus Ekofius</dc:publisher>
    <meta property="dcterms:modified">{iso_date}</meta>
  </metadata>
  <manifest>
    <!-- CSS, fonts, images, XHTML -->
  </manifest>
  <spine toc="ncx">
    <itemref idref="nav" linear="no" properties="nav"/>
    <itemref idref="title"/>
    <itemref idref="frontispiece" linear="no" optional="yes"/>
    <itemref idref="ch001"/>
    ...
    <itemref idref="ch120"/>
  </spine>
</package>
```

### Title Page

```html
<div class="title-page">
  <p class="ornament">❧</p>
  <h1>The Works of<br/>John Owen</h1>
  <hr class="rule"/>
  <p class="subtitle">Volume {N}</p>
  <p class="subtitle">{subtitle}</p>
  <p class="author"><span class="by">by</span>John Owen</p>
  <p class="editor">Edited by William H. Goold</p>
  <p class="publisher">Eduardus Ekofius</p>
</div>
```

---

## 9. Module Structure

```python
# converter.py (fresh rewrite, ~500-600 lines)

# === IMPORTS ===
import fitz                              # PyMuPDF
import pymupdf4llm                       # PyMuPDF4LLM
from ebooklib import epub
from shared import (
    VOLUME_CONFIG, VOLUME_SUBTITLES,
    EPUB_STYLESHEET, generate_font_styles,
    select_primary_font, SBL_SUPPLEMENTS, EZRA_SIL_FILES,
    convert_greek_word, convert_gideon_hebrew
)

# === CONSTANTS ===
GREEK_FONTS = {'Koine-Medium', 'ENLFEN+Koine-Medium'}
HEBREW_FONTS = {'Gideon-Medium', 'MOLFEN+Gideon-Medium'}
AGES_HEADERS = {'THE AGES DIGITAL LIBRARY', 'JOHN OWEN COLLECTION', ...}

# === STAGE 1: EXTRACTION ===
def extract_pdf_text(pdf_path):
    """Two-pass extraction: PyMuPDF4LLM + raw fitz."""

def extract_raw_spans(pdf_path):
    """Get font-aware spans via raw fitz get_text('dict')."""

# === STAGE 2: FONT CONVERSION ===
def convert_greek_hebrew_spans(spans):
    """Convert Koine-Medium / Gideon-Medium spans to Unicode."""

def tag_unicode_ranges(html):
    """Wrap Greek/Hebrew Unicode runs in lang-spans."""

# === STAGE 3: SEMANTIC REBUILD ===
def strip_ages_boilerplate(text, page_num):
    """Remove AGES headers, footers, page numbers."""

def rebuild_chapters(md_pages, converted_spans):
    """Group pages into Chapter dataclass list with hierarchy."""

def detect_chapter_boundaries(md_pages):
    """Find chapter starts via heading patterns."""

# === STAGE 4: FOOTNOTES ===
def extract_footnote_markers(text):
    """Detect [fN] patterns and return (stripped_text, markers)."""

def parse_thml_footnotes(thml_path):
    """Parse existing ThML XML FOOTNOTES section."""

def build_endnotes_chapter(footnotes):
    """Build endnotes XHTML with aside epub:type='endnote'."""

# === STAGE 5: EPUB ASSEMBLY ===
def build_epub(vol_num, chapters, footnotes):
    """Full EPUB3 assembly."""

def generate_nav_xhtml(toc_entries, title):
    """3-level NAV with landmarks."""

def generate_ncx(title, uid, toc_entries):
    """NCX for backward compatibility."""

def repackage_canonical(epub_path, src_dir):
    """Mimetype-first ZIP packaging."""

# === CCEL BRANCH ===
def parse_ccel_xml(xml_path):
    """Parse CCEL XML into Chapter list."""

# === MAIN ===
def process_owen_volume(vol_num):
    """Orchestrate full pipeline for one volume."""

def process_all_volumes():
    """Process volumes 1-16."""

if __name__ == '__main__':
    import argparse
    # --hebrews flag for Hebrews pipeline
    # Positional arg for single volume number
```

---

## 10. Dependencies

```
PyMuPDF (fitz)          — font-aware text extraction
PyMuPDF4LLM             — semantic Markdown structure extraction
ebooklib                — EPUB3 assembly
shared.py               — converters, fonts, CSS (existing, unchanged)
```

All installable via pip. PyMuPDF4LLM pulls in PyMuPDF and pymupdf-layout automatically.

---

## 11. Execution

```bash
# Single volume:
.venv/bin/python3 converter.py 3

# All 16 volumes:
.venv/bin/python3 converter.py

# Hebrews (existing EPUB2 pipeline, unchanged):
.venv/bin/python3 converter.py --hebrews
```

Output: `volumes/v{N}/output/volume_{N}.epub`

---

## 12. Volume 1 Target Metrics

| Metric | Old (pdftohtml) | Target (PyMuPDF) |
|--------|-----------------|-------------------|
| Chapters in spine | 60 (43 missing) | All ~106 |
| Greek spans | ~2000+ (Beta Code converted) | Same + font-detected |
| Footnotes | 124 (from ThML only) | 124+ (PDF FT + ThML enrichment) |
| FN markers in body | 0 linked | 129 `[fN]` → noteref links |
| Bold/italic | ~1184 tags | Preserved via 4LLM |
| NAV depth | 2-level | 3-level (L1/L2/L3) |
| AGES header stripping | Partial | Complete removal |
| Output size | ~2.3 MB | Comparable |

---

## 13. Files Changed

| File | Action |
|------|--------|
| `converter.py` | **New** — fresh rewrite (replaces existing) |
| `shared.py` | **Unchanged** |
| `PYMUPDF_PLAN.md` | This file (plan reference) |
| `AGENTS.md` | Update pipeline documentation |

No existing intermediate files are modified. The old `volume_{N}.thml.xml` and `volume_{N}.pdftohtml.xml` remain in `intermediate/` for reference and footnote enrichment.

---

## 14. Pipeline Comparison

| Aspect | Old Pipeline | New Pipeline |
|--------|-------------|--------------|
| Text extraction | `pdftohtml -xml` (external poppler) | `pymupdf4llm.to_markdown()` |
| Font detection | `fontspec` in XML | `page.get_text("dict")` spans |
| Greek/Hebrew | Position-based parser | Font-based detection |
| Footnote refs | From ThML XML | `[fN]` from Markdown + ThML |
| Structure | Manual line-to-paragraph | 4LLM Markdown hierarchy |
| Deps | poppler, pdfminer, pdftohtml | PyMuPDF + PyMuPDF4LLM only |
| Bug risk | Missing chapters, corrupted text | Direct PDF, no intermediate loss |

---

*Last updated: 2026-05-09*
