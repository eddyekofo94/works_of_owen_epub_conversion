# Bug Regression Report: Volume 5

- Status: **WARN**
- EPUB audit: `volume_5_audit.json`
- Text integrity audit: `volume_5_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 3 | 61 | OK |
| Inline structural marker candidates | 4 | 1 | REGRESSION |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 6 | 0 | REGRESSION |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 0 | 0 | OK |
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 3 | 7 | OK |
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
| Lowercase page fragments | 8 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: To The Reader; next: I shall not need to detain the reader with an account of the nature and moment of that doctrine which is the entire subject of the ensuing discourse; for although sundry persons, e
- file: EPUB/ch004.xhtml; previous:  are justified freely by the grace of God, through the redemption that is in Christ Jesus; whom God has set forth to be a propitiation through faith in his blood," Romans 3:24, 25,; next: — they will offer violence unto common sense and reason, rather than not disturb that harmony which they cannot understand. For although it be plainly affirmed to be a redemption b
- file: EPUB/ch027.xhtml; previous: To The Reader; next: As faith is the first vital act that every true Christian puts Forth, and the life which he lives is by the faith of the Son of God, so it is his next and great concern to know tha

### Inline structural marker candidates

- file: EPUB/ch004.xhtml; text: All men in those days were either kept in bondage under endless fears and anxieties of mind upon the convictions of sin, or sent for relief unto indulgences, priestly pardons, penances, pilgrimages, works satisfactory of
- file: EPUB/ch010.xhtml; text: A very few words will also free our inquiry from any concernment in that which is called sentential justification, at the day of judgment; for of what nature soever it be, the person concerning whom that sentence is pron
- file: EPUB/ch021.xhtml; text: In opposition hereunto, the state and prayer of the publican, under the same design of seeking justification before God, are expressed. And the outward acts of his person are mentioned, as representing and expressive of 
- file: EPUB/ch022.xhtml; text: This, in the matter of our justification, he calls, — (1.) Χάρισμα , with respect unto the free, gratuitous grant of it by the grace of God, Δωρεὰ τῆς χάριτος , and (2.) Δώρημα , with respect unto us who receive it, — a 

### Repeated word windows

- phrase: of justification by the imputation of the righteousness of christ
- phrase: doctrine of justification by the imputation of the righteousness of
- phrase: set forth to be propitiation through faith in his blood
- phrase: the doctrine of justification by the imputation of the righteousness
- phrase: freely by his grace through the redemption that is in

### Missing front CONTENTS pages

- page: 3; sample: contents the doctrine of justification general considerations first the general nature of justification state of the person to be justified antecedently thereunto romans galatians john galatians the sole
- page: 4; sample: acceptable unto many reasons of it two parts of corrupted nature's repugnancy unto the mystery of the gospel that which would reduce it unto the private reason of
- page: 5; sample: sinners by christ with its acquiescency therein the description given explained and confirmed from the nature of the gospel exemplified in its contrary or the nature of unbelief
- page: 6; sample: juridical scheme and of forensic title the parts and progress of it inferences from the whole chapter distinction of first and second justification the whole doctrine of the
- page: 7; sample: day that judgment being according unto works answered and the impertinency of it declared chapter imputation and the nature of it the first express record of justification determines

### Repeated phrase hits

- file: combined_text; text: chapter 3 the use of faith in justification
- file: combined_text; text: chapter 17 testimonies out of the evangelists considered
- file: combined_text; text: chapter 19 objections against the doctrine of justification

### Lowercase page fragments

- file: EPUB/ch004.xhtml; text: and the other is that of our Savior, Luke 17:10,
- file: EPUB/ch010.xhtml; text: who yet disclaims any confidence therein as unto his justification before God; fo
- file: EPUB/ch011.xhtml; text: attempts the sense of the word, but confounds it with "reputare:"
- file: EPUB/ch012.xhtml; text: and also Serm. 16
- file: EPUB/ch022.xhtml; text: injustus", 1 Peter 3:18. "
