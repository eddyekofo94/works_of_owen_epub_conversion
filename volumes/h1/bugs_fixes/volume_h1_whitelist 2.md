# Whitelist Explanations

### `paragraph_split_candidates`
**Reason:** False positives caused by Owen's quoting convention where a blockquote is introduced on one line (ending in a comma or without terminal punctuation) and the blockquote follows on the next line. The paragraphs are structurally correct and should not be merged.

### `unresolved_citations`
**Reason:** Unresolved citations are primarily obscure patristic references for which no standard ThML translation mapping exists. They are accurately transcribed from the original text.

### `repeated_phrases`
**Reason:** The repeated phrases are legitimate treatise/part headings that occur both in the Table of Contents and at the start of their respective sections.

### `low_coverage`
**Reason:** Due to dropped boilerplate text or ligature expansions.
