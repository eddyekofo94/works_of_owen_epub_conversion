# John Owen Works — Converter

## Active Converter

`converter.py` — Unified EPUB3 pipeline for Owen Works and Hebrews Commentary.

```bash
# Owen Works — process a single volume:
.venv/bin/python3 converter.py 3

# Owen Works — process all 16 volumes:
.venv/bin/python3 converter.py

# Hebrews Commentary — process all 7 volumes:
.venv/bin/python3 converter.py --hebrews

# Hebrews Commentary — process a single volume:
.venv/bin/python3 converter.py --hebrews 4
```

Outputs:
- Owen Works: `volumes/vN/output/volume_N.epub`
- Hebrews: `hebrews/volumes/hbN/output/hebrews_vN.epub`

Intermediates: `volumes/vN/intermediate/volume_N.thml.xml`

Dependencies: `.venv/bin/pip install ebooklib pdfminer.six`

---

## Pipeline Overview

| Stage | Owen Works | Hebrews |
|-------|-----------|---------|
| Source | AGES PDF / CCEL XML | Calibre EPUB2 |
| Stage 1 | PDF → ThML (`pdf_to_thml`) | Read HTML from ZIP |
| Language | Beta Code → Unicode Greek, Gideon → Unicode Hebrew | Already Unicode — tag with `lang`/`xml:lang`/`dir` |
| Stage 2 | ThML → EPUB3 | EPUB2 → EPUB3 (clean, re-tag) |
| EPUB3 | Font injection, NAV, landmarks, OPF, Apple Books | Same |

---

## Project Structure

```
Owen/
├── PLAN.md                       # Full project plan with progress tracking
├── .gitignore
├── converter.py                  # Unified EPUB3 converter (Owen Works + Hebrews)
├── shared.py                     # Constants, font pools, CSS, Greek/Hebrew maps
├── .venv/                        # Python virtual environment
├── hebrews/
│   ├── volumes/hb1–hb7/          # Per-volume directories
│   ├── covers/                   # hb1.png–hb7.png (inconsistent naming)
│   └── blemishes/                # Scan defect references
├── volumes/                       # Per-volume working directories
│   └── v1/ through v16/
│       ├── input/                # Source PDF (symlink to ../../pdfs/)
│       ├── intermediate/          # volume_N.thml.xml
│       ├── output/               # volume_N.epub
│       └── bugs_fixes/           # BUGS_AND_FIXES.md
├── covers/                       # v1.png–v16.png
├── fonts -> ../../fonts           # Symlink to shared font repository
├── pdfs/                         # Source PDFs (owen-v1.pdf through owen-v16.pdf)
├── special_sources/              # CCEL XMLs (volumes 5 and 10)
└── reference/                    # Archived old code & approaches
```

---

## Volume Metadata

| Vol | Subtitle | Source |
|-----|----------|--------|
| 1 | The Glory of Christ | AGES PDF |
| 2 | Communion with God | AGES PDF |
| 3 | The Holy Spirit | AGES PDF |
| 4 | The Work of the Spirit | AGES PDF |
| 5 | Faith and Its Evidences | CCEL XML |
| 6 | Temptation and Sin | AGES PDF |
| 7 | Sin and Grace | AGES PDF |
| 8 | Sermons to the Nation | AGES PDF |
| 9 | Sermons to the Church | AGES PDF |
| 10 | The Death of Christ | CCEL XML |
| 11 | Continuing in the Faith | AGES PDF |
| 12 | The Gospel Defended | AGES PDF |
| 13 | Ministry and Fellowship | AGES PDF |
| 14 | True and False Religion | AGES PDF |
| 15 | Church Purity and Unity | AGES PDF |
| 16 | The Church and the Bible | AGES PDF |

Hebrews: 7 volumes (hb1–hb7), all EPUB2 source.

---

## Font Strategy

**Primary pool** (deterministic per-volume hash, all support Latin + Greek + Hebrew):

| Font | Variants | Hebrew | Greek |
|------|----------|--------|-------|
| SBL BibLit | Regular | Full (incl. cantillation) | Full polytonic |
| Cardo | R/B/I | Full (incl. cantillation) | Full polytonic |
| Libertinus Serif | R/B/I/BI | Full (no cantillation) | Full polytonic |

**Always-injected supplements:** SBL BibLit, SBL Greek, SBL Hebrew, Ezra SIL

**CSS stacks:**
- Body: `"[PRIMARY]", "SBL BibLit", "Gentium Plus", serif`
- Greek: `"SBL Greek", "Cardo", "SBL BibLit", serif` (1.15em)
- Hebrew: `"SBL Hebrew", "Ezra SIL", "SBL BibLit", "Cardo", serif` (1.5em, RTL)

---

## Font Encoding Reference

**Greek — AGES Koine-Medium font (Beta Code → Unicode):**
- Maps ASCII letters to Greek letters (e.g., `a`→α, `b`→β, `g`→γ)
- Diacritics: `j/J`=smooth/rough breathing, `>/<`=acute/grave, `~/=`=circumflex, `|/{|`=iota subscript
- Final sigma: `v`→ς (at word end), `v`→σ (word-internal) — **fix pending in Phase 3**
- Full tables in `shared.py`

**Hebrew — AGES Gideon-Medium font (visual L→R → logical R→L):**
- Text stored as visual L→R order; reversed per word
- Vowels attached to preceding consonant; word order reversed
- Full tables in `shared.py`

**Hebrews EPUBs — already Unicode, needs `lang` tagging only:**
- Greek: `<span lang="el" xml:lang="el">`
- Hebrew: `<span lang="he" xml:lang="he" dir="rtl">`

---

## Dependencies

```bash
# In project venv:
.venv/bin/pip install ebooklib pdfminer.six
```

---

## Foundational Mandates

All technical standards and mandatory protocols are maintained in the root **`GEMINI.md`** file. Every agent working on this project MUST prioritize the mandates in that document to ensure technical integrity and quality.