# Text Integrity Audit: Volume h2

- Status: **WARN**
- Warnings: 7
- PDF pages: 12
- EPUB text files: 33
- EPUB paragraphs/headings: 4483

## Coverage

- PDF content tokens: 228529
- EPUB content tokens: 259430
- Approximate PDF-to-EPUB coverage ratio: 0.9981
- Pages checked: 11
- Weak page matches: 0
- Dense source windows checked: 0
- Missing dense source-window pages: 0
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 0
- Top-of-page windows skipped as unstable: 0
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 0
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 4350
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 101
- Short fragments: 44
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 7
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 9
- Roman heading candidates: 0
- Overlong heading candidates: 2
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 632
- EPUB enumerator markers: 647
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 1359
- EPUB Greek words: 1365
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 738
- EPUB Hebrew words: 739
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 89
- Missing Greek clauses: 0
- Hebrew clauses checked: 71
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 7384
- EPUB Latin words: 7719
- EPUB Tagged Latin words: 5452
- Latin word coverage ratio: 0.974
- Latin word tagging ratio: 0.7063
- Latin clauses checked: 664
- Missing Latin clauses: 58
- Tagged Latin runs checked: 1181
- Translated Latin runs: 140
- Latin translation ratio: 0.1185

## Warnings

- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Possible Paragraph Splits

- file: EPUB/ch002.xhtml; previous: curious, partly diabolical, by the instigation of the false gods whom they ministered unto. Homer puts them together, as they came afterwards mostly to be the same, Iliad. A. 62:—; next: Ἀλλ ʼ ἄγε δή τινα μάντιν ἐρείομεν , ἤ ἱερῆα
- file: EPUB/ch002.xhtml; previous: Ἀλλ ʼ ἄγε δή τινα μάντιν ἐρείομεν , ἤ ἱερῆα; next: Ἤ καὶ ὁνειροπόλον ·—
- file: EPUB/ch002.xhtml; previous: Ἤ καὶ ὁνειροπόλον ·—; next: "A prophet, or a priest, or an interpreter of dreams."
- file: EPUB/ch002.xhtml; previous: would abstain from their sacred offices after the shedding of blood, until they were, one way or other, purified to their own satisfaction. So in the poet, Virg. AEneid. ii. 717:—; next: "Tu, genitor, cape sacra manu patriosque penates;
- file: EPUB/ch002.xhtml; previous: Mc, bello e tanto digressum et caede recenti,; next: Attrectare nefas, donec me flumine vivo
- file: EPUB/ch002.xhtml; previous: Attrectare nefas, donec me flumine vivo; next: Abluero."
- file: EPUB/ch003.xhtml; previous: siderable suffrage of learned men, setting aside particular conjectures, which never received entertainment beyond the minds of their authors. And these may be reduced unto three:—; next: All agree that the glory of God is the utmost and supreme end that he intendeth in all his decrees. Although they are free acts of his will and wisdom, yet, on the supposition of t
- file: EPUB/ch004.xhtml; previous: which was to be represented in the creature to be made in their image. These things being premised, we may take a view of the pursuit and management of his particular exceptions:—; next: " Atque quod ad primum attinet; quinam scilicet illi fuerint, quos sit Deus allocutus; primo dicere possumus non necessarium esse, propter hujusmodi locutionum formas, multa indivi
- file: EPUB/ch004.xhtml; previous: l adhere unto and defend; which way of dealing in sacred things of so great importance is very perverse and froward. Thus our author, here relinquishing this conjecture, proceeds:—; next: " Sed demus esto, Deum hic aliquos compellasse, quaeramus quinam isti fuerint. Aiunt adversarii hos omnino debuisse esse sermonis et rationis capaces. Quomodo enim Deus alloqueretu
- file: EPUB/ch004.xhtml; previous: ec loqui nec intelligere possint; sed hoc non satis firmum est. Nam scimus Deum saepe etiam cum sensu et ratione carentibus colloquium instituere; ut in Esa . 1, 'Audite, coeli.' "; next: Rather than this man would omit any cavil, he will make use of such as are sapless and ridiculous. God doth not here speak unto others that are not himself, but by speaking as he d

## Inline Structural Marker Candidates

