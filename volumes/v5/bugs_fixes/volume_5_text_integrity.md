# Text Integrity Audit: Volume 5

- Status: **WARN**
- Warnings: 13
- PDF pages: 576
- EPUB text files: 39
- EPUB paragraphs/headings: 2135

## Coverage

- PDF content tokens: 197342
- EPUB content tokens: 194158
- Approximate PDF-to-EPUB coverage ratio: 0.9808
- Pages checked: 571
- Weak page matches: 9
- Dense source windows checked: 26722
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 6
- Top-of-page body windows checked: 561
- Top-of-page windows skipped as unstable: 24
- Missing top-of-page body windows: 8
- Bottom-of-page body windows checked: 527
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 10

## Paragraphs

- Body paragraphs checked: 1842
- Possible faulty paragraph splits: 3
- Structural starts excluded from split warnings: 227
- Short fragments: 25
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 4
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 2
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 436
- EPUB enumerator markers: 444
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 1161
- EPUB Greek words: 1158
- Greek word coverage ratio: 0.9965
- PDF Hebrew words: 124
- EPUB Hebrew words: 123
- Hebrew word coverage ratio: 0.9919
- Greek clauses checked: 49
- Missing Greek clauses: 0
- Hebrew clauses checked: 14
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 5337
- EPUB Latin words: 5314
- EPUB Tagged Latin words: 3261
- Latin word coverage ratio: 0.9895
- Latin word tagging ratio: 0.6137
- Latin clauses checked: 345
- Missing Latin clauses: 1
- Tagged Latin runs checked: 637
- Translated Latin runs: 409
- Latin translation ratio: 0.6421

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: contents the doctrine of justification general considerations first the general nature of justification state
- page: 4; sample: acceptable unto many reasons of it two parts of corrupted nature's repugnancy unto the
- page: 5; sample: sinners by christ with its acquiescency therein the description given explained and confirmed from
- page: 6; sample: juridical scheme and of forensic title the parts and progress of it inferences from
- page: 7; sample: day that judgment being according unto works answered and the impertinency of it declared
- page: 8; sample: chapter arguments for justification by the imputation of the righteousness of christ our own
- page: 9; sample: romans l2-21 boasting excluded in ourselves asserted in god the design and sum of
- page: 10; sample: the exception removed righteousness before conversion not intended by the apostle chapter objections against
- page: 11; sample: counted unto him for righteousness when he offered his son on the altar works
- page: 15; sample: charles wolsley baronet of some reputation who had been member of cromwell's council of

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.0; sample: contents the doctrine of justification general considerations first the general nature of justification state of the person to be justified antecedently thereunto romans galatians john galatians the sole
- page: 4; hit_ratio: 0.0; sample: acceptable unto many reasons of it two parts of corrupted nature's repugnancy unto the mystery of the gospel that which would reduce it unto the private reason of
- page: 5; hit_ratio: 0.0; sample: sinners by christ with its acquiescency therein the description given explained and confirmed from the nature of the gospel exemplified in its contrary or the nature of unbelief
- page: 6; hit_ratio: 0.0; sample: juridical scheme and of forensic title the parts and progress of it inferences from the whole chapter distinction of first and second justification the whole doctrine of the
- page: 7; hit_ratio: 0.0; sample: day that judgment being according unto works answered and the impertinency of it declared chapter imputation and the nature of it the first express record of justification determines
- page: 8; hit_ratio: 0.25; sample: chapter arguments for justification by the imputation of the righteousness of christ our own personal righteousness not that on the account whereof we are justified in the sight

## Missing Top-Of-Page Body Windows

