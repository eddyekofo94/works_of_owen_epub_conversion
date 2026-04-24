# John Owen Works — Converters

All scripts run from the directory containing PDF files and a `covers/` subfolder.

## Converters (5 total)

### 1. `scripts/` — Modular pipeline (recommended)

Two-stage pipeline using `pdfminer.six` + `ebooklib`. `scripts/shared.py` is the canonical source for Greek maps, Hebrew maps, volume metadata, and EPUB styles.

**Stage 1 — PDF → ThML XML:**
```bash
python3 scripts/pdf_to_thml.py [work_dir]
```
Outputs `volume_N.thml.xml`. Skips if `.thml.xml` exists (delete to reconvert).

**Stage 2 — ThML XML → EPUB:**
```bash
python3 scripts/thml_to_epub.py [work_dir]
```
Outputs `volume_N.epub`. Skips if `.epub` exists (delete to reconvert).

Dependencies: `pip install pdfminer.six ebooklib`

---

### 2. `convert_owen_v2.py` — Legacy monolithic pipeline

PDF → ThML XML → EPUB in one script. Uses `pdfminer.six` + `ebooklib`. Standalone (duplicates Greek maps and volume metadata from `scripts/shared.py`).

```bash
python3 convert_owen_v2.py [work_dir]
```
Outputs `volume_N.thml.xml` + `volume_N.epub`. Skips if both exist.

Dependencies: `pip install pdfminer.six ebooklib`

---

### 3. `convert_owen_to_epub.py` — Legacy direct converter

PDF → EPUB direct via `pypdf` (no ThML intermediate). Older approach, fewer features.

```bash
python3 convert_owen_to_epub.py [work_dir]
```
Outputs `volume_N.epub`. Skips if exists (delete to reconvert).

Dependencies: `pip install pypdf ebooklib`

---

### 4. `hebrews/convert_hebrews.py` — EPUB post-processor (separate project)

Processes existing EPUBs of the Hebrew commentary (not Owen Works PDFs). Rebuilds with hierarchical TOC, better formatting, and embedded CSS.

```bash
python3 hebrews/convert_hebrews.py [work_dir]
```

Dependencies: `pip install ebooklib`

---

### 5. `personal_conversion/convert_to_epub.py` — Calibre-based converter

Uses Calibre's `ebook-convert` for PDF extraction, then post-processes. Requires Calibre installed (`ebook-convert` on PATH).

```bash
python3 personal_conversion/convert_to_epub.py
```
Config: hardcoded to `owen-v1.pdf` and `covers/v1.png`. Edit script to change.

Dependencies: Calibre CLI (`ebook-convert`), `pip install ebooklib`

---

## Expected layout

```
work_dir/
├── [John_Owen]_Works_of_John_Owen_vol_01.pdf   ← PDF naming pattern
├── ...
├── covers/
│   ├── v1.jpg      (or .png)
│   └── ...v16.jpg
├── volume_N.thml.xml    (intermediate, scripts/ pipeline)
└── volume_N.epub
```

---

## Font encoding reference

**Greek — AGES Koine-Medium font (Beta Code → Unicode):**
- Maps ASCII letters to Greek letters (e.g., `a`→α, `b`→β, `g`→γ)
- Diacritics: `j/J`=smooth/rough, `>/<`=acute/grave, `~/=`=circumflex, `|/{|`=iota sub
- Final sigma: `v`→ς
- Full tables in `scripts/shared.py`

**Hebrew — AGES Gideon-Medium font (RTL reversal):**
- Text stored as visual L→R order; must be reversed per word
- Vowels attached to preceding consonant; word order reversed
- Full tables in `scripts/shared.py`

---

## Dependencies

```bash
pip install pdfminer.six ebooklib
```

(For Calibre-based converter: install Calibre separately)