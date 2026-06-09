# EPUB Audit: volume_14.epub

- Status: **WARN**
- Errors: 0
- Warnings: 3

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 100
- Manifest items: 91
- Spine items: 70
- XHTML files: 72
- Embedded fonts: 14
- NAV links: 73

## Content Checks

- Greek chars: 6690
- Untagged Greek chars: 8
- Hebrew chars: 374
- Untagged Hebrew chars: 0
- Noteref links: 163
- Endnote anchors: 164
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 2

## Warnings

- `untagged_greek`: Greek characters appear outside lang='el' context
- `repeated_phrases`: Potential repeated phrases detected
- `orphan_endnotes`: Some endnote anchors have no matching noteref

## Samples

### untagged_greek

- `EPUB/ch001.xhtml`: Ν. N.
- `EPUB/ch050.xhtml`: פֶסֶל γλυπτόν

### repeated_phrase

- `combined_text`: chapter 1 our author's preface and his method
- `combined_text`: a vindication of the animadversions on fiat lux

### page_reference_split

- `EPUB/ch010.xhtml`: p. 126.

### lowercase_paragraph_start

- `EPUB/ch012.xhtml`: come than Moses were, surely born a Jew, he would, being come into the world, rat
- `EPUB/ch030.xhtml`: yet I shall say, that as many as take notice of this discourse will do no less of
- `EPUB/ch031.xhtml`: when you know what his business was But the truth is, when you talk of the merit
- `EPUB/ch032.xhtml`: which of old she professed!
- `EPUB/ch033.xhtml`: as Lactantius reports him. But you say, "If they fall by idolatry, and yet keep a
