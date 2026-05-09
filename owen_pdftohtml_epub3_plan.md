# Owen PDF → pdftohtml → EPUB3: Plan

## Rationale

The current pipeline uses ThML (Theological Markup Language XML) as an intermediate between PDF extraction and EPUB assembly. ThML was designed as a semantic interchange format, but our ThML is produced by a font-run extractor (`pdfminer.six` + `pdf_to_thml.py`) that operates with no spatial context. This causes bugs that are fundamentally unfixable without knowing where text sits on the page.

**pdftohtml` (poppler) gives us:**
- Per-character positioning (top, left, width, height)
- Page boundaries (explicit `<page>` elements)
- Font metadata (family, size, bold/italic per text element)
- Robust extraction engine (poppler is the industry standard)

The key insight: **positional data IS the semantic signal** in a PDF. Indentation tells you a list item. Vertical gap tells you a paragraph break. Center alignment tells you a heading. The current ThML pipeline discards all of this.

---

## Which Bugs This Prevents

Mapped against known bugs from `volumes/v1/bugs_fixes/BUGS_AND_FIXES.md`:

| Bug | Current ThML Root Cause | pdftohtml Fix |
|-----|------------------------|---------------|
| **#21 Structural Misalignment** (bold Roman numerals I.–IV. promoted to chapters) | Font-run sees bold + font≥14 = `h2`, creates new chapter for each list item | Positional: `left` coordinate shows indentation (not flush-left like real headings). Sequential I, II, III, IV with same indentation = list, not headings. Font size ≈ body, not heading-sized. |
| **#16 ΧΡΙΣΤΟΛΟΓΙΑ on wrong page** | Font-run concatenates text across page boundaries | Explicit `<page>` boundaries prevent cross-page bleeding |
| **#20 Missing "CHAPTER 1" heading** | Font-run merges heading into preceding content | Heading has distinct font size (typically ≥16px) and centering — trivially detectable |
| **#18 Redundant treatise/chapter heading merge** | Font-run produces one continuous heading run for both | Treatise title on one page, "CHAPTER 1" on next (different page + position) |
| **#17/#19 Hierarchical NAV split** (chapters 8-20 at wrong level) | Partially NAV generation, partially ThML having no treatise/chapter distinction | State-machine NAV builder (see below) combined with cleaner chapter boundaries from positional data |

---

## Architecture

```
owen-v{N}.pdf
     │
     ▼
pdftohtml -xml
     │
     ▼
volume_{N}.pdftohtml.xml    ← INTERMEDIATE (saved for debugging)
     │
     ▼
converter_pdftohtml.py
  ├── XML Parser            ← reads positioned text elements + fontspecs
  ├── Flow Reconstructor    ← lines → paragraphs → chapters
  ├── Font Converter        ← Koine → Greek Unicode; Gideon → Hebrew Unicode
  ├── State-Machine NAV     ← L1 treatise / L2 chapter / L3 sub-section
  └── EPUB3 Assembler       ← same styling/fonts as GEMINI.md mandates
     │
     ▼
volume_{N}.epub             → volumes/v{N}/output_pdftohtml/
```

---

## Flow Reconstruction Algorithm

### Step 1: Parse pdftohtml XML

```xml
<page number="1" top="0" left="0" height="939" width="615">
  <fontspec id="0" size="30" family="TimesNewRomanPSMT" color="#0000d3"/>
  <fontspec id="2" size="18" family="ENLFEN+Koine-Medium" color="#0000d3"/>
  <text top="46" left="92" width="18" height="27" font="0">T</text>
  ...
</page>
```

Build a `FontSpec` catalog per page (or globally if same font IDs repeat):
- Font family → body / Koine / Gideon / unknown
- Size bucket: tiny (<10), small (10-13.9), body (14-19.9), large (20+)
- Bold/italic detection from font name suffix

### Step 2: Filter Noise

Remove from text stream:
- **Page numbers**: Small font (<10), centered horizontally OR at top/bottom margin, sequential digits
- **AGES headers**: "THE WORKS OF JOHN OWEN" repeated identically on consecutive pages
- **Scripture codes**: Pattern `<[A-Z0-9]{5,8}>`, tiny font
- **AGES Software**: "Albany, OR", "www.ageslibrary.com", "Version X.X"
- **Footer artifacts**: Single short words at extreme bottom of page

**Deduplication**: Track text hashes per page; if identical text appears at same position on 3+ consecutive pages, mark as boilerplate.

### Step 3: Group into Lines

```
Per page:
  collect all <text> elements
  sort by (top, left)
  group adjacent elements where |top1 - top2| ≤ 2px  → same line
  within each line, join text preserving font metadata per segment
