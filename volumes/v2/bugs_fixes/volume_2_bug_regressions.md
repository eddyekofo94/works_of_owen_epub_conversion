# Bug Regression Report: Volume 2

- Status: **PASS**
- EPUB audit: `volume_2_audit.json`
- Text integrity audit: `volume_2_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 59 | 68 | OK |
| Inline structural marker candidates | 0 | 1 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 2 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 3 | 55 | OK |
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
| Overlong headings containing body prose | 0 | 0 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 2 | 2 | OK |
| Noteref links without spacing class | 0 | 0 | OK |
| Scripture blockquote false positives | 0 | 0 | OK |
| Orphan scripture brackets | 0 | 0 | OK |
| Glued ordinal anchors | 0 | 0 | OK |
| Structural bold leaks | 1 | 1 | OK |
| Repeated structural markers | 0 | 0 | OK |
| Scholastic bold leaks | 0 | 0 | OK |
| Inline scholastic labels | 0 | 0 | OK |
| Trailing scholastic labels | 0 | 0 | OK |
| DIGRESSION headings not h3 | 0 | 0 | OK |
| Cross-chapter continuation before heading | 0 | 0 | OK |
| Overlong NAV entries | 0 | 0 | OK |
| Duplicate NAV labels | 0 | 0 | OK |
| Spaced caps OCR | 0 | 0 | OK |
| Lowercase page fragments | 14 | 14 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch004.xhtml; previous: Communion with the FATHER is described,; next: and practical inferences deduced from it, IV.
- file: EPUB/ch004.xhtml; previous: Part II . — The reality of communion with CHRIST is proved, CHAP. I.; and the nature of it is subsequently considered,; next: It is shown to consist in grace; and then the grace of Christ is exhibited under three divisions: — his personal grace, III. — VI.; and under this branch are two long digressions, 
- file: EPUB/ch004.xhtml; previous:  under three divisions: — his personal grace, III. — VI.; and under this branch are two long digressions, designed to unfold the glory and loveliness of Christ; — purchased grace ,; next: — X.; in which the mediatorial work of Christ is fully considered, in reference to our acceptance with God, VII., VIII.; sanctification, IX.; and the privileges of the covenant, X.
- file: EPUB/ch008.xhtml; previous: (1st.) The love of the Father unto us is an antecedent love, and that in two respects: —; next: [1st.] It is antecedent in respect of our love, 1 John 4:10, "Herein is love, not that we loved God, but that he loved us." His love goes before ours. The father loves the child, w
- file: EPUB/ch008.xhtml; previous: (2ndly.) Our love is consequential in both these regards: —; next: [1st.] In respect of the love of God. Never did creature turn his affections towards God, if the heart of God were not first set upon him.

### Repeated word windows

- phrase: pleased the father that in him should all fullness dwell
- phrase: the father that in him should all fullness dwell colossians
- phrase: bare our sins in his own body on the tree
- phrase: is with the father and with his son jesus christ
- phrase: our sins in his own body on the tree peter

### Untagged Greek characters

- file: EPUB/ch026.xhtml; text: It is God has given the earnest of the Spirit in our hearts: an expression directly answering that of Galatians 4:6, “God has sent forth the Spirit of his Son into your hearts;” that is, the person of the Spirit; for not

### Chapter headings rendered as paragraphs

- file: EPUB/ch034.xhtml; text: The second section of this chapter i
- file: EPUB/ch039.xhtml; text: Chapter 3

### Fragmented Greek span-run files

- file: EPUB/ch016.xhtml; text: <span class="greek" lang="el" xml:lang="el">[ας</span> <span class="greek" lang="el" xml:lang="el">
- file: EPUB/ch022.xhtml; text: <span class="greek" lang="el" xml:lang="el">[Ιν</span> <span class="greek" lang="el" xml:lang="el">

### Structural bold leaks

- file: EPUB/ch020.xhtml; text: Objection 1. For our absolution by and upon the death of Christ, it may be said, that “if the elect have their absolution, reconciliation, and freedom by the de

### Lowercase page fragments

- file: EPUB/ch003_title.xhtml; text: d
- file: EPUB/ch004.xhtml; text: a
- file: EPUB/ch007.xhtml; text: w
- file: EPUB/ch009.xhtml; text: i
- file: EPUB/ch013.xhtml; text: a
