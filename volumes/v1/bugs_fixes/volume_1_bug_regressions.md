# Bug Regression Report: Volume 1

- Status: **PASS**
- EPUB audit: `volume_1_audit.json`
- Text integrity audit: `volume_1_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 8 | 125 | OK |
| Inline structural marker candidates | 5 | 16 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 4 | 4 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 0 | 0 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 5 | 8 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 1 | 3 | OK |
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
| Lowercase page fragments | 7 | 38 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch004.xhtml; previous: veniret utriusque diversitas, ut unus idemque sit filius, qui se, et secundum quod verus est homo, Patre dicit minorem, et secundum quod verus est Deus Patrise profitetur aequalem"; next: — "Human nature is assumed into the society of the Creator, not that he should be the inhabitant, and that the habitation," (that is, by an inhabitation in the effects of his power
- file: EPUB/ch011.xhtml; previous: ls was subordinate unto him; and whatever instruction was thereby given unto the church in the mind and will of God, it was immediately from him, as the great prophet of the church; next: (3rdly,) By sending his Holy Spirit to inspire, act, and guide the prophets, by whom God would reveal himself. God spoke unto them by the "mouth of his holy prophets, which have be
- file: EPUB/ch011.xhtml; previous: was so to prophet of the church always as to tender manifold instructions unto the perishing, unbelieving world. Hence is he said to lighten "every man that comets into the world,"; next: John 1:9, by one way or other communicating to them some notices of God and his will; for his light shineth in, or irradiates darkness itself — that darkness which is come on the m
- file: EPUB/ch022.xhtml; previous: (1st,) That the Word ceased to be what it was, and was substantially turned into flesh; next: (2ndly,) That continuing to be what it was, it was made to be also what before it was not.
- file: EPUB/ch027.xhtml; previous: Christian Reader,; next: To design of the ensuing Discourse is to declare some part of that glory of our Lord Jesus Christ which is revealed in the Scripture, and proposed as the principal object of our fa

### Inline structural marker candidates

- file: EPUB/ch013.xhtml; text: In the confirmation hereof it will appear what judgment ought to be passed on that inquiry — which, after the uninterrupted profession of the catholic church for so many ages of a faith unto the contrary, is begun to be 
- file: EPUB/ch031.xhtml; text: That which we inquire after at present, is, the glory of Christ herein, and how we may behold that glory. And there are three things wherein we may take a prospect of it. 1. In his susception of this office. 2. In his di
- file: EPUB/ch031.xhtml; text: In the susception of this office we may behold the glory of Christ, — I. In his condescension; II. In his love.
- file: EPUB/ch040.xhtml; text: Two things we must here speak unto. 1. Why does the Lord Christ, at any time, thus hide himself in his glory from the faith of believers, that they cannot behold him? 2. How we may perceive and know that he does so withd
- file: EPUB/ch045.xhtml; text: The second thing proposed is, that notwithstanding all this provision for the growth of spiritual life in us, believers, especially in a long course of profession, are subject to decays, such as may cast them into great 

### Repeated word windows

- phrase: the glory of god in the face of jesus christ
- phrase: unto us child is born unto us son is given
- phrase: of the glory of god in the face of jesus
- phrase: us child is born unto us son is given and
- phrase: the brightness of his glory and the express image of

### Missing front CONTENTS pages

- page: 3; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ prefatory note preface chapter peter's confession matthew conceits of the papists thereon the substance
- page: 4; sample: chapter the especial principle of obedience unto the person of christ which is love its truth and reality vindicated chapter the nature operations and causes of divine love
- page: 5; sample: the glory of christ in his exaltation after the accomplishment of the work of mediation in this world representations of the glory of christ under the old testament
- page: 6; sample: of the holy trinity of the works of god and first of those that are internal and immanent of the works of god that outwardly are of him

### Repeated phrase hits

- file: combined_text; text: chapter 14 motives unto the love of christ
- file: combined_text; text: meditations and discourses on the glory of christ
- file: combined_text; text: chapter 8 of the state of corrupted nature
- file: combined_text; text: chapter 10 of the person of jesus christ
- file: combined_text; text: chapter 14 of the two-fold estate of christ

### Chapter headings rendered as paragraphs

- file: EPUB/ch003.xhtml; text: Chapter 1

### Lowercase page fragments

- file: EPUB/ch004.xhtml; text: factores
- file: EPUB/ch008.xhtml; text: as he also proclaims the same delight in him, from heaven, in the days of his fle
- file: EPUB/ch016.xhtml; text: and verse 23, "My Father will love him, and we will come unto him, and make our a
- file: EPUB/ch022.xhtml; text: and in sundry other places. The assumption, the taking of our human nature to be
- file: EPUB/ch030.xhtml; text: against him he lifted up himself; — which was the beginning of his transgression.
