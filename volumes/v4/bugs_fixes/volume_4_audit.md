# EPUB Audit: volume_4.epub

- Status: **WARN**
- Errors: 0
- Warnings: 3

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 93
- Manifest items: 84
- Spine items: 70
- XHTML files: 72
- Embedded fonts: 8
- NAV links: 70

## Content Checks

- Greek chars: 4420
- Untagged Greek chars: 23
- Hebrew chars: 687
- Untagged Hebrew chars: 19
- Noteref links: 24
- Endnote anchors: 23
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 10

## Warnings

- `untagged_greek`: Greek characters appear outside lang='el' context
- `untagged_hebrew`: Hebrew characters appear outside lang='he' context
- `repeated_phrases`: Potential repeated phrases detected

## Samples

### untagged_greek

- `EPUB/ch006.xhtml`: First, Supernatural revelation is the only objective cause and means of supernatural illumination. These things are commensurate. There is a natural knowledge of supernatural things, and that both theoretical and practic
- `EPUB/ch054.xhtml`: and nylons, the Spirit, is of the neuter. Some would have it to refer unto Christ, verse 12. But as it is not unusual in Scripture that the subjunctive article and relative should agree in gender with the following subst

### untagged_hebrew

- `EPUB/ch006.xhtml`: First, Supernatural revelation is the only objective cause and means of supernatural illumination. These things are commensurate. There is a natural knowledge of supernatural things, and that both theoretical and practic

### repeated_phrase

- `combined_text`: chapter 5 divine revelation itself the only foundation
- `combined_text`: chapter 2 zechariah 12 10 opened and vindicated
- `combined_text`: chapter 3 galatians 4 6 opened and vindicated
- `combined_text`: chapter 5 the work of the holy spirit
- `combined_text`: chapter 7 the nature of prayer in general

### structural_bold_leak

- `EPUB/ch001.xhtml`: ΠΗΕΨΜΑΤΟΛΟΓΙΑ? OR A DISCOURSE CONCERNING THE HOLY SPIRIT — CONTINUED. [BOOK VI., PART I.] THE REASON OF FAITH. PREFATORY NOTE BY THE EDITOR

### lowercase_paragraph_start

- `EPUB/ch006.xhtml`: p
- `EPUB/ch011.xhtml`: d
- `EPUB/ch016.xhtml`: p
- `EPUB/ch018.xhtml`: m
- `EPUB/ch019.xhtml`: d
