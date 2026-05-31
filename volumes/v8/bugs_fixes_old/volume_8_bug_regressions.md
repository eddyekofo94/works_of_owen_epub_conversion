# Bug Regression Report: Volume 8

- Status: **PASS**
- EPUB audit: `volume_8_audit.json`
- Text integrity audit: `volume_8_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 127 | 127 | OK |
| Inline structural marker candidates | 0 | 0 | OK |
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
| Missing Greek clauses | 0 | 0 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 0 | 0 | OK |
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
| Lowercase page fragments | 2 | 2 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: difications which appear in the Congregationalism of Owen, are conspicuous elements in the first scheme of ecclesiastical polity which he ever broached. See also his "Review of the; next: JUSTITIAM FORTITER, ἴσως , ἐπιεικῶς , ἀπροσωπολήπτως
- file: EPUB/ch003.xhtml; previous: JUSTITIAM FORTITER, ἴσως , ἐπιεικῶς , ἀπροσωπολήπτως; next: Αρχὴν IN ECCLESIASTICIS ἀνιεροτυραννικὴν DISSOLUTAM, RITUS PONTIFICIOS, NOVITIOS, ANTICHRISTIANOS ABOLITOS; PRIVILEGIA PLEBIS CHRISTIANAE POSTLIMINIO RESTITUTA;
- file: EPUB/ch003.xhtml; previous: S, EX ORDINE COMMUNIUM IN SUPREMA CURIA PARLIAM, CONGREGATIS, CONCIONEM HANC SACRAM, HUMILEM ILLAM QUIDEM, IPSORUM TAMEN VOTO JUSSUQUE PRIUS CORAM IPSIS HABITAM, NUNC LUCE DONATAM,; next: Die Mecurij 29 Aprilis, 1646.
- file: EPUB/ch004.xhtml; previous: ce fourteen generations. They alone were in Goshen, and all the world besides in thick darkness; — the dew of heaven was on them as the fleece, when else all the earth was dry. God; next: The prerogative of the Jews was chiefly in this, that to them were committed the oracles of God, Romans 3:1. To them pertained
- file: EPUB/ch004.xhtml; previous: The prerogative of the Jews was chiefly in this, that to them were committed the oracles of God, Romans 3:1. To them pertained; next: But when the fullness (Galatians 4:4; John 12:32; Acts 17:30; Mark 16:15; Malachi 3:4; Proverbs 8:31) of time came, the Son of God being sent in the likeness of sinful flesh, drew 

### Repeated word windows

- phrase: the removing of those things that are shaken as of
- phrase: removing of those things that are shaken as of things
- phrase: of those things that are shaken as of things that
- phrase: those things that are shaken as of things that are
- phrase: things that are shaken as of things that are made

### Lowercase page fragments

- file: EPUB/ch056.xhtml; text: hitherto itself? Nay, can it be consistent with common sense, that the Scripture
- file: EPUB/ch060.xhtml; text: the four evangelists, or Paul's Epistles by him? And if the present church prove
