# Text Anomaly Audit, Whitelisting, and Triage Architecture

This document provides a complete guide to how text anomalies are scanned, stored, whitelisted, and repaired within the John Owen Works digitization pipeline. This architecture is designed to be fully modular and transferrable to any text digitization, OCR correction, or EPUB conversion project.

---

## 1. Core Philosophy: OCR Error vs. Historical Orthography

When digitizing historical texts (such as 17th-century Puritan writings), the primary directive is: **NEVER modernize historical spelling or hyphenation.**

Anomalies are divided into two distinct groups:
1. **Clear OCR Noise / Typos:** Spliced letters and numbers (e.g., `w1th`), brackets inside words (e.g., `on]y`), duplicate punctuation (e.g., `,,`), layout-induced hyphen remains (e.g., `Peta-vius` split across lines), or invalid biblical citations. These must be repaired.
2. **Acceptable Historical Spellings/Hyphenations:** Compound terms or archaic forms common to the author's era (e.g., `birth-place`, `free-will`, `co-essential`, `hath`, `doth`). These must be preserved exactly as written and added to the **whitelist** rather than being modified.

---

## 2. The 9 Categories of Text Anomalies

The audit tool scans the parsed intermediate JSON files containing chapter text. It applies the following checks:

### A. Hyphenation Anomalies
*   **Purpose:** Identify hyphenated words that are residues of line breaks or incorrect OCR splitting.
*   **Heuristics:**
    1.  *Capitalized word checks:* If a capitalized word is hyphenated (e.g., `Peta-vius`), and either the left or right particle is not a recognized word (minimum length > 2), it is flagged.
    2.  *Rejoined check:* If removing the hyphen yields a valid dictionary word (e.g., `re-join` $\to$ `rejoin`, or `acknow-ledged` $\to$ `acknowledged`), it is flagged as a splittable word.
    3.  *Double unrecognized particles:* If neither particle is a recognized word (e.g., `sur-misal`), it is flagged.
*   **Regex Pattern:** `\b([A-Za-z]+)-([A-Za-z]+)\b`

### B. Punctuation Spacing Blemishes
*   **Purpose:** Locate visual alignment mistakes around punctuation characters.
*   **Checks:**
    1.  *Spaces before characters:* Space directly preceding `,`, `;`, `:`, `!`, `?` or `.` (excluding ellipses `...`).
    2.  *Duplicated punctuation:* Two or more consecutive commas (`,,`), semicolons (`;;`), colons (`::`), or exactly two periods (`..`).
    3.  *Inside bracket spaces:* Spaces directly following opening parentheses/brackets or preceding closing parentheses/brackets (e.g., `( word` or `word )`).
*   **Regex Patterns:**
    *   Spaces before punctuation: `\b[A-Za-z0-9]+\s+([,;:!?])` and `\b[A-Za-z0-9]+\s+\.(?!\.)`
    *   Duplicate period: `(?<!\.)\.\.(?!\.)`
    *   Inside brackets: `\(\s+[A-Za-z0-9]` and `[A-Za-z0-9]\s+\)`

### C. OCR & Bracket Residues
*   **Purpose:** Find stray non-alphabetic characters introduced by scanners or template files.
*   **Checks:**
    1.  *Inline brackets/parentheses:* Stray brackets split inside a word (e.g. `on]y`, `name]y`, `th[e]`).
    2.  *Mixed alphanumeric characters:* Words containing numbers inline (e.g., `w1th`, `th1s`). Standard ordinals (`1st`, `2nd`) are ignored.
    3.  *Stray ordinals or footnotes:* Typo ordinals like `(l)` meant to be `(1)`, or stray lowercase `l` following standard abbreviations (e.g., `lib. l` meant to be `lib. 1` or `lib. i`).
    4.  *Spliced/Split words:*
        *   Isolated letters (except `a`, `i`, `o`) followed by lowercase segments (e.g., `s upernatural`).
        *   Consecutive words that, if joined, form a valid dictionary word while the second part is nonsense on its own (e.g. `acknow ledged` $\to$ `acknowledged`).
*   **Regex Patterns:**
    *   Stray brackets: `\b[A-Za-z]+[\]\)]+[A-Za-z]+\b` and `\b[A-Za-z]+[\[\(]+[A-Za-z]+\b`
    *   Inline numbers: `\b[A-Za-z]+\d+[A-Za-z]+\b`
    *   Stray L: `\b(lib|cap|chap|vol|p|pp|v|sect|fol)s?\.?\s*(?:[†*‡§¶#]|\b)?\s*\bl\b`

### D. Mixed-Case Capitalization Errors
*   **Purpose:** Find OCR errors where case shifts randomly within words.
*   **Checks:** Words with uppercase characters inside them (excluding standard prefixes like `Mc`, `Mac`, `De`). E.g., `thE`, `anD`, `ChriSt`.
*   **Regex Patterns:** `\b[a-z]+[A-Z]+[a-z]*\b` and `\b[A-Z][a-z]+[A-Z]+[a-z]*\b`

### E. Unresolved Citation References
*   **Purpose:** Flag citations of patristic, classical, or ancient sources that lack corresponding English translations in the text.
*   **Checks:** Matches classical citation markers (e.g., `De Civ. Dei, lib. 22 cap. 8`) and checks if a translation exists in the translation database or adjacent text.

