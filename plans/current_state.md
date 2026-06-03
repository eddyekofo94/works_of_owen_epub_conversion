# Project State — John Owen EPUB Conversion
**Last updated:** 2026-06-02

---

## 1. Project Goal

Produce premium, scholarly EPUB3 editions of *The Works of John Owen* (16
volumes) that match the standard of the best modern critical editions — e.g.
the Battles *Calvin Institutes*, or the *Reformed Systematic Theology* (RST).

Every abbreviated inline citation Owen makes (patristic, classical, scholastic)
must be expanded to a full modern academic footnote such as:

> John Chrysostom, *Homilies on the Gospel of John* (In Evangelium Johannis
> Tractatus), Homily 15, on John 1:18 [NPNF1, 14:51; PG 59.97–98].

This is the gold standard established by the reference EPUBs in `epub_examples/`.

---

## 2. Current Status (As of 2026-06-02)

### Pipeline
- **`extract.py`** — PDF → structured JSON intermediate (`volumes/vN/intermediate/volume_N.json`)
- **`render.py`** — JSON → EPUB3 (two translation passes + patristic expansion)
- **`translation_db.py`** — The citation database (~787 `BODY_TRANSLATIONS` entries, ~1500+ `FOOTNOTE_TRANSLATIONS`)
- **`patristic_refs.py`** — Pattern-based patristic citation resolver (`WORK_MAP`, `AUTHOR_ABBREV_MAP`)
- **`scripts/scan_citations.py`** — Audit tool for all volumes

### All 16 volumes compile successfully

### Citation Resolution State
| Metric | Count |
|---|---|
| Total citations detected | 502 |
| Resolved via `BODY_TRANSLATIONS` & `WORK_MAP` | 308 (61%) |
| Self-references (Owen citing own work) | 1 |
| **UNRESOLVED — no footnote generated** | **193 (38%)** |

Full breakdown: `plans/citation_audit_report.md`  
Machine-readable: `plans/citation_audit.csv`

---

## 3. The Two-Tier Citation System

### Tier 1: `BODY_TRANSLATIONS` (translation_db.py)

Exact string → full citation. The system finds the phrase in the rendered HTML
using flexible word-by-word matching (handles HTML span tags). The footnote
shows immediately after the matched phrase.

**Format:**
```python
"Euseb. Preparat. Evang., lib. 1 cap. 3:": (
    "<b>Modern Citation:</b> Eusebius of Caesarea, "
    "<i>Praeparatio Evangelica</i> (Preparation for the Gospel), "
    "Book 1, Chapter 3 [PG 21.28]."
),
```

**When to use:** Distinctive multi-element phrases (author + work + location).

### Tier 2: `WORK_MAP` (patristic_refs.py)

Pattern-based: given (author, work_abbrev) detected from surrounding text,
automatically expands any matching `lib./cap./epist.` location reference.

**Format:**
```python
("author_key", "work_fragment"): {
    "full_title": "English Work Title",
    "latin_title": "Latin Title",
    "std_ref": ["NPNF1, 14"],
    "pl": "PL 42",
    "pg": "PG 59",
},
```

**When to use:** Same author+work cited repeatedly across volumes with different
location numbers. One entry resolves all occurrences.

**Rule:** Only produces a footnote when the specific work is identified.
If the work cannot be determined, the pass is silent — no vague "Book 7, Chapter 29" notes.

---

## 4. Unresolved Citations — Priority Queue

**255 citations currently produce no footnote.**

### Most impactful single additions (WORK_MAP entries needed)

