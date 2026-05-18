# EPUB Audit: volume_5.epub

- Status: **WARN**
- Errors: 0
- Warnings: 2

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 60
- Manifest items: 51
- Spine items: 38
- XHTML files: 39
- Embedded fonts: 8
- NAV links: 38

## Content Checks

- Greek chars: 6228
- Untagged Greek chars: 4
- Hebrew chars: 947
- Untagged Hebrew chars: 0
- Noteref links: 0
- Endnote anchors: 0
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 3

## Warnings

- `untagged_greek`: Greek characters appear outside lang='el' context
- `repeated_phrases`: Potential repeated phrases detected

## Samples

### untagged_greek

- `EPUB/ch022.xhtml`: , the note of a syllogistical inference, declares what is here asserted to be the substance of the truth pleaded for. And the comparison is continued, ὠς, — these things have themselves after the same manner.
- `EPUB/ch022.xhtml`: , — "sin," for a "sinner," (that is, passively, not actively; not by inhesion, but imputation); for this the phrase of speech and force of the antithesis seem to require. Speaking of another sense, Estius himself on the 

### repeated_phrase

- `combined_text`: chapter 3 the use of faith in justification
- `combined_text`: chapter 17 testimonies out of the evangelists considered
- `combined_text`: chapter 19 objections against the doctrine of justification

### chapter_heading_in_paragraph

- `EPUB/ch002.xhtml`: Lastly, the concluding chapter i
- `EPUB/ch005.xhtml`: So chapter 9

### lowercase_paragraph_start

- `EPUB/ch006.xhtml`: e
- `EPUB/ch009.xhtml`: q
- `EPUB/ch013.xhtml`: f
- `EPUB/ch019.xhtml`: c
- `EPUB/ch021.xhtml`: d
