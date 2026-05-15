# EPUB Audit: volume_2.epub

- Status: **WARN**
- Errors: 0
- Warnings: 1

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 82
- Manifest items: 73
- Spine items: 49
- XHTML files: 51
- Embedded fonts: 18
- NAV links: 49

## Content Checks

- Greek chars: 3531
- Untagged Greek chars: 3
- Hebrew chars: 615
- Untagged Hebrew chars: 0
- Noteref links: 26
- Endnote anchors: 26
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 0

## Warnings

- `untagged_greek`: Greek characters appear outside lang='el' context

## Samples

### untagged_greek

- `EPUB/ch026.xhtml`: It is God has given the earnest of the Spirit in our hearts: an expression directly answering that of Galatians 4:6, “God has sent forth the Spirit of his Son into your hearts;” that is, the person of the Spirit; for not

### chapter_heading_in_paragraph

- `EPUB/ch034.xhtml`: The second section of this chapter i
- `EPUB/ch039.xhtml`: Chapter 3

### fragmented_greek_span_run

- `EPUB/ch016.xhtml`: <span class="greek" lang="el" xml:lang="el">[ας</span> <span class="greek" lang="el" xml:lang="el">
- `EPUB/ch022.xhtml`: <span class="greek" lang="el" xml:lang="el">[Ιν</span> <span class="greek" lang="el" xml:lang="el">

### structural_bold_leak

- `EPUB/ch020.xhtml`: Objection 1. For our absolution by and upon the death of Christ, it may be said, that “if the elect have their absolution, reconciliation, and freedom by the de

### lowercase_paragraph_start

- `EPUB/ch003_title.xhtml`: d
- `EPUB/ch004.xhtml`: a
- `EPUB/ch007.xhtml`: w
- `EPUB/ch009.xhtml`: i
- `EPUB/ch013.xhtml`: a
