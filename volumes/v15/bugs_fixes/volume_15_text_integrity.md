# Text Integrity Audit: Volume 15

- Status: **WARN**
- Warnings: 5
- PDF pages: 683
- EPUB text files: 107
- EPUB paragraphs/headings: 2414

## Coverage

- PDF content tokens: 221576
- EPUB content tokens: 223285
- Approximate PDF-to-EPUB coverage ratio: 0.9993
- Pages checked: 675
- Weak page matches: 3
- Dense source windows checked: 29388
- Missing dense source-window pages: 1
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 659
- Top-of-page windows skipped as unstable: 13
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 615
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 1

## Paragraphs

- Body paragraphs checked: 1980
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 243
- Short fragments: 102
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
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

- PDF Latin words: 719
- EPUB Latin words: 726
- EPUB Tagged Latin words: 407
- Latin word coverage ratio: 0.9944
- Latin word tagging ratio: 0.5606
- Latin clauses checked: 57
- Missing Latin clauses: 0
- Tagged Latin runs checked: 103
- Translated Latin runs: 63
- Latin translation ratio: 0.6117

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 315; sample: many nations in the coming of christ whereunto this church state was subservient the

## Missing Bottom-Of-Page Body Windows

- page: 224; sample: the good way, and walk therein, and ye find rest for your souls" — Jeremiah 6:16.

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
- word: theft; pdf: 5; epub: 0
- word: self; pdf: 5; epub: 1
- word: eminence; pdf: 4; epub: 0
- word: defence; pdf: 3; epub: 1

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 0; epub: 9
- word: historical; pdf: 1; epub: 9
- word: greek; pdf: 6; epub: 13
- word: footnotes; pdf: 0; epub: 7
- word: modern; pdf: 0; epub: 7
- word: edition; pdf: 5; epub: 11
- word: hebrew; pdf: 0; epub: 6

## Untagged Latin Word Samples

- word: alexandria; epub: 13; tagged: 0
- word: victor; epub: 12; tagged: 0
- word: polycarpus; epub: 10; tagged: 0
- word: regulate; epub: 8; tagged: 0
- word: epiphanius; epub: 9; tagged: 1
- word: cornelius; epub: 7; tagged: 1
- word: smyrna; epub: 6; tagged: 0
- word: judea; epub: 5; tagged: 0
- word: phrygia; epub: 5; tagged: 0
- word: montanus; epub: 5; tagged: 0

## Untranslated Latin Samples

- phrase: in aeternum juremus, pontificem Romanum esse antichristum
- phrase: Ecclesia ut synagoga
- phrase: quorum sine consilio nihil agebatur in ecclesia; quod qua negligentia
- phrase: nescio, nisi forte doctorum desidia
- phrase: magis superbia, dum soli
- phrase: aliquid videri
- phrase: Hinc omnis
- phrase: Iliacos intra muros peccatur et extra
- phrase: Servilius Paulus
- phrase: spolianda trophaeis

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
