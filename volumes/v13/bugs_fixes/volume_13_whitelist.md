# Whitelist Explanation — Volume 13

This document provides explanations for the whitelisted anomalies and checks for Volume 13, ensuring transparency and adherence to the project standards.

## 1. Skipped Front-Matter Pages (Pages 3–14)
The PDF source contains raw table of contents and title pages on pages 3-14. In the EPUB, these have been replaced by a custom, beautifully formatted volume title page and table of contents (`_V13_CONTENTS_PAGE`).
- **Whitelisting action:** Added pages `3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14` to `skipped_pages` to prevent false positives regarding low text coverage, missing dense source windows, and missing top/bottom body text.

## 2. Legitimate Paragraph Splits
Some formatting elements like letter sign-offs or lists look like paragraph splits to the automated healer but are actually structurally correct.
- **Epistle dedicatory signature:** "I rest your most / obliged servant in Jesus Christ... John Owen" is a standard epistolary signing block.
- **Syllabus and lists:** Sentences starting with list/exposition lead-ins (e.g., "appears to me, that, —") are correct structural divisions.

## 3. Legitimate Inline Structural Markers
List patterns and outlines (e.g., "Now, three ways may a man receive...", "Motives to the observance...") are intended by Owen to be inline list expositions rather than separate block items.

## 4. Legitimate Unmatched Quotation Marks
Multi-paragraph quotes where only the final paragraph has a closing quote naturally trigger unmatched double-quote warnings in intermediate paragraphs:
- **Eshcol Rule IV & Rule VII:** Multi-paragraph biblical citations.
- **Chapter 5 (Augustine/Irenaeus):** Multi-paragraph Latin citations.
- **Other dialog/disputes:** Outline lists of arguments or objections where the quote spans paragraphs.

## 5. Historical Spellings and Hyphenations
In accordance with the **Text Integrity & Anomaly Triage Protocol**, authentic 17th-century orthography and hyphenation have been preserved:
- **Hyphenations:** `pole-star`, `fore-named`, `fore-cited`, `bed-chamber`, `new-fangledness`, `time-serving`, `cast-away`, `such-like`, `tender-hearted`, `God-speed`, `gazing-stock`, `non-submission`, `law-making`, `re-charge`, `co-partnership`, `non-assistance`, `weather-cock`, `birth-right`, etc.
- **Biblical Names:** `Beth-aven`, `Jabesh-gilead`.

## 6. Punctuation Spacing Blemishes
Historical printing style often added spaces before punctuation marks (e.g. `arising ;`, `denied ;`, `ordination ;`). These have been whitelisted to preserve the text layout fidelity.

## 7. List Nesting Sequence Jumps
The automated tool flags numbering sequences that do not start at `1.` or skip numbers, but these are legitimate in context:
- **Charles V:** Reference to Charles V (Emperor), not a list item.
- **Numbered Expositions:** Owen's specific lists that contain skips or start at custom numbers.
