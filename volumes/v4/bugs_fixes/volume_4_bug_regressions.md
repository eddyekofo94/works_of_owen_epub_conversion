# Bug Regression Report: Volume 4

- Status: **PASS**
- EPUB audit: `volume_4_audit.json`
- Text integrity audit: `volume_4_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 20 | 61 | OK |
| Inline structural marker candidates | 2 | 2 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 4 | 4 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
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
| Repeated phrase hits | 0 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 1 | 1 | OK |
| Chapter headings rendered as paragraphs | 1 | 1 | OK |
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
| Lowercase page fragments | 0 | 0 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch007.xhtml; previous:  in brief, that it is required that we believe the Scriptures to be the word of God with faith divine and supernatural, which cannot be deceived. Two things are replied hereunto: —; next: 1 . "That where the things believed are divine and supernatural, so is the faith whereby we believe them or give our assent unto them. Let the motives and arguments whereon we give
- file: EPUB/ch009.xhtml; previous: ered therein, because what hath been unto this day gainsaid unto it or excepted against it hath been of little weight or consideration. Unto this great inquiry, therefore, I say, —; next: We believe the Scripture to be the word of God with divine faith for its own sake only; or, our faith is resolved into the authority and truth of God only as revealing himself unto
- file: EPUB/ch009.xhtml; previous: Some of them we must mention: —; next: Deuteronomy 31:11-13, "When all Israel is come to appear before the LORD thy God in the place which he shall choose, thou shalt read this law before all Israel in their hearing. Ga
- file: EPUB/ch009.xhtml; previous: nd testimony, this written word, to be the word of God, and believe it so to be, and distinguish it from every other pretended divine revelation that is not so? This is declared, —; next: Jeremiah 23:28,29, "The prophet that hath a dream, let him tell a dream; and he that hath my word, let him speak my word faithfully. What is the chaff to the wheat? saith the LORD.
- file: EPUB/ch009.xhtml; previous: he whole entire formal reason of believing; for if it have not this, something necessary unto believing would be wanting, though that were enjoyed. And this is directly affirmed, —; next: John 20:30,31, "Many other signs truly did Jesus in the presence of his disciples, which are not written in this book: but these are written, that ye might believe that Jesus is th

### Inline structural marker candidates

- file: EPUB/ch010.xhtml; text: Now, there are greater and more evident impressions of divine excellencies left on the written word, from the infinite wisdom of the Author of it, than any that are communicated unto the works of God, of what sort soever
- file: EPUB/ch043.xhtml; text: In regard to his effects on believers, it is first proved that his effectual consolations are the privilege of believers exclusively, III. And some of his operations in them as such, and of the benefits which they in con

### Repeated word windows

- phrase: we believe the scripture to be the word of god
- phrase: to believe the scripture to be the word of god
- phrase: believe the scripture to be the word of god with
- phrase: the mind and will of god as revealed in the
- phrase: to be the word of god with faith divine and

### Missing front CONTENTS pages

- page: 3; sample: contents πηευματολογια or discourse concerning the holy spirit continued book vi part the reason of faith prefatory note by the editor preface the subject stated preliminary remarks what
- page: 4; sample: question stated the principal sufficient cause of the understanding which believers have in the mind and will of god as revealed in the scriptures the spirit of god
- page: 5; sample: book vii discourse of the work of the holy spirit in prayer prefatory note by the editor preface to the reader the use of prayer and the work
- page: 6; sample: unto whom the holy spirit is promised and given as comforter or the object of his acting in this office inhabitation of the spirit the first thing promised

### Page reference split files

- file: EPUB/ch042.xhtml; text: p. 249.

### Chapter headings rendered as paragraphs

- file: EPUB/ch005.xhtml; text: CHAPTER I
