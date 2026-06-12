# Bug Regression Report: Volume h1

- Status: **PASS**
- EPUB audit: `volume_h1_audit.json`
- Text integrity audit: `volume_h1_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 40 | 40 | OK |
| Inline structural marker candidates | 6 | 6 | OK |
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
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 0 | 7 | OK |
| Possible Beta Code residue files | 2 | 2 | OK |
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
| Structural bold leaks | 1 | 1 | OK |
| Repeated structural markers | 0 | 0 | OK |
| Scholastic bold leaks | 0 | 0 | OK |
| Inline scholastic labels | 0 | 0 | OK |
| Trailing scholastic labels | 0 | 0 | OK |
| DIGRESSION headings not h3 | 0 | 0 | OK |
| Cross-chapter continuation before heading | 0 | 0 | OK |
| Overlong NAV entries | 0 | 0 | OK |
| Duplicate NAV labels | 0 | 0 | OK |
| Spaced caps OCR | 0 | 0 | OK |
| Lowercase page fragments | 1 | 1 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch001.xhtml; previous: EXERCITATIONS ON THE EPISTLE TO THE HEBREWS; next: GENERAL PREFACE
- file: EPUB/ch001.xhtml; previous: GENERAL PREFACE; next: IT has been matter of thankfulness for many generations of the Christian church, that Dr Owen was led to concentrate all his rare endowments and vast resources on the exposition of
- file: EPUB/ch002.xhtml; previous: NOTE IN REGARD TO THE PREFACES; next: IN previous reprints of this work, instead of the prefaces which the author himself had written for the different parts of the work as they issued from the press, one general prefa
- file: EPUB/ch002.xhtml; previous: TO THE RIGHT HONOURABLE; next: SIR WILLIAM MORRICE, KNIGHT,
- file: EPUB/ch002.xhtml; previous: SIR WILLIAM MORRICE, KNIGHT,; next: ONE OF HIS MAJESTY'S MOST HONOURABLE PRIVY COUNCIL, AND PRINCIPAL SECRETARY OF STATE, ETC.

### Inline structural marker candidates

- file: EPUB/ch006.xhtml; text: 1. CLEMENT of Rome, in the judgment of Erasmus and Patrick Young; 2. TERTULLIAN, according to Sixtus Senensis ; 3. BARNABAS, according to Tertullian, Schmidt, Cameron, Twesten, Ullman, Wieseler; 4. LUKE, according to Ori
- file: EPUB/ch009.xhtml; text: 1. That it was written to Gentile Christians; 2. To Jewish believers out of Palestine; 3. To Jewish believers in Palestine; and, 4. To Jewish believers in Palestine, but more especially in Jerusalem or Caesarea.
- file: EPUB/ch022.xhtml; text: 1, 2. Ordinances and institutions of the Jewish church referred to and unfolded in the Epistle to the Hebrews—Principal heads of them mentioned therein. 3. The call of Abraham, Heb. 11:8-19. 4. The name Abram; significat
- file: EPUB/ch025.xhtml; text: 1, 2. Ordinances and institutions of the Jewish church referred to and unfolded in the Epistle to the Hebrews—Principal heads of them mentioned therein. 3. The call of Abraham, Heb. 11:8-19. 4. The name Abram; significat
- file: EPUB/ch026.xhtml; text: 1. The priest; 2. The whole congregation jointly; 3. The ruler; 4. Any of the people of the land: so that none were excluded from the privilege and benefit of this sacrifice.

### Repeated word windows

- phrase: the mighty god the everlasting father the prince of peace
- phrase: and mount sinai was altogether on smoke because the lord
- phrase: mount sinai was altogether on smoke because the lord descended
- phrase: sinai was altogether on smoke because the lord descended upon
- phrase: was altogether on smoke because the lord descended upon it

### Possible Beta Code residue files

- file: EPUB/ch020.xhtml; text: Aj
- file: EPUB/ch022.xhtml; text: Aj

### Structural bold leaks

- file: EPUB/ch002.xhtml; text: ONE OF HIS MAJESTY'S MOST HONOURABLE PRIVY COUNCIL, AND PRINCIPAL SECRETARY OF STATE, ETC.

### Lowercase page fragments

- file: EPUB/ch001.xhtml; text: p. lxxxiv. There is not much to be added in regard to the history of the work. In