```

Each line becomes a `Line` object with:
- `text_segments`: list of `(text, fontspec_id)` tuples
- `baseline`: the `top` value
- `left`: start position
- `font_info`: aggregated from segments

### Step 4: Group Lines into Paragraphs

Vertical gap rules (using the `top` coordinate):

| Gap | Action |
|-----|--------|
| `< 1.2 × line-height` | Same paragraph, continuation line |
| `1.2× – 2.5× line-height` | New paragraph in same chapter |
| `> 2.5× line-height` | Potential new section/heading boundary |
| `line starts with indent (left > margin + 20px)` | New paragraph (first-line indent) |

### Step 5: Classify Paragraph Type

Run these checks in order on each paragraph block:

```
IF font_size ≥ 20 AND centered (left near page_mid ±50px):
  → HEADING_1 (treatise title)

ELIF font_size ≥ 16 AND centered:
  → HEADING_2 (section title)

ELIF bold AND NOT indented AND matches CHAPTER|SERMON|DISCOURSE|PREFACE|EXERCITATION:
  → CHAPTER_HEADING (even if font_size is body-sized)

ELIF bold AND indented AND matches Roman numeral (I., II., III., IV.):
  → LIST_ITEM (NOT a chapter start)

ELIF font_family == "Koine":
  → GREEK_TEXT (apply Beta Code conversion)

ELIF font_family == "Gideon":
  → HEBREW_TEXT (apply Gideon conversion)

ELSE:
  → BODY_TEXT
```

### Step 6: Chapter Boundary Detection

A new chapter starts when:
1. HEADING_1 or HEADING_2 is detected (starts new `div1` equivalent)
2. CHAPTER_HEADING is detected after body text
3. Page number jumps > 1 (e.g., new page starts at 53 after 44 → likely a new work)

A chapter does NOT start when:
1. A bold Roman numeral is followed by another bold Roman numeral (sequential list)
2. An indented bold phrase (it's a list item or sub-head within current chapter)
3. Small centered text at page bottom (it's a page number or catchword)

---

## Greek/Hebrew Pipeline

### Greek (Koine-Medium font)

pdftohtml extracts raw Beta Code ASCII from Koine font text:
```
"Nai> fh>mi"  →  "Ναί φημί"
```

Per text segment with Koine font family:
1. Extract raw Beta Code string
2. Split on whitespace
3. Apply `convert_greek_word()` from `shared.py` per token
4. Join back with spaces
5. Wrap in `<span lang="el" xml:lang="el">`

**Multi-font lines**: A line may mix Koine and body font (e.g., Greek word in English sentence). Split the line into segments by font, convert Greek segments, interleave with body segments, wrap Greek in spans.

### Hebrew (Gideon-Medium font)

pdftohtml extracts raw Gideon-encoded characters:
```
"ytb;h}aæB] vyrij}yæ"  →  Hebrew Unicode
```

Per text segment with Gideon font family:
1. Extract raw Gideon string
2. Apply `convert_gideon_hebrew()` from `shared.py`
3. Wrap in `<span lang="he" xml:lang="he" dir="rtl">`

**Detection**: Gideon font family varies per PDF (the 6-character prefix changes):
- `ENLFEN+Koine-Medium`, `MOLFEN+Gideon-Medium`, `BEJNOD+Gideon-Medium`, etc.
- Detect by substring: `"Koine" in family → Greek`, `"Gideon" in family → Hebrew`

---

## NAV State Machine

Prevents the "chapters 8-20 jump to L1" bug (#17/#19) by maintaining hierarchical state:

```
States: BODY | TREATISE | CHAPTER | SUB_SECTION

Transitions:
  BODY + HEADING_1 detected          → TREATISE  (emit L1 entry)
  BODY + CHAPTER_HEADING detected    → CHAPTER   (emit L1 entry if no treatise)
  TREATISE + CHAPTER_HEADING         → CHAPTER   (emit L2 child entry)
  CHAPTER + LIST_ITEM (Roman num)    → SUB_SECTION (emit L3 child entry)
  CHAPTER + HEADING_1                → TREATISE  (close current treatise, new L1)
  CHAPTER + CHAPTER_HEADING          → CHAPTER   (emit L2 sibling)
  any + BODY_TEXT                    → stay in current state

