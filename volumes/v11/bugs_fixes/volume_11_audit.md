# EPUB Audit: volume_11.epub

- Status: **WARN**
- Errors: 0
- Warnings: 1

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 58
- Manifest items: 49
- Spine items: 29
- XHTML files: 31
- Embedded fonts: 14
- NAV links: 32

## Content Checks

- Greek chars: 11105
- Untagged Greek chars: 0
- Hebrew chars: 0
- Untagged Hebrew chars: 0
- Noteref links: 39
- Endnote anchors: 38
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 0

## Warnings

- `orphan_endnotes`: Some endnote anchors have no matching noteref

## Samples

### chapter_heading_in_paragraph

- `EPUB/contents_2.xhtml`: CHAPTER 1

### overlong_heading_body

- `EPUB/ch004.xhtml`: HIS HIGHNESS OLIVER, LORD-PROTECTOR OF THE COMMONWEALTH OF ENGLAND, SCOTLAND, AND IRELAND, WITH THE DOMINIONS THEREOF. SIR, THE wise man tells us that "no man knoweth love or hatre

### structural_bold_leak

- `EPUB/ch001.xhtml`: SAINTS PERSEVERANCE _Explained and Confirmed._ **THE CERTAIN PERMANENCY OF THEIR**
- `EPUB/ch013.xhtml`: 1. That from the beginning to verse 14 containeth a most fearful and dreadful commination and threatening of the judgments of the Lord against the whole church

### lowercase_paragraph_start

- `EPUB/ch017.xhtml`: of perseverance in reference to the
