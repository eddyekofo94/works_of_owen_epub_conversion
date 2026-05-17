# EPUB Audit: volume_2.epub

- Status: **FAIL**
- Errors: 1
- Warnings: 3

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

- Greek chars: 3398
- Untagged Greek chars: 3
- Hebrew chars: 615
- Untagged Hebrew chars: 0
- Noteref links: 25
- Endnote anchors: 26
- Boilerplate hits: 0
- Possible Beta Code files: 4
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 0

## Errors

- `literal_footnote_markers`: Literal fN footnote markers appear in rendered text

## Warnings

- `untagged_greek`: Greek characters appear outside lang='el' context
- `possible_beta_code_residue`: Possible Beta Code residue detected
- `orphan_endnotes`: Some endnote anchors have no matching noteref

## Samples

### beta_code

- `EPUB/ch018.xhtml`: ]y
- `EPUB/ch023.xhtml`: ]e
- `EPUB/ch027.xhtml`: ]y
- `EPUB/ch035.xhtml`: ]y

### untagged_greek

- `EPUB/ch027.xhtml`: It is God has given the earnest of the Spirit in our hearts: an expression directly answering that of Galatians 4:6, "God has sent forth the Spirit of his Son into your hearts;" that is, the person of the Spirit; for not

### literal_footnote_marker

- `EPUB/ch006.xhtml`: [f2]
- `EPUB/ch007.xhtml`: [f2]

### chapter_heading_in_paragraph

- `EPUB/ch035.xhtml`: The second section of this chapter i
- `EPUB/ch040.xhtml`: Chapter 3
- `EPUB/ch042.xhtml`: Chapter 3

### lowercase_paragraph_start

- `EPUB/ch003_title.xhtml`: d
- `EPUB/ch006.xhtml`: w
- `EPUB/ch007.xhtml`: w
- `EPUB/ch008.xhtml`: w
- `EPUB/ch010.xhtml`: i
