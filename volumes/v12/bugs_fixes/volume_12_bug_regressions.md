# Bug Regression Report: Volume 12

- Status: **WARN**
- EPUB audit: `volume_12_audit.json`
- Text integrity audit: `volume_12_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 276 | 61 | REGRESSION |
| Inline structural marker candidates | 3 | 1 | REGRESSION |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 3 | 0 | REGRESSION |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 1 | 0 | OK |
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
| Lowercase page fragments | 15 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch004.xhtml; previous: The Holy Ghost tells us that we are; next: And thus do all they become the house of Christ "who hold fast the confidence and the rejoicing of the hope firm unto the end," Hebrews 3:6. In this house of God there are daily bu
- file: EPUB/ch004.xhtml; previous: house of God there are daily builders, according as new living stones are to be fitted to their places therein; and continual oppositions have there been made thereto, and will be,; next: In this work of building are some employed by Jesus Christ, and will be so to the end of the world, Matthew 28:19, 20, Ephesians 4:11, 12; and some employ themselves at least in a 
- file: EPUB/ch004.xhtml; previous: and not be believed. See Calvin's epistles, about the year 1561. But the man on this occasion being sent to the meeting at Pinckzow (as Statorius), he subscribes this confession: —; next: This did the wretched man think meet to do, that he might preserve the good esteem of his patron and reserve himself for a fitter opportunity of doing mischief; which also he did, 
- file: EPUB/ch004.xhtml; previous:  of Grotius, time will evidence. Now, because this man's creed is such as is not to be paralleled, perhaps some may be contented to take it in his own words, which are as follow: —; next: To this issue did Satan drive the Socinian principles in this man and sundry others, even to a full and peremptory denial of the Lord that bought them. In answering this man, it fe
- file: EPUB/ch004.xhtml; previous: is day the Papists continue in the same idolatry (to touch that by the way), I shall give you, for your refreshment, a copy of a verse or two, whose poetry does much outgo the old,; next: The other is of Franciscus de Mendoza, in Viridario Utriusque Eruditionis, lib. 2 prob. 2, as ensueth: —

### Inline structural marker candidates

- file: EPUB/ch040.xhtml; text: Now, both these were lost at once. The heavens were darkened when it might be expected, in an ordinary course, that the sun should have shone in its full beauty, Matthew 27:45, Luke 23:44, 45; and the earth lost its stab
- file: EPUB/ch040.xhtml; text: He suffered, — [1.] In his person; [2.] In his name; [3.] In his friends; [4.] In his goods; as the curse of the law extended to all, and that universally in all these: —
- file: EPUB/ch047.xhtml; text: These Mr B. would oppose, and from the assertion of the one argue to the destruction of the other, though they sweetly and eminently comply in our communion with God. The other righteousness was before evinced. Even our 

### Repeated word windows

- phrase: made of the seed of david according to the flesh
- phrase: that they which commit sin are worthy of death romans
- phrase: they which commit sin are worthy of death romans 32
- phrase: the lord hath laid on him the iniquity of us
- phrase: lord hath laid on him the iniquity of us all

### Missing enumerator markers

- marker: (1.)
- marker: (3.)
- marker: [4.]

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
- file: EPUB/ch004.xhtml; text: and whose blasphemy comes not at all short of it. The first is of Clarus Bonarus
- file: EPUB/ch005.xhtml; text: for if we once let go those forms of sound words learned from the apostles, and t
- file: EPUB/ch006.xhtml; text: so chap. 21:6, 22:13. Which also is fully asserted, Romans 11:35, 36, "Who hath f
- file: EPUB/ch014.xhtml; text: is so far from proving that the image of God wherein man was created did consist