Stack management (for XML validity):
  TREATISE opens <ol><li> ... closes </li></ol> on next TREATISE or EOF
  CHAPTER opens <ol><li> ... closes </li></ol> on new CHAPTER, TREATISE, or EOF
  SUB_SECTION opens <li> ... closes on next SUB_SECTION, CHAPTER, or EOF
```

This ensures that once a treatise is open at L1, every subsequent chapter heading gets L2 until the next treatise title closes the hierarchy.

---

## EPUB3 Assembly (GEMINI.md §4 Compliance)

All features from the existing `converter.py` are preserved, using the same `shared.py` components:

| Feature | GEMINI.md § | Implementation |
|---------|-------------|----------------|
| Pop-up endnotes | §4.4.1 | `<a epub:type="noteref">` + `<aside epub:type="endnote">` |
| Hierarchical NAV | §4.4.2 | State-machine generated `<ol>/<li>` nesting |
| Landmarks nav | §4.4.2 | `<nav epub:type="landmarks">` |
| Font injection | §4.2 | Per-XHTML inline `@font-face` (same pattern as Beeke) |
| Greek tagging | §4.4.3 | `<span lang="el" xml:lang="el">` |
| Hebrew tagging | §4.4.3 | `<span lang="he" xml:lang="he" dir="rtl">` |
| RTL CSS fix | §4.2 | `[lang="he"] p, [lang="he"] div { text-align: left }` |
| Title page | §4.4.4 | Banner of Truth design, flexbox, gold rule |
| NAV title splitting | §4.4.5 | Treatise + Chapter split for hierarchical NAV |
| Portrait assignment | §4.4.6 | Deterministic md5 hash from portrait pool |
| Apple Books options | §5 | `com.apple.ibooks.display-options.xml` with `specified-fonts="true"` |
| OPF version 3.0 | §6 | `package` version, NCX fallback, font manifest |
| `xmlns:epub` | §7.9 | On all `<html>` elements |

## Styling — Merged from Owen Reference + Beeke Patterns

The visual target is the existing `volumes/v1/output/volume_1.epub`, with these CSS value adjustments from Beeke:

| Property | Value | Source |
|----------|-------|--------|
| `body line-height` | `1.65` | Owen original |
| `[lang="el"] font-size` | `1.4em` | Beeke |
| `[lang="he"] font-size` | `1.6em` | Beeke |
| `[lang="he"] line-height` | `1.4` | Beeke |
| Hebrew fallback | `"Ezra SIL"` (not Brill) | Owen original |
| Font injection | Per-XHTML inline `@font-face` | Beeke pattern |

### Font injection (per-XHTML inline, like Beeke)

Each chapter XHTML gets an inline `<style>` block in `<head>` with `@font-face` declarations:

```css
@font-face { font-family: "[PRIMARY]"; src: url("Fonts/[primary-file]"); font-weight: normal; font-style: normal; }
@font-face { font-family: "[PRIMARY]"; src: url("Fonts/[bold-file]"); font-weight: bold; font-style: normal; }
@font-face { font-family: "[PRIMARY]"; src: url("Fonts/[italic-file]"); font-weight: normal; font-style: italic; }
@font-face { font-family: "SBL BibLit"; src: url("Fonts/SBL_BLit.ttf"); }
@font-face { font-family: "SBL Hebrew"; src: url("Fonts/SBL_Hbrw.ttf"); }
@font-face { font-family: "SBL Greek"; src: url("Fonts/SBL_grk.ttf"); }
@font-face { font-family: "Ezra SIL"; src: url("Fonts/SILEOT.ttf"); }
body, div, p, span, h1, h2, h3, h4, h5, h6 { font-family: "[PRIMARY]", "SBL BibLit", "Gentium Plus", serif !important; }
body { line-height: 1.65; -webkit-font-smoothing: antialiased; }
[lang="el"], [lang="el"] * { font-family: "SBL Greek", "Cardo", "SBL BibLit", serif !important; font-size: 1.4em !important; }
[lang="he"], [lang="he"] * { direction: rtl; unicode-bidi: embed; font-family: "SBL Hebrew", "Ezra SIL", "SBL BibLit", "Cardo", serif !important; font-size: 1.6em !important; line-height: 1.4; }
[lang="he"], [lang="he"] p, [lang="he"], [lang="he"] div { text-align: left; }
```

Plus external `style/main.css` from `EPUB_STYLESHEET` in `shared.py` (linked via `<link>` tag in `<head>`).

### EPUB Structure (exact match)
| Component | File | Source |
|-----------|------|--------|
| Cover | `EPUB/cover.xhtml` | SVG image wrapper (same as converter.py) |
| Frontispiece | `EPUB/frontispiece.xhtml` | Portrait image + caption (same `find_portrait()` logic) |
| Title page | `EPUB/title.xhtml` | `_build_title_page()` — Banner of Truth design |
| Chapters | `EPUB/chNNN.xhtml` | `<section>` with `<h1>`/`<h2>` headings |
| Footnotes | `EPUB/ch120.xhtml` | Endnotes chapter with `<aside epub:type="endnote">` |
| NAV | `EPUB/nav.xhtml` | Hierarchical `<ol>/<li>` + landmarks |
| OPF | `content.opf` | Version 3.0, font manifest, NCX fallback |
| NCX | `toc.ncx` | Daisy 2005-1 format |
| Styles | `style/main.css` | From `shared.py` `EPUB_STYLESHEET` |
| Fonts | `Fonts/*.ttf` | Primary font + SBL supplements |
| Apple Books | `META-INF/com.apple.ibooks.display-options.xml` | `specified-fonts="true"` |

### Chapter XHTML Format (match ch008.xhtml)
```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" ...>
  <head>
    <title>{CHAPTER_TITLE}</title>
    <link href="style/main.css" rel="stylesheet" type="text/css"/>
    {FONT_STYLES}
  </head>
  <body>
    <section>
      <h1>{TREATISE_TITLE}</h1>
      <h2>{CHAPTER_NUMBER}</h2>
      <p class="Body">...</p>
    </section>
  </body>
</html>
```

Greek inline: `<span lang="EL" xml:lang="EL" class="Greek">` with inner `<span lang="el" xml:lang="el">`  
Hebrew inline: `<span lang="HE" xml:lang="HE" class="Hebrew">` with inner `<span lang="he" xml:lang="he" dir="rtl">`

---

## Output Structure

```
volumes/v{N}/
├── intermediate/
│   ├── volume_{N}.thml.xml          ← UNCHANGED (existing pipeline)
│   └── volume_{N}.pdftohtml.xml     ← NEW (saved for debugging/reproducibility)
├── output/
│   └── volume_{N}.epub              ← UNCHANGED (ThML pipeline)
└── output_pdftohtml/
    └── volume_{N}.epub              ← NEW (pdftohtml pipeline)
```

Skips volumes 5 and 10 (CCEL XML source, no PDF).

---

## Implementation Phases

### Phase 1: Core Engine
- [x] Verify pdftohtml XML format with all font variants
- [x] Write pdftohtml XML parser (fontspec catalog + text element extraction)
- [x] Implement noise filtering (page numbers, AGES boilerplate, scripture codes)
- [x] Implement line grouping and paragraph detection
- [x] Implement heading classification
- [ ] Test on Volume 1, inspect output quality

### Phase 2: Greek/Hebrew + Chapter Building
- [ ] Implement Koine font detection and Beta Code conversion
- [ ] Implement Gideon font detection and Gideon conversion
- [ ] Handle multi-font line splitting
- [ ] Build chapter XHTML content
- [ ] Build treatise title pages
- [ ] Test on Volume 1 (verify Greek/Hebrew fidelity)

### Phase 3: EPUB3 Assembly
- [ ] Wire into shared.py (VOLUME_CONFIG, stylesheet, fonts)
- [ ] Implement NAV state machine
- [ ] Add frontispiece, title page, landmarks, Apple Books config
- [ ] Full EPUB3 repackage
- [ ] Test on Volume 1 end-to-end

### Phase 4: Validation & Rollout
- [ ] Compare Volume 1 output against reference EPUB
- [ ] Run on volumes 2-4, 6-9 (PDF-only)
- [ ] Log any new bugs to BUGS_AND_FIXES.md
- [ ] Update AGENTS.md with new converter usage