- file: EPUB/ch009.xhtml; text: That the Lord Christ is called a priest on some account or other, and is so, these men cannot deny, and therefore on all occasions they do in words expressly confess it. But their endeavour is, to persuade us that little or nothing is si...
- file: EPUB/ch022.xhtml; text: VER. 13.—1. The authority of God the Father in the exaltation of Jesus Christ as the head and mediator of the church, is greatly to be regarded by believers. 2. The exaltation of Christ is the great pledge of the acceptance of the work o...
- file: EPUB/ch023.xhtml; text: VER. 17.—1. God is not displeased with any thing in his people but sin. 2. Public sins, sins in societies, are great provocations of God. 3. God sometimes will make men who have been wickedly exemplary in sin righteously exemplary in the...
- file: EPUB/ch023.xhtml; text: VER. 11.—1. An interest in the gospel consisteth not in an outward profession of it, but in a real participation of those things wherein the perfection of its state doth consist. 2. The pre-eminence of the gospel state above the legal is...
- file: EPUB/ch023.xhtml; text: VER. 26.—1. It was inconsistent with the wisdom, goodness, grace, and love of God, that Christ should often suffer in that way which was necessary to the offering of himself, namely, by his death and blood-shedding. 2. It was impossible,...
- file: EPUB/ch024.xhtml; text: VER. 11.—1. An interest in the gospel consisteth not in an outward profession of it, but in a real participation of those things wherein the perfection of its state doth consist. 2. The pre-eminence of the gospel state above the legal is...
- file: EPUB/ch025.xhtml; text: VER. 26.—1. It was inconsistent with the wisdom, goodness, grace, and love of God, that Christ should often suffer in that way which was necessary to the offering of himself, namely, by his death and blood-shedding. 2. It was impossible,...

## Suspicious Large-Number Starts

- file: EPUB/ch003.xhtml; text: 14. Let us, therefore, now consider the arguments or reasons in particular which they plead who maintain this assertion. The principal of them were invented and made use of by some of the ancient schoolmen; and others ha
- file: EPUB/ch006.xhtml; text: 48. The sum of what they all plead is, that there is no such thing as justice in God, requiring that sin be punished; that the cause and fountain of punishment in God is anger, wrath, or fury; that these denote free acts
- file: EPUB/ch010.xhtml; text: 20. Reasons for so doing.
- file: EPUB/ch010.xhtml; text: 10. It remaineth that we consider the pretences and pleas of our adversaries in the defence of their opinion. It is that, I confess, which they have no concernment in for its own sake, being only a necessary consequent o
- file: EPUB/ch010.xhtml; text: 11. It is no matter at all whom we fix upon to call to an account herein. Their wits are barren in a peculiar manner on this subject, so that they all say the same things, one after another, without any considerable vari
- file: EPUB/ch010.xhtml; text: 20. I had sundry reasons why I chose to insist on a particular examination of these discourses of Crellius; for it is confessed that none among our adversaries have handled those things with more diligence and subtilty t
- file: EPUB/ch019.xhtml; text: 22. The Jews call them משכותאי ,—that is, "Sabbatarians;" which must be from some observation of the Sabbath in a distinct manner or for different reasons from themselves. Buxtorf and our late learned lexicographer rende
- file: EPUB/ch020.xhtml; text: 10. III. Be sure to bring good and right principles unto the performance of the duty of keeping a day of rest holy unto the Lord. Some of these I shall name, as confirmed expressly in, or drawn evidently from, the preced
- file: EPUB/ch023.xhtml; text: 12. The proper grammatical sense of the words themselves is duly to be inquired into and pondered.

## Overlong Heading Candidates

- file: EPUB/ch023.xhtml; tag: h2; text: THE OBLIGATION, ADVANTAGE, AND NECESSITY, OF STEADFAST ADHERENCE TO THE GOSPEL INFERRED AND URGED FROM THE PRECEDING DOCTRINES, AND FROM THE TRIUMPHS OF FAITH AS EXEMPLIFIED BY THE SAINTS
- file: EPUB/ch026.xhtml; tag: h2; text: THE OBLIGATION, ADVANTAGE, AND NECESSITY, OF STEADFAST ADHERENCE TO THE GOSPEL INFERRED AND URGED FROM THE PRECEDING DOCTRINES, AND FROM THE TRIUMPHS OF FAITH AS EXEMPLIFIED BY THE SAINTS

## Short Fragments

- file: EPUB/ch002.xhtml; text: Ἤ καὶ ὁνειροπόλον ·—
- file: EPUB/ch002.xhtml; text: Abluero."
- file: EPUB/ch003.xhtml; text: 12.
- file: EPUB/ch003.xhtml; text: 13.
- file: EPUB/ch003.xhtml; text: 15.
- file: EPUB/ch003.xhtml; text: 16.
- file: EPUB/ch006.xhtml; text: 5.
- file: EPUB/ch006.xhtml; text: A DIGRESSION
- file: EPUB/ch010.xhtml; text: 7.
- file: EPUB/ch010.xhtml; text: 8.

