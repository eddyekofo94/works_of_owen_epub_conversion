# EPUB Audit: volume_13.epub

- Status: **WARN**
- Errors: 0
- Warnings: 1

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 121
- Manifest items: 112
- Spine items: 84
- XHTML files: 85
- Embedded fonts: 22
- NAV links: 86

## Content Checks

- Greek chars: 5764
- Untagged Greek chars: 134
- Hebrew chars: 87
- Untagged Hebrew chars: 0
- Noteref links: 211
- Endnote anchors: 211
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

- `EPUB/ch027.xhtml`: Δοῦλον Κυρίου οὐ δεῖ μάχεσθαι.
- `EPUB/ch027.xhtml`: Δεῖ τὸν ἐπίσκοπον ἀνέγκλητον εῖναι, ὡς Θεοῦ οἰκονόμον, μὴ αὐθάδη, μὴ ὀργίλον, μὴ πάροινον, μὴ πλήκτην, μὴ αἰσχροκερδῆ.
- `EPUB/ch046.xhtml`: Οὐδὲν ἄτερ γραφῆς.

### chapter_heading_in_paragraph

- `EPUB/ch016.xhtml`: Chapter 4
- `EPUB/ch020.xhtml`: Chapter 11

### lowercase_paragraph_start

- `EPUB/ch004.xhtml`: will be mounting. In the matter concerning which I propose my weak essay, some wo
- `EPUB/ch007.xhtml`: and again,
- `EPUB/ch009.xhtml`: and Jeremiah 20:9, "His word was in mine heart as a burning fire shut up in my bo
- `EPUB/ch011.xhtml`: to which add that of the apostle,
- `EPUB/ch022.xhtml`: who is herein followed by not a few of the Papists. Hence saith Biel., "
