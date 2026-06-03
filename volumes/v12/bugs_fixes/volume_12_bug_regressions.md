# Bug Regression Report: Volume 12

- Status: **WARN**
- EPUB audit: `volume_12_audit.json`
- Text integrity audit: `volume_12_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 257 | 285 | OK |
| Inline structural marker candidates | 6 | 6 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 3 | 3 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 1 | 1 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 0 | 0 | OK |
| Missing Greek clauses | 20 | 16 | REGRESSION |
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
- file: EPUB/ch004.xhtml; previous: house of God there are daily builders, according as new living stones are to be fitted to their places therein; and continual oppositions have there been made thereto, and will be,; next: In this work of building are some employed by Jesus Christ, and will be so to the end of the world, Matthew 28:19, 20, Ephesians 4:11, 12; and some employ themselves at least in a 
- file: EPUB/ch004.xhtml; previous: and not be believed. See Calvin's epistles, about the year 1561. But the man on this occasion being sent to the meeting at Pinckzow (as Statorius), he subscribes this confession: —; next: This did the wretched man think meet to do, that he might preserve the good esteem of his patron and reserve himself for a fitter opportunity of doing mischief; which also he did, 

### Inline structural marker candidates

- file: EPUB/ch017.xhtml; text: The intendment of these questions being the application of what is spoken of Christ, either as mediator or as man, unto his person, to the exclusion of any other consideration, namely, that of a divine nature therein, th
- file: EPUB/ch022.xhtml; text: The first they propose is taken from Hebrews 1:3, where the words spoken of Christ are, Φέρων τε τὰ πάντα τῷ ῥήματι τῆς δυνάμεως αὑτοῦ , [1] — "Upholding all things by the word of his power."
- file: EPUB/ch032.xhtml; text: Of the same judgment with him is Volk. de Vera Relig. lib. 4:cap. 11: [2] de Christi invocatione, Schlichting. ad Meisner., pp. 206, 207, and generally the rest of them; which again how consistent it is with what they af
- file: EPUB/ch040.xhtml; text: He suffered, — [1.] In his person; [2.] In his name; [3.] In his friends; [4.] In his goods; as the curse of the law extended to all, and that universally in all these: —
- file: EPUB/ch047.xhtml; text: I answer, The words there are used in a law sense, and are declarative of the righteousness of God in rewarding the keepers of the law of nature, or the moral law, according to the law of the covenant of works. This is e

### Repeated word windows

- phrase: made of the seed of david according to the flesh
- phrase: that they which commit sin are worthy of death romans
- phrase: they which commit sin are worthy of death romans 32
- phrase: the lord hath laid on him the iniquity of us
- phrase: lord hath laid on him the iniquity of us all

### Missing front CONTENTS pages

- page: 3; sample: contents of vindiciae evangelicae or the mystery of the gospel vindicated and socinianism examined prefatory note by the editor dedication epistle dedicatory preface to the reader mr biddle's
- page: 4; sample: 20 of the priestly office of christ how he was priest when he entered on his office and how he dischargeth it 21 of the death of christ
- page: 5; sample: vindiciae evangelicae or the mystery of the gospel vindicated and socinianism examined in the consideration and confutation of catechism called scripture catechism written by biddle and the catechism

### Missing enumerator markers

- marker: (1.)

### Low Greek word coverage

- {'word': 'ζητήσεις', 'pdf': 3, 'epub': 0}

### Missing Greek clauses

- page: 63; sample: αθανατους μεν πρωτα θεους νομω ως διακειται τιμα και σεβου ορκον επειθ
- page: 748; sample: γινεται φθονος ερις βλασφημιαι υπονοιαι πονηραι παραδιατριβαι
- page: 748; sample: το γινεσθαι πατερα παιδων λυπη φοβος φροντις
- page: 749; sample: φιλει γαρ οκειν πραγμ ανηρ πρασσων μεγα
- page: 749; sample: ως ουχ υπαρχων αλλα τιμωρουμενος

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
