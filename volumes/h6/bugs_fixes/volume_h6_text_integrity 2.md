# Text Integrity Audit: Volume h6

- Status: **WARN**
- Warnings: 7
- PDF pages: 12
- EPUB text files: 53
- EPUB paragraphs/headings: 7185

## Coverage

- PDF content tokens: 242437
- EPUB content tokens: 481968
- Approximate PDF-to-EPUB coverage ratio: 0.9998
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

- Body paragraphs checked: 7006
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 485
- Short fragments: 403
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 40
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 6
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 1250
- EPUB enumerator markers: 2487
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 8

## Greek / Hebrew

- PDF Greek words: 4349
- EPUB Greek words: 8602
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 459
- EPUB Hebrew words: 910
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 141
- Missing Greek clauses: 0
- Hebrew clauses checked: 46
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 2956
- EPUB Latin words: 5819
- EPUB Tagged Latin words: 2396
- Latin word coverage ratio: 0.9993
- Latin word tagging ratio: 0.4118
- Latin clauses checked: 154
- Missing Latin clauses: 0
- Tagged Latin runs checked: 674
- Translated Latin runs: 53
- Latin translation ratio: 0.0786

## Warnings

- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Possible Paragraph Splits

- file: EPUB/ch002.xhtml; previous: And some directions we may take from the wisdom of the apostle in this management of his present subject, in our preaching or teaching of spiritual things; for,—; next: Obs. I. When the nature and weight of the matter treated of, or the variety of arguments wherein it is concerned, do require that our discourse of it should be drawn forth unto a l
- file: EPUB/ch002.xhtml; previous: is sufferings; and in this place, the declaration of his glory in his priestly office. The same glory and advancement hath respect unto various acts and powers in the Lord Christ:—; next: Ἐκάθισεν . [1.] The manner of his enjoyment of this dignity and glory is expressed in the word ἐκάθισεν , "he sat down." Hereof there was nothing typical in the legal high priest,
- file: EPUB/ch002.xhtml; previous: anifestation of the glorious presence of God. With respect hereunto our Saviour hath taught us to call on "our Father which is in heaven." And from the words we may observe, that,—; next: Obs. III. The principal glory of the priestly office of Christ depends on the glorious exaltation of his person.—To this end is it here pleaded by the apostle, and thereby he evinc
- file: EPUB/ch002.xhtml; previous: doth also communicate all good things from God unto us; for the whole administration of things sacred between God and the church is committed unto him. And we must observe, that,—; next: Obs. I. The Lord Christ, in the height of his glory, condescends to discharge the office of a public minister in the behalf of the church.—We are not to bound our faith on Christ a
- file: EPUB/ch002.xhtml; previous: This was "the true tabernacle, which the Lord pitched," and whereof Christ is the "minister." And we may observe,—; next: Obs. II. That all spiritually sacred and holy things are laid up in Christ.—All the utensils of holy worship of old, all means of sacred light and purification, were all placed and
- file: EPUB/ch002.xhtml; previous: s of the heavenly things themselves," which are all laid up in Christ, "the true tabernacle." They are all enclosed in him, and it will be in vain to seek for them elsewhere. For,—; next: Obs. III. He hath the ministration of all these holy things committed unto him.—He is the minister both of the sanctuary and tabernacle, and of all things contained in them. Herein
- file: EPUB/ch002.xhtml; previous: nd the "minchoth" were offerings of dead things, as of corn, oil, meats, and drinks. To offer all these was the office of the priesthood ordained. And we are taught thereby, that,—; next: Obs. II. There is no approach unto God without continual respect unto sacrifice and atonement. The principal end of sacrifices was to make atonement for sin.—And so necessary was t
- file: EPUB/ch002.xhtml; previous: 4. The matter of it, "somewhat to offer:"—; next: Ὅθεν . 1. The note of inference is ὅθεν , "wherefore." It is frequently used by the apostle in this epistle, when he proves his present assertions, from the old institutions of the
- file: EPUB/ch002.xhtml; previous: hat which was past; and here he only shows how necessary it was that he should have himself to offer, and so to offer himself, as he had done. And from these words we may observe,—; next: Obs. III. That there was no salvation to be had for us, no, not by Jesus Christ himself, without his sacrifice and oblation.—"It was of necessity that he should have somewhat to of
- file: EPUB/ch002.xhtml; previous: Obs. V. The Lord Christ being to save the church in the way of office, he was not to be spared in any thing necessary thereunto.—And in conformity unto him,—; next: Obs. VI. Whatever state or condition we are called unto, what is necessary unto that state is indispensably required of us.—So are holiness and obedience required unto a state of r

