# Bug Regression Report: Volume 5

- Status: **PASS**
- EPUB audit: `volume_5_audit.json`
- Text integrity audit: `volume_5_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 0 | 0 | OK |
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
| Repeated phrase hits | 3 | 3 | OK |
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
| Lowercase page fragments | 8 | 8 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Inline structural marker candidates

- file: EPUB/ch002.xhtml; text: Lastly, the concluding chapter is devoted to an explanation of the passages in Paul and James which are alleged to be at variance but which are proved to be in perfect harmony, 20. — Ed.
- file: EPUB/ch004.xhtml; text: All men in those days were either kept in bondage under endless fears and anxieties of mind upon the convictions of sin, or sent for relief unto indulgences, priestly pardons, penances, pilgrimages, works satisfactory of
- file: EPUB/ch009.xhtml; text: What it is that, when a justified person is guilty of sin (as guilty he is more or less every day), and his conscience is pressed with a sense thereof, as that only thing which can endanger or intercept his justified est
- file: EPUB/ch010.xhtml; text: A very few words will also free our inquiry from any concernment in that which is called sentential justification, at the day of judgment; for of what nature soever it be, the person concerning whom that sentence is pron
- file: EPUB/ch021.xhtml; text: In opposition hereunto, the state and prayer of the publican, under the same design of seeking justification before God, are expressed. And the outward acts of his person are mentioned, as representing and expressive of 

### Repeated word windows

- phrase: of justification by the imputation of the righteousness of christ
- phrase: doctrine of justification by the imputation of the righteousness of
- phrase: set forth to be propitiation through faith in his blood
- phrase: the doctrine of justification by the imputation of the righteousness
- phrase: freely by his grace through the redemption that is in

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
