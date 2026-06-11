# Volume 7 Whitelist Exclusions

This document lists and explains all whitelisted items for Volume 7 of the John Owen Works conversion project.

## 1. Anomalies

### Hyphenation Anomalies
The following hyphenated words are authentic to Owen's 17th-century orthography and should not be modernized or split:
* `non-proficiency`
* `evil-doer`
* `new-fangledness`
* `over-earnest`
* `pre-admonition` / `pre-admonitions`
* `un-humbled`
* `here-withal`
* `top-stone`
* `over-fullness`
* `cross-ways`
* `stout-heartedness` / `stout-hearted`
* `fire-ball`
* `hand-breadth`
* `three-fold`
* `un-commanded`
* `where-into`
* `Adul-lam` (place name)
* `ale-house`
* `Spiritual-mindedness`
* `over-valuation`

### Punctuation Spacing Blemishes
Benign spacing artifacts in the original print that do not hinder legibility:
* Spaced punctuation (e.g. `and ,`, `ignorant ,`, `hereafter .`, `sin .`, `Lord ;`, `flatteries :`, `seasons .`, `no .`).
* Spaced numbers in lists or outlines (e.g. `1 .`, `2 .`, `3 .`, `4 .`, `5 .`, `6 .`, `7 .`, `1st .`, `2dly .`, `st .`).
* Double periods (`..`) resulting from abbreviation formatting.

### OCR & Bracket Residues
* `them)is`: An archaic contraction or print artifact.

### Mixed-Case Capitalization Errors
* `menlHow`: Print spacing error ("men. How" or similar) in the source text.

### Structural Nesting Sequence Jumps
Authentic jumps in the outline sequences of the original print source:
* `I. ... III.`
* `III.` (starting sequence)
* `II.` (starting sequence)
* `1. ... 3.`
* `II. ... XIX.`
* `3. ... 5.`

### Unmatched Quotation Marks
Quotations containing translation snippets or blockquotes where the matching quotation mark is outside the scanned paragraph context:
* Latin/Syriac quotes in chapter introductions.
* Scripture citations and long expository extracts.

## 2. Text Integrity Exclusions

### Weak/Missing Pages & Front Matter TOC Loss
* **Pages 3, 7, 24**: These are early/introductory pages containing the Table of Contents, Analysis, and Title page. Since we override them or exclude them in the converter (`volumes/v7/convert.py`) using custom HTML overrides, they are naturally missing from the main sequential flow matching.
* **Pages 31, 37, 39, 45, 59**: These pages contain Greek phrases (e.g. `δωρεα`) or complex bible citations that lead to minor mismatch warnings in dense page-window scans. The text itself is fully present in the EPUB.

### Top/Bottom-of-Page Text Loss
* **Page 2, 3, 24, 183**: Minor header/footer lines or transitional page breaks that are skipped or overriden as front matter.

### Inline Structural Markers
These are authentic inline enumerators inside prose paragraphs that should not start new block-level paragraphs:
* `"To those who confine the whole of obedience to morality"` (Analysis inline enumeration).
* `"Special trials and temptations; and 3. Heavenly and eternal realities"` (Analysis inline list).
* `"It is the spiritual mind alone that can reconcile those things"` (Contains inline enumerator `1st.`).
* `"The reason of the assurance that sin shall have no more dominion over believers"` (Contains inline `1.`, `2.`, `3.` outline).

### Paragraph Splits
Suspicious transitions that represent correct paragraph breaks in context:
* `To The Reader`
* Greek quotes (`Αδύνατον γὰρ τοὺς`)
* Multi-part list items and headings (e.g. `III.`, `XIX.`, `(5thly.)`, `John Owen`, `D.D. LONDON: 1688`).

## 3. Ignored Warnings
The following warnings are ignored as they represent false positives or benign features:
* `low_latin_tagging` / `low_latin_translation_coverage`: Latin vocabulary checks flag common English words or names (like `sincere`, `poor`, `Damasus`).
* `repeated_windows`: Flags `"the grace and duty of being spiritually minded"`, which is the legitimate title of the second treatise and naturally repeated.
* `roman_heading_candidates` / `enumerator_sequence_candidates`: Owen's list jumps are authentic and verified against the print edition.
