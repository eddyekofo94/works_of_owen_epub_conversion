# EPUB Audit: volume_14.epub

- Status: **WARN**
- Errors: 0
- Warnings: 2

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 98
- Manifest items: 89
- Spine items: 69
- XHTML files: 71
- Embedded fonts: 14
- NAV links: 72

## Content Checks

- Greek chars: 6690
- Untagged Greek chars: 8
- Hebrew chars: 374
- Untagged Hebrew chars: 0
- Noteref links: 52
- Endnote anchors: 51
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 2

## Warnings

- `untagged_greek`: Greek characters appear outside lang='el' context
- `repeated_phrases`: Potential repeated phrases detected

## Samples

### untagged_greek

- `EPUB/ch002.xhtml`: Ν. N.
- `EPUB/ch051.xhtml`: פֶסֶל γλυπτόν

### repeated_phrase

- `combined_text`: chapter 1 our author's preface and his method
- `combined_text`: a vindication of the animadversions on fiat lux

### page_reference_split

- `EPUB/ch011.xhtml`: p. 126.
