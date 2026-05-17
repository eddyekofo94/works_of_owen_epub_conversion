# Bug Regression Report: Volume 1

- Status: **PASS**
- EPUB audit: `volume_1_audit.json`
- Text integrity audit: `volume_1_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 72 | 116 | OK |
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
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 16 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 8 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 5 | 8 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 2 | 3 | OK |
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
| Lowercase page fragments | 8 | 38 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch005.xhtml; previous: PETER'S CONFESSION; MATTHEW 16:16 — CONCEITS OF THE PAPISTS THEREON — THE SUBSTANCE AND EXCELLENCY OF THAT CONFESSION; next: Our blessed Savior, inquiring of his disciples their apprehensions concerning his person, and their faith in him, Simon Peter — as he was usually the forwardest on all such occasio
- file: EPUB/ch006.xhtml; previous: OPPOSITION MADE UNTO THE CHURCH AS BUILT UPON THE PERSON OF CHRIST; next: There are in the words of our Savior unto Peter concerning the foundation of the church, a promise of its preservation, and a prediction of the opposition that should be made there
- file: EPUB/ch007.xhtml; previous: THE PERSON OF CHRIST THE MOST INEFFABLE EFFECT OF DIVINE WISDOM AND GOODNESS — THENCE THE NEXT CAUSE OF ALL TRUE RELIGION — IN WHAT SENSE IT IS SO; next: The person of Christ is the most glorious and ineffable effect of divine wisdom, grace, and power; and therefore is the next foundation of all acceptable religion and worship. The 
- file: EPUB/ch008.xhtml; previous: TO PERSON OF CHRIST THE FOUNDATION OF ALL THE COUNSELS OF GOD; next: Secondly, The person of Christ is the foundation of all the counsels of God, as unto his own eternal glory in the vocation, sanctification, and salvation of the church. That which 
- file: EPUB/ch009.xhtml; previous: THE PERSON OF CHRIST THE GREAT REPRESENTATIVE OF GOD AND HIS WILL; next: What may be known of God, is, — his nature and existence, with the holy counsels of his will. A representation of them unto us is the foundation of all religion, and the means of o

### Inline structural marker candidates

- file: EPUB/ch078.xhtml; text: A.M. of Northampton, 1781. FT4 A statement occurs in the "Encyclopaedia Britannica" that Owen's works are printed in seven folio volumes. If it be meant that there are seven folio volumes of Owen's works, there is a sens

### Repeated word windows

- phrase: the glory of god in the face of jesus christ
- phrase: between our beholding the glory of christ by faith in
- phrase: our beholding the glory of christ by faith in this
- phrase: beholding the glory of christ by faith in this world
- phrase: the glory of christ by faith in this world and

### Missing Greek clauses

- page: 26; sample: υτος εστιν ηε προς τον πατερα αγουσα ηοσος ηε πετρα ηε κλεις
- page: 31; sample: πρόσωπον ὁμοιούσιος ἑτερούσιος ἐξ οὐκ
- page: 32; sample: ὑπόστατις φύσις μίαν φύσιν ὅτι κατ ἀλήθειαν ἐστὶ μία φύσις τοῦ λόγου
- page: 37; sample: ἔνωσιν φυσικὴν ἕνωσιν κατὰ σύνθεσιν
- page: 37; sample: υἱὸς θεοῦ ὑιὸς ἀνθρώπου γίνεται οὕτω δὲ φωτὸς ἡλίου μία καὶ

### Untagged Greek characters

- file: EPUB/ch004.xhtml; text: , κ.τ.λ. (cap. 6)
- file: EPUB/ch005.xhtml; text: , κ.τ.λ." — "Thou art a rock, and on thee will I build." At least the gender had not been altered, but he would have said, "
- file: EPUB/ch019.xhtml; text: .τ. λ., 2 Corinthians 3:18. We behold his glory "in a glass," which implants the image of it on our minds. And hereby the mind is transformed into the same image, made like unto Christ so represented unto us — which is t

### Repeated phrase hits

- file: combined_text; text: chapter 14 motives unto the love of christ
- file: combined_text; text: meditations and discourses on the glory of christ
- file: combined_text; text: chapter 8 of the state of corrupted nature
- file: combined_text; text: chapter 10 of the person of jesus christ
- file: combined_text; text: chapter 14 of the two-fold estate of christ

### Chapter headings rendered as paragraphs

- file: EPUB/ch003.xhtml; text: Chapter 1
- file: EPUB/ch049.xhtml; text: A. Only by Jesus Christ. — Chapter 9

### Lowercase page fragments

- file: EPUB/ch020.xhtml; text: i
- file: EPUB/ch030.xhtml; text: a
- file: EPUB/ch043.xhtml; text: i
- file: EPUB/ch044.xhtml; text: i
- file: EPUB/ch050.xhtml; text: i
