# Bug Regression Report: Volume 15

- Status: **WARN**
- EPUB audit: `volume_15_audit.json`
- Text integrity audit: `volume_15_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 105 | 61 | REGRESSION |
| Inline structural marker candidates | 0 | 1 | OK |
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
| EPUB packaging errors | 1 | 0 | REGRESSION |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 1 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 0 | 0 | OK |
| Overlong headings containing body prose | 2 | 0 | REGRESSION |
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

- file: EPUB/ch011.xhtml; previous: rpose, — namely, that the ordinances and institutions of the gospel may be administered to the edification of the church. Now, this the apostle expressly affirms, Ephesians 4:7-13,; next: The Lord Jesus, who hath appointed the office of the ministry, hath also provided sufficient furniture for the persons called according to his mind to the discharge of that office 
- file: EPUB/ch015.xhtml; previous: invent, and nothing less can support. Unto such as these we shall not so much as tender satisfaction, until they are capable of receiving the advice of the apostle, Ephesians 4:31,; next: It is for the sake of them alone who really value and esteem love, peace, and unity among Christians for themselves, that we here tender an account of our thoughts and principles c
- file: EPUB/ch016.xhtml; previous: to rise on the evil and on the good, and sendeth rain on the just and on the unjust." Now, all mankind may be cast into two ranks or orders: for, first, there are those who are yet; next: — such, we mean, as are either negatively or privatively infidels or unbelievers, who have yet never heard the sound of the gospel, or do continue to refuse and reject it where it 
- file: EPUB/ch016.xhtml; previous: "Go ye into all the world, and preach the gospel to every creature," he adds unto it that decretory sentence concerning the everlasting condition of all men with respect thereunto,; next: As the preaching of the gospel, and the belief on Jesus Christ thereon, are the only means of obtaining salvation, so all those who are not made partakers of them must perish etern
- file: EPUB/ch017.xhtml; previous: e unto any particular church on the earth; and so it often falleth out, as we could manifest by instances, did that work now lie before us. This is the church which the Lord Christ; next: And we must acknowledge that in all things this is the church unto which we have our first and principal regard, as being the spring from which all other considerations of the chur

### Repeated word windows

- phrase: the unity of the spirit in the bond of peace
- phrase: the whole body fitly joined together and compacted by that
- phrase: whole body fitly joined together and compacted by that which
- phrase: body fitly joined together and compacted by that which every
- phrase: fitly joined together and compacted by that which every joint

### EPUB packaging errors

- {'code': 'noteref_targets_missing', 'message': 'Some noteref targets do not have matching endnote anchors', 'examples': ['EPUB/endnotes.xhtml#fn186', 'EPUB/endnotes.xhtml#fn347']}

### Repeated phrase hits

- file: combined_text; text: chapter 7 no other church-state of divine institution

### Overlong headings containing body prose

- file: EPUB/ch071.xhtml; text: MAY A PERSON BE CALLED TO, OR BE EMPLOYED IN, A PART ONLY OF THE OFFICE OR WORK OF THE MINISTRY; OR MAY HE HOLD THE RELATION AND EXERCISE THE DUTY OF AN ELDER OR MINISTER UNTO MORE
- file: EPUB/ch082.xhtml; text: MAY NOT THE CHURCH, IN THE SOLEMN WORSHIP OF GOD, AND CELEBRATION OF THE ORDINANCES OF THE GOSPEL, MAKE USE OF AND CONTENT ITSELF IN THE USE OF FORMS OF PRAYER IN AN UNKNOWN TONGUE
