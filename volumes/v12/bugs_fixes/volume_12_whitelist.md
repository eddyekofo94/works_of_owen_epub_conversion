# Whitelist Exceptions — Volume 12

This file documents and explains the whitelisted anomalies and EPUB audit warnings for John Owen's Works, Volume 12 (*Vindiciae Evangelicae*).

## 1. EPUB Audit Exclusions

### Code: `possible_beta_code_residue`
* **Trigger Text**: `Aj` in `endnotes.xhtml`
* **Reasoning**: This is the legitimate historical abbreviation of Sophocles' *Ajax*, referenced in the footnotes. It is not a Beta Code formatting leftover.

### Code: `repeated_phrases`
* **Trigger Text**: `"of the death of christ and of justification"`
* **Reasoning**: This is the correct, full title of the treatise being referenced/exposed in the text. The repetition is contextual and necessary.

## 2. Text Anomalies Exclusions

### Category: `OCR & Bracket Residues`
The following strings represent either legitimate Latin words/abbreviations or acceptable 17th-century styling, rather than OCR errors:
* `s subsisting`, `b si`, `u the`, `w him`, `b from`, `B hath`: Legitimate text fragments, or historical spelling/bracket variants.
* `qui et`, `e manibus`, `E verbo`, `Pater noster`, `e lacu`, `seal et`: Correct Latin phrases or historical orthographical choices that trigger anomaly alerts but are authentic to the source.
* `blind eyes`: Legitimate English text that triggers mechanical alert thresholds.

### Category: `Structural Nesting Sequence Jumps`
* **Reasoning**: These are legitimate numbering or citations inside the text (e.g. references like `Book 12`, `cap. 13 fol. 15`, `Ezekiel 5:13`, `Hebrews 9:12`, etc.) that trigger false positive sequence jump warnings because they resemble list item markers but are actually part of the running prose.

### Category: `Unmatched Quotation Marks`
* **Reasoning**: These represent multi-paragraph blockquotes or catechism dialogue runs where a opening quote starts in one paragraph and closing quotes are placed in later paragraphs, causing the single-paragraph quote audit to flag them. All of these occurrences are structurally correct in context.

### Category: `Text Integrity Exclusions`
* **Reasoning**: Standard false positives due to deliberate editorial expansions (e.g., expanding initials to full names), styling enhancements (bold list headers `**(1.)**`), and standard signature blocks that do not require line-joining.
