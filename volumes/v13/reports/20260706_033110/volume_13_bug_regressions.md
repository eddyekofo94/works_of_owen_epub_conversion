# Bug Regression Report: Volume 13

- Status: **WARN**
- EPUB audit: `volume_13_audit.json`
- Text integrity audit: `volume_13_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 1 | 95 | OK |
| Inline structural marker candidates | 0 | 13 | OK |
| Syllabus-anchor candidates | 8 | 16 | OK |
| Repeated word windows | 15 | 25 | OK |
| Missing front CONTENTS pages | 0 | 2 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 6 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 1 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 0 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 2 | 2 | OK |
| Overlong headings containing body prose | 0 | 2 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 0 | OK |
| Fragmented Hebrew span-run files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |
| Scripture blockquote false positives | 0 | 0 | OK |
| Orphan scripture brackets | 0 | 0 | OK |
| Glued ordinal anchors | 0 | 0 | OK |
| Structural bold leaks | 0 | 0 | OK |
| Repeated structural markers | 0 | 0 | OK |
| Scholastic bold leaks | 0 | 0 | OK |
| Inline scholastic labels | 0 | 0 | OK |
| Trailing scholastic labels | 0 | 0 | OK |
| DIGRESSION headings not h3 | 0 | 0 | OK |
| Cross-chapter continuation before heading | 0 | 0 | OK |
| Overlong NAV entries | 0 | 0 | OK |
| Duplicate NAV labels | 0 | 0 | OK |
| Spaced caps OCR | 0 | 0 | OK |
| Lowercase page fragments | 9 | 10 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |
| Implemented absent samples | 0 | 0 | OK |

## New Warning Codes

- Text integrity: unenriched_legacy_footnotes, unresolved_modern_references, untranslated_substantial_foreign_passages

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch048.xhtml; previous: ld be restrained. It is far from my purpose to return him any answer in the like manner to these things; to do it " — opus est mangone perito Qui Smithfieldensi polleat eloquio." †; next: Yet some instances of prodigious excesses in this kind will, in our process, be reflected on; and it may be the repetition of them may make an appearance, unto some less considerat

### Syllabus-anchor candidates

- file: EPUB/ch016.xhtml
- file: EPUB/ch016.xhtml
- file: EPUB/ch021.xhtml
- file: EPUB/ch022.xhtml
- file: EPUB/ch026.xhtml

### Repeated word windows

- phrase: not fear the lord god hath spoken who can but
- phrase: fear the lord god hath spoken who can but prophesy
- phrase: remember them which have the rule over you who have
- phrase: them which have the rule over you who have spoken
- phrase: which have the rule over you who have spoken unto

### Missing Greek clauses

- page: 263; sample: δουλον κυριου ου δει μαχεσθαι

### Chapter headings rendered as paragraphs

- file: EPUB/ch016.xhtml; text: Chapter 4
- file: EPUB/ch020.xhtml; text: Chapter 11

### Lowercase page fragments

- file: EPUB/ch004.xhtml; text: will be mounting. In the matter concerning which I propose my weak essay, some wo
- file: EPUB/ch007.xhtml; text: and again,
- file: EPUB/ch009.xhtml; text: and Jeremiah 20:9, "His word was in mine heart as a burning fire shut up in my bo
- file: EPUB/ch011.xhtml; text: to which add that of the apostle,
- file: EPUB/ch022.xhtml; text: who is herein followed by not a few of the Papists. Hence saith Biel., "
