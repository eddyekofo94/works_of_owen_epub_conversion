# Text Integrity Audit: Volume h4

- Status: **WARN**
- Warnings: 8
- PDF pages: 13
- EPUB text files: 39
- EPUB paragraphs/headings: 4622

## Coverage

- PDF content tokens: 257295
- EPUB content tokens: 474915
- Approximate PDF-to-EPUB coverage ratio: 0.9996
- Pages checked: 12
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

- Body paragraphs checked: 4487
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 503
- Short fragments: 76
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 16
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 711
- EPUB enumerator markers: 1293
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 3

## Greek / Hebrew

- PDF Greek words: 4466
- EPUB Greek words: 8476
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 767
- EPUB Hebrew words: 1277
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 223
- Missing Greek clauses: 0
- Hebrew clauses checked: 86
- Missing Hebrew clauses: 1

## Latin

- PDF Latin words: 3077
- EPUB Latin words: 5805
- EPUB Tagged Latin words: 2413
- Latin word coverage ratio: 0.9925
- Latin word tagging ratio: 0.4157
- Latin clauses checked: 162
- Missing Latin clauses: 4
- Tagged Latin runs checked: 792
- Translated Latin runs: 65
- Latin translation ratio: 0.0821

## Warnings

- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_hebrew_clauses`: Some dense Hebrew passages from the PDF are missing from the EPUB
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Possible Paragraph Splits

- file: EPUB/ch001.xhtml; previous: men of one age: Eccles. 1:4, "One generation passeth away, and another generation cometh,"—that is, the men of one age. See Deut. 32:7. So is γενεή , as in Homer's Iliad, vi. 146:—; next: Οἵη περ θύλλων γενεὴ , τοιήδε καὶ ἀνδρῶν .
- file: EPUB/ch001.xhtml; previous: oice of God, if you will choose so to do, take heed of that which would certainly be a hinderance thereof.' Thus dealeth the apostle with the Hebrews; and herein teacheth us that,—; next: Obs. V. The formal reason of all our obedience consists in its relation to the voice or authority of God.
- file: EPUB/ch001.xhtml; previous: whereon they invited unto a feast all the priests that ministered. But most frequently they so express a present opportunity or season. So the Greeks use σήμερον , as in Anacreon,—; next: Σήμερον μέλει μοι · τὸ δὲ αὔριον τίς οἷδε ;—
- file: EPUB/ch001.xhtml; previous: Σήμερον μέλει μοι · τὸ δὲ αὔριον τίς οἷδε ;—; next: "My care is for to-day" (the present season); "who knows to-morrow" (or the time to come)?
- file: EPUB/ch001.xhtml; previous: fall out). "Sufficient unto the day" (the present time and season) "is the evil thereof." To the same purpose do they use "hodie" in the Latin tongue, as in these common sayings,—; next: " Sera nimis vita est crastina , viv' hodie:"
- file: EPUB/ch001.xhtml; previous: And,—; next: " Qui non est hodie, cras minus aptus erit;" with many other sayings of the like importance. This, then, is the sense and meaning of the word absolutely considered. The apostle exh
- file: EPUB/ch001.xhtml; previous: another observation which the words opened will afford unto us, arising from the season, which the apostle presseth upon their consideration in that word "to-day." And it is that,—; next: Obs. XI. Especial seasons of grace for obedience are in an especial manner to be observed and improved.
- file: EPUB/ch001.xhtml; previous: int conspiracy as it were of all the persons of that age. These are they who were guilty of the sin here reported. And we may observe from this expression and remembrance of them,—; next: Obs. XII. That the examples of our forefathers are of use and concernment unto us, and objects of our deepest consideration.
- file: EPUB/ch001.xhtml; previous: sins, so that at least they are prevalent in them. Hence the apostle chargeth national sins on the Cretians, from the testimony of Epimenides, who had observed them amongst them;—; next: Κρῆτες ἀεὶ ψεῦσται , κακὰ θήρια , γάστερες ἀργαί ,
- file: EPUB/ch001.xhtml; previous: Κρῆτες ἀεὶ ψεῦσται , κακὰ θήρια , γάστερες ἀργαί ,; next: Tit. 1:12, "The Cretians are alway liars, evil beasts, slow bellies." Lying, dissimulation, cruelty, and sloth, were the sins of that nation from one generation to another, childre

## Inline Structural Marker Candidates

- file: EPUB/ch002.xhtml; text: 1. What from the nature of the things themselves, which are suited unto the various states, conditions, and apprehensions of the minds of men; 2. What from the manner of their expression, on which a character of divine wisdom is impresse...
- file: EPUB/ch003.xhtml; text: 1. What from the nature of the things themselves, which are suited unto the various states, conditions, and apprehensions of the minds of men; 2. What from the manner of their expression, on which a character of divine wisdom is impresse...
- file: EPUB/ch005.xhtml; text: 1. That those that preach it are sent of God; 2. That what is preached be according to the analogy of faith; 3. That it be drawn from the written word; 4. That it be delivered in the name and authority of God.
- file: EPUB/ch010.xhtml; text: 1. That those that preach it are sent of God; 2. That what is preached be according to the analogy of faith; 3. That it be drawn from the written word; 4. That it be delivered in the name and authority of God.
- file: EPUB/ch014.xhtml; text: To complete our profession, yea, to constitute our ὁμολογία , there is required that we make a solemn declaration of our subjection unto the gospel in these things. And this is made two ways. (1.) By works. (2.) By words.
- file: EPUB/ch017.xhtml; text: To complete our profession, yea, to constitute our ὁμολογία , there is required that we make a solemn declaration of our subjection unto the gospel in these things. And this is made two ways. (1.) By works. (2.) By words.
- file: EPUB/ch017.xhtml; text: Ἔχομεν ἀρχιερέα . "We have an high priest." The apostle introduceth this for another purpose. Yet withal he lets the Hebrews know that in the gospel state there is no loss of privilege in any thing as to what the church enjoyed under the...
- file: EPUB/ch018.xhtml; text: Ἔχομεν ἀρχιερέα . "We have an high priest." The apostle introduceth this for another purpose. Yet withal he lets the Hebrews know that in the gospel state there is no loss of privilege in any thing as to what the church enjoyed under the...
- file: EPUB/ch019.xhtml; text: 1. Frequency in offending; 2. Greatness of offences; 3. Instability in promises and engagements. These are things apt to give provocations beyond what ordinary moderation and meekness can bear withal, especially where they are accompanie...
- file: EPUB/ch022.xhtml; text: 1. Frequency in offending; 2. Greatness of offences; 3. Instability in promises and engagements. These are things apt to give provocations beyond what ordinary moderation and meekness can bear withal, especially where they are accompanie...

## Short Fragments

- file: EPUB/ch001.xhtml; text: And,—
- file: EPUB/ch001.xhtml; text: Sub Jove semper eris ."
- file: EPUB/ch001.xhtml; text: Ἀπὸ Θεοῦ ζῶντος .
- file: EPUB/ch001.xhtml; text: Ἁμαρτίας .
- file: EPUB/ch001.xhtml; text: Σκληρυνθῇ .
- file: EPUB/ch002.xhtml; text: Ἀπὸ Θεοῦ ζῶντος .
- file: EPUB/ch002.xhtml; text: Ἁμαρτίας .
- file: EPUB/ch002.xhtml; text: Σκληρυνθῇ .
- file: EPUB/ch002.xhtml; text: Κῶλα .
- file: EPUB/ch002.xhtml; text: Membra natant."

## Enumerator Sequence Candidates

- file: EPUB/ch001.xhtml; marker: (2.); family: paren_decimal; context: (2.) They are said also to have tempted God: "In the temptation; when your fathers tempted me." Wherein their provocation did consist, and what was the sin which is so expressed, we ha
- file: EPUB/ch001.xhtml; marker: [2.]; family: bracket_decimal; context: [2.] The next thing in the words is that especial evil which the apostle cautions the Hebrews against, as that which a heart made evil by the prevalency of unbelief would tend unto, an
- file: EPUB/ch002.xhtml; marker: [2.]; family: bracket_decimal; context: [2.] The next thing in the words is that especial evil which the apostle cautions the Hebrews against, as that which a heart made evil by the prevalency of unbelief would tend unto, an

## Repeated Windows

- phrase: if ye will hear his voice harden not your hearts; count: 11
- phrase: it is said to-day if ye will hear his voice; count: 10
- phrase: any of you should seem to come short of it; count: 10
- phrase: although the works were finished from the foundation of the; count: 10
- phrase: the works were finished from the foundation of the world; count: 10
- phrase: to-day if ye will hear his voice harden not your; count: 9
- phrase: thought it not robbery to be equal with god but; count: 8
- phrase: became obedient unto death even the death of the cross; count: 8
- phrase: unto us was the gospel preached even as unto them; count: 8
- phrase: not as the word of men but as it is; count: 8

## Missing Word Samples

- word: quæ; pdf: 9; epub: 0
- word: αλλʼ; pdf: 9; epub: 0
- word: καθʼ; pdf: 7; epub: 0
- word: αφʼ; pdf: 6; epub: 0
- word: œcumenius; pdf: 5; epub: 0
- word: κατʼ; pdf: 4; epub: 0
- word: substantiæ; pdf: 3; epub: 0
- word: διʼ; pdf: 3; epub: 0
- word: nostræ; pdf: 3; epub: 0
- word: æternæ; pdf: 3; epub: 0

## Excess Word Samples

- word: the; pdf: 19920; epub: 36577
- word: of; pdf: 15212; epub: 28027
- word: and; pdf: 12409; epub: 22921
- word: in; pdf: 7828; epub: 14337
- word: is; pdf: 6528; epub: 12110
- word: to; pdf: 6353; epub: 11717
- word: it; pdf: 4944; epub: 9128
- word: he; pdf: 3239; epub: 6112
- word: as; pdf: 3085; epub: 5698
- word: his; pdf: 3101; epub: 5700

## Missing Hebrew Clauses

- page: 2; word_count: 3; sample: כְּקֹלוֹ קוֹל יְהוֹהָ

## Missing Latin Word Samples

- word: œcumenius; pdf: 5; epub: 0

## Untagged Latin Word Samples

- word: cor; epub: 254; tagged: 10
- word: isa; epub: 194; tagged: 2
- word: elsewhere; epub: 115; tagged: 0
- word: abraham; epub: 103; tagged: 0
- word: immediate; epub: 91; tagged: 0
- word: mere; epub: 88; tagged: 0
- word: terror; epub: 78; tagged: 0
- word: iii; epub: 68; tagged: 0
- word: num; epub: 67; tagged: 2
- word: poor; epub: 58; tagged: 2

## Missing Latin Clauses

- page: 13; word_count: 4; sample: in cœlo et terra
- page: 13; word_count: 4; sample: cœlestis a deo constitutus
- page: 13; word_count: 4; sample: nam et pœnas peccatorum
- page: 13; word_count: 9; sample: et vitam æternam largitur spiritus nostros in manus suas

## Untranslated Latin Samples

- phrase: ut ad iram eum provocetis tanquam
- phrase: offensus fui," "incensus fui
- phrase: exsecratus sum
- phrase: filia vocis
- phrase: curvicervicum pecus
- phrase: exacerbo," "provoco
- phrase: exacerbatio," "provocatio
- phrase: etsi," "etiamsi
- phrase: mihi generatio ista
- phrase: me." "Pertuli eam, sed non sine taedio

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
