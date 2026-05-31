# Bug Regression Report: Volume 8

- Status: **WARN**
- EPUB audit: `volume_8_audit.json`
- Text integrity audit: `volume_8_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 125 | 127 | OK |
| Inline structural marker candidates | 5 | 0 | REGRESSION |
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

- file: EPUB/ch001.xhtml; previous: ndiscriminate courtesy. There is a curious record which we may quote, as showing that the Parliament exercised some measure of discrimination in voting thanks on these occasions: —; next: There are no means of ascertaining what ministers actually preached on the occasion here referred to. The ministers who had been appointed to preach were Mr. Owen, Mr. John Simson,
- file: EPUB/ch003.xhtml; previous: difications which appear in the Congregationalism of Owen, are conspicuous elements in the first scheme of ecclesiastical polity which he ever broached. See also his "Review of the; next: JUSTITIAM FORTITER, ἴσως , ἐπιεικῶς , ἀπροσωπολήπτως
- file: EPUB/ch003.xhtml; previous: JUSTITIAM FORTITER, ἴσως , ἐπιεικῶς , ἀπροσωπολήπτως; next: Αρχὴν IN ECCLESIASTICIS ἀνιεροτυραννικὴν DISSOLUTAM, RITUS PONTIFICIOS, NOVITIOS, ANTICHRISTIANOS ABOLITOS; PRIVILEGIA PLEBIS CHRISTIANAE POSTLIMINIO RESTITUTA;
- file: EPUB/ch003.xhtml; previous: S, EX ORDINE COMMUNIUM IN SUPREMA CURIA PARLIAM, CONGREGATIS, CONCIONEM HANC SACRAM, HUMILEM ILLAM QUIDEM, IPSORUM TAMEN VOTO JUSSUQUE PRIUS CORAM IPSIS HABITAM, NUNC LUCE DONATAM,; next: Die Mecurij 29 Aprilis, 1646.
- file: EPUB/ch004.xhtml; previous: ce fourteen generations. They alone were in Goshen, and all the world besides in thick darkness; — the dew of heaven was on them as the fleece, when else all the earth was dry. God; next: The prerogative of the Jews was chiefly in this, that to them were committed the oracles of God, Romans 3:1. To them pertained

### Inline structural marker candidates

- file: EPUB/ch010.xhtml; text: "A prayer of Habakkuk the prophet upon Shigionoth. O LORD, I have heard thy speech, and was afraid: O LORD, revive thy work in the midst of the years, make known; in wrath remember mercy. God came from Teman, and the Hol
- file: EPUB/ch010.xhtml; text: Observation 2. Prophets' discoveries of fearful judgments must be attended with fervent prayers. That messenger hath done but half his business who delivers his errand, but returns not an answer. He that brings God's mes
- file: EPUB/ch010.xhtml; text: The reasons of this are taken, — 1. From their envy; 2. From their carnal fear; — the two principles whereby they are acted in reference to the saints of God.
- file: EPUB/ch014.xhtml; text: Now, the Lord will do this, — 1. Because of his own engagement. 2. For our encouragement. And that is twofold. (1.) Of truth and fidelity. (2.) Of honor and glory.
- file: EPUB/ch038.xhtml; text: Now, because you wait on God for direction in reference to the propagation of the gospel, and the preventing that which is contrary to sound doctrine and godliness, I shall, — [1.] Show you very briefly what God has prom

### Repeated word windows

- phrase: not the only nor the chief reason of our believing
- phrase: the only nor the chief reason of our believing the
- phrase: only nor the chief reason of our believing the scripture
- phrase: nor the chief reason of our believing the scripture to
- phrase: the chief reason of our believing the scripture to be

### Lowercase page fragments

- file: EPUB/ch056.xhtml; text: hitherto itself? Nay, can it be consistent with common sense, that the Scripture
- file: EPUB/ch060.xhtml; text: the four evangelists, or Paul's Epistles by him? And if the present church prove
