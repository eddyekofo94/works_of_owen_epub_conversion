# Bug Regression Report: Volume 4

- Status: **WARN**
- EPUB audit: `volume_4_audit.json`
- Text integrity audit: `volume_4_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 75 | 61 | REGRESSION |
| Inline structural marker candidates | 2 | 1 | REGRESSION |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
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
| Repeated phrase hits | 10 | 7 | REGRESSION |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 1 | 0 | REGRESSION |
| Chapter headings rendered as paragraphs | 1 | 0 | REGRESSION |
| Overlong headings containing body prose | 0 | 0 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 0 | OK |
| Fragmented Hebrew span-run files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |
| Scripture blockquote false positives | 0 | 0 | OK |
| Orphan scripture brackets | 0 | 0 | OK |
| Glued ordinal anchors | 0 | 0 | OK |
| Structural bold leaks | 1 | 0 | REGRESSION |
| Repeated structural markers | 0 | 0 | OK |
| Scholastic bold leaks | 0 | 0 | OK |
| Inline scholastic labels | 0 | 0 | OK |
| Trailing scholastic labels | 0 | 0 | OK |
| DIGRESSION headings not h3 | 0 | 0 | OK |
| Cross-chapter continuation before heading | 0 | 0 | OK |
| Overlong NAV entries | 0 | 0 | OK |
| Duplicate NAV labels | 0 | 0 | OK |
| Spaced caps OCR | 0 | 0 | OK |
| Lowercase page fragments | 1 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch001.xhtml; previous: EDITED BY; next: WILLIAM H. GOOLD
- file: EPUB/ch001.xhtml; previous: WILLIAM H. GOOLD; next: ΠΗΕΥΜΑΤΟΛΟΓΙΑ ? OR A DISCOURSE CONCERNING THE HOLY SPIRIT — CONTINUED. [BOOK VI., PART I.] THE REASON OF FAITH. PREFATORY NOTE BY THE EDITOR
- file: EPUB/ch001.xhtml; previous: 4. - Extraordinary spiritual gifts, [1 Corinthians 12:5] -; next: 11.
- file: EPUB/ch007.xhtml; previous: we do believe; and the reason why we do believe them is, because they are proposed in the Scripture. Thus the apostle expresseth the whole of what we intend: 1 Corinthians 15:3, 4,; next: Christ's death, and burial, and resurrection, are the things proposed unto us to be believed, and so the object of our faith; but the reason why we believe them is, because they ar
- file: EPUB/ch008.xhtml; previous: o deservedly, for where it is absolute it is unquestionable; that which is most ancient in any kind is most true. God himself makes use of this plea against idols: Isaiah 43:10-12,; next: That which he asserts is, that he alone is God, and no other: this he calls the people to testify by this argument, that he was among them as God, — that is, in the church, — befor

### Inline structural marker candidates

- file: EPUB/ch044.xhtml; text: Among the special benefits indicated are, — 1. The unction of the Spirit, 5; 2. sealing of the Spirit, expounded in a brief comment on [Ephesians 1:13] 4:30, VI.; and, 3. The Spirit as an earnest, considered in reference
- file: EPUB/ch052.xhtml; text: What remains is, to inquire, — 1. What benefit or advantage we have by this unction; 2. How this belongs unto our consolation, seeing the Holy Spirit is thus bestowed on us as he is promised to be the comforter of the ch

### Repeated word windows

- phrase: we believe the scripture to be the word of god
- phrase: to believe the scripture to be the word of god
- phrase: the mind and will of god as revealed in the
- phrase: believe the scripture to be the word of god with
- phrase: to be the word of god with faith divine and

### Repeated phrase hits

- file: combined_text; text: chapter 5 divine revelation itself the only foundation
- file: combined_text; text: chapter 2 zechariah 12 10 opened and vindicated
- file: combined_text; text: chapter 3 galatians 4 6 opened and vindicated
- file: combined_text; text: chapter 5 the work of the holy spirit
- file: combined_text; text: chapter 7 the nature of prayer in general

### Page reference split files

- file: EPUB/ch043.xhtml; text: p. 249.

### Chapter headings rendered as paragraphs

- file: EPUB/ch006.xhtml; text: CHAPTER I

### Structural bold leaks

- file: EPUB/ch001.xhtml; text: ΠΗΕΥΜΑΤΟΛΟΓΙΑ? OR A DISCOURSE CONCERNING THE HOLY SPIRIT — CONTINUED. [BOOK VI., PART I.] THE REASON OF FAITH. PREFATORY NOTE BY THE EDITOR

### Lowercase page fragments

- file: EPUB/ch055.xhtml; text: should receive strong consolation in all their distresses, when they flee for ref
