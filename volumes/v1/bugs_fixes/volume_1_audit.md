# EPUB Audit: volume_1.epub

- Status: **WARN**
- Errors: 0
- Warnings: 4

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 105
- Manifest items: 96
- Spine items: 83
- XHTML files: 84
- Embedded fonts: 8
- NAV links: 82

## Content Checks

- Greek chars: 4282
- Untagged Greek chars: 8
- Hebrew chars: 155
- Untagged Hebrew chars: 0
- Noteref links: 130
- Endnote anchors: 124
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 5

## Warnings

- `missing_cover_manifest_hint`: No obvious cover image manifest hint found
- `untagged_greek`: Greek characters appear outside lang='el' context
- `repeated_phrases`: Potential repeated phrases detected
- `orphan_endnotes`: Some endnote anchors have no matching noteref

## Samples

### untagged_greek

- `EPUB/ch004.xhtml`: , κ.τ.λ. (cap. 6)
- `EPUB/ch005.xhtml`: , κ.τ.λ." — "Thou art a rock, and on thee will I build." At least the gender had not been altered, but he would have said, "
- `EPUB/ch019.xhtml`: .τ. λ., 2 Corinthians 3:18. We behold his glory "in a glass," which implants the image of it on our minds. And hereby the mind is transformed into the same image, made like unto Christ so represented unto us — which is t

### repeated_phrase

- `combined_text`: chapter 14 motives unto the love of christ
- `combined_text`: meditations and discourses on the glory of christ
- `combined_text`: chapter 8 of the state of corrupted nature
- `combined_text`: chapter 10 of the person of jesus christ
- `combined_text`: chapter 14 of the two-fold estate of christ

### chapter_heading_in_paragraph

- `EPUB/ch003.xhtml`: Chapter 1
- `EPUB/ch049.xhtml`: A. Only by Jesus Christ. — Chapter 9

### lowercase_paragraph_start

- `EPUB/ch004.xhtml`: a
- `EPUB/ch008.xhtml`: a
- `EPUB/ch020.xhtml`: i
- `EPUB/ch024.xhtml`: w
- `EPUB/ch030.xhtml`: a
