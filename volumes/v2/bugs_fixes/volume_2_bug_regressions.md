# Bug Regression Report: Volume 2

- Status: **PASS**
- EPUB audit: `volume_2_audit.json`
- Text integrity audit: `volume_2_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 13 | 209 | OK |
| Inline structural marker candidates | 1 | 1 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 2 | 2 | OK |
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
| Chapter headings rendered as paragraphs | 1 | 2 | OK |
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
| Lowercase page fragments | 10 | 15 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch001.xhtml; previous: CHRISTIAN READER,; next: IT is now six years past since I was brought under an engagement of promise for the publishing of some meditations on the subject which thou wilt find handled in the ensuing treati
- file: EPUB/ch002.xhtml; previous: To The Reader; next: ALPHONSUS, king of Spain, is said to have found food and physic in reading Livy; and Ferdinand, king of Sicily, in reading Quintus Curtius Rufus : but thou hast here nobler enterta
- file: EPUB/ch002.xhtml; previous: Reader, I am Thy servant in Christ Jesus; next: Daniel Burgess
- file: EPUB/ch005.xhtml; previous: der three divisions: — his _personal grace,_ III. — VI.; and under this branch are two long digressions, designed to unfold the glory and loveliness of Christ; _— purchased grace_,; next: VII.
- file: EPUB/ch008.xhtml; previous:  And you have distinct mention of the love of the Splint, Romans 15:30. The apostle also peculiarly directs his supplication to him in that solemn benediction, 2 Corinthians 13:14,; next: And such benedictions are originally supplications. He is likewise entitled unto all instituted worship, from the appointment of the administration of baptism in his name, Matthew 

### Inline structural marker candidates

- file: EPUB/ch005.xhtml; text: Part I. — The fact of communion with God is asserted, CHAP. I Passages in Scripture are quoted to show that special mention is made of communion with all the persons of the Trinity, II. Communion with the FATHER is descr

### Repeated word windows

- phrase: is with the father and with his son jesus christ
- phrase: bare our sins in his own body on the tree
- phrase: our fellowship is with the father and with his son
- phrase: fellowship is with the father and with his son jesus
- phrase: pleased the father that in him should all fullness dwell

### Missing front CONTENTS pages

- page: 3; sample: contents of vol of communion with god the father son and holy ghost prefatory note by the editor preface note to the reader by burgess part chapter that
- page: 6; sample: of the powers of the world to come unction by the spirit isaiah the various teachings of the holy ghost how the spirit of adoption and of supplication

### Repeated phrase hits

- file: combined_text; text: part 3 of communion with the holy ghost

### Chapter headings rendered as paragraphs

- file: EPUB/ch042.xhtml; text: Chapter 3

### Lowercase page fragments

- file: EPUB/ch008.xhtml; text: and verses 13,14, "Every creature which is in heaven, and on the earth, and under
- file: EPUB/ch013.xhtml; text: which, in the phrase of another evangelist, is, "White as snow, so as no fuller o
- file: EPUB/ch017.xhtml; text: he rejoices in him who was to take away the curse, by being made a curse for us.
- file: EPUB/ch019.xhtml; text: because that we could not in that condition of weakness whereinto we are cast by
- file: EPUB/ch023.xhtml; text: no more in bondage, but have the liberty of sons. And this liberty respects, —
