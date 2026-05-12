# EPUB Audit: volume_3.epub

- Status: **WARN**
- Errors: 0
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
- Repeated phrase hits: 4

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

- `combined_text`: chapter 2 general dispensation of the holy spirit
- `combined_text`: chapter 2 works of the holy spirit preparatory
- `combined_text`: book 4 chapter 1 the nature of sanctification
- `combined_text`: chapter 3 believers the only object of sanctification
