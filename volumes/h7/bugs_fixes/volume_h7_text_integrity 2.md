# Text Integrity Audit: Volume h7

- Status: **WARN**
- Warnings: 8
- PDF pages: 11
- EPUB text files: 65
- EPUB paragraphs/headings: 6533

## Coverage

- PDF content tokens: 195683
- EPUB content tokens: 364227
- Approximate PDF-to-EPUB coverage ratio: 0.9998
- Pages checked: 10
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

- Body paragraphs checked: 6323
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 155
- Short fragments: 379
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 40
- Reference continuation splits: 2
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 1214
- EPUB enumerator markers: 2246
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 4

## Greek / Hebrew

- PDF Greek words: 3856
- EPUB Greek words: 7119
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 343
- EPUB Hebrew words: 609
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 155
- Missing Greek clauses: 0
- Hebrew clauses checked: 44
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 2125
- EPUB Latin words: 3898
- EPUB Tagged Latin words: 836
- Latin word coverage ratio: 1.0
- Latin word tagging ratio: 0.2145
- Latin clauses checked: 41
- Missing Latin clauses: 0
- Tagged Latin runs checked: 324
- Translated Latin runs: 29
- Latin translation ratio: 0.0895

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `reference_continuation_splits`: Some scripture or chapter references are split across paragraph boundaries
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Possible Paragraph Splits

- file: EPUB/ch002.xhtml; previous: In these ways, and by these means, "faith is the substance of things hoped for;" and,—; next: Obs. I. No faith will carry us through the difficulties of our profession, from oppositions within and without, giving us constancy and perseverance therein unto the end, but that
- file: EPUB/ch002.xhtml; previous: hat it makes a life on things invisible. It is not only conversant about them, but mixeth itself with them, making them the spiritual nourishment of the soul, 2 Cor. 4:16-18. And,—; next: Obs. III. The glory of our religion is, that it depends on, and is resolved into invisible things. They are far more excellent and glorious than any thing that sense can behold or
- file: EPUB/ch002.xhtml; previous: sion under trouble and persecution; with a discovery of the nature and end of the ensuing instances, with their suitableness unto his purpose. And we may observe in general, that,—; next: Obs. V. It is faith alone that takes believers out of this world whilst they are in it, that exalts them above it whilst they are under its rage; that enables them to live upon thi
- file: EPUB/ch003.xhtml; previous: ony is assigned to faith alone; as for other reasons, so because all those other things were fruits of their faith, whose acceptance with God depended thereon. And we may observe,—; next: Obs. III. It is faith alone which from the beginning of the world (or from the giving of the first promise) was the means and way of obtaining acceptance with God.—There hath been
- file: EPUB/ch004.xhtml; previous: ne; and some assigned such a beginning unto it, as it had been better it never had any. Nothing but an assent unto divine revelation can give us a clear understanding hereof. And,—; next: Obs. II. Then doth faith put forth its power in our minds in a due manner, when it gives us clear and distinct apprehensions of the things we do believe. Faith that gives not under
- file: EPUB/ch004.xhtml; previous: ished," perfected, completely framed. Being originally, as unto the matter of them, created out of nothing, in the six days' work they were completely finished and perfected. And,—; next: Obs. III. As God's first work was, so all his works shall be perfect.—He undertakes nothing but what he will finish and complete in beauty and order. And not only the original prod
- file: EPUB/ch004.xhtml; previous: , that is, ὥστε , "so that." 'By faith alone we understand that the worlds were made; namely, "so as that the things which are seen were not made of things which do appear." And,—; next: Obs. IV. The aids of reason, with the due consideration of the nature, use, and end of all things, ought to be admitted of, to confirm our minds in the persuasion of the original c
- file: EPUB/ch005.xhtml; previous: at, it may be, gathered "raptim,"—without choice or judgment of what was most meet to be offered unto God. And it is for ever dedicated as a rule for the church in all ages, that,—; next: Obs. II. We are to serve God with the best that we have, the best that is in our power, with the best of our spiritual abilities; which God afterwards fully confirmed.
- file: EPUB/ch005.xhtml; previous: ypocritically, he did it not in a mere attendance unto the outward duty; but it was kindled in his own heart by the Holy Spirit, before it was fired on the altar from heaven. For,—; next: Obs. III. God gives no consequential approbation of any duties of believers, but where the principle of a living faith goes previously in their performance.
- file: EPUB/ch005.xhtml; previous: 4. As to the consequences of Abel's faith,—; next: The first consequent of this efficacy of faith in Abel is, that "he obtained witness that he was righteous."

## Inline Structural Marker Candidates

- file: EPUB/ch006.xhtml; text: Of this Enoch it is affirmed, 1. That he was "translated;" 2. The end of that translation is declared, "that he should not see death;" 3. The consequent of it, "he was not found;" 4. The efficient cause of that translation, and the reaso...
- file: EPUB/ch006.xhtml; text: In the field of conjectures used on this occasion, I judge it probable, (1.) That his rapture was visible, in the sight of many that feared God, who were to be witnesses of it unto the world, that it might be his ordinance for the convic...
- file: EPUB/ch008.xhtml; text: There is in the words, 1. The person spoken of or instanced in; which is Noah.
- file: EPUB/ch008.xhtml; text: Δι ʼ ἧς . (2.) Lastly, There is a double consequent of this faith of Noah and his obedience therein; [1.] With respect unto the world, "he condemned it;" [2.] With respect unto himself, he "became heir of the righteousness which is by fa...
- file: EPUB/ch011.xhtml; text: There is in the words, 1. A supposition that these pilgrims had originally a country of their own whereunto they did belong.
- file: EPUB/ch011.xhtml; text: This preparation, therefore, of a city denotes, (1.) An eternal act of the will and wisdom of God, in designing heaven and glory unto the elect.
- file: EPUB/ch011.xhtml; text: What was the faith of Abraham in particular, how his thoughts wrought in him, is not expressed in the original story: yet are two things plain therein; [1.] That he was not cast into any distraction of mind, any disorderly passions, comp...
- file: EPUB/ch011.xhtml; text: Obs. V. We may also consider, that, 1. If we are children of Abraham, we have no reason to expect an exemption from the greatest trials, that the same faith which was in him is able to conflict withal.
- file: EPUB/ch016.xhtml; text: There is in the words, 1. A supposition that these pilgrims had originally a country of their own whereunto they did belong.
- file: EPUB/ch017.xhtml; text: This preparation, therefore, of a city denotes, (1.) An eternal act of the will and wisdom of God, in designing heaven and glory unto the elect.

