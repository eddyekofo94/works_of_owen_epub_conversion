# Text Integrity Audit: Volume h5

- Status: **WARN**
- Warnings: 10
- PDF pages: 12
- EPUB text files: 34
- EPUB paragraphs/headings: 4320

## Coverage

- PDF content tokens: 242911
- EPUB content tokens: 421159
- Approximate PDF-to-EPUB coverage ratio: 0.9993
- Pages checked: 11
- Weak page matches: 1
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

- Body paragraphs checked: 4208
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 337
- Short fragments: 152
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 32
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 2
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 826
- EPUB enumerator markers: 1464
- Missing enumerator marker forms: 1
- Enumerator sequence candidates: 4

## Greek / Hebrew

- PDF Greek words: 3241
- EPUB Greek words: 5551
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 399
- EPUB Hebrew words: 631
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 145
- Missing Greek clauses: 0
- Hebrew clauses checked: 48
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3365
- EPUB Latin words: 6134
- EPUB Tagged Latin words: 2537
- Latin word coverage ratio: 0.9878
- Latin word tagging ratio: 0.4136
- Latin clauses checked: 174
- Missing Latin clauses: 8
- Tagged Latin runs checked: 726
- Translated Latin runs: 114
- Latin translation ratio: 0.157

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Possible Paragraph Splits

- file: EPUB/ch002.xhtml; previous: all. Neither was a due consideration hereof ever more necessary than it is in the days wherein we live. And other things may be added of the like nature unto this purpose. Again,—; next: Obs. II. Some important doctrines of truth may, in the preaching of the gospel, be omitted for a season, but none must ever be forgotten or neglected.—So deals the apostle in this
- file: EPUB/ch002.xhtml; previous: , with the utmost endeavours of our whole souls. 'We have abode long enough by the shore; let us now hoist our sails and launch forth into the deep.' And we may hence learn, that,—; next: Obs. III. It is a necessary duty of the dispensers of the gospel to excite their hearers, by all pressing considerations, to make a progress in the knowledge of the truth. Thus dea
- file: EPUB/ch002.xhtml; previous: g he had, the principal subject of his epistles is constantly the increase of light and knowledge in the churches, which he knew to be so necessary for them. We may therefore add,—; next: Obs. IV. The case of that people is deplorable and dangerous whose teachers are not able to carry them on in the knowledge of the mysteries of the gospel. The key of knowledge may
- file: EPUB/ch003.xhtml; previous: From what hath been discoursed, we may inquire after our own interest in this great and necessary duty; to assist us wherein I shall yet add some further directions; as,—; next: Repentance is twofold: first, Initial; secondly, Continued in our whole course; and our inquiry is to be after our interest in both of them. The former is that whose general nature
- file: EPUB/ch003.xhtml; previous: Now there are several ways whereby men miss their duty with respect unto this first principle, and thereby ruin their souls eternally:—; next: 1 Some utterly despise it. Such are the presumptuous sinners mentioned, Deut. 29:19, 20. As they disregard the curse of the law, so they do also the promise of the gospel, as unto
- file: EPUB/ch003.xhtml; previous: p. 3. This, then, was that which he here minds the Hebrews of, as the principal foundation of that profession of the gospel which they had taken on them. And we may observe, that,—; next: Obs. II. Faith in God as to the accomplishing of the great promise, in sending his Son Jesus Christ to save us from our sins, is the great fundamental principle of our interest in
- file: EPUB/ch003.xhtml; previous: body which died, in all the essential and integral parts of it, rendering it, in a reunion of or with the soul, immortal, or of an eternal duration, in blessedness or misery. And,—; next: Obs. IV. The doctrine of the resurrection is a fundamental principle of the gospel, the faith whereof is indispensably necessary unto the obedience and consolation of all that prof
- file: EPUB/ch003.xhtml; previous: This principle being thus cleared and confirmed, it may not be amiss to show what practical improvement it doth require. And,—; next: Obs. V. It is manifest that there is no duty in religion that is not, or ought not to be, influenced by the consideration of it.
- file: EPUB/ch003.xhtml; previous: eligion. But the reader is at liberty to follow whether of these interpretations he pleaseth. And from the whole of what hath been discoursed we may take the ensuing observations:—; next: Obs. VI. Persons to be admitted into the church, and unto a participation of all the holy ordinances thereof, had need be well instructed in the important principles of the gospel.
- file: EPUB/ch004.xhtml; previous: fers unto some especial gospel privileges, which professors in those days were promiscuously made partakers of; and what they were in particular we must in the next place inquire:—; next: Ἅπαξ φωτισθέντες .

