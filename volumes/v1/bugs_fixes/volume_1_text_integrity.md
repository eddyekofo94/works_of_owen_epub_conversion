# Text Integrity Audit: Volume 1

- Status: **WARN**
- Warnings: 10
- PDF pages: 633
- EPUB text files: 84
- EPUB paragraphs/headings: 2705

## Coverage

- PDF content tokens: 205010
- EPUB content tokens: 205874
- Approximate PDF-to-EPUB coverage ratio: 0.9993
- Pages checked: 622
- Weak page matches: 5
- Dense source windows checked: 27414
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 4
- Top-of-page body windows checked: 586
- Top-of-page windows skipped as unstable: 13
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 534
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 2

## Paragraphs

- Body paragraphs checked: 2255
- Possible faulty paragraph splits: 8
- Structural starts excluded from split warnings: 115
- Short fragments: 11
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 5
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
- EPUB Greek words: 811
- Greek word coverage ratio: 0.9973
- PDF Hebrew words: 20
- EPUB Hebrew words: 20
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 38
- Missing Greek clauses: 0
- Hebrew clauses checked: 1
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3423
- EPUB Latin words: 3463
- EPUB Tagged Latin words: 1149
- Latin word coverage ratio: 0.998
- Latin word tagging ratio: 0.3318
- Latin clauses checked: 150
- Missing Latin clauses: 0
- Tagged Latin runs checked: 288
- Translated Latin runs: 163
- Latin translation ratio: 0.566

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ
- page: 4; sample: person of christ which is love its truth and reality vindicated chapter the nature
- page: 5; sample: the accomplishment of the work of mediation in this world representations of the glory
- page: 6; sample: of the holy trinity of the works of god and first of those that
- page: 9; sample: embraces the most comprehensive view of this vitally-important subject his exposition of psalm exhibits
- page: 10; sample: learned puritan we are informed by dr steven that his exposition of the epistle
- page: 11; sample: owen whose name towers into just pre eminence among all his venerable compeers in
- page: 21; sample: individuals since the reformation next to calvin's institutions we would have deemed it our
- page: 44; sample: πατρος και του υιου και του αγιου πνευματος πιστευομενης ομοτιμου της αξιας και συναιδιου
- page: 51; sample: imago id est verbum dei ad eum qui est ad imaginem hoc est hominem

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.0; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ prefatory note preface chapter peter's confession matthew conceits of the papists thereon the substance
- page: 4; hit_ratio: 0.5; sample: chapter the especial principle of obedience unto the person of christ which is love its truth and reality vindicated chapter the nature operations and causes of divine love
- page: 5; hit_ratio: 0.5; sample: the glory of christ in his exaltation after the accomplishment of the work of mediation in this world representations of the glory of christ under the old testament
- page: 6; hit_ratio: 0.25; sample: of the holy trinity of the works of god and first of those that are internal and immanent of the works of god that outwardly are of him

## Missing Bottom-Of-Page Body Windows

