# Whitelist Log — Volume 2 (Communion with God)

This document contains a human-readable list of all items whitelisted in `volume_2_whitelist.json`. These exclusions prevent the automated QA audit (`scripts/run_all_checks.py`) from flagging false positives or historical spelling variations as conversion errors.

---

## 1. Anomalies (Historical Orthography & Layout Sequences)

### Hyphenation Anomalies
These words represent authentic 17th-century spelling variants or compound hyphens. In accordance with the text integrity protocol, they are preserved in their original historical format rather than modernized:

*   **`re-assume`**: 17th-century prefix hyphenation.
*   **`banqueting-houses`**: Archaic compound noun.
*   **`head-stone`**: Historic spelling of "headstone".
*   **`days-man`**: Refers to an arbitrator or mediator (Job 9:33).
*   **`hand-writing`**: Archaic compound form of "handwriting".
*   **`Day-spring`**: Biblical spelling for dawn/morning star (Luke 1:78).
*   **`Day-star`**: Biblical spelling for morning star (2 Peter 1:19).
*   **`Hephzi-bah`**: Hyphenated transliteration of the Hebrew name Hephzibah.
*   **`well-head`**: Archaic compound for source or spring.
*   **`law-making`**: Archaic compound adjective.
*   **`non-imputation`**: Theological compound.
*   **`son-like`**: Historic compound adjective.
*   **`co-heirs`**: Archaic spelling of "coheirs".
*   **`un-son`**: Historic theological term.
*   **`well-spring`**: Biblical spelling of "wellspring".
*   **`co-partners`**: Historic spelling of "copartners".
*   **`maran-atha`**: Hyphenated Aramaic term (1 Cor 16:22).
*   **`tri-unity`**: Historic hyphenated form of "triunity" (Trinity).

### Structural Nesting Sequence Jumps
These outlines contain jumps in their sequential enumerations which are intentional formatting structures in John Owen's original text layout:
*   **`I. ... III.`**: Intentional skip or transition in roman numerals.
*   **`2.`**: Outlines that begin directly on item 2 or contain standalone nested points.
*   **`2. ... 10.`**: Jumps or custom outlines in chapter summaries or arguments.

---

## 2. Text Integrity & Layout Constraints

### Ignored Warnings
The following warnings are suppressed globally for Volume 2 because they represent known layout and transcription realities (e.g. running headers/footers in the PDF that are redacted in the EPUB, or Latin passages without modern translations):
*   `low_latin_tagging`
*   `low_latin_translation_coverage`
*   `repeated_phrases`
*   `weak_page_coverage`
*   `dense_source_window_loss`
*   `front_matter_toc_loss`
*   `top_of_page_text_loss`
*   `bottom_of_page_text_loss`
*   `repeated_windows`

### Skipped & Weak Pages
*   **Pages 3–10 (Skipped):** Table of Contents (TOC) and front matter pages. These pages use non-standard page structures, layouts, and lists that do not match prose chapter formats.
*   **Pages 5, 10 (Weak Matching):** Specific front-matter pages with low prose density or formatting that deviates from the main body template.

### Redacted Header/Footer Loss
These lines are present as running headers or publisher marks in the PDF but are correctly omitted from the EPUB flow:
*   `"This Edition of first published by Johnstone & Hunter, 1850-53"` (Publisher info).
*   `"CONTENTS OF VOL. 2. OF COMMUNION WITH GOD THE FATHER,"` (Running TOC header).

---

## 3. Paragraph Splits (Valid Continuation & Layout Breaks)

These transitions look like paragraph splits (e.g. lines starting with lowercase letters, name listings, or short phrases) but represent valid structural layouts:

1.  **`CHRISTIAN READER,` $\rightarrow$ `IT is now six years...`**
    *   *Rationale:* Preface greeting split from the first paragraph body.
2.  **`To The Reader` $\rightarrow$ `ALPHONSUS, king of Spain...`**
    *   *Rationale:* Prefatory title heading split from the introductory line.
3.  **`Reader, I am Thy servant...` $\rightarrow$ `Daniel Burgess`**
    *   *Rationale:* Signature block for Daniel Burgess at the end of his preface.
4.  **`Romans 15:30...` $\rightarrow$ `And such benedictions...`**
    *   *Rationale:* Sentence continuation across a Bible citation split.
5.  **`Obj. 3. "I cannot...` $\rightarrow$ `Could I find...`**
    *   *Rationale:* Subpoint transition layout containing inline quotes.
6.  **`Jesus, as he is "God blessed...` $\rightarrow$ `The endless, bottomless...`**
    *   *Rationale:* Continuation paragraph starting with a lowercase adjective describing the person of Christ.
7.  **`...he is all wholly to be desired...` $\rightarrow$ `Lovely in his person...`**
    *   *Rationale:* List-like descriptive sentences starting with lowercase adjectives.
8.  **`Greek passages (`$\rightarrow$`)`**
    *   *Rationale:* Greek translation block insertions (e.g., in `ch035`) causing segmentations.

---

## 4. Unmatched Quotation Marks

John Owen's text features long blockquotes, embedded scripts, and multi-paragraph citations (especially in Latin and Greek) where quotation marks do not follow modern open/close matching rules on a single-paragraph basis. 

The whitelisted items include:
*   Treatise title page fragments (e.g., the cover and introductory pages of *Of Communion*).
*   Scripture and blockquote blocks starting with opening quotes that continue across several pages.
*   Long Latin citations (e.g. from Augustine, Cicero, and medieval scholars) where the text has smart quotes or double quotes that close across multiple paragraphs.
*   Preface comments and objections containing balanced quotes that cross paragraph bounds.
