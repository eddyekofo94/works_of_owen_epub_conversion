# Bug Regression Report: Volume 7

- Status: **PASS**
- EPUB audit: `volume_7_audit.json`
- Text integrity audit: `volume_7_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 0 | 61 | OK |
| Inline structural marker candidates | 0 | 2 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 2 | 2 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 1 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 1 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 0 | 0 | OK |
| Overlong headings containing body prose | 0 | 0 | OK |
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
| Lowercase page fragments | 6 | 6 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Repeated word windows

- phrase: the good word of god and the powers of the
- phrase: good word of god and the powers of the world
- phrase: word of god and the powers of the world to
- phrase: of god and the powers of the world to come
- phrase: the knowledge of his glory in the face of jesus

### Missing front CONTENTS pages

- page: 3; sample: contents of nature and causes of apostasy from the gospel prefatory note by the editor the nature of apostasy from the gospel declared in an exposition of hebrews
- page: 7; sample: law doth not destroy the dominion of sin and how grace dethrones sin and gives dominion over it the practical observations drawn from end application made of the

### Repeated phrase hits

- file: combined_text; text: the grace and duty of being spiritually minded

### Lowercase page fragments

- file: EPUB/ch017.xhtml; text: may be applied unto the men of this persuasion: either they alone know the state
- file: EPUB/ch026.xhtml; text: and this he doth as the "liberal deviseth liberal things," verse 8. From his own
- file: EPUB/ch029.xhtml; text: and chapter 4:15,16, "We have not an high priest that cannot be touched with the
- file: EPUB/ch033.xhtml; text: l
- file: EPUB/ch034.xhtml; text: for hereby our minds, that were created in a state of blessed adherence unto God,