- page: 26; sample: oijkodomh>sw mou th<n ejhkklhsi>an, kai< pu>lai a[|dou ouj katiscu>sousin aujth~v".
- page: 293; sample: of God. Such are "ejnsa>rkwsiv", "incarnation;" "ejnswma>twsiv", "embodying," "ejnanqrw>phsiv", "inhumanation;" "hJ despotikh<

## Possible Paragraph Splits

- file: EPUB/ch004.xhtml; previous: veniret utriusque diversitas, ut unus idemque sit filius, qui se, et secundum quod verus est homo, Patre dicit minorem, et secundum quod verus est Deus Patrise profitetur aequalem"; next: — "Human nature is assumed into the society of the Creator, not that he should be the inhabitant, and that the habitation," (that is, by an inhabitation in the effects of his power
- file: EPUB/ch011.xhtml; previous: ls was subordinate unto him; and whatever instruction was thereby given unto the church in the mind and will of God, it was immediately from him, as the great prophet of the church; next: (3rdly,) By sending his Holy Spirit to inspire, act, and guide the prophets, by whom God would reveal himself. God spoke unto them by the "mouth of his holy prophets, which have be
- file: EPUB/ch011.xhtml; previous: was so to prophet of the church always as to tender manifold instructions unto the perishing, unbelieving world. Hence is he said to lighten "every man that comets into the world,"; next: John 1:9, by one way or other communicating to them some notices of God and his will; for his light shineth in, or irradiates darkness itself — that darkness which is come on the m
- file: EPUB/ch022.xhtml; previous: (1st,) That the Word ceased to be what it was, and was substantially turned into flesh; next: (2ndly,) That continuing to be what it was, it was made to be also what before it was not.
- file: EPUB/ch027.xhtml; previous: Christian Reader,; next: To design of the ensuing Discourse is to declare some part of that glory of our Lord Jesus Christ which is revealed in the Scripture, and proposed as the principal object of our fa
- file: EPUB/ch039.xhtml; previous: Yea, whilst we are in this tabernacle, we groan earnestly, as being burdened, because we are not "absent from the body, and present with the Lord," 2 Corinthians 5:2, 4, 8; next: The more we grow in faith and spiritual light, the more sensible are we of our present burdens, and the more vehemently do we groan for deliverance into the perfect liberty of the
- file: EPUB/ch042.xhtml; previous: To The Reader; next: The design of this preface is not to commend either the author or the matter contained in this little book. Let every reader do as he finds cause.
- file: EPUB/ch048.xhtml; previous: Your servant in the work of the Lord; next: J.O.

## Inline Structural Marker Candidates

- file: EPUB/ch013.xhtml; text: In the confirmation hereof it will appear what judgment ought to be passed on that inquiry — which, after the uninterrupted profession of the catholic church for so many ages of a faith unto the contrary, is begun to be made by some amon...
- file: EPUB/ch031.xhtml; text: That which we inquire after at present, is, the glory of Christ herein, and how we may behold that glory. And there are three things wherein we may take a prospect of it. 1. In his susception of this office. 2. In his discharge of it. 3....
- file: EPUB/ch031.xhtml; text: In the susception of this office we may behold the glory of Christ, — I. In his condescension; II. In his love.
- file: EPUB/ch040.xhtml; text: Two things we must here speak unto. 1. Why does the Lord Christ, at any time, thus hide himself in his glory from the faith of believers, that they cannot behold him? 2. How we may perceive and know that he does so withdraw himself from ...
- file: EPUB/ch045.xhtml; text: The second thing proposed is, that notwithstanding all this provision for the growth of spiritual life in us, believers, especially in a long course of profession, are subject to decays, such as may cast them into great perplexities, and...

## Roman Heading Candidates

- file: EPUB/ch033.xhtml; text: I. 1. What he did, what obedience he yielded unto the law of God in the discharge of his office (with respect whereunto he said, "Lo, I come to do thy will, O God; yea, thy law is in my heart"), it was all on his own fre

## Short Fragments

- file: EPUB/ch001.xhtml; text: Edinburgh, August 1850
- file: EPUB/ch009.xhtml; text: All this himself instructs us in.
- file: EPUB/ch011.xhtml; text: This must be declared.
- file: EPUB/ch027.xhtml; text: Christian Reader,
- file: EPUB/ch035.xhtml; text: The sum is,
- file: EPUB/ch037.xhtml; text: And, —
- file: EPUB/ch041.xhtml; text: END.
- file: EPUB/ch042.xhtml; text: To The Reader
- file: EPUB/ch045.xhtml; text: END OF PART 2.
- file: EPUB/ch048.xhtml; text: J.O.

## Repeated Windows

- phrase: the glory of god in the face of jesus christ; count: 12
- phrase: unto us child is born unto us son is given; count: 6
- phrase: of the glory of god in the face of jesus; count: 6
- phrase: us child is born unto us son is given and; count: 5
- phrase: the brightness of his glory and the express image of; count: 5
- phrase: brightness of his glory and the express image of his; count: 5
- phrase: of his glory and the express image of his person; count: 5
- phrase: are changed into the same image from glory to glory; count: 5
- phrase: both which are in heaven and which are on earth; count: 5
- phrase: the only-begotten son who is in the bosom of the; count: 5

## Missing Word Samples

- word: pre; pdf: 6; epub: 2
- word: eminence; pdf: 5; epub: 1
- word: mindedness; pdf: 3; epub: 0

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 2; epub: 11
- word: historical; pdf: 2; epub: 10
- word: modern; pdf: 4; epub: 11
- word: footnotes; pdf: 0; epub: 7
- word: hebrew; pdf: 3; epub: 9

## Untagged Latin Word Samples

- word: nor; epub: 352; tagged: 5
- word: jesus; epub: 254; tagged: 7
- word: yea; epub: 97; tagged: 1
- word: immediate; epub: 97; tagged: 2
- word: distinct; epub: 86; tagged: 1
- word: thereunto; epub: 73; tagged: 3
- word: mere; epub: 66; tagged: 0
- word: hereunto; epub: 63; tagged: 2
- word: whereas; epub: 60; tagged: 0
- word: adam; epub: 52; tagged: 3

## Untranslated Latin Samples

- phrase: bias — in an inveterate
- phrase: quarto (Amsterdam
- phrase: operis absentibus
- phrase: Salus Electorum Sauguis
- phrase: quam conspici
- phrase: contemplate a separate
- phrase: Quod si super unum illum Petrum tantum
- phrase: totam eclesiam
- phrase: quid dicturus
- phrase: et apostolorum

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
