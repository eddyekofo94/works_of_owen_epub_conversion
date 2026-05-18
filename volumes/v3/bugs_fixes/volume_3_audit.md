# EPUB Audit: volume_3.epub

- Status: **FAIL**
- Errors: 1
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
- Empty bracket noise files: 1
- Missing chapter initialization files: 0
- Repeated phrase hits: 4

## Errors

- `empty_bracket_noise`: Empty bracket residue appears in rendered text

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

### empty_bracket_noise

- `EPUB/ch001.xhtml`: The Works of John Owen Vol. 3 ΠΝΕΥΜΑΤΟΛΟΓΙΑ A DISCOURSE CONCERNING THE HOLY SPIRIT, PREFATORY NOTE BY THE EDITOR, TO THE READERS, Book 1. 1. — GENERAL PRINCIPLES CONCERNING THE HOLY SPIRIT AND HIS WORK. 1 Corinthians; 1

### chapter_heading_in_paragraph

- `EPUB/ch011.xhtml`: Chapter 44

### fragmented_greek_span_run

- `EPUB/ch007.xhtml`: <span lang="el" xml:lang="el">Περὶ</span> <span lang="el" xml:lang="el">
- `EPUB/ch008.xhtml`: <span lang="el" xml:lang="el">τὸ</span> <span lang="el" xml:lang="el">
- `EPUB/ch009.xhtml`: <span lang="el" xml:lang="el">εἰς</span> <span lang="el" xml:lang="el">
- `EPUB/ch011.xhtml`: <span lang="el" xml:lang="el">οῦν</span> <span lang="el" xml:lang="el">
- `EPUB/ch013.xhtml`: <span lang="el" xml:lang="el">ἔχει</span> <span lang="el" xml:lang="el">

### fragmented_hebrew_span_run

- `EPUB/ch007.xhtml`: <span lang="he" xml:lang="he" dir="rtl">םח</span> <span lang="he" xml:lang="he" dir="rtl">
- `EPUB/ch008.xhtml`: <span lang="he" xml:lang="he" dir="rtl">מגּיד</span> <span lang="he" xml:lang="he" dir="rtl">
- `EPUB/ch009.xhtml`: <span lang="he" xml:lang="he" dir="rtl">רחת</span> <span lang="he" xml:lang="he" dir="rtl">
- `EPUB/ch010.xhtml`: <span lang="he" xml:lang="he" dir="rtl">ְרֹס</span> <span lang="he" xml:lang="he" dir="rtl">
- `EPUB/ch011.xhtml`: <span lang="he" xml:lang="he" dir="rtl">עָרָה</span> <span lang="he" xml:lang="he" dir="rtl">

### lowercase_paragraph_start

- `EPUB/ch004.xhtml`: c
- `EPUB/ch010.xhtml`: e
- `EPUB/ch011.xhtml`: g
- `EPUB/ch022.xhtml`: t
- `EPUB/ch023.xhtml`: w

### noteref_leading_space

- `EPUB/ch007.xhtml`: <a class="noteref" epub:type="noteref"
- `EPUB/ch008.xhtml`: <a class="noteref" epub:type="noteref"
- `EPUB/ch009.xhtml`: <a class="noteref" epub:type="noteref"
- `EPUB/ch010.xhtml`: <a class="noteref" epub:type="noteref"
- `EPUB/ch011.xhtml`: <a class="noteref" epub:type="noteref"
