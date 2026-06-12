# Bug Regression Report: Volume 14

- Status: **PASS**
- EPUB audit: `volume_14_audit.json`
- Text integrity audit: `volume_14_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 0 | 75 | OK |
| Inline structural marker candidates | 4 | 12 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 3 | 3 | OK |
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

### Inline structural marker candidates

- file: EPUB/ch030.xhtml; text: And I know that, concerning all your dispute and arguings in these pages, you may say what Lucian doth about his "true story:" Γράφω τοίνυν περὶ ῶν μήτ εῖδον , μήτ ἔπαθον , μήτε παρ ἄλλων ἐπυθόμην ? — "You write about th
- file: EPUB/ch033.xhtml; text: Do you think it so easy for you, " Cornicum oculos, configere," as Cicero tells us an attorney, one Cn. Flavius, thought to do, in going beyond all that the great lawyers had done before him, Orat. pro Muraena , 11. We c
- file: EPUB/ch041.xhtml; text: Some few observations upon this discourse of yours will farther manifest the absurdity of that consequence which you feign not to have been taken notice of in the "Animadversions;" for which you had no cause, but that yo
- file: EPUB/ch044.xhtml; text: Our Savior gave them equal commission to teach all nations; told them that as his Father had sent him so he sent them; that he had chosen them twelve, but that one of them was a devil, — never that one of them should be 

### Repeated word windows

- phrase: chapter farther vindication of the second chapter of the animadversions
- phrase: that whence and from whom we first received our religion
- phrase: whence and from whom we first received our religion there
- phrase: and from whom we first received our religion there and
- phrase: from whom we first received our religion there and with

### Missing front CONTENTS pages

- page: 3; sample: contents of animadversions on treatise entitled fiat lux prefatory note by the editor to the reader preface chap our author's preface and his method heathen pleas general principles
- page: 5; sample: proposals from protestant principles tending unto moderation and unity farther vindication of the second chapter of the animadversions the remaining principles of fiat lux considered judicious readers schoolmen
- page: 6; sample: communion heroes of the ass's head whose worship was objected to jews and christians the church of rome no safe guide prefatory note by the editor preface some

### Page reference split files

- file: EPUB/ch010.xhtml; text: p. 126.
