# Bug Regression Report: Volume 1

- Status: **PASS**
- EPUB audit: `volume_1_audit.json`
- Text integrity audit: `volume_1_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 116 | 116 | OK |
| Inline structural marker candidates | 1 | 1 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 10 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 8 | 8 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 3 | 3 | OK |
| Overlong headings containing body prose | 0 | 0 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 0 | OK |
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
| Lowercase page fragments | 38 | 38 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch001.xhtml; previous: **GENERAL PREFACE.**; next: IT would be presumption to enter upon any commendation of John Owen as an author and divine. His works will continue to gather round them the respect and admiration of the Church o
- file: EPUB/ch005.xhtml; previous: **A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST**; next: **CHAPTER 1**
- file: EPUB/ch005.xhtml; previous: **CHAPTER 1**; next: **PETER'S CONFESSION; Matthew 16:16MATTHEW 16:16 — CONCEITS OF THE PAPISTS THEREON — THE SUBSTANCE AND EXCELLENCY OF THAT CONFESSION**
- file: EPUB/ch005.xhtml; previous: **PETER'S CONFESSION; Matthew 16:16MATTHEW 16:16 — CONCEITS OF THE PAPISTS THEREON — THE SUBSTANCE AND EXCELLENCY OF THAT CONFESSION**; next: Our blessed Savior, inquiring of his disciples their apprehensions concerning his person, and their faith in him, Simon Peter — as he was usually the forwardest on all such occasio
- file: EPUB/ch011.xhtml; previous: But —; next: There was yet more required thereunto, or to render his offices effectual unto their proper ends. Not one of them could have been so, had he been no more than a man — had he had no

### Inline structural marker candidates

- file: EPUB/ch019.xhtml; text: Whatever men may fancy to the contrary, it is the design of the apostle, in sundry places of his writings, to prove that they did so, especially Romans 1; 1 Corinthians 1. Wherefore, it was an infinite condescension of d

### Repeated word windows

- phrase: the glory of god in the face of jesus christ
- phrase: between our beholding the glory of christ by faith in
- phrase: our beholding the glory of christ by faith in this
- phrase: beholding the glory of christ by faith in this world
- phrase: the glory of christ by faith in this world and

### Untagged Greek characters

- file: EPUB/ch004.xhtml; text: , ηε etc, saith Ignatius: Epist. ad Philadelph. — “He” (that is, Christ) “is the way leading unto the Father, the rock, the key, the shepherd” — wherein he has respect unto this testimony. And Origin expressly denies the
- file: EPUB/ch004.xhtml; text: , κ.τ.λ. (cap. 6)
- file: EPUB/ch005.xhtml; text: , κ.τ.λ.” — “Thou art a rock, and on thee will I build.” At least the gender had not been altered, but he would have said, “
- file: EPUB/ch019.xhtml; text: .τ. λ., 2 Corinthians 3:182 Corinthians 3:18. We behold his glory “in a glass,” which implants the image of it on our minds. And hereby the mind is transformed into the same image, made like unto Christ so represented un

### Repeated phrase hits

- file: combined_text; text: chapter 14 motives unto the love of christ
- file: combined_text; text: meditations and discourses on the glory of christ
- file: combined_text; text: chapter 8 of the state of corrupted nature
- file: combined_text; text: chapter 10 of the person of jesus christ
- file: combined_text; text: chapter 14 of the two-fold estate of christ

### Chapter headings rendered as paragraphs

- file: EPUB/ch005.xhtml; text: **CHAPTER 1
- file: EPUB/ch028.xhtml; text: **CHAPTER 1
- file: EPUB/ch049.xhtml; text: governeth all things. — Chapter 6

### Lowercase page fragments

- file: EPUB/ch002_title.xhtml; text: m
- file: EPUB/ch008.xhtml; text: a
- file: EPUB/ch015.xhtml; text: p
- file: EPUB/ch019.xhtml; text: r
- file: EPUB/ch024.xhtml; text: o
