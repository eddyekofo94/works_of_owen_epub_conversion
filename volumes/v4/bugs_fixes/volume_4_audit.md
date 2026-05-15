# EPUB Audit: volume_4.epub

- Status: **FAIL**
- Errors: 5
- Warnings: 2

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 93
- Manifest items: 85
- Spine items: 71
- XHTML files: 73
- Embedded fonts: 8
- NAV links: 71

## Content Checks

- Greek chars: 4550
- Untagged Greek chars: 0
- Hebrew chars: 600
- Untagged Hebrew chars: 0
- Noteref links: 23
- Endnote anchors: 23
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Page reference split files: 0
- Chapter headings in paragraphs: 0
- Missing chapter initialization files: 0
- Fragmented Greek span-run files: 22
- Blockquotes: 0
- Repeated phrase hits: 10

## Errors

- `fragmented_greek_span_runs`: Three or more adjacent Greek words are split into separate spans
- `inline_scholastic_labels`: Scholastic labels appear mid-paragraph instead of as anchors
- `nav_overlong_entries`: Navigation entries are too long and appear to contain paragraph text
- `spaced_caps_ocr`: OCR-spaced all-caps words remain in XHTML
- `greek_diacritic_residue`: Standalone Greek diacritic residues (j, J, etc.) found near Greek text

## Warnings

- `repeated_phrases`: Potential repeated phrases detected
- `missing_apple_options`: Missing Apple Books display-options file

## Samples

### repeated_phrase

- `combined_text`: chapter 7 inferences from the whole
- `combined_text`: chapter 4 the nature of prayer
- `combined_text`: chapter 4 inhabitation of the spirit
- `combined_text`: divine revelation itself the only foundation
- `combined_text`: zechariah 12 10 opened and vindicated

### fragmented_greek_span_run

- `EPUB/ch009.xhtml`: three or more adjacent Greek spans
- `EPUB/ch011.xhtml`: three or more adjacent Greek spans
- `EPUB/ch013.xhtml`: three or more adjacent Greek spans
- `EPUB/ch019.xhtml`: three or more adjacent Greek spans
- `EPUB/ch020.xhtml`: three or more adjacent Greek spans

### inline_scholastic_label

- `EPUB/ch013.xhtml`: scholastic label appears mid-paragraph

### nav_overlong_entry

- `EPUB/nav.xhtml`: Chapter 6 - the Nature of Divine Revelations — the Nature of Divine Revelations — Their Self- Evidencing Power Considered, Particularly That of the Scriptures as the Word of God.

### spaced_caps

- `EPUB/ch007.xhtml`: M Y
- `EPUB/ch036.xhtml`: J J

### greek_diacritic_residue

- `EPUB/ch013.xhtml`: δ j ε
- `EPUB/ch033.xhtml`: ν J Ε
- `EPUB/ch036.xhtml`: ῦ j Ι
- `EPUB/ch040.xhtml`: ρ j α
- `EPUB/ch054.xhtml`: ν j Ο
