# Bug Regression Report: Volume 3

- Status: **PASS**
- EPUB audit: `volume_3_audit.json`
- Text integrity audit: `volume_3_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 4 | 176 | OK |
| Inline structural marker candidates | 0 | 14 | OK |
| Repeated word windows | 0 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 1 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 0 | 1 | OK |
| Missing Hebrew clauses | 0 | 5 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 0 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 0 | 4 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 0 | 1 | OK |
| Overlong headings containing body prose | 0 | 0 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 0 | OK |
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
| Lowercase page fragments | 0 | 20 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch027.xhtml; previous: em. We might, therefore, hence give direction in some inquiries, which, indeed, deserve a larger discussion if our present design would admit of it. One only I shall instance in: —; next: May a person who is yet unregenerate pray for the Spirit of regeneration to effect that work in him; for whereas, as such, he is promised only unto the elect, such a person, not kn
- file: EPUB/ch030.xhtml; previous: y is increased. This the apostle instructs us in at large, 1 Corinthians 10:6-11. Now, both these concur in the example of holiness that is given us in the person of Christ; for, —; next: It is by all confessed that examples are most effectual ways of instruction, and, if seasonably proposed, do secretly solicit the mind unto imitation, and almost unavoidably inclin
- file: EPUB/ch037.xhtml; previous: on, which is declared to be one end of the oblation of Christ, chapter 1:3. So where he is said to "wash us from our sins in his own blood," — namely, as shed and offered for us, —; next: Revelation 1:5, it is not only the expiation of guilt, but the purification of filth, that is intended.
- file: EPUB/ch038.xhtml; previous: mediately controlled by impetuous lusts and affections, which darken its directions and silence its commands. Hence is the common saying not so common as what is signified by it, —; next: —— "Video meliora proboque, Deteriora sequor ."——[Ovid. Metam., lib. 7:20.] Hence the whole soul is filled with fierce contradictions and conflicts, Vanity, instability, folly, sen