- page: 4; sample: acceptable unto many — Reasons of it — Two parts of corrupted nature's repugnancy unto the mystery of the gospel: — 1. That which would reduce it unto the private reason
- page: 5; sample: sinners by Christ, with its acquiescency therein — The description given, explained and confirmed: — 1. From the nature of the gospel — Exemplified in its contrary, or the
- page: 6; sample: juridical scheme, and of a forensic title — The parts and progress of it — Inferences from the whole
- page: 7; sample: day, that judgment being according unto works, answered; and the impertinency of it declared
- page: 9; sample: Romans 5:l2-21 — Boasting excluded in ourselves, asserted in God — The design and sum of the apostle's argument — Objection of Socinus removed —
- page: 10; sample: The exception removed — Righteousness before conversion, not intended by the apostle
- page: 31; sample: compliance wherewithal. So Pighius himself complained of them, Controv. 2,
- page: 126; sample: verse 47, "He that be1ieveth on me has everlasting life;" chapter 7:38,

## Missing Bottom-Of-Page Body Windows

- page: 3; sample: of the gospel esteemed folly — Reason, as corrupted, repugnant unto the mystery of grace — Accommodation of spiritual mysteries unto corrupt reason, wherefore
- page: 4; sample: The nature of justifying faith in particular, or of faith in the exercise of it, whereby we are justified — The heart's approbation of the way of the justification and salvation of
- page: 5; sample: Romans 4:6, 11; 5:9, 10; 2 Corinthians 5:20, 21; Matthew 1:21; Acts 13:39; Galatians 2:16, etc. — Justification in the Scripture, proposed under a
- page: 6; sample: glory, the whole of justification at the last day — The argument that we are justified in this life in the same manner, and on the same grounds, as we shall be judged at the last
- page: 7; sample: necessity — Other objections, arising mostly from mistakes of the truth, asserted, discussed, and answered
- page: 8; sample: alone the means of justification on our part — Faith itself, absolutely considered, not the righteousness that is imputed unto us — Proved by sundry arguments
- page: 9; sample: with respect unto the law and gospel — External righteousness only required by the law, an impious imagination — Works wrought before faith only rejected —
- page: 10; sample: and causes; the other, as unto its signs and evidence — Proved by the instances insisted on — How the Scripture was fulfilled, that Abraham believed in God, and it was
- page: 169; sample: Proverbs 17:15, qyDixæ [æyvir]mæW [v;r; qyDix]mæ, — "He that justifieth the wicked, and
- page: 233; sample: and applying them unto our Savior in his sufferings, he says thus, jEpeida<n ta<v hJmete>rav koinopoiei~ eijv eJauto<n aJmarti>av? —

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: To The Reader; next: I shall not need to detain the reader with an account of the nature and moment of that doctrine which is the entire subject of the ensuing discourse; for although sundry persons, e
- file: EPUB/ch004.xhtml; previous: are justified freely by the grace of God, through the redemption that is in Christ Jesus; whom God has set forth to be a propitiation through faith in his blood," Romans 3:24, 25,; next: — they will offer violence unto common sense and reason, rather than not disturb that harmony which they cannot understand. For although it be plainly affirmed to be a redemption b
- file: EPUB/ch027.xhtml; previous: To The Reader; next: As faith is the first vital act that every true Christian puts Forth, and the life which he lives is by the faith of the Son of God, so it is his next and great concern to know tha

## Inline Structural Marker Candidates

- file: EPUB/ch004.xhtml; text: All men in those days were either kept in bondage under endless fears and anxieties of mind upon the convictions of sin, or sent for relief unto indulgences, priestly pardons, penances, pilgrimages, works satisfactory of their own, and s...
- file: EPUB/ch010.xhtml; text: A very few words will also free our inquiry from any concernment in that which is called sentential justification, at the day of judgment; for of what nature soever it be, the person concerning whom that sentence is pronounced was, — (1....
- file: EPUB/ch021.xhtml; text: In opposition hereunto, the state and prayer of the publican, under the same design of seeking justification before God, are expressed. And the outward acts of his person are mentioned, as representing and expressive of the inward frame ...
- file: EPUB/ch022.xhtml; text: This, in the matter of our justification, he calls, — (1.) Χάρισμα , with respect unto the free, gratuitous grant of it by the grace of God, Δωρεὰ τῆς χάριτος , and (2.) Δώρημα , with respect unto us who receive it, — a free gift it is u...

## Roman Heading Candidates

- file: EPUB/ch014.xhtml; text: III. There is a justification of convinced sinners on their believing.

## Overlong Heading Candidates

- file: EPUB/ch012.xhtml; tag: h3; text: IMPUTATION OF THE SINS OF THE CHURCH UNTO CHRIST — GROUNDS OF IT — THE NATURE OF HIS SURETISHIP — CAUSES OF THE NEW COVENANT — CHRIST AND THE CHURCH ONE MYSTICAL PERSON — CONSEQUENTS THEREOF
- file: EPUB/ch022.xhtml; tag: h3; text: THE NATURE OF JUSTIFICATION AS DECLARED IN THE EPISTLES OF ST. PAUL, IN THAT UNTO THE ROMANS ESPECIALLY. — 3:4CHAP. 3,4,5,10; 1 CORINTHIANS 1:30; 2 Corinthians 5:212 CORINTHIANS 5:21; GALATIANS 2:16; EPHESIANS 2:8-10; PHILIPPIANS 3:8, 9.)

