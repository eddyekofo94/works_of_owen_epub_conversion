# Bug Regression Report: Volume 1

- Status: **PASS**
- EPUB audit: `volume_1_audit.json`
- Text integrity audit: `volume_1_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 13 | 125 | OK |
| Inline structural marker candidates | 0 | 16 | OK |
| Syllabus-anchor candidates | 15 | 16 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 4 | OK |
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
| Repeated phrase hits | 0 | 8 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 2 | 3 | OK |
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
| Lowercase page fragments | 7 | 38 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |
| Implemented absent samples | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch004.xhtml; previous:  καὶ θεοφιλῶν ἀνδρῶν μετεωριζομένη — διὰ μίαν ἐκείνην , ἥν αὐτὸς ἀπεφήνατο λέξιν , εἴπων , Επὶ τὴν πέτραν οἰκοδομήσω μου τὴν ἐηκκλησίαν , καὶ πύλαι ᾅδου οὐ κατισχύσουσιν αὐτῆς ". †; next: He proves the verity of divine predictions from the glorious accomplishment of that word, and the promise of our Savior, that he would build his church on the rock, (that is, himse
- file: EPUB/ch004.xhtml; previous:  enim erat Christus, super quod fundamentum etiam ipse aedificatus est Petrus. Fundamentum quippe aliud nemo potest ponere, praeter id quod positum est, quod est Jesus Christus". †; next: — "He (Christ) meant the universal church, which in this world is shaken with divers temptations, as with showers, floods, and tempests, yet falleth not, because it is built on the
- file: EPUB/ch004.xhtml; previous: To the same purpose. speaks Eusebius ‡ at large: Demonstratio Evang., lib. 5 cap. 2. ◇; next: Leo well adds hereunto the consideration of his incarnation, in these excellent words: (Serm. 9, De Nativit.) ◇ " Quia in Christo Jesus Filio Dei non solum ad divinam essentiam, se
- file: EPUB/ch004.xhtml; previous: αὴς ἥλιος σὺν ἀνθρώποις ἐπὶ γῆς πολιτευοίτο , οὐδένα τῶν ἑπὶ τῆς γῆς μείναι ἆν ἀδιάφορον , πάντων συλλήβδην ἐμψύχων ὁμοῦ καὶ ἀψύχων ἀθρόᾳ τῃ τοῦ φωτὸς προσβολῇ διαφθαρησομένων ". †; next: The sense of which words, with some that follow in the same place, is unto this purpose: By the beams of the sunlight, and life, and heat, unto the procreation, sustentation, refre
- file: EPUB/ch004.xhtml; previous: he image of God, even the Father, who by him is represented unto us. See the same book, chap. 7, to the same purpose; also, De Ecclesiast. Theol. contra Marcell., lib. 2 cap. 17. ◇; next: Clemens abounds much in the affirmation of this truth concerning the person of Christ, and we may yet add, from a multitude to the same purpose, one or more testimonies from him. T

### Syllabus-anchor candidates

- file: EPUB/ch006.xhtml
- file: EPUB/ch010.xhtml
- file: EPUB/ch014.xhtml
- file: EPUB/ch014.xhtml
- file: EPUB/ch022.xhtml

### Repeated word windows

- phrase: the glory of god in the face of jesus christ
- phrase: unto us child is born unto us son is given
- phrase: of the glory of god in the face of jesus
- phrase: us child is born unto us son is given and
- phrase: the brightness of his glory and the express image of

### Chapter headings rendered as paragraphs

- file: EPUB/ch003.xhtml; text: Chapter 1
- file: EPUB/ch049.xhtml; text: Chapter 7

### Lowercase page fragments

- file: EPUB/ch004.xhtml; text: factores
- file: EPUB/ch008.xhtml; text: as he also proclaims the same delight in him, from heaven, in the days of his fle
- file: EPUB/ch016.xhtml; text: and verse 23, "My Father will love him, and we will come unto him, and make our a
- file: EPUB/ch022.xhtml; text: and in sundry other places. The assumption, the taking of our human nature to be
- file: EPUB/ch030.xhtml; text: against him he lifted up himself; — which was the beginning of his transgression.
