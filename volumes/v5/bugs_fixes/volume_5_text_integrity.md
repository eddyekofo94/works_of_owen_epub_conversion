# Text Integrity Audit: Volume 5

- Status: **WARN**
- Warnings: 7
- PDF pages: 576
- EPUB text files: 39
- EPUB paragraphs/headings: 2147

## Coverage

- PDF content tokens: 193208
- EPUB content tokens: 194170
- Approximate PDF-to-EPUB coverage ratio: 0.9998
- Pages checked: 562
- Weak page matches: 0
- Dense source windows checked: 26771
- Missing dense source-window pages: 1
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 561
- Top-of-page windows skipped as unstable: 8
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 527
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 1854
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 228
- Short fragments: 27
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 2
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 2
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 434
- EPUB enumerator markers: 444
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 1158
- EPUB Greek words: 1158
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 123
- EPUB Hebrew words: 123
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 49
- Missing Greek clauses: 0
- Hebrew clauses checked: 14
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3124
- EPUB Latin words: 3118
- EPUB Tagged Latin words: 2602
- Latin word coverage ratio: 0.9968
- Latin word tagging ratio: 0.8345
- Latin clauses checked: 330
- Missing Latin clauses: 1
- Tagged Latin runs checked: 591
- Translated Latin runs: 392
- Latin translation ratio: 0.6633

## Warnings

- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 473; sample: may be assured of their salvation tantum religio potuit suadere malorum so will men

## Missing Top-Of-Page Body Windows

- page: 126; sample: verse 47, "He that be1ieveth on me has everlasting life;" chapter 7:38,

## Inline Structural Marker Candidates

- file: EPUB/ch002.xhtml; text: Lastly, the concluding chapter is devoted to an explanation of the passages in Paul and James which are alleged to be at variance but which are proved to be in perfect harmony, 20. — Ed.
- file: EPUB/ch004.xhtml; text: All men in those days were either kept in bondage under endless fears and anxieties of mind upon the convictions of sin, or sent for relief unto indulgences, priestly pardons, penances, pilgrimages, works satisfactory of their own, and s...

## Roman Heading Candidates

- file: EPUB/ch014.xhtml; text: III. There is a justification of convinced sinners on their believing.

## Overlong Heading Candidates

- file: EPUB/ch012.xhtml; tag: h3; text: IMPUTATION OF THE SINS OF THE CHURCH UNTO CHRIST — GROUNDS OF IT — THE NATURE OF HIS SURETISHIP — CAUSES OF THE NEW COVENANT — CHRIST AND THE CHURCH ONE MYSTICAL PERSON — CONSEQUENTS THEREOF
- file: EPUB/ch022.xhtml; tag: h3; text: THE NATURE OF JUSTIFICATION AS DECLARED IN THE EPISTLES OF ST. PAUL, IN THAT UNTO THE ROMANS ESPECIALLY. — 3:4CHAP. 3,4,5,10; 1 CORINTHIANS 1:30; 2 Corinthians 5:212 CORINTHIANS 5:21; GALATIANS 2:16; EPHESIANS 2:8-10; PHILIPPIANS 3:8,9.)

## Short Fragments

- file: EPUB/ch003.xhtml; text: To The Reader
- file: EPUB/ch003.xhtml; text: J.O.
- file: EPUB/ch003.xhtml; text: From my study, May the 30th, 1677
- file: EPUB/ch004.xhtml; text: And again,
- file: EPUB/ch004.xhtml; text: Or that of the psalmist,
- file: EPUB/ch004.xhtml; text: Or,
- file: EPUB/ch004.xhtml; text: Wherefore,
- file: EPUB/ch004.xhtml; text: And afterwards:
- file: EPUB/ch006.xhtml; text: — of his love;
- file: EPUB/ch006.xhtml; text: —of his grace;

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

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 3; epub: 12
- word: historical; pdf: 4; epub: 12
- word: greek; pdf: 5; epub: 12
- word: modern; pdf: 3; epub: 10
- word: footnotes; pdf: 0; epub: 7
- word: hebrew; pdf: 4; epub: 10
- word: edition; pdf: 2; epub: 8
- word: section; pdf: 0; epub: 6

## Untagged Latin Word Samples

- word: socinus; epub: 29; tagged: 2
- word: onesimus; epub: 10; tagged: 0
- word: obviate; epub: 8; tagged: 0
- word: reus; epub: 13; tagged: 5
- word: adequate; epub: 7; tagged: 0
- word: thomas; epub: 6; tagged: 0
- word: genius; epub: 5; tagged: 0
- word: schlichtingius; epub: 5; tagged: 0
- word: grotius; epub: 5; tagged: 0
- word: pelagius; epub: 4; tagged: 0

## Missing Latin Clauses

- page: 359; word_count: 59; sample: non solum illa opera legis quae sunt in veteribus sacramentis et nunc

## Untranslated Latin Samples

- phrase: Articulus stantis
- phrase: cadentis ecclesiae
- phrase: nulla pietatis
- phrase: nullo laudato prioris vitae exemplo commendatos; imo ut
- phrase: videmus, per vagabundos, et contentionum zeli carnalis plenos
- phrase: alios ex castris, aulis, ganeis, prolatam esse. Scrupuli ab excellenti viro propositi
- phrase: in "materia probabili
- phrase: Albertus Pighius
- phrase: Dissimulate non possumus
- phrase: vel primam doctrinae Christianae

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