### F. Structural Nesting Sequence Jumps
*   **Purpose:** Audit outlines and lists for missing entries or structural numbering jumps.
*   **Checks:** Extracts sequential list markers (`1. 2. 3.`, `(a) (b) (c)`, `I. II. III.`) and checks if there are gaps (e.g., a `1.` followed shortly by a `3.`, skipping `2.`). It filters out biblical references (e.g. `John 3:16`) and publication dates.

### G. Invalid Bible References
*   **Purpose:** Catch OCR errors in scripture references.
*   **Checks:** Compares chapter numbers against a dictionary of maximum chapters per Bible book (e.g., flagging `Romans 18` or `Genesis 52`).

### H. List Formatting Inconsistencies
*   **Purpose:** Verify visual consistency in list rendering.
*   **Checks:** Identifies if a single sequence of items mixes bold and plain markers (e.g., `**1.**` mixed with `2.`).

### I. Unmatched Quotation Marks
*   **Purpose:** Detect unbalanced quotation marks that disrupt reader alignment.
*   **Checks:** Counts straight and curly double quotes (`"`, `“`, `”`) within paragraphs and flags paragraphs with odd counts.

---

## 3. Storage Schema

To make the findings actionable for developers and other agents, they are saved in the volume's `bugs_fixes/` subdirectory under two formats:

### A. JSON Output (`volume_N_anomalies.json`)
Allows programmatic parsing and validation:
```json
{
  "volume": "7",
  "total_words_audited": 184512,
  "total_anomalies_count": 2,
  "anomalies": {
    "Hyphenation Anomalies": [
      {
        "target": "Peta-vius",
        "description": "Capitalized hyphenation with unrecognized left particle",
        "chapter": "Chapter I",
        "contexts": [
          "... written by Peta-vius in his work ..."
        ]
      }
    ],
    "OCR & Bracket Residues": []
  },
  "unused_whitelist_anomalies": {}
}
```

### B. Markdown Output (`volume_N_anomalies.md`)
Allows direct human triage:
```markdown
# Text Integrity & Anomaly Audit Report: Volume 7

* **Total Words Audited:** 184512
* **Total Suspected Anomalies Found:** 2

## Summary by Category
* **Hyphenation Anomalies:** 1 items
* **OCR & Bracket Residues:** 1 items

---

## Hyphenation Anomalies
### 1. `Peta-vius`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Chapter I*
* **Contexts:**
  * ... written by **Peta-vius** in his work ...
```

---

## 4. The Whitelisting Mechanism

When anomalies are identified as acceptable historical forms or false positives, they are whitelisted.

### A. Whitelist Storage
Every volume maintains two synced files under `volumes/vN/bugs_fixes/`:
1.  `volume_N_whitelist.json` - Read by the audit script to filter future runs.
2.  `volume_N_whitelist.md` - A human-readable file explaining *why* each item was whitelisted.

### B. JSON Schema (`volume_N_whitelist.json`)
```json
{
  "anomalies": {
    "Hyphenation Anomalies": [
      "birth-place",
      "free-will",
      "co-essential"
    ],
    "Punctuation Spacing Blemishes": [],
    "OCR & Bracket Residues": [
      "Scanner Substring False Positives"
    ],
    "Unmatched Quotation Marks": []
  }
}
```

### C. Markdown Schema (`volume_N_whitelist.md`)
```markdown
# Volume 7 Whitelist Audits

This document lists and explains all whitelisted items for Volume 7.

## Hyphenation Anomalies
* `birth-place`: Authentic 17th-century compound hyphenation.
* `free-will`: Authentic historical compound hyphenation.

## OCR & Bracket Residues
* `e coelo`: Valid Latin phrase; split word scanner false positive.
```

### D. Audit Filtration Logic
During an audit run, the script checks targets against the JSON whitelist. The matching logic incorporates clean-ups (stripping HTML, markdown symbols, and footnotes) to avoid mismatching due to minor formatting shifts:
```python
def is_whitelisted(category: str, target: str, whitelist: dict) -> bool:
    items = whitelist.get("anomalies", {}).get(category, [])
    # Normalize strings (remove markdown, HTML tags, trim, and lowercase)
    # ...
    return normalized_target in normalized_items
```

---

## 5. Resolution & Override Mechanism

When an anomaly is determined to be a genuine OCR error, it is repaired by adding it to the `OVERRIDES` dictionary inside the volume's per-volume script (`volumes/vN/convert.py`).

```python
# volumes/v7/convert.py
OVERRIDES = {
    "text_replacements": {
        "Peta-vius": "Petavius",
        "on]y": "only",
        "name]y": "namely",
        "w1th": "with"
    }
}
```

During the rendering process (Stage 2), these overrides are applied to the raw text blocks before outputting to EPUB XHTML.

---

## 6. Replication Checklist for Other Projects

To apply this exact architecture to another text processing or eBook conversion project, follow these steps:

1.  **Define a Standard Dictionary:** Load system dictionary words (e.g. `/usr/share/dict/words`) and extend it with a custom set of project-specific terms (e.g. theological, historical, or scientific terminology).
2.  **Implement Heuristics:** Write python functions scanning for the 9 categories of checks. Enforcement of word boundaries (`\b`) is essential to prevent false positives.
3.  **Generate Structured Reports:** Output programmatic JSON files to track metrics over time, and Markdown reports to make triage effortless.
4.  **Create Double-Whitelists:** Require both a JSON file for the parser to read and a Markdown file with human-readable rationale. This ensures that whitelists do not silently decay or contain unverified entries.
5.  **Build a Replacement Pipeline:** Set up a configuration layer where replacements are loaded dynamically per document volume to keep the base code clean and generic.
