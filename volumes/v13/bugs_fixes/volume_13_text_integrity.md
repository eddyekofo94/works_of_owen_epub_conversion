# Text Integrity Audit: Volume 13

- Status: **WARN**
- Warnings: 8
- PDF pages: 749
- EPUB text files: 84
- EPUB paragraphs/headings: 2220

## Coverage

- PDF content tokens: 247367
- EPUB content tokens: 249604
- Approximate PDF-to-EPUB coverage ratio: 0.9989
- Pages checked: 725
- Weak page matches: 4
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

- Body paragraphs checked: 1782
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 111
- Short fragments: 32
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
- EPUB enumerator markers: 90
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1038
- EPUB Greek words: 1030
- Greek word coverage ratio: 0.9744
- PDF Hebrew words: 12
- EPUB Hebrew words: 12
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 59
- Missing Greek clauses: 1
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 2127
- EPUB Latin words: 2055
- EPUB Tagged Latin words: 1427
- Latin word coverage ratio: 0.9558
- Latin word tagging ratio: 0.6944
- Latin clauses checked: 197
- Missing Latin clauses: 11
- Tagged Latin runs checked: 379
- Translated Latin runs: 176
- Latin translation ratio: 0.4644

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB

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
- file: EPUB/ch007.xhtml; text: Whence I conclude, —
- file: EPUB/ch011.xhtml; text: Whence.it appears, that, —
- file: EPUB/ch012.xhtml; text: Τῷ Θεῷ ἀριστομεγίστῳ δόζα .
- file: EPUB/ch015.xhtml; text: To The Reader
- file: EPUB/ch016.xhtml; text: 2 Thessalonians 3:1,2,
- file: EPUB/ch016.xhtml; text: 1 Timothy 1:16-18,
- file: EPUB/ch016.xhtml; text: Song of Solomon 6:4,

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

- word: prefatory; pdf: 14; epub: 30
- word: editor; pdf: 0; epub: 12
- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 0; epub: 9
- word: volume; pdf: 5; epub: 13
- word: historical; pdf: 0; epub: 8
- word: modern; pdf: 5; epub: 12
- word: greek; pdf: 2; epub: 9
- word: footnotes; pdf: 0; epub: 7
- word: edition; pdf: 2; epub: 8

## Missing Greek Clauses

- page: 263; word_count: 5; sample: δουλον κυριου ου δει μαχεσθαι

## Untagged Latin Word Samples

- word: populi; epub: 8; tagged: 0
- word: apollos; epub: 7; tagged: 0
- word: regulate; epub: 7; tagged: 0
- word: metropolis; epub: 6; tagged: 0
- word: cenchrea; epub: 6; tagged: 0
- word: judea; epub: 6; tagged: 0
- word: prelate; epub: 5; tagged: 0
- word: rigor; epub: 5; tagged: 0
- word: demonstrandum; epub: 5; tagged: 0
- word: aen; epub: 6; tagged: 1

## Missing Latin Clauses

- page: 389; word_count: 6; sample: christianorum merito sane illicita si illicitis
- page: 389; word_count: 4; sample: merito damnanda si quis
- page: 389; word_count: 5; sample: ea queritur eo titulo quo
- page: 389; word_count: 5; sample: factionibus querela est in cujus
- page: 389; word_count: 13; sample: aliquando convenimus hoc sumus congregati quod et dispersi hoc universi quod et
- page: 389; word_count: 4; sample: quum probi cum boni
- page: 389; word_count: 11; sample: cum pii cum casti congregantur non est factio dicenda sed curia
- page: 437; word_count: 11; sample: non partum studiis agimur sed sumsimus arma consiliis inimica tuis discordia
- page: 682; word_count: 8; sample: religione eapita quae plurimum habere videntur obscuritatis tantis
- page: 682; word_count: 5; sample: quam ubi cogitur assensus hugo

## Untranslated Latin Samples

- phrase: Medio tutissimus
- phrase: Sixtus Senensis
- phrase: in causa facili
- phrase: bonum oritur ex integris
- phrase: ecclesia: puto propterea quia
- phrase: contra ecclesiam
- phrase: facturos esse particulas; et
- phrase: Christo non tantam
- phrase: ecclesia magnas
- phrase: non qua itur, sed qua eundum est

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
