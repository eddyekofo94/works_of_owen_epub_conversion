# Text Integrity Audit: Volume 15

- Status: **WARN**
- Warnings: 8
- PDF pages: 683
- EPUB text files: 107
- EPUB paragraphs/headings: 2435

## Coverage

- PDF content tokens: 221576
- EPUB content tokens: 223303
- Approximate PDF-to-EPUB coverage ratio: 0.9994
- Pages checked: 675
- Weak page matches: 3
- Dense source windows checked: 29601
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 659
- Top-of-page windows skipped as unstable: 13
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 615
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 2000
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 243
- Short fragments: 102
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 2
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 0
- Overlong heading candidates: 7
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 402
- EPUB enumerator markers: 412
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 872
- EPUB Greek words: 873
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 2
- EPUB Hebrew words: 2
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 39
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 1575
- EPUB Latin words: 1596
- EPUB Tagged Latin words: 473
- Latin word coverage ratio: 0.9968
- Latin word tagging ratio: 0.2964
- Latin clauses checked: 62
- Missing Latin clauses: 0
- Tagged Latin runs checked: 118
- Translated Latin runs: 52
- Latin translation ratio: 0.4407

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: righteousness and legal ceremonies contended for together the reason of it chapter the disciples
- page: 4; sample: worship prohibitions of additions produced considered applied chapter of the authority needful for the
- page: 5; sample: ignorance readiness to take offense remedies hereof pride false teachers chapter grounds and reasons
- page: 7; sample: discourse concerning liturgies and their imposition prefatory note it deserves attention that this pamphlet
- page: 10; sample: from the authority of the law maker the latter he utterly rejected as introduced
- page: 17; sample: de rom pontif lib cap but whereas they double the mumber of the sacred
- page: 19; sample: executed by persons variously called thereunto acording to his mind and will the only
- page: 29; sample: their religion as were then fallen out lib concione advocata cum solenne carmen precationis
- page: 34; sample: about such things as were not in rerum natura in the days wherein those
- page: 52; sample: may keep the commandments of the lord your god which command you chapter what

## Inline Structural Marker Candidates

- file: EPUB/ch026.xhtml; text: Whereas, therefore, the Lord Christ, in the exercise of his right and power, on the grant of the Father of a perpetual visible kingdom in this world, and the discharge of his own promise, hath, — (1.) Appointed the ordinary offices, whic...
- file: EPUB/ch034.xhtml; text: It might be easily demonstrated what great numbers [there are] amongst us, — [1.] Who have imbibed atheistical opinions, and either vent them or speak presumptuously, according unto their influence and tendency every day; [2.] Who are pr...

## Suspicious Large-Number Starts

- file: EPUB/ch007.xhtml; text: 30. again, cap. 39:
- file: EPUB/ch029.xhtml; text: 42. Montanus fell into his dotage on the same account; so did Novatianus at Rome, Euseb., lib. 6 cap. 43, and Arius at Alexandria. Hence is that censure of them by Lactantius, lib. 4 cap. 30:
- file: EPUB/ch034.xhtml; text: 12. If the reader would have an account of the lives and manners of the first churches in their members, he may find it in Clem. Epist. ad Cor . pp. 2-4; Justin Mart. Apol. 2; Tertullian in his Algol. and lib. 2 ad Uxor.
- file: EPUB/ch038.xhtml; text: 15. So in the excellent epistle of the churches of Vienne and Lyons unto the churches of Asia and Phrygia, concerning the persecutions that befell them, as they declare themselves to have been particular churches only, s

## Overlong Heading Candidates

