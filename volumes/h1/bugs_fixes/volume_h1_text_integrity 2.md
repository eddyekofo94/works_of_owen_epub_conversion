# Text Integrity Audit: Volume h1

- Status: **WARN**
- Warnings: 7
- PDF pages: 11
- EPUB text files: 37
- EPUB paragraphs/headings: 4365

## Coverage

- PDF content tokens: 238094
- EPUB content tokens: 412563
- Approximate PDF-to-EPUB coverage ratio: 0.9999
- Pages checked: 10
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

- Body paragraphs checked: 4203
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 85
- Short fragments: 174
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 6
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 51
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 372
- EPUB enumerator markers: 630
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 2121
- EPUB Greek words: 2741
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 3554
- EPUB Hebrew words: 6773
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 120
- Missing Greek clauses: 0
- Hebrew clauses checked: 357
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 4593
- EPUB Latin words: 7931
- EPUB Tagged Latin words: 2824
- Latin word coverage ratio: 1.0
- Latin word tagging ratio: 0.3561
- Latin clauses checked: 191
- Missing Latin clauses: 0
- Tagged Latin runs checked: 870
- Translated Latin runs: 60
- Latin translation ratio: 0.069

## Warnings

- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Possible Paragraph Splits

- file: EPUB/ch001.xhtml; previous: EXERCITATIONS ON THE EPISTLE TO THE HEBREWS; next: GENERAL PREFACE
- file: EPUB/ch001.xhtml; previous: GENERAL PREFACE; next: IT has been matter of thankfulness for many generations of the Christian church, that Dr Owen was led to concentrate all his rare endowments and vast resources on the exposition of
- file: EPUB/ch002.xhtml; previous: NOTE IN REGARD TO THE PREFACES; next: IN previous reprints of this work, instead of the prefaces which the author himself had written for the different parts of the work as they issued from the press, one general prefa
- file: EPUB/ch002.xhtml; previous: TO THE RIGHT HONOURABLE; next: SIR WILLIAM MORRICE, KNIGHT,
- file: EPUB/ch002.xhtml; previous: SIR WILLIAM MORRICE, KNIGHT,; next: ONE OF HIS MAJESTY'S MOST HONOURABLE PRIVY COUNCIL, AND PRINCIPAL SECRETARY OF STATE, ETC.
- file: EPUB/ch002.xhtml; previous: SIR,; next: THE dedication of books unto persons of worth and honour hath secured itself from the impeachment of censure, by taking sanctuary in the usage of all times and ages. Herein, theref
- file: EPUB/ch002.xhtml; previous: mstances (needless to be repeated) seems to render an account of the reason of my particular address unto you in this manner necessary. This, therefore, I shall give, but briefly:—; next: " Ne longo sermone morer tua tempora ."
- file: EPUB/ch002.xhtml; previous: irmation of them, is left to the judgment of persons indifferent and unprejudiced; the manner of their handling is submitted unto yours, which is highly and singularly esteemed by,; next: Sir,
- file: EPUB/ch002.xhtml; previous: Sir,; next: Your most humble and obliged servant,
- file: EPUB/ch002.xhtml; previous: Your most humble and obliged servant,; next: John Owen

## Inline Structural Marker Candidates

- file: EPUB/ch006.xhtml; text: 1. CLEMENT of Rome, in the judgment of Erasmus and Patrick Young; 2. TERTULLIAN, according to Sixtus Senensis ; 3. BARNABAS, according to Tertullian, Schmidt, Cameron, Twesten, Ullman, Wieseler; 4. LUKE, according to Origen, S. Crell, Gr...
- file: EPUB/ch009.xhtml; text: 1. That it was written to Gentile Christians; 2. To Jewish believers out of Palestine; 3. To Jewish believers in Palestine; and, 4. To Jewish believers in Palestine, but more especially in Jerusalem or Caesarea.
- file: EPUB/ch022.xhtml; text: 1, 2. Ordinances and institutions of the Jewish church referred to and unfolded in the Epistle to the Hebrews—Principal heads of them mentioned therein. 3. The call of Abraham, Heb. 11:8-19. 4. The name Abram; signification of it—Changed...
- file: EPUB/ch025.xhtml; text: 1, 2. Ordinances and institutions of the Jewish church referred to and unfolded in the Epistle to the Hebrews—Principal heads of them mentioned therein. 3. The call of Abraham, Heb. 11:8-19. 4. The name Abram; signification of it—Changed...
- file: EPUB/ch026.xhtml; text: 1. The priest; 2. The whole congregation jointly; 3. The ruler; 4. Any of the people of the land: so that none were excluded from the privilege and benefit of this sacrifice.
- file: EPUB/ch030.xhtml; text: 1. The priest; 2. The whole congregation jointly; 3. The ruler; 4. Any of the people of the land: so that none were excluded from the privilege and benefit of this sacrifice.

## Suspicious Large-Number Starts

