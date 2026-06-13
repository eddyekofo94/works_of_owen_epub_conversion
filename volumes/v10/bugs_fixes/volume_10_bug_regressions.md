# Bug Regression Report: Volume 10

- Status: **PASS**
- EPUB audit: `volume_10_audit.json`
- Text integrity audit: `volume_10_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 0 | 165 | OK |
| Inline structural marker candidates | 7 | 8 | OK |
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
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 1 | OK |
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
| Chapter headings rendered as paragraphs | 1 | 1 | OK |
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
| Lowercase page fragments | 1 | 35 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Inline structural marker candidates

- file: EPUB/ch020.xhtml; text: In 1650, Mr. Home, minister at Lynn in Norfolk, a man, according to Palmer (Nonconf. Mem., 3. pp. 6, 7), "of exemplary and primitive piety," and author of several works, published a reply to Owen's work, under the title,
- file: EPUB/ch021.xhtml; text: Arg. 6. From Scripture assertions and consequences. Answers to the proofs of this sixth argument: — 1. From 1 John 4:14; John 1:4, 7; 1 Timothy 2:4. 2. From some texts before vindicated. 3. From Psalm 19:4; Romans 10:18;
- file: EPUB/ch031.xhtml; text: Now, what is it to obey the grace of God? Is it not to believe? Therefore, it seems that Christ intercedeth for them that they may believe, upon condition that they do believe. Others, more cautiously, assert the good us
- file: EPUB/ch046.xhtml; text: Let now any one tell me what the reprobates, in this life, lie under more? And do not all the elect, until their actual reconciliation, in and by Christ, lie under the very same? for, — (1.) Are not their prayers an abom
- file: EPUB/ch052.xhtml; text: That God gave not his Son, — 1. For them who never do believe; 2. Much less for them who never hear of him, and so evidently want means of faith; 3. For them on whom he hath determined not to bestow effectual grace, that

### Repeated word windows

- phrase: that we might be made the righteousness of god in
- phrase: we might be made the righteousness of god in him
- phrase: made him to be sin for us who knew no
- phrase: him to be sin for us who knew no sin
- phrase: hath set forth to be propitiation through faith in his

### Chapter headings rendered as paragraphs

- file: EPUB/ch021.xhtml; text: Chapter 1

### Lowercase page fragments

- file: EPUB/ch021.xhtml; text: of the whole work is prefixed to it. We have not felt at liberty to adopt the num