## Short Fragments

- file: EPUB/ch003.xhtml; text: To The Reader
- file: EPUB/ch003.xhtml; text: J.O.
- file: EPUB/ch003.xhtml; text: From my study, May the 30th, 1677
- file: EPUB/ch004.xhtml; text: And again,
- file: EPUB/ch004.xhtml; text: Or that of the psalmist,
- file: EPUB/ch004.xhtml; text: Or,
- file: EPUB/ch004.xhtml; text: And afterwards:
- file: EPUB/ch006.xhtml; text: — of his love;
- file: EPUB/ch006.xhtml; text: —of his grace;
- file: EPUB/ch006.xhtml; text: — of his wisdom;

## Repeated Windows

- phrase: of justification by the imputation of the righteousness of christ; count: 11
- phrase: doctrine of justification by the imputation of the righteousness of; count: 10
- phrase: set forth to be propitiation through faith in his blood; count: 10
- phrase: the doctrine of justification by the imputation of the righteousness; count: 9
- phrase: freely by his grace through the redemption that is in; count: 9
- phrase: justified freely by his grace through the redemption that is; count: 8
- phrase: by his grace through the redemption that is in christ; count: 8
- phrase: his grace through the redemption that is in christ jesus; count: 8
- phrase: whom god has set forth to be propitiation through faith; count: 8
- phrase: god has set forth to be propitiation through faith in; count: 8

## Missing Word Samples

- word: alterations; pdf: 3; epub: 1
- word: apostolical; pdf: 3; epub: 1

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 3; epub: 12
- word: historical; pdf: 5; epub: 12
- word: greek; pdf: 5; epub: 12
- word: modern; pdf: 3; epub: 10
- word: footnotes; pdf: 0; epub: 7
- word: edition; pdf: 2; epub: 8
- word: section; pdf: 0; epub: 6

## Untagged Latin Word Samples

- word: nor; epub: 424; tagged: 12
- word: jesus; epub: 234; tagged: 10
- word: thereunto; epub: 109; tagged: 5
- word: yea; epub: 104; tagged: 1
- word: whereas; epub: 104; tagged: 1
- word: adam; epub: 93; tagged: 4
- word: abraham; epub: 81; tagged: 0
- word: hereunto; epub: 60; tagged: 0
- word: mere; epub: 48; tagged: 0
- word: whereunto; epub: 48; tagged: 1

## Missing Latin Clauses

- page: 359; word_count: 59; sample: non solum illa opera legis quae sunt in veteribus sacramentis et nunc

## Untranslated Latin Samples

- phrase: Articulus stantis
- phrase: cadentis ecclesiae
- phrase: nor endeavor
- phrase: nulla pietatis
- phrase: nullo laudato prioris vitae exemplo commendatos; imo ut
- phrase: videmus, per vagabundos, et contentionum zeli carnalis plenos
- phrase: alios ex castris, aulis, ganeis, prolatam esse. Scrupuli ab excellenti viro propositi
- phrase: hupodikoi tooi Theoo
- phrase: in "materia probabili
- phrase: Albertus Pighius

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
