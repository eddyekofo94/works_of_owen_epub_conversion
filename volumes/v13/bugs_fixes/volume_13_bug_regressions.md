# Bug Regression Report: Volume 13

- Status: **WARN**
- EPUB audit: `volume_13_audit.json`
- Text integrity audit: `volume_13_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 9 | 95 | OK |
| Inline structural marker candidates | 3 | 8 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 2 | 2 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 6 | 6 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 1 | 16 | OK |
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
| Chapter headings rendered as paragraphs | 1 | 2 | OK |
| Overlong headings containing body prose | 2 | 2 | OK |
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
| Lowercase page fragments | 10 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: ays of mercy and grace which are necessary to carry you along through all your engagements, until you arrive at the haven of everlasting glory, where you would be. I rest your most; next: obliged servant in Jesus Christ, our common Master
- file: EPUB/ch003.xhtml; previous: obliged servant in Jesus Christ, our common Master; next: John Owen
- file: EPUB/ch015.xhtml; previous: To The Reader; next: THERE are, Christian reader, certain principles in church affairs generally consented unto by all men aiming at reformation and the furtherance of the power of godliness therein, h
- file: EPUB/ch026.xhtml; previous: h and making profession of Christianity, may claim admission into the society of Christians within those bounds, and enjoy the privileges and ordinances which are there dispensed,"; next: Ans. of Commit., p. 105. This is also pursued by the authors of Jus Divinum Ministerii Anglicani, pp. 9,10, where, after the repetition of the words first mentioned, they add, that
- file: EPUB/ch029.xhtml; previous: To The Reader; next: CHRISTIAN READER,

### Inline structural marker candidates

- file: EPUB/ch009.xhtml; text: Now, three ways may a man receive, and be assured that he hath received, this divine mission, or know that he is called of God to the preaching of the word; I mean not that persuasion of divine concurrence which is neces
- file: EPUB/ch031.xhtml; text: Thus, in general, to take a view of some particular passages in the appendix destined to this good work: The first section tries, with much wit and rhetoric, to improve the pretended alteration of judgment to the blemish
- file: EPUB/ch059.xhtml; text: The reasonableness of this gospel institution is manifested by the Holy Ghost: — 1. From the law of nature, Luke 10:7; 1 Corinthians 9:7, 11. 2. From the law of nations, in the same place. 3. From the tendency and equity

### Repeated word windows

- phrase: the grounds and reasons on which protestant dissenters desire their
- phrase: grounds and reasons on which protestant dissenters desire their liberty
- phrase: the state of the kingdom with respect to the present
- phrase: state of the kingdom with respect to the present bill
- phrase: of the kingdom with respect to the present bill against

### Missing front CONTENTS pages

- page: 3; sample: contents of the duty of pastors and people distinguished preface of the administration of holy things among the patriarchs before the law of the same among the jews
- page: 8; sample: an answer etc brief vindication of the nonconformists from the charge of schism prefatory note by the editor brief vindication etc truth and innocence vindicated prefatory note by

### Missing enumerator markers

- marker: (1.)
- marker: (2.)
- marker: (3.)
- marker: (4.)
- marker: (5.)

### Missing Greek clauses

- page: 263; sample: δουλον κυριου ου δει μαχεσθαι

### Repeated phrase hits

- file: combined_text; text: eshcol a cluster of the fruit of canaan
- file: combined_text; text: a review of the true nature of schism
- file: combined_text; text: chapter 3 a review of the charger's preface

### Chapter headings rendered as paragraphs

- file: EPUB/ch020.xhtml; text: Chapter 11

### Overlong headings containing body prose

- file: EPUB/ch049.xhtml; text: [Inconsistent expressions of Parker in regard to the power of the magistrate and the rights of conscience — The design of his discourse to prove the magistrate's authority to gover
- file: EPUB/ch050.xhtml; text: [Alleged power of the magistrate over the conscience in matters of morality refuted — Distinction between moral virtue and grace — Meaning of the terms — Four propositions of Parke

### Lowercase page fragments

- file: EPUB/ch003.xhtml; text: obliged servant in Jesus Christ, our common Master
- file: EPUB/ch004.xhtml; text: will be mounting. In the matter concerning which I propose my weak essay, some wo
- file: EPUB/ch007.xhtml; text: and again,
- file: EPUB/ch009.xhtml; text: and Jeremiah 20:9, "His word was in mine heart as a burning fire shut up in my bo
- file: EPUB/ch011.xhtml; text: to which add that of the apostle,
