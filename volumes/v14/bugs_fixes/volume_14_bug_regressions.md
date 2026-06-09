# Bug Regression Report: Volume 14

- Status: **WARN**
- EPUB audit: `volume_14_audit.json`
- Text integrity audit: `volume_14_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 4 | 75 | OK |
| Inline structural marker candidates | 6 | 12 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 3 | 3 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 7 | 7 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 2 | 16 | OK |
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
| Lowercase page fragments | 7 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: READER,; next: THE treatise entitled "Fiat Lux," which thou wilt find examined in the ensuing discourse, was lent unto me, not long since, by an honorable person, with a request to return an answ
- file: EPUB/ch029.xhtml; previous: CHRISTIAN READER,; next: ALTHOUGH our Lord Jesus Christ hath laid blessed and stable foundations of unity, peace, and agreement in judgment and affection amongst all his disciples, and given forth command 
- file: EPUB/ch045.xhtml; previous: r thou be an apostle, or an evangelist, or a prophet, or whatever thou be; for subjection overthrows not piety. And he saith not simply, 'Let him obey,' but, 'Let him be subject.'"; next: The very same instances are given by Theodoret, Oecumenius, and Theophylact. Bernard, Epist. 42, ad Archiepisc. Senonena, meets with your exception, which in his days began to be b
- file: EPUB/ch050.xhtml; previous: τεύουσι — "But if any should say, 'Why do our images work no miracles?' to them we answer, 'Because,' as the apostle saith, 'signs are for unbelievers, not for them that believe.'"; next: And yet the misadventure of it is, that the most of the miracles which they report and build their faith upon were wrought as by, so amongst, their chiefest believers. And what wer

### Inline structural marker candidates

- file: EPUB/ch030.xhtml; text: And I know that, concerning all your dispute and arguings in these pages, you may say what Lucian doth about his "true story:" Γράφω τοίνυν περὶ ῶν μήτ εῖδον , μήτ ἔπαθον , μήτε παρ ἄλλων ἐπυθόμην ? — "You write about th
- file: EPUB/ch033.xhtml; text: Do you think it so easy for you, "Cornicum oculos, configere," as Cicero tells us an attorney, one Cn. Flavius, thought to do, in going beyond all that the great lawyers had done before him, Orat. pro Muraena, 11. We can
- file: EPUB/ch038.xhtml; text: The present face of Christianity makes the worm a wearisome wilderness; nor should I think any thing a more necessary duty than it would be for persons of piety and ability to apologize for the religion of Jesus Christ, 
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

### Missing enumerator markers

- marker: (1.)
- marker: (2.)
- marker: (3.)
- marker: (4.)
- marker: (5.)

### Missing Greek clauses

- page: 209; sample: αρχομενοι μεν ολιγοι τε ησαν και εν εφρονουν ες πληθος δε σπαρεντες
- page: 235; sample: εχθρος γαρ μοι κεινος ομως αιδαο πυλησιν ος

### Untagged Greek characters

- file: EPUB/ch001.xhtml; text: Ν. N.
- file: EPUB/ch050.xhtml; text: פֶסֶל γλυπτόν

### Repeated phrase hits

- file: combined_text; text: chapter 1 our author's preface and his method
- file: combined_text; text: a vindication of the animadversions on fiat lux

### Page reference split files

- file: EPUB/ch010.xhtml; text: p. 126.

### Lowercase page fragments

- file: EPUB/ch012.xhtml; text: come than Moses were, surely born a Jew, he would, being come into the world, rat
- file: EPUB/ch030.xhtml; text: yet I shall say, that as many as take notice of this discourse will do no less of
- file: EPUB/ch031.xhtml; text: when you know what his business was But the truth is, when you talk of the merit
- file: EPUB/ch032.xhtml; text: which of old she professed!
- file: EPUB/ch033.xhtml; text: as Lactantius reports him. But you say, "If they fall by idolatry, and yet keep a
