# Bug Regression Report: Volume h3

- Status: **WARN**
- EPUB audit: `volume_h3_audit.json`
- Text integrity audit: `volume_h3_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 40 | 61 | OK |
| Inline structural marker candidates | 8 | 1 | REGRESSION |
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
| Missing configured fonts | 1 | 0 | REGRESSION |
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

- Text integrity: font_config_missing

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch002.xhtml; previous:  הנביאים האחרונים חגי זכריה ומלאכי נסתלקה רוח הקודש מישראל ;—'After the death of the latter prophets, Haggai, Zechariah, and Malachi, the Holy Spirit was taken away from Israel.' "; next: It is, then, confessed "that God ceased to speak to the church in prophets, as to their oral teaching and writing, after the days of Malachi; which season of the want of vision, th
- file: EPUB/ch002.xhtml; previous: efore mentions light in particular, because of an allusion to the light at first created by God, when of all other things, whereto there is no such allusion, he maketh no mention,"; next: Ans. [1.] The new creation granted by the men of this persuasion being only a moral suasion of the minds of men by the outward doctrine of the gospel, I know not what allusion can 
- file: EPUB/ch002.xhtml; previous: ρακτὴρ τῆς ὑποστάσεως αὐτοῦ , φέρων τε τὰ πάντα τῷ ῥήματι τῆς δυνάμεως αὑτοῦ , δι ʼ ἑαυτοῦ καθαρισμὸν ποιησάμενος τῶν ἁμαρτιῶν ἡμῶν , ἐκάθισεν ἐν δεξιᾷ τῆς μεγαλωσύνης ἐν ὑψηλοῖς ‚; next: Δι ʼ ἑαυτοῦ is wanting in MS. T.; but the sense requires the words, and all other ancient copies retain them. Ἡμῶν is wanting in some copies; and one or two for ἐκάθισε have καθίζε
- file: EPUB/ch002.xhtml; previous: ee: thy throne shall be established for ever." (1 Chron. 17:14, "But I will settle him in mine house and in my kingdom for ever: and his throne shall be established for evermore."); next: This is the whole divine oracle from whence the apostle takes the testimony under consideration; and the difficulty wherewith it is attended ariseth from hence, that it is not easy
- file: EPUB/ch003.xhtml; previous: ρακτὴρ τῆς ὑποστάσεως αὐτοῦ , φέρων τε τὰ πάντα τῷ ῥήματι τῆς δυνάμεως αὑτοῦ , δι ʼ ἑαυτοῦ καθαρισμὸν ποιησάμενος τῶν ἁμαρτιῶν ἡμῶν , ἐκάθισεν ἐν δεξιᾷ τῆς μεγαλωσύνης ἐν ὑψηλοῖς ‚; next: Δι ʼ ἑαυτοῦ is wanting in MS. T.; but the sense requires the words, and all other ancient copies retain them. Ἡμῶν is wanting in some copies; and one or two for ἐκάθισε have καθίζε

### Inline structural marker candidates

- file: EPUB/ch006.xhtml; text: Wherefore he adds, (3.) what is direct to his pretension, "That all the words, or things signified by them, in any testimony, which are firstly spoken of one, and then are, for some of the causes mentioned" (that is, con
- file: EPUB/ch009.xhtml; text: Wherefore he adds, (3.) what is direct to his pretension, "That all the words, or things signified by them, in any testimony, which are firstly spoken of one, and then are, for some of the causes mentioned" (that is, con
- file: EPUB/ch013.xhtml; text: Εἰ γάρ , "si enim," "etenim," "and if," "for if." Ὁ λόγος λαληθεὶς , " sermo dictus ;" נֶילְתָא דֵּאתְמֵלַלֵת , Syr., " sermo qui dictus est," or "pronuntiatus ," "the word which was spoken or pronounced,"—properly, as w
- file: EPUB/ch013.xhtml; text: He further describes the gospel, (2.) From the way and means of its conveyance unto us. It was "confirmed unto us by them that heard him." And herein also he prevents an objection that might arise in the minds of the Heb
- file: EPUB/ch014.xhtml; text: Εἰ γάρ , "si enim," "etenim," "and if," "for if." Ὁ λόγος λαληθεὶς , " sermo dictus ;" נֶילְתָא דֵּאתְמֵלַלֵת , Syr., " sermo qui dictus est," or "pronuntiatus ," "the word which was spoken or pronounced,"—properly, as w

### Repeated word windows

- phrase: for whom are all things and by whom are all
- phrase: whom are all things and by whom are all things
- phrase: the brightness of his glory and the express image of
- phrase: brightness of his glory and the express image of his
- phrase: of his glory and the express image of his person

### Missing configured fonts

- {'volume': 'h3', 'configured_font': 'bembo', 'expected_path': '/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/fonts/bembo', 'note': 'Font directory fonts/bembo/ exists but contains no .otf or .ttf files.  Add the font files to fix this.'}
