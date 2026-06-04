# Bug Regression Report: Volume 1

- Status: **PASS**
- EPUB audit: `volume_1_audit.json`
- Text integrity audit: `volume_1_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 19 | 125 | OK |
| Inline structural marker candidates | 15 | 16 | OK |
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

- file: EPUB/ch004.xhtml; previous: nim erat Christus, super quod fundamentum etiam ipse aedificatus est Petrus. Fundamentum quippe aliud nemo potest ponere, praeter id quod positum est, quod est Jesus Christus". [1]; next: — "He (Christ) meant the universal church, which in this world is shaken with divers temptations, as with showers, floods, and tempests, yet falleth not, because it is built on the
- file: EPUB/ch004.xhtml; previous: rtium coelu, ineffabilia dicit, quomodo nos exprimere possumus paternae generationis arcanum, quod nec sentire potuimus nec audire? Quid te ista questionum tormenta delectant?" [2]; next: — "I inquire of you when and how the Son was begotten? Impossible it is to me to know the mystery of this generation. My mind faileth, my voice is silent — and not only mine, but o
- file: EPUB/ch004.xhtml; previous: To the same purpose. speaks Eusebius at large: Demonstratio Evang., lib. 5 cap. 2. [47]; next: Leo well adds hereunto the consideration of his incarnation, in these excellent words: (Serm. 9, De Nativit.:) [73] "Quia in Christo Jesus Filio Dei non solum ad divinam essentiam,
- file: EPUB/ch004.xhtml; previous: veniret utriusque diversitas, ut unus idemque sit filius, qui se, et secundum quod verus est homo, Patre dicit minorem, et secundum quod verus est Deus Patrise profitetur aequalem"; next: — "Human nature is assumed into the society of the Creator, not that he should be the inhabitant, and that the habitation," (that is, by an inhabitation in the effects of his power
- file: EPUB/ch004.xhtml; previous: image of God, even the Father, who by him is represented unto us. See the same book, chap. 7, to the same purpose; also, De Ecclesiast. Theol. contra Marcell., lib. 2 cap. 17. [27]; next: Clemens abounds much in the affirmation of this truth concerning the person of Christ, and we may yet add, from a multitude to the same purpose, one or more testimonies from him. T

### Inline structural marker candidates

- file: EPUB/ch001.xhtml; text: They have repeatedly appeared in the language of Holland; and by the Dutch divines the most favorable mention is made of the various treatises of our pious and learned Puritan. We are informed by Dr Steven, 2 that his Ex
- file: EPUB/ch004.xhtml; text: We may take an instance hereof with respect unto the Nestorian heresy, condemned in the first Ephesian Council, and afterwards in that at Chalcedon. Cyril of Alexandria, a man learned and vehement, designed by all means 
- file: EPUB/ch004.xhtml; text: As he is in his divine person his eternal, essential image; so, in his incarnation, as the teacher of men, he is the representative image of God unto the church, as is afterwards declared. So also Jerome expresseth his m
- file: EPUB/ch004.xhtml; text: Clemens abounds much in the affirmation of this truth concerning the person of Christ, and we may yet add, from a multitude to the same purpose, one or more testimonies from him. Treating of Christ as the teacher of all 
- file: EPUB/ch004.xhtml; text: Herein we consider the incarnation of the Son of God, with respect unto the recovery and salvation of the church alone. Some have contended that he should have been incarnate, had man never fallen or sinned. Of these are

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

- file: EPUB/ch004.xhtml; text: factores autem sermonum ejus facti, communionem habeamus cum ipso".
- file: EPUB/ch008.xhtml; text: as he also proclaims the same delight in him, from heaven, in the days of his fle
- file: EPUB/ch016.xhtml; text: and verse 23, "My Father will love him, and we will come unto him, and make our a
- file: EPUB/ch022.xhtml; text: and in sundry other places. The assumption, the taking of our human nature to be
- file: EPUB/ch030.xhtml; text: against him he lifted up himself; — which was the beginning of his transgression.
