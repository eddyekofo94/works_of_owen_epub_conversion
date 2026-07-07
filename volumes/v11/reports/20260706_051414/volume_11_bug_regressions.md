# Bug Regression Report: Volume 11

- Status: **WARN**
- EPUB audit: `volume_11_audit.json`
- Text integrity audit: `volume_11_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 5 | 150 | OK |
| Inline structural marker candidates | 1 | 8 | OK |
| Syllabus-anchor candidates | 3 | 16 | OK |
| Repeated word windows | 0 | 25 | OK |
| Missing front CONTENTS pages | 0 | 2 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 5 | OK |
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
| Repeated phrase hits | 0 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 0 | 1 | OK |
| Overlong headings containing body prose | 0 | 1 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 0 | OK |
| Fragmented Hebrew span-run files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |
| Scripture blockquote false positives | 0 | 0 | OK |
| Orphan scripture brackets | 0 | 0 | OK |
| Glued ordinal anchors | 0 | 0 | OK |
| Structural bold leaks | 0 | 2 | OK |
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
| Implemented absent samples | 0 | 0 | OK |

## New Warning Codes

- Text integrity: unenriched_legacy_footnotes

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch005.xhtml; previous: k to deal so harshly with some of them with whom he hath to do. And it is still feared that "Parata tollit cornua; Qualis Lycambae spretus infido gener, Aut acer hostis Bupalo ." 3; next: It might, indeed, be the more excusable if evident provocation were always ready at hand to be charged with the blame of this procedure, if he said only,
- file: EPUB/ch006.xhtml; previous: To the same purpose, with application to a particular person, doth that great and holy doctor discourse, De Doctrin. Christiana, lib. 3 cap. 33. ◇; next: Saith he,
- file: EPUB/ch006.xhtml; previous:  "Nulla," saith he, "quidem nobis incumbit necessitas, ut in tanta exemplarium et editionum varietate et inconstantia, nihil uspiam Ignatio interpolatum ant adsutum affirmemus ." †; next: And, indeed, the foisted passages in many places are so evident, yea shameful, that no man who is not resolved to say any thing, without care of proof or truth, can once appear in 
- file: EPUB/ch006.xhtml; previous: make the matter more clear, cap. 13, he disputes, that " Auxilium sine quo nullus perseverat, et per quod quilibet perseverat, est Spiritus Sanctus, divina bonitas et voluntas ." †; next: Every cause of bringing sinful man to God is called by them "auxilium.' In these three, " Spiritus Sanctus, divina bonitas, et voluntas ," he compriseth the chief causes of perseve
- file: EPUB/ch009.xhtml; previous: cally insinuates into their understandings and affections, for their establishment, is an exurgency § of that description of himself which he gives, verse 28: from his eternity , —; next: He is "the everlasting God;" from his power, — He is "the Creator of the ends of the earth;" from his unchangeableness, — "He fainteth not," he waxeth not weary, and therefore ther

### Inline structural marker candidates

- file: EPUB/ch024.xhtml; text: and defile themselves daily with the pollutions of the world. This consequence, according to the principles and known tenets of our adversaries, is legitimate and true, inasmuch as they hold 'That true believers may fall

### Syllabus-anchor candidates

- file: EPUB/ch006.xhtml
- file: EPUB/ch006.xhtml
- file: EPUB/ch008.xhtml

### Lowercase page fragments

- file: EPUB/ch010.xhtml; text: which how it can be done by a naked engagement for the resurrection of them that
- file: EPUB/ch012.xhtml; text: and in [1 John 4:10] 1 John 4:10, "Herein is love, not that we loved God, but tha
- file: EPUB/ch014.xhtml; text: and then he concludes again, as the issue of his debate, verse 9, "So then they w
- file: EPUB/ch015.xhtml; text: and verse 22, "Let them be one, even as we, are one." And that ye may not think t
- file: EPUB/ch019.xhtml; text: causing us, chap. 4:24, to "put on the new man, which after God is created in rig