- file: EPUB/ch005.xhtml; text: 14. Not rejected by any of that church; 15. Only not publicly approved—The church of Rome not the sole proposer of books canonical.
- file: EPUB/ch005.xhtml; text: 34. Tradition concerning the authority of this Epistle—Not justly liable to any exceptions— 35. From the author; 36. Circumstances; 37. Subject-matter; 38. Style. 39. Testimonies. 40. Conclusion.
- file: EPUB/ch005.xhtml; text: 96. These quotations are numerous, and are arranged by Moses Stuart into four classes, according to the degree of their correspondence with the original Epistle from which they were taken. They prove more than the existe
- file: EPUB/ch005.xhtml; text: 96. Clement, in the 36th chapter of his epistle, introduces a quotation from Scripture under the common formula that bespeaks an appeal to divine authority: Γέγραπται γὰρ οὕτως · Ὁποιῶν τοὺς ἀγγέλους αὑτοῦ πνεύματα , καὶ
- file: EPUB/ch007.xhtml; text: 23. And it seems likewise to be written before the martyrdom of James at Jerusalem, in that he affirms that the church of the Hebrews had "not yet resisted unto blood," chap. 12:4; it being very probable that together wi
- file: EPUB/ch007.xhtml; text: 61. The most recent authority, Dr Davidson, remarks, "If the letter was written by Paul, it could only have proceeded from him during the first two years of his imprisonment noticed at the close of the Acts. It preceded
- file: EPUB/ch008.xhtml; text: 14. Eusebius says, "Paul wrote to the Hebrews in his vernacular language, and, according to report, either Luke or Clement" (i.e., of Rome) "translated it," Euseb. iii.
- file: EPUB/ch008.xhtml; text: 38. Jerome remarks, "He had written as a Hebrew to Hebrews, in the Hebrew tongue," and "this Epistle was translated into Greek; so that the colouring of the style was made different in this way from that of Paul's." The
- file: EPUB/ch009.xhtml; text: 14. Εὐλογῶν εὐλογήσω σε , καὶ πληθύνων πληθυνῶ σε ·—"Blessing I will bless thee, and multiplying I will multiply thee." From Gen. 22:17. The LXX., Πληθυνῶ τὸ σπέρμα σου ,—"I will multiply thy seed."
- file: EPUB/ch009.xhtml; text: 20. Τοῦτο τὸ αἷμα τῆς διαθήκης , ἧς ἐνετείλατο πρὸς ὑμᾶς ὁ Θεός ·—"This is the blood of the covenant which God hath enjoined unto you." From Exod. 24:8. The sense of the Hebrew text is alluded unto, not the words absolut

## Roman Heading Candidates

- file: EPUB/ch006.xhtml; text: II. Some ascribe it directly and exclusively to Paul;

## Short Fragments

- file: EPUB/ch001.xhtml; text: GENERAL PREFACE
- file: EPUB/ch001.xhtml; text: EDINBURGH, March 1854
- file: EPUB/ch002.xhtml; text: NOTE IN REGARD TO THE PREFACES
- file: EPUB/ch002.xhtml; text: TO THE RIGHT HONOURABLE
- file: EPUB/ch002.xhtml; text: SIR WILLIAM MORRICE, KNIGHT,
- file: EPUB/ch002.xhtml; text: SIR,
- file: EPUB/ch002.xhtml; text: Sir,
- file: EPUB/ch002.xhtml; text: John Owen
- file: EPUB/ch002.xhtml; text: March 20, 1667.
- file: EPUB/ch003.xhtml; text: I.—TO THE CHRISTIAN READER

## Repeated Windows

- phrase: the mighty god the everlasting father the prince of peace; count: 8
- phrase: and mount sinai was altogether on smoke because the lord; count: 6
- phrase: mount sinai was altogether on smoke because the lord descended; count: 6
- phrase: sinai was altogether on smoke because the lord descended upon; count: 6
- phrase: was altogether on smoke because the lord descended upon it; count: 6
- phrase: altogether on smoke because the lord descended upon it in; count: 6
- phrase: on smoke because the lord descended upon it in fire; count: 6
- phrase: smoke because the lord descended upon it in fire and; count: 6
- phrase: because the lord descended upon it in fire and the; count: 6
- phrase: brightness of his glory and the express image of his; count: 6

## Missing Word Samples

- word: κατʼ; pdf: 10; epub: 0
- word: παρʼ; pdf: 3; epub: 0
- word: επʼ; pdf: 3; epub: 0

## Excess Word Samples

- word: him; pdf: 1177; epub: 2143
- word: messiah; pdf: 919; epub: 1789
- word: first; pdf: 686; epub: 1246
- word: jews; pdf: 630; epub: 1146
- word: time; pdf: 489; epub: 901
- word: people; pdf: 413; epub: 797
- word: place; pdf: 429; epub: 796
- word: world; pdf: 386; epub: 719
- word: man; pdf: 351; epub: 646
- word: come; pdf: 333; epub: 626

## Untagged Latin Word Samples

- word: abraham; epub: 365; tagged: 2
- word: targum; epub: 200; tagged: 2
- word: isa; epub: 197; tagged: 2
- word: num; epub: 188; tagged: 8
- word: cyrus; epub: 146; tagged: 4
- word: adam; epub: 139; tagged: 4
- word: elsewhere; epub: 106; tagged: 5
- word: kimchi; epub: 96; tagged: 4
- word: sinai; epub: 83; tagged: 0
- word: poor; epub: 71; tagged: 2

## Untranslated Latin Samples

- phrase: Egregium est opus hoc
- phrase: testis de auctoris singulari
- phrase: atque industria quam ad illud conficiendum
- phrase: Ne longo
- phrase: tua tempora
- phrase: as de facto
- phrase: as Enjedinus, Socinus, ‡ Smalcius, ‡ Crellius
- phrase: Pascitur in vivis livor, post fata
- phrase: Crellius, Grotius
- phrase: is genitivus adjuncti

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
