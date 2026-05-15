# EPUB Audit: volume_3.epub

- Status: **FAIL**
- Errors: 5
- Warnings: 5

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 72
- Manifest items: 64
- Spine items: 44
- XHTML files: 46
- Embedded fonts: 14
- NAV links: 45

## Content Checks

- Greek chars: 10343
- Untagged Greek chars: 59
- Hebrew chars: 1455
- Untagged Hebrew chars: 93
- Noteref links: 140
- Endnote anchors: 141
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 1
- Page reference split files: 0
- Chapter headings in paragraphs: 0
- Missing chapter initialization files: 0
- Fragmented Greek span-run files: 18
- Blockquotes: 0
- Repeated phrase hits: 2

## Errors

- `empty_bracket_noise`: Empty bracket residue appears in rendered text
- `unprocessed_ages_markers`: AGES verse markers remain unprocessed in XHTML
- `fragmented_greek_span_runs`: Three or more adjacent Greek words are split into separate spans
- `orphan_scripture_brackets`: Orphan AGES brackets remain before scripture references
- `inline_scholastic_labels`: Scholastic labels appear mid-paragraph instead of as anchors

## Warnings

- `untagged_greek`: Greek characters appear outside lang='el' context
- `untagged_hebrew`: Hebrew characters appear outside lang='he' context
- `repeated_phrases`: Potential repeated phrases detected
- `orphan_endnotes`: Some endnote anchors have no matching noteref
- `missing_apple_options`: Missing Apple Books display-options file

## Samples

### untagged_greek

- `EPUB/ch008.xhtml`: BEFORE we engage into the consideration of the things themselves concerning which we are to treat, it will be necessary to speak something unto the name whereby the third person in the Trinity is commonly known and pecul
- `EPUB/ch008.xhtml`: κ.τ.λ, — “The wind bloweth where it listeth, and thou hearest the sound thereof, but canst not tell whence it cometh, nor whither it goeth;” which is a proper description of this first signification of the word. It is an
- `EPUB/ch008.xhtml`: ὁ
- `EPUB/ch009.xhtml`: ὁ
- `EPUB/ch009.xhtml`: ἡ

### untagged_hebrew

- `EPUB/ch001.xhtml`: æח and
- `EPUB/ch001.xhtml`: æח for the wind or anything invisible with a sensible agitation, Amos 4:13 — Mistakes of the ancients rectified by Hierom —
- `EPUB/ch001.xhtml`: æח metaphorically for vanity, metonymically for the part or quarter of anything; for our vital breath, the rational soul, the affections, angels good and bad — Ambiguity from the use of the word, how to be removed — Rule
- `EPUB/ch007.xhtml`: æע, they write and call him
- `EPUB/ch008.xhtml`: æח and

### repeated_phrase

- `combined_text`: chapter 2 sanctification a progressive work
- `combined_text`: chapter 4 the defilement of sin

### empty_bracket_noise

- `EPUB/ch001.xhtml`: The Works of John Owen Vol. 3 ΠΝΕΥΜΑΤΟΛΟΓΙΑ A DISCOURSE CONCERNING THE HOLY SPIRIT, PREFATORY NOTE BY THE EDITOR, TO THE READERS, Book 1. 1. — GENERAL PRINCIPLES CONCERNING THE HOLY SPIRIT AND HIS WORK. 1 Corinthians; 1

### unprocessed_ages_marker

- `EPUB/ch007.xhtml`: &lt;4611605&gt;
- `EPUB/endnotes.xhtml`: &lt;460211&gt;

### fragmented_greek_span_run

- `EPUB/ch007.xhtml`: three or more adjacent Greek spans
- `EPUB/ch008.xhtml`: three or more adjacent Greek spans
- `EPUB/ch009.xhtml`: three or more adjacent Greek spans
- `EPUB/ch011.xhtml`: three or more adjacent Greek spans
- `EPUB/ch013.xhtml`: three or more adjacent Greek spans

### orphan_scripture_bracket

- `EPUB/ch008.xhtml`: [ Psalm 76:12]
- `EPUB/ch014.xhtml`: [John 14:15-17.]
- `EPUB/ch016.xhtml`: [Mark 13:32]
- `EPUB/ch023.xhtml`: [John 5:40.]

### inline_scholastic_label

- `EPUB/ch015.xhtml`: scholastic label appears mid-paragraph
- `EPUB/ch023.xhtml`: scholastic label appears mid-paragraph