## Inline Structural Marker Candidates

- file: EPUB/ch004.xhtml; text: Obs. III. There is a goodness and excellency in this heavenly gift, which may be tasted or experienced in some measure by such as never receive them, in their life, power, and efficacy. They may taste,—(1.) Of the word in its truth, not ...
- file: EPUB/ch004.xhtml; text: 1. Its communication or application unto the earth,—it falls upon it; 2. An especial adjunct thereof in its frequency,—it falls often on it; 3. By that reception which the earth is naturally fitted and suited to give unto it,—it drinketh...
- file: EPUB/ch004.xhtml; text: Μεταλαμβάνει εὐλογίας ἀπὸ τοῦ Θεοῦ . The earth must be tilled, from its nature and the law of its creation, And therefore Adam was to have tilled and wrought the ground in the garden even before the fall, Gen. 2:15. And this is the princ...
- file: EPUB/ch004.xhtml; text: They are, therefore, no otherwise meet for God but in and through Christ, according to the infinite condescension which he is pleased to exercise in the covenant of grace. Therein doth the Lord Christ, 1. Make our persons accepted, as wa...
- file: EPUB/ch005.xhtml; text: Obs. III. There is a goodness and excellency in this heavenly gift, which may be tasted or experienced in some measure by such as never receive them, in their life, power, and efficacy. They may taste,—(1.) Of the word in its truth, not ...
- file: EPUB/ch006.xhtml; text: 1. Its communication or application unto the earth,—it falls upon it; 2. An especial adjunct thereof in its frequency,—it falls often on it; 3. By that reception which the earth is naturally fitted and suited to give unto it,—it drinketh...
- file: EPUB/ch006.xhtml; text: Μεταλαμβάνει εὐλογίας ἀπὸ τοῦ Θεοῦ . The earth must be tilled, from its nature and the law of its creation, And therefore Adam was to have tilled and wrought the ground in the garden even before the fall, Gen. 2:15. And this is the princ...
- file: EPUB/ch006.xhtml; text: They are, therefore, no otherwise meet for God but in and through Christ, according to the infinite condescension which he is pleased to exercise in the covenant of grace. Therein doth the Lord Christ, 1. Make our persons accepted, as wa...
- file: EPUB/ch006.xhtml; text: The especial design of the apostle, in this and the following verses, is to declare his good-will towards the Hebrews, his judgment of their state and condition, the reasons and grounds of that judgment, with the proper use and end of th...
- file: EPUB/ch006.xhtml; text: It followeth hence, (1.) That whatever be the state and condition of them unto whom we dispense the word, or whatever we may conceive it to be, we are not, with respect thereunto, to baulk or waive the delivery and pressing of any evange...

## Suspicious Large-Number Starts

- file: EPUB/ch004.xhtml; text: 14. They saw hereby that there was not an ordinary or common work only of grace on these Corinthians, engaging them into a common profession, and the duties of it,—which yet was a matter of great thankfulness unto God; b
- file: EPUB/ch006.xhtml; text: 14. They saw hereby that there was not an ordinary or common work only of grace on these Corinthians, engaging them into a common profession, and the duties of it,—which yet was a matter of great thankfulness unto God; b

## Short Fragments

- file: EPUB/ch003.xhtml; text: Νεκρῶν ἔργων .
- file: EPUB/ch004.xhtml; text: Ἐάνπερ ἐπιτρέπῃ ὁ Θεός .
- file: EPUB/ch004.xhtml; text: Ἅπαξ φωτισθέντες .
- file: EPUB/ch004.xhtml; text: Τῆς δωρεᾶς τῆς ἐπουρανίου .
- file: EPUB/ch004.xhtml; text: Γευσαμένους τε .
- file: EPUB/ch004.xhtml; text: Καλὸν Θεοῦ ῥῆμα .
- file: EPUB/ch004.xhtml; text: Δυνάμεις τε μέλλοντος αἰῶνος . 5.
- file: EPUB/ch004.xhtml; text: Ἀκάνθας καὶ τριβόλους .
- file: EPUB/ch004.xhtml; text: Κατάρας ἐγγύς .
- file: EPUB/ch004.xhtml; text: Ἧς τὸ τέλος εἰς καῦσιν . 3.

## Missing Enumerator Markers

