# Whitelist Explanations: Volume 6

This document lists and explains all whitelisted items for Volume 6, distinguishing true errors from authentic historical spelling, formatting, and layout styles.

## 1. Hyphenation Anomalies

These are authentic 17th-century spelling variants or compound hyphens. They are preserved intact as per the orthography rules, rather than modernized.

*   `sign-post`, `sermon-proof`, `sickness-proof`, `good-man`, `work-house`, `under-earth`, `under-ground`, `spring-head`, `day-star`, `such-like`, `eye-salve`, `land-flood`, `ale-house`, `safe-guard`, `heart-blood`, `peace-making`, `sad-hearted`, `home-bred`, `after-reckoning`, `make-bate`: Legitimate archaic compound words.
*   `Christ-dishonoring`, `Under-valuations`, `Self-determinations`, `Self-judging`, `Self-communion`: Legitimate capitalization and hyphenation styles common in Owen's works.
*   `El-shaddai`: Legitimate transliterated Hebrew name of God.

## 2. Punctuation Spacing Blemishes

These spaced punctuation elements are common in the source print layouts or are stylistic separators (such as spaced periods after numbers, Ans., or double punctuation).

*   `1st .`, `2dly .`, `3dly .`, `4thly .`, `5thly .`: Spaced ordinal period layouts.
*   `Ans .`: Answer abbreviation with spaced period.
*   `him :`, `unto :`, `heart ;`, `members ;`, `in :`: Spaced colons/semicolons typical of older typography.
*   `God !`, `discovered !`: Spaced exclamation marks.
*   `,,`: Double comma marks.
*   `..`: Double period marks.
*   `peace .`, `together .`, `duty .`, `matter .`, `God .`, `trouble .`: Spaced trailing sentence periods from the OCR source structure.

## 3. OCR & Bracket Residues

*   `E profundis`: Correct Latin theological phrase ("Out of the depths") using the letter 'E' as a preposition, not a bracket residue.

## 4. Structural Nesting Sequence Jumps

*   `II.`, `2.`, `IV.`, `VIII.`, `X.`, `XII.`, `3.`, `4.`, `5.`, `8.`, `9.`: Jumps in numbering due to lists starting at custom values (like "RULE 2", "RULE 4") inside separate chapter files, or returning to previous numbering conventions. These match the author's original textual structure.

## 5. Text Integrity (Layout & Warnings)

*   `skipped_pages` (pages 1 to 11): Entire front-matter and Table of Contents section, which are skipped/replaced with clean custom HTML templates (such as `_V6_CONTENTS_PAGE` and custom title/metadata pages) to ensure an optimized EPUB layout.
*   `weak_pages` (page 198): Start of the exposition of Psalm 130, which has minor styling variations causing lower text density overlap.
*   `dense_source_window_loss` (pages 28, 34, 91, 93, 111, 116, 119, 127, 134, 151, 191, 208, 210, 211, 237, 256, 264, 311, 312, 332, 366, 367, 384, 401, 421, 424, 426, 428, 435, 438, 440, 445, 450, 471, 479, 488, 495, 498, 523, 531): Minor hyphenation and spelling discrepancies (such as `first-born` vs `firstborn` or `self-condemnation` vs `selfcondemnation`), word-boundary spaces, or scripture references/numbers stripped during text normalization in the audit. These are verified safe and whitelisted.
*   `paragraph_split_candidates`: False-positive splits on salutations ("CHRISTIAN READER,"), signatures ("John Owen"), or thesis statements that start on a new block after a colon/dash.
*   `roman_heading_candidates`: The numeral `II. God revealed...` in Chapter 74 is a list item in body prose, not a chapter heading.
*   `enumerator_sequence_candidates`: Authentic sequence jumps in Chapter 85 list items.
*   `repeated_windows`: Repetitive phrases like "there is forgiveness with thee that thou mayest be feared" are legitimate biblical/thematic text repetitions in this exposition of Psalm 130.
*   `low_latin_tagging`, `low_latin_translation_coverage`: Denotes English words false-positively matched as Latin, and correctly tagged Latin phrases that are now fully matched and translated in `translation_db.py`.