| Author | Work abbreviated | Owen's text | Key needed |
|---|---|---|---|
| Robert Bellarmine | *De Iustificatione* | `Bellar. de Justif., lib. 2 cap. 7` | `("bellar","de justif")` |
| Robert Bellarmine | *De Amissione Gratiae* | `Bellar. De Amiss. Grat., lib. 4` | `("bellar","de amiss")` |
| Robert Bellarmine | *De Gratia et Libero Arbitrio* | `Bellar. De Grat. et Lib. Arb., lib. 6` | `("bellar","de grat")` |
| Faustus Socinus | *De Iesu Christo Servatore* | `Socin. de Servant. lib. 3 cap. 3` | `("socin","de servat")` |
| Melchior Cano | *Loci Theologici* | `Canus, Loc. Theol., lib. 2 cap. 8` | `("canus","loc theol")` |
| Cyril of Alexandria | *Commentary on John* | `Cyrillus Alexandrinus in Joan. lib. 11` | `("cyril","in joan")` |
| Theodoret of Cyrrhus | *Ecclesiastical History* | `Theodoret, lib. 5 cap. 9` | *(already in DB — check author detection)* |
| Sozomen | *Ecclesiastical History* | `Sozomen Hist. Eccles., lib. 7` | `("sozomen","hist eccles")` |
| John of Damascus | *De Fide Orthodoxa* | `Damascen, lib. 4 chap. 3` | `("damasc","de fide")` |
| Bernard of Clairvaux | *Epistolae* | `Bernard, Epist. 190` | `("bernard","epist")` |

### Volume-by-volume breakdown
See `plans/citation_audit_report.md` for the complete per-volume list with
context snippets, probable works, and recommended action for each citation.

---

## 5. Quality Standard for New Citations

Match the format in `epub_examples/Calvin-institutes-Battles-2-Volumes_ver3-updated.epub`
and `epub_examples/RST-v1-epub3.epub`. Every footnote must include:

1. **Author** — full name (not abbreviation)
2. **Work title** — italicised English title
3. **Latin title** — in parentheses after English title (e.g. *(De Trinitate)*)
4. **Location** — Book/Chapter/Section in standard notation (not "lib. 2 cap. 8")
5. **Standard reference** — at least ONE of: NPNF1/2, ANF, PL, PG, Loeb with volume:page

**Example (target standard):**
> Augustine, *On the Trinity* (De Trinitate), Book 5, Chapters 8–9
> [NPNF1, 3:87; PL 42.912].

**NOT acceptable:**
> Modern Citation: Augustine of Hippo, Book 5, Chapter 8, 9.

---

## 6. Rendering Pipeline Flow

```
PDF
  └─ extract.py → volumes/vN/intermediate/volume_N.json
       └─ render.py → volumes/vN/output/volume_N.epub
            ├─ markdown_to_html()           (raw text → HTML)
            ├─ _apply_premium_*()           (stylistic polish)
            ├─ _apply_translations()        (Tier 1: BODY_TRANSLATIONS exact match)
            │    └─ strips <span lang="la"> from blockquotes before html_escape
            └─ _expand_inline_citations()   (Tier 2: WORK_MAP pattern match)
                 ├─ PATRISTIC_CITATION_RE   (detects lib./epist./serm. etc.)
                 ├─ PAREN_CHAPTER_RE        (detects parenthetical (cap. N))
                 ├─ _find_author_in_context()  (most-recent author in 300-char window)
                 ├─ _find_work_in_context()   (dot-normalized work abbrev search)
                 └─ build_citation_note()     (returns None if work unidentified)
```

---

## 7. How to Run

```bash
cd Owen-translation-citations

# Rebuild a single volume (render only — no re-extraction):
python3 volumes/v1/convert.py --render-only

# Run the citation audit (see what's resolved and what isn't):
python3 scripts/scan_citations.py
python3 scripts/scan_citations.py --vol 5 --unresolved
python3 scripts/scan_citations.py --csv output.csv

# Run the test suite:
/path/to/.venv/bin/python3 -m pytest tests/ -q
```

---

## 8. Next Session Priorities

1. **Research and add Bellarmine works** — De Iustificatione, De Amissione Gratiae,
   De Gratia et Libero Arbitrio (resolves ~30 citations in v5, v12, v16)
2. **Research and add Socinus works** — De Iesu Christo Servatore, Praelectiones Theologicae
   (resolves ~15 citations in v5, v10)
3. **Add Sozomen, Damascene, Melchior Cano** to AUTHOR_ABBREV_MAP + WORK_MAP
4. **Volume 14 (Hebrews)** — rabbinic citation chains need special attention
5. **Volume 15** (41 unresolved) — Reformation-era polemics, Melanchthon, Lutheran sources