- marker: (1st); pdf: 1; epub: 0; examples: [{'location': 'pdf:p7', 'context': 'f, the place of the glorious presence of God. And this also may be considered two ways:— (1st). With respect unto what he hath already done for us; and two things are included therein: [1st.] That he h...

## Enumerator Sequence Candidates

- file: EPUB/ch010.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) By way of preparation. And this is twofold: [1st.] With respect unto our present gracious entrance into the holiest by faith and prayer. This way was not made for us whilst the ol
- file: EPUB/ch010.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) With respect unto what he hath yet to do for us. Hence it is that he is not said absolutely to enter into his glory, but to enter as a priest, as through a veil, as into the holy
- file: EPUB/ch011.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) By way of preparation. And this is twofold: [1st.] With respect unto our present gracious entrance into the holiest by faith and prayer. This way was not made for us whilst the ol
- file: EPUB/ch011.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) With respect unto what he hath yet to do for us. Hence it is that he is not said absolutely to enter into his glory, but to enter as a priest, as through a veil, as into the holy

## Repeated Windows

- phrase: made an high priest for ever after the order of; count: 10
- phrase: an high priest for ever after the order of melchisedec; count: 10
- phrase: because they were not suffered to continue by reason of; count: 8
- phrase: they were not suffered to continue by reason of death; count: 8
- phrase: of the word unto the souls and consciences of men; count: 6
- phrase: herein is love not that we loved god but that; count: 6
- phrase: is love not that we loved god but that he; count: 6
- phrase: love not that we loved god but that he loved; count: 6
- phrase: not that we loved god but that he loved us; count: 6
- phrase: that we loved god but that he loved us and; count: 6

## Missing Word Samples

- word: καθʼ; pdf: 17; epub: 0
- word: διʼ; pdf: 14; epub: 0
- word: επʼ; pdf: 7; epub: 0
- word: quæ; pdf: 6; epub: 0
- word: vitæ; pdf: 6; epub: 0
- word: æternum; pdf: 6; epub: 0
- word: fœderis; pdf: 6; epub: 0
- word: cæsar; pdf: 5; epub: 0
- word: hæc; pdf: 5; epub: 0
- word: εφʼ; pdf: 5; epub: 0

## Excess Word Samples

- word: priesthood; pdf: 489; epub: 902
- word: love; pdf: 440; epub: 852
- word: priest; pdf: 453; epub: 827
- word: office; pdf: 385; epub: 715
- word: word; pdf: 359; epub: 649
- word: high; pdf: 269; epub: 532
- word: place; pdf: 312; epub: 568
- word: work; pdf: 288; epub: 528
- word: covenant; pdf: 264; epub: 495
- word: melchisedec; pdf: 250; epub: 476

## Missing Latin Word Samples

- word: æternum; pdf: 6; epub: 0
- word: fœderis; pdf: 6; epub: 0
- word: œcumenius; pdf: 3; epub: 0
- word: hæreditario; pdf: 3; epub: 0

## Untagged Latin Word Samples

- word: abraham; epub: 502; tagged: 10
- word: cor; epub: 188; tagged: 0
- word: isa; epub: 161; tagged: 0
- word: levi; epub: 138; tagged: 4
- word: immediate; epub: 81; tagged: 2
- word: poor; epub: 79; tagged: 0
- word: sincere; epub: 67; tagged: 0
- word: mediator; epub: 66; tagged: 0
- word: mere; epub: 64; tagged: 2
- word: elsewhere; epub: 61; tagged: 0

## Missing Latin Clauses

- page: 6; word_count: 6; sample: ut non præcidatur ut non abscindatur
- page: 7; word_count: 4; sample: ubi præcursor pro nobis
- page: 9; word_count: 7; sample: sunt liberorum quatenus jus hæreditatis ad eos
- page: 9; word_count: 6; sample: vis illa hæreditatis de qua diximus
- page: 9; word_count: 8; sample: sed tantum ad tollendas quasdam pœnas temporarias et
- page: 11; word_count: 4; sample: sed fœderis sponsor nominatur
- page: 11; word_count: 7; sample: autem christus pro fœderis divini veritate non
- page: 11; word_count: 5; sample: præstantioris fœderis factus est sacerdos

## Untranslated Latin Samples

- phrase: ideo," "quapropter," "propterea
- phrase: emittamus," or "demittamus
- phrase: initii Christi
- phrase: inchoationis Christi
- phrase: omisso qui in Christo
- phrase: omitto," "missum facio
- phrase: sermo exordii Christi;" "sermo quo instituuntur
- phrase: non rursum," "non iterum
- phrase: terminus a quo
- phrase: as, "Est profecto Deus qui haec

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
