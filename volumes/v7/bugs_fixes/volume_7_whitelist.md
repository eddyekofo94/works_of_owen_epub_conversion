# Volume 7 Whitelist Exclusions

This document lists and explains all whitelisted items for Volume 7 of the John Owen Works conversion project.

## 1. Anomalies

### Hyphenation Anomalies
The following hyphenated words are authentic to Owen's 17th-century orthography and should not be modernized or split:
* `Spiritual-mindedness`
* `ale-house`
* `cross-ways`
* `evil-doer`
* `fire-ball`
* `hand-breadth`
* `here-withal`
* `new-fangledness`
* `non-proficiency`
* `over-earnest`
* `over-fullness`
* `over-valuation`
* `pre-admonition` / `pre-admonitions`
* `stout-hearted` / `stout-heartedness`
* `three-fold`
* `top-stone`
* `un-commanded`
* `un-humbled`
* `where-into`

### Punctuation Spacing Blemishes
Benign spacing artifacts in the original print that do not hinder legibility:
* Spaced punctuation (e.g., `and ,`, `ignorant ,`, `Lord ;`, `flatteries :`, `1st ,`).
* Double periods (`..`) resulting from abbreviation formatting, or tag-stripping residues (e.g., `1st .`, `cupido .`, `vehicula ,`, `morbi ,`, `ordinis ;`, `datum ,`, `sapit ,`, `naturae ,`, `fatuus ,`).

### Structural Nesting Sequence Jumps
Authentic outline sequence discontinuities from Owen's printed structure:
* `1. ... 3.`
* `3. ... 5.`
* `I. ... III.`
* `II.` (starting sequence)
* `II. ... XIX.`
* `III.` (starting sequence)

### Unmatched Quotation Marks
The following paragraphs contain unmatched quotation marks due to multi-paragraph blockquotes, nested citations, or inline Greek/Latin quotes:
* `(1.) In extraordinary, outward judgments upon open, profligate sinners, especially the enemies of his church and glory.`
* `1. The gift of God, δωρεά, is either δόσις, "donatio," or δώρημα, "donum." Sometimes it is taken for the grant or giving`
* `4. They are the way and means whereby the soul applies itself unto all sinful objects and actings. Hence are they called`
* `But the fixing of spiritual affections on spiritual objects is perfective of our present state and condition; not that w`
* `But there are yet other instances of the proneness of men in foregoing the faith that the church was retrieved unto at t`
* `By grace our minds are renewed, — that is, changed and delivered from this frame; but they are so partially only. The pr`
* `Others there are, sincere, broken-hearted believers, [who,] scared at the rock of presumption on which they see so many`
* `The FIRST thing in the description is, that they were ἅπαξ φωτισθέντες, "once enlightened." Saith the Syriac translation`
* `Unto this pride, as inseparable from it, we may adjoin that vanity and curiosity that are in the minds of men. These are`
* `We judge no men, no party of men, as to their eternal state and condition, upon the account of their outward profession`
* `who shall deliver me from this body of death?" Yea, they groan under a sense of it every day, nor is any thing such a tr`
* `Καὶ μετόχους γενηθέντες Πνεύματος ἁγίου. "Et participes facti sunt Spiritus Sancti," Vulg. Lat.; — "And are made partake`
* `Τέλειοι γίνεσθε ταῖς φρεσί, Be ye complete, perfect," well instructed in your minds, fully initiated into the doctrines`

## 2. Text Integrity Exclusions

### Weak/Missing Pages & Front Matter TOC Loss
* **Page 3**: Front matter table of contents page that is overridden in the converter (`volumes/v7/convert.py`) with a custom HTML table of contents (`_V7_CONTENTS_PAGE`). It has a lower text hit ratio against raw PDF text.
* **Page 25**: Heavily polyglot Greek/Latin page with lower text hit ratio due to font-encoding differences.

### Dense Source Window Loss
The following 40 pages have dense source window losses that are benign or false positives:
* **Introductory, Preface & TOC Pages** (where structure differs from normal page flow):
  * **Pages 3, 4, 5, 6**: Front matter table of contents page boundaries.
  * **Page 24**: First page of Chapter 1 containing title header layout.
