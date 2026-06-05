# Bug Regression Report: Volume 12

- Status: **WARN**
- EPUB audit: `volume_12_audit.json`
- Text integrity audit: `volume_12_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 39 | 285 | OK |
| Inline structural marker candidates | 2 | 6 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 1 | 3 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 1 | 1 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 0 | 0 | OK |
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 2 | 7 | OK |
| Possible Beta Code residue files | 1 | 2 | OK |
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
| Inline scholastic labels | 2 | 0 | REGRESSION |
| Trailing scholastic labels | 0 | 0 | OK |
| DIGRESSION headings not h3 | 0 | 0 | OK |
| Cross-chapter continuation before heading | 0 | 0 | OK |
| Overlong NAV entries | 0 | 0 | OK |
| Duplicate NAV labels | 0 | 0 | OK |
| Spaced caps OCR | 0 | 0 | OK |
| Lowercase page fragments | 15 | 20 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: gst you, that, according to your several degrees, you would take it into your patronage or use, affording him in his daily labors the benefit of your prayers at the throne of grace; next: who is your unworthy fellow-laborer
- file: EPUB/ch003.xhtml; previous: who is your unworthy fellow-laborer; next: John Owen
- file: EPUB/ch003.xhtml; previous: John Owen; next: OXON. CH. CH. COLL., April 1 [1655.]
- file: EPUB/ch004.xhtml; previous: er, nam ratio vocabuli non patitur, ut quis dicatur sine matre pater: et si Logos filius erat, natus ex patre sine matre; dic mihi quomodo peporit eum, per ventrem an per latus." †; next: To this height of atheism and blasphemy had Satan wrought up the spirit of the man; so that I must say he is the only person in the world, that I ever read or heard of, that ever d
- file: EPUB/ch004.xhtml; previous: n possumus, aliquid in quo nitamur conquirimus ; sequiturque, ut frequens ac mobilis transitus maximum perfecti operis impedimentum sit." † — Paterc. Hist. Romans lib. 1 cap. 17. *; next: I wish some such things may not be said of the doctrine of the reformed churches. It was not long since raised to a great height of purity in itself, and perspicuity in the way of 

### Inline structural marker candidates

- file: EPUB/ch040.xhtml; text: He suffered, — [1.] In his person; [2.] In his name; [3.] In his friends; [4.] In his goods; as the curse of the law extended to all, and that universally in all these: —
- file: EPUB/ch047.xhtml; text: These Mr B. would oppose, and from the assertion of the one argue to the destruction of the other, though they sweetly and eminently comply in our communion with God. The other righteousness was before evinced. Even our 

### Repeated word windows

- phrase: made of the seed of david according to the flesh
- phrase: that they which commit sin are worthy of death romans
- phrase: the lord hath laid on him the iniquity of us
- phrase: lord hath laid on him the iniquity of us all
- phrase: known unto god are all his works from the beginning

### Missing front CONTENTS pages

- page: 5; sample: vindiciae evangelicae or the mystery of the gospel vindicated and socinianism examined in the consideration and confutation of catechism called scripture catechism written by biddle and the catechism

### Missing enumerator markers

- marker: (1.)

### Repeated phrase hits

- file: combined_text; text: of the death of christ and of justification
- file: combined_text; text: a review of the annotations of hugo grotius

### Possible Beta Code residue files

- file: EPUB/endnotes.xhtml; text: ja

### Inline scholastic labels

- file: EPUB/ch020.xhtml; text: e Ans.
- file: EPUB/ch049.xhtml; text: d Ans.

### Lowercase page fragments

- file: EPUB/ch003.xhtml; text: who is your unworthy fellow-laborer
- file: EPUB/ch004.xhtml; text: and whose blasphemy comes not at all short of it. The first is of
- file: EPUB/ch005.xhtml; text: for if we once let go those forms of sound words learned from the apostles, and t
- file: EPUB/ch006.xhtml; text: so chap. 21:6, 22:13. Which also is fully asserted, Romans 11:35, 36, "Who hath f
- file: EPUB/ch014.xhtml; text: is so far from proving that the image of God wherein man was created did consist