## Repeated Windows

- phrase: the necessity of the priesthood of christ on the supposition; count: 4
- phrase: necessity of the priesthood of christ on the supposition of; count: 4
- phrase: of the priesthood of christ on the supposition of sin; count: 4
- phrase: the priesthood of christ on the supposition of sin and; count: 4
- phrase: priesthood of christ on the supposition of sin and grace; count: 4
- phrase: and god blessed the seventh day and sanctified it because; count: 4
- phrase: god blessed the seventh day and sanctified it because that; count: 4
- phrase: blessed the seventh day and sanctified it because that in; count: 4
- phrase: the seventh day and sanctified it because that in it; count: 4
- phrase: seventh day and sanctified it because that in it he; count: 4

## Missing Word Samples

- word: quæ; pdf: 44; epub: 0
- word: hæc; pdf: 20; epub: 0
- word: naturæ; pdf: 8; epub: 0
- word: cœlo; pdf: 7; epub: 0
- word: judæis; pdf: 7; epub: 0
- word: nostræ; pdf: 7; epub: 0
- word: præterea; pdf: 6; epub: 0
- word: pœna; pdf: 6; epub: 0
- word: cœlum; pdf: 6; epub: 0
- word: hebræos; pdf: 6; epub: 0

## Excess Word Samples

- word: quae; pdf: 1; epub: 45
- word: trials; pdf: 30; epub: 58
- word: encouragement; pdf: 28; epub: 51
- word: haec; pdf: 0; epub: 20
- word: afflictions; pdf: 17; epub: 33
- word: mercies; pdf: 17; epub: 32
- word: preserve; pdf: 16; epub: 30
- word: persecution; pdf: 15; epub: 29
- word: dangerous; pdf: 14; epub: 27
- word: evils; pdf: 13; epub: 25

## Missing Latin Word Samples

- word: cœlo; pdf: 7; epub: 0
- word: judæis; pdf: 7; epub: 0
- word: præterea; pdf: 6; epub: 0
- word: pœna; pdf: 6; epub: 0
- word: cœlum; pdf: 6; epub: 0
- word: hebræos; pdf: 6; epub: 0
- word: quædam; pdf: 5; epub: 0
- word: cœlis; pdf: 5; epub: 0
- word: prosopopœia; pdf: 4; epub: 0
- word: cætera; pdf: 4; epub: 0

## Untagged Latin Word Samples

- word: mere; epub: 76; tagged: 2
- word: immediate; epub: 68; tagged: 2
- word: mediator; epub: 65; tagged: 0
- word: abraham; epub: 57; tagged: 0
- word: isa; epub: 54; tagged: 1
- word: elsewhere; epub: 51; tagged: 0
- word: crellius; epub: 48; tagged: 2
- word: adam; epub: 46; tagged: 1
- word: undergo; epub: 31; tagged: 0
- word: terror; epub: 31; tagged: 0

## Missing Latin Clauses

- page: 3; word_count: 7; sample: in mundum non ad præstandum humano generi
- page: 3; word_count: 6; sample: sed ad præbenda bonorum actuum exempla
- page: 3; word_count: 48; sample: si ex hoc loquendi formula numerus et natura dei venanda et colligenda
- page: 3; word_count: 11; sample: qui loquebatur sed loquebatur præsentibus aliis hinc autem non immediate sequitur
- page: 3; word_count: 11; sample: pluribus adhuc consequentiis opus est nimirum quærendum statim est quinam illi
- page: 3; word_count: 5; sample: omnium præstantissimum creaturus introducitur a
- page: 3; word_count: 5; sample: sophoclis qui in œdipo coloneo
- page: 3; word_count: 16; sample: indubitatum est verba præscripta a sapientia dici si enim versio pagnini merceri
- page: 3; word_count: 8; sample: et verba præscripta ab intelligentia proferantur sequitur locum
- page: 3; word_count: 4; sample: loquendi formulis prosopopœiam non

## Untranslated Latin Samples

- phrase: sacerdotio fungi," or "munus
- phrase: is "sacerdotio fungor
- phrase: in sacris operari
- phrase: officio fungi
- phrase: pontificatus, sacerdotium
- phrase: Veii: "Tuo
- phrase: instinctus, pergo ad delendam
- phrase: hinc decumam
- phrase: praedae voveo," Liv
- phrase: tanto digressum et

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
