# EPUB Audit: volume_12.epub

- Status: **WARN**
- Errors: 0
- Warnings: 3

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 84
- Manifest items: 75
- Spine items: 58
- XHTML files: 60
- Embedded fonts: 11
- NAV links: 61

## Content Checks

- Greek chars: 14115
- Untagged Greek chars: 0
- Hebrew chars: 1448
- Untagged Hebrew chars: 0
- Noteref links: 505
- Endnote anchors: 502
- Boilerplate hits: 0
- Possible Beta Code files: 3
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 2

## Warnings

- `possible_beta_code_residue`: Possible Beta Code residue detected
- `repeated_phrases`: Potential repeated phrases detected
- `orphan_endnotes`: Some endnote anchors have no matching noteref

## Samples

### beta_code

- `EPUB/ch050.xhtml`: Jo
- `EPUB/contents_2.xhtml`: ~v
- `EPUB/endnotes.xhtml`: ja

### repeated_phrase

- `combined_text`: of the death of christ and of justification
- `combined_text`: a review of the annotations of hugo grotius

### inline_scholastic_label

- `EPUB/ch020.xhtml`: e Ans.
- `EPUB/ch049.xhtml`: d Ans.
