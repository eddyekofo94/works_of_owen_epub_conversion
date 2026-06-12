# Bug Regression Report: Volume h6

- Status: **WARN**
- EPUB audit: `volume_h6_audit.json`
- Text integrity audit: `volume_h6_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 40 | 61 | OK |
| Inline structural marker candidates | 40 | 1 | REGRESSION |
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

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch002.xhtml; previous: And some directions we may take from the wisdom of the apostle in this management of his present subject, in our preaching or teaching of spiritual things; for,—; next: Obs. I. When the nature and weight of the matter treated of, or the variety of arguments wherein it is concerned, do require that our discourse of it should be drawn forth unto a l
- file: EPUB/ch002.xhtml; previous: is sufferings; and in this place, the declaration of his glory in his priestly office. The same glory and advancement hath respect unto various acts and powers in the Lord Christ:—; next: Ἐκάθισεν . [1.] The manner of his enjoyment of this dignity and glory is expressed in the word ἐκάθισεν , "he sat down." Hereof there was nothing typical in the legal high priest, 
- file: EPUB/ch002.xhtml; previous: anifestation of the glorious presence of God. With respect hereunto our Saviour hath taught us to call on "our Father which is in heaven." And from the words we may observe, that,—; next: Obs. III. The principal glory of the priestly office of Christ depends on the glorious exaltation of his person.—To this end is it here pleaded by the apostle, and thereby he evinc
- file: EPUB/ch002.xhtml; previous:  doth also communicate all good things from God unto us; for the whole administration of things sacred between God and the church is committed unto him. And we must observe, that,—; next: Obs. I. The Lord Christ, in the height of his glory, condescends to discharge the office of a public minister in the behalf of the church.—We are not to bound our faith on Christ a
- file: EPUB/ch002.xhtml; previous: This was "the true tabernacle, which the Lord pitched," and whereof Christ is the "minister." And we may observe,—; next: Obs. II. That all spiritually sacred and holy things are laid up in Christ.—All the utensils of holy worship of old, all means of sacred light and purification, were all placed and

### Inline structural marker candidates

- file: EPUB/ch002.xhtml; text: Πᾶς ἀρχιερεύς . In the first, 1. The universality of the expression is to be observed: Πᾶς ἀρχιερεύς ,—"Every high priest." By the context, this universal is cast under a limitation with respect unto the law: "Every high
- file: EPUB/ch004.xhtml; text: Πᾶς ἀρχιερεύς . In the first, 1. The universality of the expression is to be observed: Πᾶς ἀρχιερεύς ,—"Every high priest." By the context, this universal is cast under a limitation with respect unto the law: "Every high
- file: EPUB/ch005.xhtml; text: In the words may be observed, 1. The persons spoken of; "who."
- file: EPUB/ch006.xhtml; text: In the words may be observed, 1. The persons spoken of; "who."
- file: EPUB/ch008.xhtml; text: In the promise itself we may consider, 1. Whom it is made unto, 2. What it is that is promised:—

### Repeated word windows

- phrase: the entrance of the high priest into the holy place
- phrase: in the volume of the book it is written of
- phrase: the volume of the book it is written of me
- phrase: in him dwelleth all the fulness of the godhead bodily
- phrase: that the blood of bulls and of goats should take
