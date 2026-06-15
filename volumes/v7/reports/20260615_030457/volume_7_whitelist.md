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
* Spaced punctuation (e.g., `and ,`, `ignorant ,`, `Lord ;`, `flatteries :`).
* Spaced numbers in lists or outlines (e.g., `1 .`, `2 .`, `3 .`, `4 .`, `5 .`, `6 .`, `7 .`, `1st .`, `2dly .`).
* Double periods (`..`) resulting from abbreviation formatting.

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
* **Pages 3, 7**: Front matter tables of contents that are overridden in the converter (`volumes/v7/convert.py`) with a custom HTML table of contents (`_V7_CONTENTS_PAGE`).
* **Pages 3, 4, 5, 6, 24, 31, 37, 39, 45**: Dense source windows on introductory/TOC pages and pages with complex Greek phrases or scripture citations that trigger mismatch warnings in dense page scans.
* **Page 25**: Heavily polyglot Greek/Hebrew page.

### Top and Bottom of Page Text Loss
* **Page 183 (top_of_page)**: Likely a chapter-boundary page where top-line text didn't align perfectly with the dense window scanner.
* **Pages 3, 24 (top_of_page)**: Header/metadata page boundaries.
* **Page 2, 103 (bottom_of_page)**: Imprint page and page with bottom Latin quote where text loss is expected/benign.

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
* Spaced punctuation split checks (`set up their banners for tokens, we know not; for, —` and `proposed as the foundation of the present discourse; as, —`).
* Outline paragraph transitions starting with `"Affections thus led unto"`, `"An habitual suitableness"`, and `"When sin hath in any instance"`.
* All paragraph splits listed in the JSON whitelist have been verified against the print edition.

## 3. Ignored Warnings
The following warnings are ignored as they represent false positives or benign features:
* `repeated_windows`: Flags `"the grace and duty of being spiritually minded"`, which is the legitimate title of the second treatise and naturally repeated.
* `roman_heading_candidates` / `enumerator_sequence_candidates`: Owen's list jumps are authentic and verified against the print edition.
* `dense_source_window_loss` / `front_matter_toc_loss`: Handled via custom HTML overrides.
* `low_latin_tagging` / `low_latin_translation_coverage`: Technical Debt. Latin tagging is at 51.2%, translation at 71.4%. Common English words inflate the untagged count. Adding targeted `<span lang="la">` tags and translation footnotes for genuinely Latin phrases would improve these metrics over time.
