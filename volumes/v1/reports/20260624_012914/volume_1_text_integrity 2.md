# Text Integrity Audit: Volume 1

- Status: **WARN**
- Warnings: 1
- PDF pages: 633
- EPUB text files: 84
- EPUB paragraphs/headings: 2710

## Coverage

- PDF content tokens: 205054
- EPUB content tokens: 206095
- Approximate PDF-to-EPUB coverage ratio: 0.9993
- Pages checked: 622
- Weak page matches: 0
- Dense source windows checked: 27503
- Missing dense source-window pages: 22
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 4
- Top-of-page body windows checked: 586
- Top-of-page windows skipped as unstable: 6
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 534
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 2262
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 126
- Short fragments: 12
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 310
- EPUB enumerator markers: 320
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 811
- EPUB Greek words: 810
- Greek word coverage ratio: 0.9987
- PDF Hebrew words: 20
- EPUB Hebrew words: 20
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 38
- Missing Greek clauses: 0
- Hebrew clauses checked: 1
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 1378
- EPUB Latin words: 1381
- EPUB Tagged Latin words: 983
- Latin word coverage ratio: 0.9985
- Latin word tagging ratio: 0.7118
- Latin clauses checked: 129
- Missing Latin clauses: 0
- Tagged Latin runs checked: 258
- Translated Latin runs: 162
- Latin translation ratio: 0.6279

## Warnings

- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors

## Missing Dense Source Windows

- page: 3; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ
- page: 4; sample: person of christ which is love its truth and reality vindicated chapter the nature
- page: 5; sample: the accomplishment of the work of mediation in this world representations of the glory
- page: 6; sample: of the holy trinity of the works of god and first of those that
- page: 7; sample: and misapprehension on the principles asserted in the prolegomena and appendix to walton's polyglot
- page: 9; sample: embraces the most comprehensive view of this vitally-important subject his exposition of psalm exhibits
- page: 10; sample: learned puritan we are informed by dr steven that his exposition of the epistle
- page: 21; sample: individuals since the reformation next to calvin's institutions we would have deemed it our
- page: 51; sample: imago id est verbum dei ad eum qui est ad imaginem hoc est hominem
- page: 53; sample: declaration of the glorious mystery of the person of christ chapter peter's confession matthew

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.0; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ prefatory note preface chapter peter's confession matthew conceits of the papists thereon the substance
- page: 4; hit_ratio: 0.5; sample: chapter the especial principle of obedience unto the person of christ which is love its truth and reality vindicated chapter the nature operations and causes of divine love
- page: 5; hit_ratio: 0.5; sample: the glory of christ in his exaltation after the accomplishment of the work of mediation in this world representations of the glory of christ under the old testament
- page: 6; hit_ratio: 0.25; sample: of the holy trinity of the works of god and first of those that are internal and immanent of the works of god that outwardly are of him

## Roman Heading Candidates

- file: EPUB/ch033.xhtml; text: I. 1. What he did, what obedience he yielded unto the law of God in the discharge of his office (with respect whereunto he said, "Lo, I come to do thy will, O God; yea, thy law is in my heart"), it was all on his own fre

## Short Fragments

- file: EPUB/ch001.xhtml; text: Edinburgh, August 1850
- file: EPUB/ch009.xhtml; text: All this himself instructs us in.
- file: EPUB/ch011.xhtml; text: This must be declared.
- file: EPUB/ch027.xhtml; text: Christian Reader,
- file: EPUB/ch029.xhtml; text: For, —
- file: EPUB/ch035.xhtml; text: The sum is,
- file: EPUB/ch037.xhtml; text: And, —
- file: EPUB/ch041.xhtml; text: END.
- file: EPUB/ch042.xhtml; text: To The Reader
- file: EPUB/ch045.xhtml; text: END OF PART 2.

## Repeated Windows

- phrase: the glory of god in the face of jesus christ; count: 12
- phrase: unto us child is born unto us son is given; count: 6
- phrase: of the glory of god in the face of jesus; count: 6
- phrase: shall we dare to say that the gates of hell; count: 5
- phrase: us child is born unto us son is given and; count: 5
- phrase: the brightness of his glory and the express image of; count: 5
- phrase: brightness of his glory and the express image of his; count: 5
- phrase: of his glory and the express image of his person; count: 5
- phrase: are changed into the same image from glory to glory; count: 5
- phrase: both which are in heaven and which are on earth; count: 5

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 2; epub: 11
- word: historical; pdf: 2; epub: 10
- word: modern; pdf: 4; epub: 11
- word: footnotes; pdf: 0; epub: 7
- word: hebrew; pdf: 3; epub: 9

## Untagged Latin Word Samples

- word: incarnate; epub: 36; tagged: 0
- word: nestorius; epub: 8; tagged: 0
- word: consummate; epub: 8; tagged: 0
- word: ultimate; epub: 8; tagged: 0
- word: adequate; epub: 8; tagged: 0
- word: invocate; epub: 7; tagged: 0
- word: inanimate; epub: 6; tagged: 0
- word: indicate; epub: 5; tagged: 0
- word: thomas; epub: 5; tagged: 0
- word: serm; epub: 5; tagged: 0

## Untranslated Latin Samples

- phrase: quarto (Amsterdam
- phrase: operis absentibus [by us being absent from the press]
- phrase: Salus Electorum Sanguis
- phrase: quam conspici
- phrase: Quod si super unum illum Petrum tantum [For if you think the whole church was built upon that one Peter alone...]
- phrase: quid dicturus [what will you say]
- phrase: et apostolorum [and of the apostles]
- phrase: Num audebimus dicere quod adversus Petrum unum non prevaliturae sunt portae inferorum [Shall we dare to say that the gates of hell will not prevail against Peter alone?]
- phrase: Unum hoc est [This is one thing]
- phrase: fundamentum, una haec est

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
