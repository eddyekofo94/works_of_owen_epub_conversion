# Text Integrity Audit: Volume 13

- Status: **WARN**
- Warnings: 6
- PDF pages: 749
- EPUB text files: 84
- EPUB paragraphs/headings: 2253

## Coverage

- PDF content tokens: 247367
- EPUB content tokens: 250552
- Approximate PDF-to-EPUB coverage ratio: 0.9994
- Pages checked: 725
- Weak page matches: 3
- Dense source windows checked: 33423
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 720
- Top-of-page windows skipped as unstable: 8
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 679
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 1810
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 111
- Short fragments: 37
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 4
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 15
- PDF enumerator markers: 80
- EPUB enumerator markers: 92
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1038
- EPUB Greek words: 1058
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 12
- EPUB Hebrew words: 12
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 59
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3026
- EPUB Latin words: 3101
- EPUB Tagged Latin words: 1651
- Latin word coverage ratio: 0.9954
- Latin word tagging ratio: 0.5324
- Latin clauses checked: 208
- Missing Latin clauses: 0
- Tagged Latin runs checked: 409
- Translated Latin runs: 173
- Latin translation ratio: 0.423

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 21; sample: priesthood by divine institution yet do not thence conclude with aquin 1a 2ae quest
- page: 31; sample: the law of nature being pre supposed we find them farther speaking often one
- page: 46; sample: or no may better serve to illustrate plutarch's discourse of socrates demon than any
- page: 50; sample: and jesuits pretending falsely by their impostures to the power of miracle working though
- page: 58; sample: they may interest themselves in holy soul concerning affairs both in respect of their
- page: 68; sample: is an ignorant congregation of which thanks to our prelates pluralists non residents homilies
- page: 76; sample: eshcol cluster of the fruit of canaan rules of walking in fellowship with reference
- page: 77; sample: election appointment acceptation submission galatians acts thessalonians acts corinthians which do not gire them
- page: 82; sample: saith he it altogether for our sakes for our sakes no doubt this is
- page: 87; sample: commandment and is peculiarly the law of christ john thessalonians john the state and

## Suspicious Large-Number Starts

- file: EPUB/ch005.xhtml; text: 12. ae. quest.
- file: EPUB/ch022.xhtml; text: 10. I no way doubt of the perpetual existence of innumerable believers in every age, and such as made the profession that is absolutely necessary to salvation, one way or other, though I question a regular association of
- file: EPUB/ch022.xhtml; text: 22. In what sense this church is visible was before declared. Men elected, redeemed, justified, as such, are not visible, for that which makes them so is not; but this hinders not but they may be so upon the other consid
- file: EPUB/ch023.xhtml; text: 29. There being, then, in the world a great multitude, which no man can number, of all nations, kindreds, people, and language, professing the doctrine of the gospel, not tied to mountains or hills, John 4:21, 23, but wo

## Roman Heading Candidates

- file: EPUB/ch030.xhtml; text: C. hardly refrain from calling a man Satan for speaking the truth? It is well if we know of what Spirit we are.
- file: EPUB/ch032.xhtml; text: C. knows how easy it were to make his own words dress him up in all those ornaments wherein he labors to make me appear in the world, by such glosses, inversions, additions, and interpositions, as he is pleased to make u
- file: EPUB/ch039.xhtml; text: C. himself is bound to come into it, and yet I do not think that his not so doing makes him a schismatic; and as for relinquishment, I assert no more than what he himself concludes to be lawful. And thus, Christian reade
- file: EPUB/ch059.xhtml; text: IV. The payment of tithes, —

## Short Fragments

- file: EPUB/ch002.xhtml; text: M AY 11, 1644.
- file: EPUB/ch002.xhtml; text: JOSEPH CARYL.
- file: EPUB/ch003.xhtml; text: John Owen
- file: EPUB/ch007.xhtml; text: and again,
- file: EPUB/ch007.xhtml; text: Whence I conclude, —
- file: EPUB/ch011.xhtml; text: to which add that of the apostle,
- file: EPUB/ch011.xhtml; text: Whence.it appears, that, —
- file: EPUB/ch012.xhtml; text: Τῷ Θεῷ ἀριστομεγίστῳ δόζα .
- file: EPUB/ch015.xhtml; text: To The Reader
- file: EPUB/ch016.xhtml; text: 2 Thessalonians 3:1,2,

## Enumerator Sequence Candidates

- file: EPUB/ch023.xhtml; marker: (2.); family: paren_decimal; context: (2.) That doing so, in the course of our lives we manifest and declare a principle that is utterly inconsistent with the belief of those truths which outwardly we profess; or, —
- file: EPUB/ch042.xhtml; marker: [16]; family: bracket_decimal; context: Nor did I, as is pretended, plead for their presbyterian way in the year [16]46; all the ministers almost in the county of Essex know the contrary, one especially, being a man of great ability and moderation of spirit, and for his knowle...

## Repeated Windows

- phrase: not fear the lord god hath spoken who can but; count: 3
- phrase: fear the lord god hath spoken who can but prophesy; count: 3
- phrase: remember them which have the rule over you who have; count: 3
- phrase: them which have the rule over you who have spoken; count: 3
- phrase: which have the rule over you who have spoken unto; count: 3
- phrase: have the rule over you who have spoken unto you; count: 3
- phrase: the rule over you who have spoken unto you the; count: 3
- phrase: rule over you who have spoken unto you the word; count: 3
- phrase: over you who have spoken unto you the word of; count: 3
- phrase: you who have spoken unto you the word of god; count: 3

## Missing Word Samples

- word: self; pdf: 13; epub: 6
- word: fellow; pdf: 3; epub: 0
- word: re; pdf: 3; epub: 1

## Excess Word Samples

- word: ii; pdf: 15; epub: 31
- word: prefatory; pdf: 14; epub: 30
- word: volume; pdf: 5; epub: 18
- word: editor; pdf: 0; epub: 12
- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 0; epub: 9
- word: historical; pdf: 0; epub: 8
- word: citizens; pdf: 8; epub: 15
- word: bill; pdf: 6; epub: 13
- word: modern; pdf: 5; epub: 12

## Untagged Latin Word Samples

- word: magistrate; epub: 232; tagged: 1
- word: dissent; epub: 70; tagged: 0
- word: relate; epub: 21; tagged: 0
- word: door; epub: 17; tagged: 0
- word: ago; epub: 16; tagged: 0
- word: pleas; epub: 15; tagged: 0
- word: iii; epub: 14; tagged: 0
- word: tract; epub: 14; tagged: 0
- word: nowhere; epub: 14; tagged: 0
- word: superior; epub: 15; tagged: 1

## Untranslated Latin Samples

- phrase: Medio tutissimus
- phrase: Sixtus Senensis
- phrase: in causa facili
- phrase: bonum oritur ex integris
- phrase: prophetae de Christo quam de ecclesia: puto propterea quia
- phrase: contra ecclesiam
- phrase: facturos esse particulas; et de Christo non tantam
- phrase: habituros, de ecclesia magnas
- phrase: non qua itur, sed qua eundum est
- phrase: Consuetudo sine veritate est vetustas erroris

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
