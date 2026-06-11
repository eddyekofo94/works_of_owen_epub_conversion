# EPUB Audit: volume_h1.epub

- Status: **WARN**
- Errors: 0
- Warnings: 1

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 73
- Manifest items: 64
- Spine items: 38
- XHTML files: 39
- Embedded fonts: 20
- NAV links: 40

## Content Checks

- Greek chars: 14863
- Untagged Greek chars: 0
- Hebrew chars: 36153
- Untagged Hebrew chars: 0
- Noteref links: 146
- Endnote anchors: 146
- Boilerplate hits: 0
- Possible Beta Code files: 2
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 0

## Warnings

- `possible_beta_code_residue`: Possible Beta Code residue detected

## Samples

### beta_code

- `EPUB/ch020.xhtml`: Aj
- `EPUB/ch022.xhtml`: Aj

### structural_bold_leak

- `EPUB/ch002.xhtml`: ONE OF HIS MAJESTY'S MOST HONOURABLE PRIVY COUNCIL, AND PRINCIPAL SECRETARY OF STATE, ETC.

### lowercase_paragraph_start

- `EPUB/ch001.xhtml`: p. lxxxiv. There is not much to be added in regard to the history of the work. In