## Inline Structural Marker Candidates

- file: EPUB/ch002.xhtml; text: Πᾶς ἀρχιερεύς . In the first, 1. The universality of the expression is to be observed: Πᾶς ἀρχιερεύς ,—"Every high priest." By the context, this universal is cast under a limitation with respect unto the law: "Every high priest" that is ...
- file: EPUB/ch004.xhtml; text: Πᾶς ἀρχιερεύς . In the first, 1. The universality of the expression is to be observed: Πᾶς ἀρχιερεύς ,—"Every high priest." By the context, this universal is cast under a limitation with respect unto the law: "Every high priest" that is ...
- file: EPUB/ch005.xhtml; text: In the words may be observed, 1. The persons spoken of; "who."
- file: EPUB/ch006.xhtml; text: In the words may be observed, 1. The persons spoken of; "who."
- file: EPUB/ch008.xhtml; text: In the promise itself we may consider, 1. Whom it is made unto, 2. What it is that is promised:—
- file: EPUB/ch008.xhtml; text: Τὸ δέ . There are in the words, (1.) The notation of the subject, τὸ δέ ,—"but that," or 'that, whatever it be.' The general rule gives evidence unto the former inference, 'Whatever it be that waxeth old.'
- file: EPUB/ch011.xhtml; text: In the promise itself we may consider, 1. Whom it is made unto, 2. What it is that is promised:—
- file: EPUB/ch012.xhtml; text: Τὸ δέ . There are in the words, (1.) The notation of the subject, τὸ δέ ,—"but that," or 'that, whatever it be.' The general rule gives evidence unto the former inference, 'Whatever it be that waxeth old.'
- file: EPUB/ch012.xhtml; text: Our translation thus rendering the words, avoids the ambiguity mentioned in the Vulgar Latin. "First of all there was a tabernacle made." But whereas our rendering is also obscure, "the first" being mentioned, where only one thing went b...
- file: EPUB/ch015.xhtml; text: Our translation thus rendering the words, avoids the ambiguity mentioned in the Vulgar Latin. "First of all there was a tabernacle made." But whereas our rendering is also obscure, "the first" being mentioned, where only one thing went b...

## Suspicious Large-Number Starts

- file: EPUB/ch008.xhtml; text: 12. Quibus ipse Deus causam seu modum ac rationem hujus rei aperit, quae ingenti illius gratia ac misericordia populo exhibenda continetur . Hac futurum dicit ut populus tanto ardore sibi serviat, suásque leges observet.
- file: EPUB/ch011.xhtml; text: 12. Quibus ipse Deus causam seu modum ac rationem hujus rei aperit, quae ingenti illius gratia ac misericordia populo exhibenda continetur . Hac futurum dicit ut populus tanto ardore sibi serviat, suásque leges observet.
- file: EPUB/ch015.xhtml; text: 11. 2. What are the especial services he performed, in answer unto those of the legal high priest, and their preference above them, ver. 12.
- file: EPUB/ch020.xhtml; text: 11. 2. What are the especial services he performed, in answer unto those of the legal high priest, and their preference above them, ver. 12.
- file: EPUB/ch034.xhtml; text: 12. 2. The consequence on the part of Christ, by whom it was offered, ver. 12, 13.
- file: EPUB/ch036.xhtml; text: 12. 2. The consequence on the part of Christ, by whom it was offered, ver. 12, 13.

## Short Fragments

- file: EPUB/ch002.xhtml; text: Ἐπὶ τοῖς λεγομένοις .
- file: EPUB/ch002.xhtml; text: Τῆς μεγαλωσύνης .
- file: EPUB/ch002.xhtml; text: Ἐν οὐρανοῖς .
- file: EPUB/ch002.xhtml; text: Καὶ τῆς σκηνῆς τῆς ἀληθινῆς .
- file: EPUB/ch002.xhtml; text: Δῶρά τε καὶ θυσίας .
- file: EPUB/ch002.xhtml; text: Τὶ ὁ προσενέγκῃ .
- file: EPUB/ch003.xhtml; text: Καὶ τῆς σκηνῆς τῆς ἀληθινῆς .
- file: EPUB/ch004.xhtml; text: Δῶρά τε καὶ θυσίας .
- file: EPUB/ch004.xhtml; text: Τὶ ὁ προσενέγκῃ .
- file: EPUB/ch005.xhtml; text: Ὑποδείγματι .