## Reference Continuation Splits

- file: EPUB/ch034.xhtml; previous: All this he "patiently endured," as the sense of the word was declared on the foregoing verse.; next: 4.
- file: EPUB/ch036.xhtml; previous: All this he "patiently endured," as the sense of the word was declared on the foregoing verse.; next: 4.

## Short Fragments

- file: EPUB/ch002.xhtml; text: Πίστις .
- file: EPUB/ch002.xhtml; text: Ἐλπιζομένων .
- file: EPUB/ch002.xhtml; text: Οὐ βλεπομένων .
- file: EPUB/ch003.xhtml; text: Οἱ πρεσβύτεροι .
- file: EPUB/ch003.xhtml; text: Ἐμαρτυρήθησαν .
- file: EPUB/ch004.xhtml; text: Κατηρτίσθαι .
- file: EPUB/ch004.xhtml; text: Ῥήματι Θεοῦ .
- file: EPUB/ch004.xhtml; text: Τὰ βλεπόμενα .
- file: EPUB/ch004.xhtml; text: Εἰς τὸ μὴ γεγονέναι .
- file: EPUB/ch006.xhtml; text: Τοῦ μὴ ἰδεῖν θάνατον .

## Enumerator Sequence Candidates

- file: EPUB/ch027.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) It hath this advantage, because it hath a remaining interest in all the faculties of our souls. It is not in us as a disease that attempts and weakens one single part of the body,
- file: EPUB/ch027.xhtml; marker: (2dly.); family: paren_ordinal; context: olute perfection in this life. This we are always to aim at, and pray for, 1 Thess. 5:23. (2dly.) We ought actually to lay it aside in such a measure and degree, as that it may not be a prevalent hinderance unto us in any of the duties o...
- file: EPUB/ch034.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) It hath this advantage, because it hath a remaining interest in all the faculties of our souls. It is not in us as a disease that attempts and weakens one single part of the body,
- file: EPUB/ch034.xhtml; marker: (2dly.); family: paren_ordinal; context: olute perfection in this life. This we are always to aim at, and pray for, 1 Thess. 5:23. (2dly.) We ought actually to lay it aside in such a measure and degree, as that it may not be a prevalent hinderance unto us in any of the duties o...

## Repeated Windows

- phrase: run with patience the race that is set before us; count: 7
- phrase: seed all the nations of the earth should be blessed; count: 6
- phrase: made mention of the departing of the children of israel; count: 6
- phrase: the two states of the law and the gospel with; count: 6
- phrase: every weight and the sin that doth so easily beset; count: 6
- phrase: weight and the sin that doth so easily beset us; count: 6
- phrase: entreated that the word should not be spoken to them; count: 6
- phrase: that the word should not be spoken to them any; count: 6
- phrase: the word should not be spoken to them any more; count: 6
- phrase: that which is well-pleasing in his sight through jesus christ; count: 6

## Missing Word Samples

- word: διʼ; pdf: 9; epub: 0
- word: τουτʼ; pdf: 4; epub: 0
- word: αφʼ; pdf: 3; epub: 0
- word: απʼ; pdf: 3; epub: 0
- word: ουδʼ; pdf: 3; epub: 0

## Excess Word Samples

- word: the; pdf: 16495; epub: 30767
- word: of; pdf: 11999; epub: 22292
- word: and; pdf: 8355; epub: 15524
- word: in; pdf: 6222; epub: 11580
- word: is; pdf: 5078; epub: 9415
- word: it; pdf: 4126; epub: 7636
- word: to; pdf: 3825; epub: 7138
- word: as; pdf: 2424; epub: 4458
- word: for; pdf: 2037; epub: 3814
- word: be; pdf: 1987; epub: 3752

## Untagged Latin Word Samples

- word: abraham; epub: 406; tagged: 2
- word: cor; epub: 175; tagged: 0
- word: iii; epub: 122; tagged: 0
- word: isa; epub: 104; tagged: 2
- word: terror; epub: 88; tagged: 0
- word: immediate; epub: 82; tagged: 2
- word: poor; epub: 77; tagged: 0
- word: vii; epub: 71; tagged: 0
- word: undergo; epub: 70; tagged: 0
- word: sinai; epub: 68; tagged: 4

## Untranslated Latin Samples

- phrase: sperandarum substantia rerum
- phrase: is, "quae sperantur
- phrase: Beza, ‡ "illud quo
- phrase: argumentum illud quod
- phrase: Illud ex quo
- phrase: testimonium consequuti," "adepti;" "testimonio ornati
- phrase: aedificata, constructa, ornata, praeparata, creata, condita
- phrase: secula," "seculum," "mundum
- phrase: ut ex invisibilibus visibilia
- phrase: quae cernimus," "quae cernuntur

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
