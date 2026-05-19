# Bug Regression Report: Volume 2

- Status: **PASS**
- EPUB audit: `volume_2_audit.json`
- Text integrity audit: `volume_2_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 209 | 209 | OK |
| Inline structural marker candidates | 0 | 1 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 2 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
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
| Chapter headings rendered as paragraphs | 2 | 2 | OK |
| Overlong headings containing body prose | 0 | 0 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 2 | OK |
| Fragmented Hebrew span-run files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |
| Scripture blockquote false positives | 0 | 0 | OK |
| Orphan scripture brackets | 0 | 0 | OK |
| Glued ordinal anchors | 0 | 0 | OK |
| Structural bold leaks | 0 | 1 | OK |
| Repeated structural markers | 0 | 0 | OK |
| Scholastic bold leaks | 0 | 0 | OK |
| Inline scholastic labels | 0 | 0 | OK |
| Trailing scholastic labels | 0 | 0 | OK |
| DIGRESSION headings not h3 | 0 | 0 | OK |
| Cross-chapter continuation before heading | 0 | 0 | OK |
| Overlong NAV entries | 0 | 0 | OK |
| Duplicate NAV labels | 0 | 0 | OK |
| Spaced caps OCR | 0 | 0 | OK |
| Lowercase page fragments | 14 | 15 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch002.xhtml; previous: Reader, I am Thy servant in Christ Jesus; next: DANIEL BURGESS
- file: EPUB/ch008.xhtml; previous: n what the peculiar appropriation of this distinct communion unto the several persons doth consist, must, in the first place, be made manifest. 14 1 John 5:7, the apostle tells us,; next: In heaven they are, and bear witness to us. And what is it that they bear witness unto? Unto the sonship of Christ, and the salvation of believers in his blood. Of the carrying on 
- file: EPUB/ch008.xhtml; previous: Sometimes the Son only is spoken of, as to this purpose. 1 Corinthians 1:9,; next: — of which place afterward.
- file: EPUB/ch008.xhtml; previous: Sometimes the Spirit alone is mentioned. 2 Corinthians 13:14,; next: This distinct communion, then, of the saints with the Father, Son, and Spirit, is very plain in the Scripture; but yet it may admit of farther demonstration Only this caution I mus
- file: EPUB/ch008.xhtml; previous: er: these graces as acted in prayer and praises, and as clothed with instituted worship, are peculiarly directed unto him. "Ye call on the Father," 1 Peter 1:17, Ephesians 3:14,15,; next: Bowing the knee compriseth the whole worship of God, both that which is moral, in the universal obedience he requireth, and those peculiar ways of carrying it on which are by him a

### Repeated word windows

- phrase: bare our sins in his own body on the tree
- phrase: is with the father and with his son jesus christ
- phrase: pleased the father that in him should all fullness dwell
- phrase: the father that in him should all fullness dwell colossians
- phrase: father that in him should all fullness dwell colossians 19

### Repeated phrase hits

- file: combined_text; text: part 3 of communion with the holy ghost

### Chapter headings rendered as paragraphs

- file: EPUB/ch035.xhtml; text: The second section of this chapter i
- file: EPUB/ch042.xhtml; text: Chapter 3

### Lowercase page fragments

- file: EPUB/ch008.xhtml; text: a
- file: EPUB/ch014.xhtml; text: a
- file: EPUB/ch016.xhtml; text: i
- file: EPUB/ch017.xhtml; text: a
- file: EPUB/ch019.xhtml; text: b
