# EPUB Audit: volume_1.epub

- Status: **WARN**
- Errors: 0
- Warnings: 4

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 101
- Manifest items: 93
- Spine items: 83
- XHTML files: 85
- Embedded fonts: 4
- NAV links: 83

## Content Checks

- Greek chars: 3953
- Untagged Greek chars: 55
- Hebrew chars: 154
- Untagged Hebrew chars: 0
- Noteref links: 125
- Endnote anchors: 124
- Boilerplate hits: 0
- Possible Beta Code files: 2
- Escaped language-tag files: 0
- Repeated phrase hits: 6

## Warnings

- `untagged_greek`: Greek characters appear outside lang='el' context
- `possible_beta_code_residue`: Possible Beta Code residue detected
- `repeated_phrases`: Potential repeated phrases detected
- `missing_apple_options`: Missing Apple Books display-options file

## Samples

### beta_code

- `EPUB/ch036.xhtml`: ]y
- `EPUB/ch045.xhtml`: ]y

### untagged_greek

- `EPUB/ch004.xhtml`: Chap. I. The foundation of the whole is laid in the indication of those words of our blessed Savior, wherein he declares himself to be the rock whereon the church is built: (Matthew 16:18:) “And I say also unto thee, Tha
- `EPUB/ch004.xhtml`: ὀ͂
- `EPUB/ch004.xhtml`: But because there neither was nor can be any composition, properly so called, of the divine and human natures, and because the Son of God was a perfect person before his incarnation, wherein he remained what he was, and 
- `EPUB/ch004.xhtml`: , ὁ
- `EPUB/ch004.xhtml`: , ὁ

### repeated_phrase

- `combined_text`: chapter 14 motives unto the love of christ
- `combined_text`: meditations and discourses on the glory of christ
- `combined_text`: the greater catechism chapter 1 of the scripture
- `combined_text`: chapter 8 of the state of corrupted nature
- `combined_text`: chapter 10 of the person of jesus christ
