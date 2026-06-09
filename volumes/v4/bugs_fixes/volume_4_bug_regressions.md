# Bug Regression Report: Volume 4

- Status: **WARN**
- EPUB audit: `volume_4_audit.json`
- Text integrity audit: `volume_4_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 9 | 61 | OK |
| Inline structural marker candidates | 6 | 1 | REGRESSION |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 4 | 0 | REGRESSION |
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
| Lowercase page fragments | 8 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch029.xhtml; previous: Its general nature is considered, — prayer having been defined to be a spiritual faculty of exercising Christian graces in the way of vocal requests and supplications to God,; next: IV.
- file: EPUB/ch029.xhtml; previous: on of our spiritual wants; acquainting us with the promises of grace and mercy for our relief; and leading us to express desires for any blessing in order to right and proper ends,; next: V.
- file: EPUB/ch029.xhtml; previous: planting holy and gracious desires after the objects sought; giving us delight in God as the object of prayer; and keeping us intent on Christ, as the way and ground of acceptance,; next: VI.
- file: EPUB/ch029.xhtml; previous: The manner of prayer is farther considered with special reference to [Ephesians 6:18]; next: VII.
- file: EPUB/ch044.xhtml; previous: In regard to his effects on believers, it is first proved that his effectual consolations are the privilege of believers exclusively,; next: III.

### Inline structural marker candidates

- file: EPUB/ch016.xhtml; text: 2. Into the especial nature of the Spirit's work in enlightening us into a knowledge of the mind of God in Scripture. Its nature is first considered by a reference to several scriptural expressions descriptive of it, suc
- file: EPUB/ch024.xhtml; text: Nor do I believe that any one who doth and can thus pray as he ought, in a conscientious study of the word, shall ever be left unto the final prevalency of any pernicious error or the ignorance of any fundamental truth. 
- file: EPUB/ch037.xhtml; text: I say, therefore, — 1. That the things insisted on are in some degree and measure necessary unto all acceptable prayer. The Scripture assigns them thereunto, and believers find them so by their own experience. For we dis
- file: EPUB/ch044.xhtml; text: Among the special benefits indicated are, — 1. The unction of the Spirit, 5; 2. sealing of the Spirit, expounded in a brief comment on [Ephesians 1:13] 4:30, VI.; and, 3. The Spirit as an earnest, considered in reference
- file: EPUB/ch052.xhtml; text: What remains is, to inquire, — 1. What benefit or advantage we have by this unction; 2. How this belongs unto our consolation, seeing the Holy Spirit is thus bestowed on us as he is promised to be the comforter of the ch

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

### Lowercase page fragments

- file: EPUB/ch007.xhtml; text: or the things delivered in the Scripture and farther declared by Christ, which be
- file: EPUB/ch009.xhtml; text: nor is there any of the divines of that church which diment herein. We do not, th
- file: EPUB/ch011.xhtml; text: for "of his own will doth God beget us with the word of truth," James 1:18.
- file: EPUB/ch013.xhtml; text: saith Stapleton; — "The secret testimony of the Spirit is altogether necessary, t
- file: EPUB/ch021.xhtml; text: for men are very apt to please themselves with the working and improvement of the