## Enumerator Sequence Candidates

- file: EPUB/ch005.xhtml; marker: (2dly.); family: paren_ordinal; context: ises and threatenings of reward and punishment; the first of grace, the other of justice. (2dly.) The expression of these promises and threatenings in external signs; the first in the tree of life, the latter in that of the knowledge of ...
- file: EPUB/ch005.xhtml; marker: [2dly.]; family: bracket_ordinal; context: [2dly.] By his acceptance of the commands concerning the tree of life, and that of the knowledge of good and evil, as the signs and pledges of this covenant. So was it established as a co
- file: EPUB/ch007.xhtml; marker: (2dly.); family: paren_ordinal; context: ises and threatenings of reward and punishment; the first of grace, the other of justice. (2dly.) The expression of these promises and threatenings in external signs; the first in the tree of life, the latter in that of the knowledge of ...
- file: EPUB/ch007.xhtml; marker: [2dly.]; family: bracket_ordinal; context: [2dly.] By his acceptance of the commands concerning the tree of life, and that of the knowledge of good and evil, as the signs and pledges of this covenant. So was it established as a co
- file: EPUB/ch012.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) Although the temple, with its glorious fabric and excellent order, added much unto the outward beauty and splendour of the sacred worship, yet was it no more but a large exemplifi
- file: EPUB/ch012.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) It was the pledge and means of God's residence or dwelling among them, which expresseth the peculiar manner of his presence, mentioned in general before. The tabernacle was God's
- file: EPUB/ch014.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) Although the temple, with its glorious fabric and excellent order, added much unto the outward beauty and splendour of the sacred worship, yet was it no more but a large exemplifi
- file: EPUB/ch014.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) It was the pledge and means of God's residence or dwelling among them, which expresseth the peculiar manner of his presence, mentioned in general before. The tabernacle was God's

## Repeated Windows

- phrase: the entrance of the high priest into the holy place; count: 12
- phrase: in the volume of the book it is written of; count: 10
- phrase: the volume of the book it is written of me; count: 10
- phrase: in him dwelleth all the fulness of the godhead bodily; count: 8
- phrase: that the blood of bulls and of goats should take; count: 8
- phrase: the blood of bulls and of goats should take away; count: 8
- phrase: blood of bulls and of goats should take away sins; count: 8
- phrase: the offering of the body of jesus christ once for; count: 8
- phrase: offering of the body of jesus christ once for all; count: 8
- phrase: will be unto them god and they shall be to; count: 8

## Missing Word Samples

- word: καθʼ; pdf: 17; epub: 0
- word: κατʼ; pdf: 12; epub: 0
- word: ουδʼ; pdf: 5; epub: 0
- word: τουτʼ; pdf: 5; epub: 0
- word: διʼ; pdf: 4; epub: 0

## Excess Word Samples

- word: the; pdf: 24168; epub: 48005
- word: of; pdf: 16392; epub: 32527
- word: and; pdf: 10286; epub: 20442
- word: in; pdf: 6992; epub: 13865
- word: is; pdf: 5731; epub: 11347
- word: it; pdf: 5617; epub: 11182
- word: to; pdf: 3967; epub: 7880
- word: was; pdf: 3647; epub: 7268
- word: he; pdf: 3080; epub: 6081
- word: as; pdf: 2786; epub: 5534

## Untagged Latin Word Samples

- word: mediator; epub: 299; tagged: 6
- word: sinai; epub: 140; tagged: 4
- word: cor; epub: 122; tagged: 0
- word: testator; epub: 122; tagged: 0
- word: abraham; epub: 108; tagged: 0
- word: elsewhere; epub: 106; tagged: 0
- word: immediate; epub: 106; tagged: 0
- word: mere; epub: 99; tagged: 0
- word: iii; epub: 81; tagged: 0
- word: isa; epub: 77; tagged: 0

## Untranslated Latin Samples

- phrase: autem dicendo
- phrase: super ea quae dicuntur
- phrase: Beza, "majestatis illius;" or, "throni virtutis magnificandi
- phrase: ratio est posita
- phrase: in affectibus. Rerum repetitio et congregatio, quae
- phrase: a quibusdam Latinorum enumeratio, et memoriam judicis
- phrase: et totam simul causam ante oculos
- phrase: et etiam si per singula minus
- phrase: quae repetemus quam
- phrase: dicenda sunt, et (quod Graeco verbo

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
