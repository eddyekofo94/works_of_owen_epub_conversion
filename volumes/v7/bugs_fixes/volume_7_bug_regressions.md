# Bug Regression Report: Volume 7

- Status: **WARN**
- EPUB audit: `volume_7_audit.json`
- Text integrity audit: `volume_7_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 126 | 61 | REGRESSION |
| Inline structural marker candidates | 3 | 1 | REGRESSION |
| Repeated word windows | 25 | 25 | OK |
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
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 1 | 0 | REGRESSION |
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

## New Warning Codes

- Text integrity: flat_analysis_chapters

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch001.xhtml; previous: EDITED BY; next: WILLIAM H. GOOLD
- file: EPUB/ch001.xhtml; previous: WILLIAM H. GOOLD; next: NATURE AND CAUSES OF APOSTASY FROM THE GOSPEL.
- file: EPUB/ch003.xhtml; previous: rked the reign of Charles II has often been the subject of speculation and inquiry. Mr Macaulay thus confirms our author's estimate of the rapid decline of morality at this time: —; next: The historian, dealing with the surface of affairs rather than with the springs of conduct, may account the vulgar theory of a reaction against enforced strictness sufficient to ex
- file: EPUB/ch005.xhtml; previous: each shall be, if they endeavor not to prevent it with their utmost diligence, and the open hazard of all their earthly concerns. A learned writer of the church of England affirms,; next: And after he had declared that "ministers of the gospel may deny Christ, or manifest their being ashamed of the gospel, by not opposing his word at they ought unto the sins of men,
- file: EPUB/ch007.xhtml; previous: Certainly the Lord Christ may say to the churches and nations among whom his name is yet owned in the world, what God said of old concerning that of the Jews, then his only church,; next: Yea, to most of them as in another place,

### Inline structural marker candidates

- file: EPUB/ch006.xhtml; text: They may taste, — 1. Of the word in its truth, not its power; 2. Of the worship of the church in its outward order, not in its inward beauty; 3. Of the gifts of the church, not its graces.
- file: EPUB/ch021.xhtml; text: An inquiry follows into the objects of spiritual thoughts; which are, — 1. The dispensations of Providence; 2. Special trials and temptations; and 3. Heavenly and eternal realities. In regard to the latter, —
- file: EPUB/ch022.xhtml; text: An inquiry follows into the objects of spiritual thoughts; which are, — 1. The dispensations of Providence; 2. Special trials and temptations; and 3. Heavenly and eternal realities. In regard to the latter, —

### Repeated word windows

- phrase: nature of this grace and duty of being spiritually minded
- phrase: the true notion and consideration of spiritual and heavenly things
- phrase: dominion of sin which we are freed from and discharged
- phrase: of sin which we are freed from and discharged of
- phrase: sin which we are freed from and discharged of by

### Flat ANALYSIS chapters

- file: EPUB/ch022.xhtml

### Repeated phrase hits

- file: combined_text; text: the grace and duty of being spiritually minded
