# Volume 1 Whitelist Explanations

This document lists and explains the whitelisted anomalies and ignored warnings in **Volume 1** (The Glory of Christ) to prevent them from inflating the quality `Need` score.

## 1. Ignored Warnings (`text_integrity`)

*   **`low_latin_tagging`**: Many short Latin legal/theological terms are woven naturally into 17th-century English prose and do not require separate `<span lang="la">` tags.
*   **`low_latin_translation_coverage`**: Not all historical Latin citations or phrases require side-by-side translation database entries.
*   **`front_matter_toc_loss`**: The table of contents is custom-crafted in `volume_1_contents_page` override and early PDF pages 3-6 aren't parsed as body text chapters.
*   **`roman_heading_candidates`**: Roman numeral prefixes used as list indicators (e.g., `I. 1. What he did...` in Chapter 15) are valid list items, not centered heading elements.
*   **`repeated_windows`**: Repeated word windows (mostly common Scripture quotes) are expected and authentic text, not ghost layer residues.

## 2. Hyphenation Anomalies

These are authentic 17th-century spellings and compounds which must be preserved as-is rather than modernized:

*   **`Spiritual-mindedness`**: Historic capitalization and hyphenation for Owen's key theological concept.
*   **`Bar-jona`**: Archaic biblical patronymic compound.
*   **`pole-star`**: Historic spelling of the compound.
*   **`over-valuation`**: Historic compound spelling.
*   **`day-star`**: Historic biblical/theological compound.
*   **`merchant-man`**: Historic biblical/theological compound.
*   **`days-man`**: Historic biblical compound (mediator).
*   **`re-collected` / `re-collection`**: Owen's specific theological term for gathering together all things in Christ (recapitulation).
*   **`hundred-fold` / `two-fold` / `TWO-FOLD`**: Archaic spelling of numerical compounds.
*   **`re-stipulation`**: Historic covenant theology terminology.

## 3. Structural Nesting Sequence Jumps

*   **`13.`** (Preface): False positive caused by Augustine citation context `"Serm. 13."`, which is not a list enumerator.
*   **`4. ... 7.`** (Chapter 10): Legitimate list sequence jump in the author's structure.
*   **`III.`** (Chapter 15 / Preface): Legitimate list item starting at III in local sections.
*   **`10.`** (The Lesser Catechism): False positive caused by the reference `"Chap 10."`.

## 4. Unmatched Quotation Marks

These paragraphs contain an odd number of double quotation marks due to nested scripture quotations, multi-paragraph quote continuations, or foreign-language quotations:

*   `He (Christ) meant the universal church...`
*   `Non enim aliter nos discere poteramus...`
*   `factores autem sermonum ejus facti...`
*   `The first of these is the constant doctrine of the whole ancient church...`
*   `We have no means — no corporeal, no intellectual instrument...`
*   `1. "Objectum reale et formale fidei"...`
*   `3. "Lumen praeparans, elevans, disponens subjectum"...`
*   `The solemn ordinary worship of the church...`
*   `There was in his words both a profession of his own faith...`
*   `III. The third thing proposed to declare the use...`
*   `This is that "Holy One" which...`
*   `Through the blood of this everlasting covenant...`
*   `2. The minds of men are apt by their troubles...`
*   `4. The sight of the glory of Christ...`
*   `1. Infinite wisdom is one of the most glorious...`
*   `Our constant exercise in meditation...`
*   `This, therefore, is the present case: — Where there are...`
*   `Gracious acceptation: "Receive us graciously."`
*   `Dr. Owen had at that time the charge...`

## 5. Weak Pages & Dense Source Window Loss

*   **Weak Pages `[3, 4, 5, 6, 533]`**: Pages 3-6 represent front matter/contents pages which do not contain main body text and thus have no strong match. Page 533 is a blank page or back-matter transition page in the PDF.
*   **Dense Windows Loss `[3, 4, 5, 6, 7, 9, 10, 11, 21, 51]`**: Early PDF pages and specific pages containing publisher's introductory materials, editorial prefaces, and indexes that do not map directly to EPUB chapters.
