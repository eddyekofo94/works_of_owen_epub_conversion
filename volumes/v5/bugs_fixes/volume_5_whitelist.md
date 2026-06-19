# Volume 5 Whitelist

This document explains the whitelisted text integrity warnings, anomalies, and expected missing elements in Volume 5.

## Text Integrity

### ignored_warnings
- **repeated_phrases**: Whitelisted because Owen frequently quotes identical verses or theological formulas (like "the whole body fitly joined together and compacted") across close proximity, which triggers the repeated phrase warning but is authentic to the text.

### skipped_pages
- **[3, 4, 5, 6, 7, 8, 9, 10, 11]**: Front matter, tables of contents, and other prefatory content correctly omitted from the main parsed chapter bodies.

### paragraph_splits
- Legitimate structural boundaries or list items that begin with lowercase letters or mid-sentence continuations resulting from Owen's deep theological outlining.
  - "To The Reader"
  - "was this, —"
  - "Whence I argue, —"
  - "the inquiry is, —"
  - "Justification by the law is this, —"
  - "various inquiries are made, —"
  - "hence we argue, —"
  - "observed, —"
  - "There was עֲצֶרֶת הַדְּבָרִים , —"
  - "I shall consider, first, —"
  - "Hence we argue, —"
  - "Wherefore, —"
  - "Again, —"
  - "the question proposed, —"

### top_of_page_text_loss
- **31**: Legitimate empty space or non-body content at the top of the page.

### dense_source_window_loss
- **[15, 16, 35, 77, 88, 89, 122, 126, 137, 151, 157, 173, 182, 207, 281, 292, 297, 307, 353, 358, 359, 365, 377, 393, 418, 431, 436, 442, 457, 469, 499, 513, 538]**: These pages contain extensive Patristic Latin quotes, scriptural lists, or densely nested structural elements that inherently resist generic window-matching algorithms.

## Anomalies

### OCR & Bracket Residues
- **qui et**: A known Latin fragment.

### Hyphenation Anomalies
- Valid 17th-century orthography and theological compounds (e.g., "wire-draw", "dikaio-oo", "non-imputation", "sub-distinguished", "non-solvent", "blood-guiltiness", "co-interest"). Per the project mandate, these historical spellings must not be modernized.

### Structural Nesting Sequence Jumps
- **[2., 5. ... 7., 3. ... 5., 2. ... 4.]**: Owen's numbering can be irregular or interrupted by digressions. These jumps reflect the source text.

### Unmatched Quotation Marks
- Owen's 17th-century convention of opening quotation marks without closing them in debate/citation/Scripture contexts. These are authentic and should not be modernized.
  - "The first inquiry in this matter, in a way of duty, is after the proper relief"
  - "Credisne te non posse salvari"
  - "Whence the prophet says in the psalm"
  - "The excellent words of Justin Martyr"
  - "A full comprehension of it no creature"
  - "But the true and genuine signification of these words"
  - "3. \"Ex injuria; or,"
  - "(1.) \"Injuriarum,\" of wrongs:"
  - "In this state the apostle interposes himself"
  - "(1.) The Lord Christ, our mediator and surety"
  - "We shall take our fourth argument from the express exclusion"
  - "originally included no merit"
  - "Si obedientia vitae Christi nobis"
  - "injustus\", 1 Peter 3:18"
  - "This treatise, entitled Gospel Grounds and Evidences"
  - "Isaiah 13:6, 7; — \"When the day"

### Invalid Bible References
- **John 22**: Appears in the source text as a typo for John 20. The project rules permit keeping the source text's numbering unless an override is strictly mandated, but since it's just flagged, whitelisting it acknowledges it.