- file: EPUB/ch049.xhtml; tag: h3; text: MAY NOT SUCH AN ESTATE OF FAITH AND PERFECTION IN OBEDIENCE BE ATTAINED IN THIS LIFE, AS WHEREIN BELIEVERS MAY BE FREED FROM ALL OBLIGATION UNTO THE OBSERVATION OF GOSPEL INSTITUTIONS?
- file: EPUB/ch056.xhtml; tag: h3; text: WHAT IS PRINCIPALLY TO BE ATTENDED UNTO BY US IN THE MANNER OF THE CELEBRATION OF THE WORSHIP OF GOD, AND OBSERVATION OF THE INSTITUTIONS AND ORDINANCES OF THE GOSPEL?
- file: EPUB/ch059.xhtml; tag: h3; text: WHENCE MAY IT APPEAR THAT THE RIGHT AND DUE OBSERVATION OF INSTITUTED WORSHIP IS OF GREAT IMPORTANCE UNTO THE GLORY OF GOD, AND OF HIGH CONCERNMENT UNTO THE SOULS OF MEN?
- file: EPUB/ch065.xhtml; tag: h3; text: SEEING THE CHURCH IS A SOCIETY OR SPIRITUAL INCORPORATION OF PERSONS UNDER RULE, GOVERNMENT, OR DISCIPLINE, DECLARE WHO OR WHAT ARE THE RULERS, GOVERNORS, OR OFFICERS THEREIN UNDER JESUS CHRIST?
- file: EPUB/ch066.xhtml; tag: h3; text: SEEING THE CHURCH IS A SOCIETY OR SPIRITUAL INCORPORATION OF PERSONS UNDER RULE, GOVERNMENT, OR DISCIPLINE, DECLARE WHO OR WHAT ARE THE RULERS, GOVERNORS, OR OFFICERS THEREIN UNDER JESUS CHRIST?
- file: EPUB/ch071.xhtml; tag: h3; text: MAY A PERSON BE CALLED TO, OR BE EMPLOYED IN, A PART ONLY OF THE OFFICE OR WORK OF THE MINISTRY; OR MAY HE HOLD THE RELATION AND EXERCISE THE DUTY OF AN ELDER OR MINISTER UNTO MORE CHURCHES THAN ONE AT THE SAME TIME?
- file: EPUB/ch082.xhtml; tag: h3; text: MAY NOT THE CHURCH, IN THE SOLEMN WORSHIP OF GOD, AND CELEBRATION OF THE ORDINANCES OF THE GOSPEL, MAKE USE OF AND CONTENT ITSELF IN THE USE OF FORMS OF PRAYER IN AN UNKNOWN TONGUE COMPOSED BY OTHERS, AND PRESCRIBED UNTO THEM?

## Short Fragments

- file: EPUB/ch022.xhtml; text: To The Reader
- file: EPUB/ch028.xhtml; text: Cels., lib. 8.
- file: EPUB/ch032.xhtml; text: Yet, —
- file: EPUB/ch036.xhtml; text: I answer briefly, —
- file: EPUB/ch036.xhtml; text: Yea, but, —
- file: EPUB/ch037.xhtml; text: I say, therefore, —
- file: EPUB/ch037.xhtml; text: Or, —
- file: EPUB/ch038.xhtml; text: I answer, —
- file: EPUB/ch040.xhtml; text: OWEN ON COMMUNION WITH GOD.
- file: EPUB/ch043.xhtml; text: Answer —

## Repeated Windows

- phrase: the whole body fitly joined together and compacted by that; count: 6
- phrase: whole body fitly joined together and compacted by that which; count: 6
- phrase: body fitly joined together and compacted by that which every; count: 6
- phrase: fitly joined together and compacted by that which every joint; count: 6
- phrase: joined together and compacted by that which every joint supplieth; count: 6
- phrase: together and compacted by that which every joint supplieth according; count: 6
- phrase: and compacted by that which every joint supplieth according to; count: 6
- phrase: compacted by that which every joint supplieth according to the; count: 6
- phrase: by that which every joint supplieth according to the effectual; count: 6
- phrase: that which every joint supplieth according to the effectual working; count: 6

## Missing Word Samples

- word: pre; pdf: 6; epub: 0
- word: self; pdf: 5; epub: 1
- word: eminence; pdf: 4; epub: 0
- word: defence; pdf: 3; epub: 1

## Excess Word Samples

- word: churchstate; pdf: 0; epub: 19
- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 0; epub: 9
- word: churchcommunion; pdf: 0; epub: 9
- word: historical; pdf: 1; epub: 9
- word: greek; pdf: 6; epub: 13
- word: footnotes; pdf: 0; epub: 7
- word: modern; pdf: 0; epub: 7
- word: edition; pdf: 5; epub: 11
- word: hebrew; pdf: 0; epub: 6

## Untagged Latin Word Samples

- word: dissent; epub: 42; tagged: 1
- word: separate; epub: 34; tagged: 0
- word: immediate; epub: 33; tagged: 0
- word: severe; epub: 32; tagged: 0
- word: plea; epub: 31; tagged: 0
- word: magistrate; epub: 30; tagged: 0
- word: sincere; epub: 29; tagged: 0
- word: communicate; epub: 26; tagged: 0
- word: poor; epub: 25; tagged: 0
- word: mere; epub: 24; tagged: 1

## Untranslated Latin Samples

- phrase: Musculus, Grotius
- phrase: Santesius, Pamelius
- phrase: Alcuinus, Amatorius, Rabanus
- phrase: Walafridus Strabo, Rupertus Titiensis, Berno, Radulphus Tangrensis
- phrase: Baronius, ad an. Christi
- phrase: De Nativitate
- phrase: ad Orthodoxos, Dionysius
- phrase: manibus expansis
- phrase: de facto
- phrase: in Asia or Africa

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
