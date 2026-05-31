# EPUB Audit: volume_4.epub

- Status: **WARN**
- Errors: 0
- Warnings: 1

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 97
- Manifest items: 88
- Spine items: 69
- XHTML files: 71
- Embedded fonts: 13
- NAV links: 72

## Content Checks

- Greek chars: 4075
- Untagged Greek chars: 0
- Hebrew chars: 698
- Untagged Hebrew chars: 0
- Noteref links: 24
- Endnote anchors: 23
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 10

## Warnings

- `repeated_phrases`: Potential repeated phrases detected

## Samples

### repeated_phrase

- `combined_text`: chapter 5 divine revelation itself the only foundation
- `combined_text`: chapter 2 zechariah 12 10 opened and vindicated
- `combined_text`: chapter 3 galatians 4 6 opened and vindicated
- `combined_text`: chapter 5 the work of the holy spirit
- `combined_text`: chapter 7 the nature of prayer in general

### page_reference_split

- `EPUB/ch043.xhtml`: p. 249.

### chapter_heading_in_paragraph

- `EPUB/ch006.xhtml`: CHAPTER I

### structural_bold_leak

- `EPUB/ch001.xhtml`: ΠΗΕΥΜΑΤΟΛΟΓΙΑ? OR A DISCOURSE CONCERNING THE HOLY SPIRIT — CONTINUED. [BOOK VI., PART I.] THE REASON OF FAITH. PREFATORY NOTE BY THE EDITOR

### lowercase_paragraph_start

- `EPUB/ch055.xhtml`: should receive strong consolation in all their distresses, when they flee for ref
