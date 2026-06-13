# Volume 16 Whitelist Explanations

This document lists and explains the whitelisted anomalies and ignored warnings in **Volume 16** (The Church and the Bible) to prevent them from inflating the quality `Need` score.

## 1. Ignored Warnings (`text_integrity`)

*   **`low_latin_tagging`**: Many short Latin legal/theological terms are woven naturally into 17th-century English prose and do not require separate `<span lang="la">` tags.
*   **`low_latin_translation_coverage`**: Not all historical Latin citations or phrases require side-by-side translation database entries.
*   **`repeated_phrases`**: The warning for "they will not see but they shall see" is a Scripture citation (Isaiah 26:11) that is naturally repeated in the text and is not a duplicate typo.
*   **`repeated_windows`**: Natural repetitions in prose discussing specialized theological concepts (such as Ben Asher and Ben Naphtali readings).
*   **`roman_heading_candidates`**: Occurrences where single letters (e.g., "L.") are flagged as Roman numerals.
*   **`suspicious_large_number_starts`**: Legitimate numbered lists in sermons starting with larger numbers.
*   **`enumerator_sequence_candidates`**: Non-sequential lists or list items that are authentic to the original treatise layout.
*   **`flat_analysis_chapters`**: Short analysis sections containing very few headings, matching the original printed outline layout.

## 2. Weak Pages & Skipped Pages

*   **`weak_pages` [360]**: PDF page 360 is the title page for the treatise *Of the Divine Original, Authority, Self-Evidencing Light, and Power of the Scriptures*, which is replaced by custom-crafted HTML in `treatise_title_overrides`.
*   **`skipped_pages` [5, 6]**: Preliminary pages in the PDF that contain back-matter or blank pages.

## 3. Paragraph Splits

The following splits are whitelisted as they are correct layout splits, not line-break artifacts:
*   **Aristophanes quote** on page 111 (before the Greek quote block).
*   **Editor signatures (ED.)** on pages 112 and 115.
*   **Answer indicator** on page 113.
*   **Dante / Latin quote block** on page 114.

## 4. Text Loss (Top/Bottom & Dense Windows)

*   **`dense_source_window_loss` [10, 16, 19, 25, 27, 28, 33, 34, 43, 48]**: Pages where minor corrections (e.g., adding quotation marks to scriptural text, minor spelling corrections, hyphens, and Latin translation insertions) cause exact word-window matches to fail, though the content is fully present.
*   **`top_of_page_text_loss` [43, 333, 363]**: Headings and salutations at the top of pages that are styled differently in the EPUB (as headers or blocks).
*   **`bottom_of_page_text_loss` [2, 593]**: Metadata info (page 2) and pages where a Greek phrase is corrected with standard breathing marks (`οὖν` vs `οῦν` on page 593), breaking exact matching.

## 5. Structural Nesting Sequence Jumps

These list item jumps represent either actual structures in the author's argument or false positives from citation numbers (like sermon titles or dates):

*   **`3. ... 5.`, `2. ... 5.`, etc.**: Legitimate numbering variations or list item starts in sermon titles (e.g., Sermon 4, Sermon 8, Sermon 10, Sermon 11, Sermon 12, Sermon 13 starting points).

## 6. OCR & Bracket Residues

*   **`s ibly`, `t and`, `U as`, `e last`, `s may`**: False positives where the scanner flags correct prose strings as brackets or OCR fragments.

## 7. Punctuation Spacing Blemishes

*   **`..`**: Whitelisted minor double periods in specific abbreviations or quotes.
