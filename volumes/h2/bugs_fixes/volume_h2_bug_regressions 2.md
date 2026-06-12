# Bug Regression Report: Volume h2

- Status: **WARN**
- EPUB audit: `volume_h2_audit.json`
- Text integrity audit: `volume_h2_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 40 | 61 | OK |
| Inline structural marker candidates | 7 | 1 | REGRESSION |
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
| Repeated phrase hits | 2 | 7 | OK |
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

- file: EPUB/ch002.xhtml; previous:  curious, partly diabolical, by the instigation of the false gods whom they ministered unto. Homer puts them together, as they came afterwards mostly to be the same, Iliad. A. 62:—; next: Ἀλλ ʼ ἄγε δή τινα μάντιν ἐρείομεν , ἤ ἱερῆα
- file: EPUB/ch002.xhtml; previous: Ἀλλ ʼ ἄγε δή τινα μάντιν ἐρείομεν , ἤ ἱερῆα; next: Ἤ καὶ ὁνειροπόλον ·—
- file: EPUB/ch002.xhtml; previous: Ἤ καὶ ὁνειροπόλον ·—; next: "A prophet, or a priest, or an interpreter of dreams."
- file: EPUB/ch002.xhtml; previous:  would abstain from their sacred offices after the shedding of blood, until they were, one way or other, purified to their own satisfaction. So in the poet, Virg. AEneid. ii. 717:—; next: "Tu, genitor, cape sacra manu patriosque penates;
- file: EPUB/ch002.xhtml; previous: Mc, bello e tanto digressum et caede recenti,; next: Attrectare nefas, donec me flumine vivo

### Inline structural marker candidates

- file: EPUB/ch009.xhtml; text: That the Lord Christ is called a priest on some account or other, and is so, these men cannot deny, and therefore on all occasions they do in words expressly confess it. But their endeavour is, to persuade us that little
- file: EPUB/ch022.xhtml; text: VER. 13.—1. The authority of God the Father in the exaltation of Jesus Christ as the head and mediator of the church, is greatly to be regarded by believers. 2. The exaltation of Christ is the great pledge of the accepta
- file: EPUB/ch023.xhtml; text: VER. 17.—1. God is not displeased with any thing in his people but sin. 2. Public sins, sins in societies, are great provocations of God. 3. God sometimes will make men who have been wickedly exemplary in sin righteously
- file: EPUB/ch023.xhtml; text: VER. 11.—1. An interest in the gospel consisteth not in an outward profession of it, but in a real participation of those things wherein the perfection of its state doth consist. 2. The pre-eminence of the gospel state a
- file: EPUB/ch023.xhtml; text: VER. 26.—1. It was inconsistent with the wisdom, goodness, grace, and love of God, that Christ should often suffer in that way which was necessary to the offering of himself, namely, by his death and blood-shedding. 2. I

### Repeated word windows

- phrase: the necessity of the priesthood of christ on the supposition
- phrase: necessity of the priesthood of christ on the supposition of
- phrase: of the priesthood of christ on the supposition of sin
- phrase: the priesthood of christ on the supposition of sin and
- phrase: priesthood of christ on the supposition of sin and grace

### Repeated phrase hits

- file: combined_text; text: part iv concerning the sacerdotal office of christ
- file: combined_text; text: part v concerning a day of sacred rest