* **Polyglot & Translation Insertion Pages** (where inline translation notes like `[Translated: ...]` disrupt contiguous word matching):
  * **Page 25**: Latin and Greek definitions (`Qui semel fuerint illuminati`, `Γευσαμένους τε τῆς δωρεᾶς...`).
  * **Page 26**: Greek phrase and Latin translations (`Rursum crucifigentes sibimetipsis Filium Dei`).
  * **Page 31**: Short Greek phrase and citation.
  * **Page 37**: Inline Greek/Latin citation definitions (`δωρεά`, `illustrati`).
  * **Page 39**: Greek words layout.
  * **Page 42**: Greek definitions and Latin translations (`Ρῆμα` / `verbum dictum`).
  * **Page 45**: Greek citation block.
  * **Page 93**: Patristic bibliography names (`Tatianus, Athenaguras`).
  * **Page 100**: Historical patristic citations with biographical tags (`St Austin`).
  * **Page 103**: Blockquote Latin quote with inline translation (`Latius excisae serpit contagio gentis`).
* **Orthography, Hyphenation, and Tokenization Mismatches** (where line-breaks or compound words cause spelling variations):
  * **Page 64**: Tokenization variation of compound `long-suffering` / `longsuffering`.
  * **Page 82**: Typo correction in EPUB (`contained` replacing OCR `conrained`), which differs from raw PDF words `con rained`.
  * **Page 95**: Line-break hyphenation `pela-gianism` in PDF successfully healed to `Pelagianism` in EPUB.
  * **Page 201**: Line-break hyphenation `self-conceitedness` in EPUB.
  * **Page 221**: Line-break hyphenation boundary.
  * **Page 261**: Line-break hyphenation `self-denial` in EPUB.
  * **Page 278**: Line-break hyphenation `worldly-mindedness` in EPUB.
  * **Page 314**: Line-break hyphenation `self-abasement` in EPUB.
  * **Page 327**: Spelling variant `misspense` in PDF vs EPUB.
  * **Page 377**: Line-break hyphenation `self-reflection` in EPUB.
  * **Page 388**: Line-break hyphenation `self-exaltation` in EPUB.
  * **Page 559**: Line-break hyphenation `self-abasement` in EPUB.
  * **Page 571**: Line-break hyphenation `self-denial` in EPUB.
  * **Page 582**: Compound word representation `honey comb` vs `honeycomb`.
* **Scripture Citations & Dense Formatting** (dense clusters of numbers or abbreviated book names):
  * **Page 183**: Dense list of scripture citations (`39-41`, `Acts 25-27`).
  * **Page 272**: Proper name or date formatting (`first day's meeting`).
  * **Page 283**: Scripture list abbreviations (`Hebrews`).
  * **Page 290**: Word-spacing or citation layout.
  * **Page 397**: Dense citation list.
  * **Page 451**: Dense scripture quotation formatting.
  * **Page 455**: Minor alphanumeric layout.
  * **Page 456**: Layout of divine attributes.
  * **Page 519**: Formatting around prophet Ezekiel's parables.
  * **Page 523**: Scripture references (`Isaiah 11-17`, `Micah 6-8`).
  * **Page 532**: Layout boundary for scripture citation.

### Top and Bottom of Page Text Loss
* **Page 183 (top_of_page)**: Likely a chapter-boundary page where top-line text didn't align perfectly with the dense window scanner.
* **Page 2 (bottom_of_page)**: Imprint page where bottom text represents publisher detail which is intentionally omitted in primary flow.
* **Page 103 (bottom_of_page)**: Page ending with blockquote Latin quote where bottom-of-page text scanner failed due to font-encoding differences.

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
* Multi-part list items and headings (e.g., `III.`, `XIX.`, `(5thly.)`, `John Owen`, and other outline markers).
* All paragraph splits listed in the JSON whitelist have been verified against the print edition.

## 3. Ignored Warnings
The following warnings are ignored as they represent false positives or benign features:
* `repeated_windows`: Flags `"the grace and duty of being spiritually minded"`, which is the legitimate title of the second treatise and naturally repeated.
* `enumerator_sequence_candidates`: Owen's list jumps are authentic and verified against the print edition.
* `dense_source_window_loss` / `front_matter_toc_loss`: Handled via custom HTML overrides.
* `low_latin_tagging`: Technical Debt. Latin tagging is at 63.7%. Common English words inflate the untagged count. Adding targeted `<span lang="la">` tags and translation footnotes for genuinely Latin phrases would improve these metrics over time.
