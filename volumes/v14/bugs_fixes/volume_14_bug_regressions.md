# Bug Regression Report: Volume 14

- Status: **PASS**
- EPUB audit: `volume_14_audit.json`
- Text integrity audit: `volume_14_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 75 | 75 | OK |
| Inline structural marker candidates | 1 | 12 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 3 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 7 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 1 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 8 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 2 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 1 | 1 | OK |
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

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch001.xhtml; previous: EDITED BY; next: WILLIAM H. GOOLD
- file: EPUB/ch001.xhtml; previous: WILLIAM H. GOOLD; next: ANIMADVERSIONS ON A TREATISE ENTITLED "FIAT LUX."
- file: EPUB/ch001.xhtml; previous: PREFATORY NOTE BY THE EDITOR; next: Preface Chap. 1. — Our author's preface, and his method
- file: EPUB/ch001.xhtml; previous: 7. —; next: Use of reason
- file: EPUB/ch005.xhtml; previous: orld, began in Ireland, amongst his good Roman Catholics, who were blessed from Rome into rebellion and murder, somewhat before any drop of blood was shed in England or Scotland, —; next: Let them that are innocent throw stones at others: Roman Catholics are unfit to be employed in that work. But it was never judged either a safe or honest way to judge of any religi

### Inline structural marker candidates

- file: EPUB/ch031.xhtml; text: And I know that, concerning all your dispute and arguings in these pages, you may say what Lucian doth about his "true story:" Γράφω τοίνυν περὶ ῶν μήτ εῖδον , μήτ ἔπαθον , μήτε παρ ἄλλων ἐπυθόμην ? — "You write about th

### Repeated word windows

- phrase: fiat lux prefatory note by the editor to the reader
- phrase: vindication of the first chapter of the animadversions the method
- phrase: of the first chapter of the animadversions the method of
- phrase: the first chapter of the animadversions the method of fiat
- phrase: defense of the second chapter of the animadversions principles of

### Untagged Greek characters

- file: EPUB/ch002.xhtml; text: Ν. N.
- file: EPUB/ch051.xhtml; text: פֶסֶל γλυπτόν

### Repeated phrase hits

- file: combined_text; text: chapter 1 our author's preface and his method
- file: combined_text; text: a vindication of the animadversions on fiat lux

### Page reference split files

- file: EPUB/ch011.xhtml; text: p. 126.
