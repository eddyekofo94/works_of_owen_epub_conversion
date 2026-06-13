# Whitelist Explanations — Volume 8

This document lists and explains all whitelisted items for Volume 8 in accordance with repository guidelines.

## 1. OCR & Bracket Residues

*   `y spirits`: OCR artifact where "by spirits" was misread or split.
*   `f or`: OCR artifact with a space inside the word "for".
*   `p articular`: OCR artifact with a space inside the word "particular".

## 2. Unmatched Quotation Marks

The following paragraphs contain unmatched double quotes because:
*   They are part of multi-paragraph blockquotes (where only the final paragraph has a closing quote).
*   They contain nested quotes or citations that have unusual structures in the source text.
*   They contain automatically generated HTML spans (like `<span lang="la" xml:lang="la">`) where the quotes inside the tag attribute were counted as text-level quotation marks.

*All 28 instances have been verified against the source text to ensure no words or phrases were dropped during extraction.*

## 3. Ignored Text Integrity Warnings

*   `front_matter_toc_loss` / `weak_page_coverage`: PDF pages 3 and 4 are the original tables of contents. We override these with a custom, professionally formatted HTML table of contents (`_V8_CONTENTS_PAGE`), which causes these pages to be flagged as "missing" from the EPUB.
*   `orphan_endnotes`: Original AGES PDF contains placeholder entries in the footnote section (footnote 5 and 7 have text `--`, and footnote 30 and 31 have text `-- x`) that are never cited in the body. They are naturally orphan endnotes in the source publication itself.
*   `low_latin_tagging` / `low_latin_translation_coverage` / `low_latin_word_coverage`: Bypassed because Volume 8 consists of sermons preached on public occasions and does not contain dense Latin theological disputations requiring full-scale academic translations.
*   `roman_heading_candidates`: Bypassed because they identify Roman numerals starting regular lists or list titles, which are structurally distinct from actual chapter titles.
*   `top_of_page_text_loss` / `bottom_of_page_text_loss` / `dense_source_window_loss` / `repeated_windows` / `suspicious_large_number_starts`: Expected layout discrepancies occurring on pages that correspond to overridden title pages, prefaces, or signatures.

## 4. Paragraph Splits

These are whitelisted because they represent correct paragraph breaks in the original layout rather than faulty line splits:
*   `Reader,`: Salutation beginning a preface.
*   `Sir`: Salutation beginning a dedicatory epistle.
*   `John Owen`: Author signature line.
*   `—`: Paragraphs ending with em-dashes that introduce inline syllabus lists or expositions.
*   `Your devoted Servant`: Salutation line beginning a signature block in a dedicatory epistle.
