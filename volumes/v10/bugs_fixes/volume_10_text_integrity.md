# Text Integrity Audit: Volume 10

- Status: **WARN**
- Warnings: 7
- PDF pages: 828
- EPUB text files: 105
- EPUB paragraphs/headings: 3299

## Coverage

- PDF content tokens: 262672
- EPUB content tokens: 263166
- Approximate PDF-to-EPUB coverage ratio: 0.9984
- Pages checked: 807
- Weak page matches: 5
- Dense source windows checked: 35125
- Missing dense source-window pages: 1
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 776
- Top-of-page windows skipped as unstable: 7
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 704
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 2696
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 189
- Short fragments: 33
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 5
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 185
- EPUB enumerator markers: 196
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 822
- EPUB Greek words: 845
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 18
- EPUB Hebrew words: 18
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 40
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 1417
- EPUB Latin words: 1412
- EPUB Tagged Latin words: 843
- Latin word coverage ratio: 0.9915
- Latin word tagging ratio: 0.597
- Latin clauses checked: 95
- Missing Latin clauses: 1
- Tagged Latin runs checked: 270
- Translated Latin runs: 156
- Latin translation ratio: 0.5778

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 21; sample: differences we all at this day grieve to behold tantum religio potuit suadere malorum

## Inline Structural Marker Candidates

- file: EPUB/ch020.xhtml; text: In 1650, Mr. Home, minister at Lynn in Norfolk, a man, according to Palmer (Nonconf. Mem., 3. pp. 6, 7), "of exemplary and primitive piety," and author of several works, published a reply to Owen's work, under the title, "The Open Door f...

## Suspicious Large-Number Starts

- file: EPUB/ch013.xhtml; text: 36. To abide argueth a continued, uninterrupted act.
- file: EPUB/ch014.xhtml; text: 96. All which assertions, how contrary they are to the express word of God, I shall now demonstrate.
- file: EPUB/ch058.xhtml; text: 13. [A.D. 350]: —
- file: EPUB/ch084.xhtml; text: 117. And again, Aristotle says, "It is a very strong proof, if all shall agree in what we shall say." And in that observation another author concurs: "The things that are commonly agreed on are worthy of credit." And her
- file: EPUB/ch085.xhtml; text: 389 It remains, then, that we should now consider, in the third place, what testimony God has given, and is still giving, to this essential attribute of his in the works of providence. This Paul takes notice of, Romans 1

## Roman Heading Candidates

- file: EPUB/ch058.xhtml; text: V. CYRIL of Jerusalem, Cataches.

## Short Fragments

- file: EPUB/ch002.xhtml; text: JOHN WHITE
- file: EPUB/ch004.xhtml; text: TO THE CHRISTIAN READER.
- file: EPUB/ch018.xhtml; text: Τῷ Θεῷ ἀριστομεγίστῳ δόξα .
- file: EPUB/ch021.xhtml; text: 1 . Of the work;
- file: EPUB/ch022.xhtml; text: TO THE READER.
- file: EPUB/ch022.xhtml; text: READER,
- file: EPUB/ch027.xhtml; text: Whence he saith,
- file: EPUB/ch030.xhtml; text: VI.
- file: EPUB/ch048.xhtml; text: Arg. 15.
- file: EPUB/ch053.xhtml; text: Where, —

## Repeated Windows

- phrase: that we might be made the righteousness of god in; count: 13
- phrase: we might be made the righteousness of god in him; count: 13
- phrase: made him to be sin for us who knew no; count: 8
- phrase: him to be sin for us who knew no sin; count: 8
- phrase: hath set forth to be propitiation through faith in his; count: 7
- phrase: set forth to be propitiation through faith in his blood; count: 7
- phrase: propitiation through faith in his blood to declare his righteousness; count: 7
- phrase: to be sin for us who knew no sin that; count: 7
- phrase: known unto god are all his works from the beginning; count: 6
- phrase: even so father for so it seemed good in thy; count: 6

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 11; epub: 20
- word: historical; pdf: 2; epub: 10
- word: modern; pdf: 5; epub: 12
- word: chapters; pdf: 5; epub: 12
- word: footnotes; pdf: 0; epub: 7
- word: hebrew; pdf: 3; epub: 9
- word: edition; pdf: 2; epub: 8

## Untagged Latin Word Samples

- word: ejusdem; epub: 17; tagged: 0
- word: tantidem; epub: 12; tagged: 0
- word: mediate; epub: 3; tagged: 0
- word: apella; epub: 4; tagged: 1
- word: clamor; epub: 3; tagged: 0
- word: rumor; epub: 3; tagged: 0
- word: expiate; epub: 3; tagged: 0
- word: diatriba; epub: 3; tagged: 0
- word: suetonius; epub: 3; tagged: 0
- word: scotus; epub: 4; tagged: 1

## Missing Latin Clauses

- page: 170; word_count: 5; sample: salus electorum sanguis jesu or

## Untranslated Latin Samples

- phrase: Junius, ‡ Arminius
- phrase: traharis; Per tamen adversi gradieris cornua Tauri
- phrase: ora Leonis
- phrase: tam astutum esse
- phrase: materiam vestris, qui scribitis, sequam Viribus; et versate diu, quid
- phrase: Judaeus Apella
- phrase: pro mundo contento
- phrase: ultimate, or intermediate
- phrase: finis convertuntur
- phrase: copia verborum

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
