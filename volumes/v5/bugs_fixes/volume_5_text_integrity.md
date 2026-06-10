# Text Integrity Audit: Volume 5

- Status: **WARN**
- Warnings: 8
- PDF pages: 576
- EPUB text files: 39
- EPUB paragraphs/headings: 2155

## Coverage

- PDF content tokens: 193208
- EPUB content tokens: 194160
- Approximate PDF-to-EPUB coverage ratio: 0.9998
- Pages checked: 562
- Weak page matches: 0
- Dense source windows checked: 26785
- Missing dense source-window pages: 33
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 561
- Top-of-page windows skipped as unstable: 8
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 527
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 1862
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 229
- Short fragments: 27
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 6
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

- PDF Latin words: 4133
- EPUB Latin words: 4160
- EPUB Tagged Latin words: 2805
- Latin word coverage ratio: 0.9973
- Latin word tagging ratio: 0.6743
- Latin clauses checked: 339
- Missing Latin clauses: 1
- Tagged Latin runs checked: 598
- Translated Latin runs: 379
- Latin translation ratio: 0.6338

## Warnings

- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 15; sample: charles wolsley baronet of some reputation who had been member of cromwell's council of
- page: 16; sample: joseph williams of kidderminster at last the time of his mr grimshawe's an active
- page: 35; sample: totum committe hac sola te totum contege totum immisce te in hac morte in
- page: 77; sample: how unsearchable are his judgments and his ways past finding romans 33-36 see to
- page: 88; sample: the old testament as is plainly declared luke 25-27 for it was not necessary
- page: 89; sample: them which will be pleaded in their proper place chapter 14-18 but we may
- page: 122; sample: the clear revelation of christ and his mediation so did the psalmist psalm and
- page: 126; sample: of his belly shall flow rivers of living water so chapter 35-37 acts that
- page: 137; sample: mentioned in the scripture what shall we do what shall we do to be
- page: 151; sample: acts the word of god acts thessalonians the atonement made by the blood of

## Inline Structural Marker Candidates

- file: EPUB/ch002.xhtml; text: Lastly, the concluding chapter is devoted to an explanation of the passages in Paul and James which are alleged to be at variance but which are proved to be in perfect harmony, 20. — Ed.
- file: EPUB/ch004.xhtml; text: All men in those days were either kept in bondage under endless fears and anxieties of mind upon the convictions of sin, or sent for relief unto indulgences, priestly pardons, penances, pilgrimages, works satisfactory of their own, and s...
- file: EPUB/ch009.xhtml; text: What it is that, when a justified person is guilty of sin (as guilty he is more or less every day), and his conscience is pressed with a sense thereof, as that only thing which can endanger or intercept his justified estate, his favor wi...
- file: EPUB/ch010.xhtml; text: A very few words will also free our inquiry from any concernment in that which is called sentential justification, at the day of judgment; for of what nature soever it be, the person concerning whom that sentence is pronounced was, — (1....
- file: EPUB/ch021.xhtml; text: In opposition hereunto, the state and prayer of the publican, under the same design of seeking justification before God, are expressed. And the outward acts of his person are mentioned, as representing and expressive of the inward frame ...
- file: EPUB/ch022.xhtml; text: This, in the matter of our justification, he calls, — (1.) Χάρισμα , with respect unto the free, gratuitous grant of it by the grace of God, Δωρεὰ τῆς χάριτος , and (2.) Δώρημα , with respect unto us who receive it, — a free gift it is u...

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

- word: adam; epub: 93; tagged: 3
- word: abraham; epub: 81; tagged: 0
- word: mere; epub: 48; tagged: 0
- word: plea; epub: 45; tagged: 0
- word: mediator; epub: 42; tagged: 0
- word: sincere; epub: 41; tagged: 0
- word: immediate; epub: 32; tagged: 1
- word: nowhere; epub: 33; tagged: 3
- word: elsewhere; epub: 27; tagged: 0
- word: socinus; epub: 29; tagged: 6

## Missing Latin Clauses

- page: 359; word_count: 59; sample: non solum illa opera legis quae sunt in veteribus sacramentis et nunc

## Untranslated Latin Samples

- phrase: Articulus stantis
- phrase: cadentis ecclesiae
- phrase: nulla pietatis
- phrase: nullo laudato prioris vitae exemplo commendatos; imo ut
- phrase: videmus, per vagabundos, et contentionum zeli carnalis plenos
- phrase: alios ex castris, aulis, ganeis, prolatam esse. Scrupuli ab excellenti viro propositi
- phrase: hupodikoi tooi Theoo
- phrase: in "materia probabili
- phrase: Albertus Pighius
- phrase: Dissimulate non possumus

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
