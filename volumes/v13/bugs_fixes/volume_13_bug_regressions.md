# Bug Regression Report: Volume 13

- Status: **PASS**
- EPUB audit: `volume_13_audit.json`
- Text integrity audit: `volume_13_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 29 | 95 | OK |
| Inline structural marker candidates | 13 | 13 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 2 | 2 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 6 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
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
| Chapter headings rendered as paragraphs | 2 | 2 | OK |
| Overlong headings containing body prose | 0 | 2 | OK |
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
| Lowercase page fragments | 10 | 10 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: ays of mercy and grace which are necessary to carry you along through all your engagements, until you arrive at the haven of everlasting glory, where you would be. I rest your most; next: obliged servant in Jesus Christ, our common Master
- file: EPUB/ch003.xhtml; previous: obliged servant in Jesus Christ, our common Master; next: John Owen
- file: EPUB/ch011.xhtml; previous: From these and the like places it appears to me, that, —; next: There is a general obligation on all Christians to promote the conversion and instruction of sinners, and men erring from the right way.
- file: EPUB/ch011.xhtml; previous: At least, we may deduce from them, by the way of analogy, that, —; next: Whatsoever necessary truth is revealed to any out of the word of God, not before known, he ought to have an uncontradicted liberty of declaring that truth, provided that he use suc
- file: EPUB/ch011.xhtml; previous: Whence.it appears, that, —; next: Truth revealed unto any carries along with it an unmovable persuasion of conscience (which is powerfully obligatory) that it ought to be published and spoken to others.

### Inline structural marker candidates

- file: EPUB/ch009.xhtml; text: Now, three ways may a man receive, and be assured that he hath received, this divine mission, or know that he is called of God to the preaching of the word; I mean not that persuasion of divine concurrence which is neces
- file: EPUB/ch016.xhtml; text: Motives to the observance of this rule are: — 1. The name wherein they speak and administer, 2 Corinthians 5:20. 2. The work which they do, 1 Corinthians 3:9; 2 Corinthians 6:1; Timothy 4:16. 3. The return that they make
- file: EPUB/ch016.xhtml; text: Explication III. The greatness of the work (for which who is sufficient? 2 Corinthians 2:16); — the strength of the opposition which lies against it, 1 Corinthians 16:9; Revelation 12:12; 2 Timothy 4:3-5; — the concernme
- file: EPUB/ch016.xhtml; text: Let motives hereunto be, — 1. God's command. 2. Our own preservation from sin and protection from punishment, that with others we be not infected and plagued. 3. Christ's delight in the purity of his ordinances. 4. His d
- file: EPUB/ch016.xhtml; text: Now, to a right performance of this duty, and in the discharge of it, are required, — 1. A due valuation, strong desire, and high esteem of the church's prosperity, in every member of it, Psalm 122:6. 2. Bowels of compas

### Repeated word windows

- phrase: brief vindication of the nonconformists from the charge of schism
- phrase: an account of the grounds and reasons on which protestant
- phrase: account of the grounds and reasons on which protestant dissenters
- phrase: of the grounds and reasons on which protestant dissenters desire
- phrase: the lion hath roared who will not fear the lord

### Missing front CONTENTS pages

- page: 3; sample: contents of the duty of pastors and people distinguished preface of the administration of holy things among the patriarchs before the law of the same among the jews
- page: 8; sample: an answer etc brief vindication of the nonconformists from the charge of schism prefatory note by the editor brief vindication etc truth and innocence vindicated prefatory note by

### Chapter headings rendered as paragraphs

- file: EPUB/ch016.xhtml; text: Chapter 4
- file: EPUB/ch020.xhtml; text: Chapter 11

### Lowercase page fragments

- file: EPUB/ch003.xhtml; text: obliged servant in Jesus Christ, our common Master
- file: EPUB/ch004.xhtml; text: will be mounting. In the matter concerning which I propose my weak essay, some wo
- file: EPUB/ch007.xhtml; text: and again,
- file: EPUB/ch009.xhtml; text: and Jeremiah 20:9, "His word was in mine heart as a burning fire shut up in my bo
- file: EPUB/ch011.xhtml; text: to which add that of the apostle,
