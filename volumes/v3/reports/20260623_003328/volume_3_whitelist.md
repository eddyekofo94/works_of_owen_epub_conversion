# Whitelist Log — Volume 3 (Pneumatologia)

This document contains a human-readable list of all items whitelisted in `volume_3_whitelist.json`. These exclusions prevent the automated QA audit (`scripts/run_all_checks.py`) from flagging false positives or historical spelling variations as conversion errors.

---

## 1. Anomalies (Historical Orthography & Layout Sequences)

### Punctuation Spacing Blemishes
These items represent historical layout punctuation and spacing sequences that are whitelisted to prevent false positives:
- Spaced periods (e.g. `1 .`, `2dly .`, `end .`, `Ans .`, `idem .`, `4thly .`, `habit .`, `3dly .`, `Assimilation :`, `transgression :`, `free ;`, `n )`, `sin :`).

### OCR & Bracket Residues
- `express[ed` and `express[ed]` represent bracketed additions in the source text.

### Structural Nesting Sequence Jumps
- Outline sequence jumps (e.g. `1. ... 3.`, `2. ... 4.`, `4. ... 6.`, `3. ... 7.`, `1. ... 4.`, `2. ... 5.`) that are intentional in Owen's original text layout.

---

## 2. Text Integrity & Layout Constraints

### Ignored Warnings
The following warnings are suppressed globally for Volume 3 because they represent known layout and transcription realities (e.g. running headers/footers in the PDF that are redacted in the EPUB, or Latin passages without modern translations):
*   `low_word_coverage`
*   `low_latin_tagging`
*   `low_latin_translation_coverage`
*   `repeated_phrases`
*   `enumerator_sequence_candidates`
*   `repeated_windows`
*   `dense_source_window_loss`

### Skipped & Weak Pages
*   **Pages 3–31 (Skipped):** Table of Contents (TOC) and front matter pages. These pages use non-standard page structures, layouts, and lists that do not match prose chapter formats.
*   **Weak pages:** Specific front-matter and low-density matching pages with layout variations.

---

## 3. Paragraph Splits (Valid Continuation & Layout Breaks)

These transitions look like paragraph splits (e.g. lines starting with lowercase letters, name listings, or short phrases) but represent valid structural layouts:
- Preface greetings, signature blocks, sentence continuations across Bible citations, or subpoint transitions.

---

## 4. Unmatched Quotation Marks

John Owen's text features long blockquotes, embedded scripts, and multi-paragraph citations where quotation marks do not follow modern open/close matching rules on a single-paragraph basis. 

The whitelisted items include:
*   Treatise title page fragments (e.g., chrysostom quote and editorial notes).
*   Scripture and blockquote blocks starting with opening quotes that continue across several pages.
*   Long Latin and Greek citations where the text has smart quotes or double quotes that close across multiple paragraphs.
*   Preface comments and objections containing balanced quotes that cross paragraph bounds.
