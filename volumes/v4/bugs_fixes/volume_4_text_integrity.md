# Text Integrity Audit: Volume 4

- Status: **WARN**
- Warnings: 12
- PDF pages: 650
- EPUB text files: 70
- EPUB paragraphs/headings: 2109

## Coverage

- PDF content tokens: 219414
- EPUB content tokens: 220016
- Approximate PDF-to-EPUB coverage ratio: 0.9985
- Pages checked: 641
- Weak page matches: 6
- Dense source windows checked: 28298
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 4
- Top-of-page body windows checked: 622
- Top-of-page windows skipped as unstable: 28
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 605
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 10

## Paragraphs

- Body paragraphs checked: 1765
- Possible faulty paragraph splits: 9
- Structural starts excluded from split warnings: 295
- Short fragments: 20
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 6
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 0
- Overlong heading candidates: 1
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 416
- EPUB enumerator markers: 429
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 713
- EPUB Greek words: 712
- Greek word coverage ratio: 0.9899
- PDF Hebrew words: 99
- EPUB Hebrew words: 99
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 38
- Missing Greek clauses: 0
- Hebrew clauses checked: 7
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3199
- EPUB Latin words: 3226
- EPUB Tagged Latin words: 102
- Latin word coverage ratio: 0.9978
- Latin word tagging ratio: 0.0316
- Latin clauses checked: 114
- Missing Latin clauses: 0
- Tagged Latin runs checked: 9
- Translated Latin runs: 7
- Latin translation ratio: 0.7778

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: contents πηευματολογια or discourse concerning the holy spirit continued book vi part the reason
- page: 4; sample: question stated the principal sufficient cause of the understanding which believers have in the
- page: 5; sample: book vii discourse of the work of the holy spirit in prayer prefatory note
- page: 6; sample: given as comforter or the object of his acting in this office inhabitation of
- page: 8; sample: be the word of god with the causes and nature of that faith wherewith
- page: 17; sample: and power this they do undeniably and infallibly psalm romans 19-21 yet it is
- page: 19; sample: own counsels as it is expressed psalm and although this fell not out without
- page: 20; sample: of curse unto the contrary malachi 4-6 so the writings of the new testament
- page: 21; sample: is the only repository of all divine supernatural revelation psalm isaiah timothy the pretenses
- page: 22; sample: in the ministry of the word see matthew corinthians 18-20 ephesians 11-15 timothy the

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.25; sample: contents πηευματολογια or discourse concerning the holy spirit continued book vi part the reason of faith prefatory note by the editor preface the subject stated preliminary remarks what
- page: 4; hit_ratio: 0.5; sample: question stated the principal sufficient cause of the understanding which believers have in the mind and will of god as revealed in the scriptures the spirit of god
- page: 5; hit_ratio: 0.25; sample: book vii discourse of the work of the holy spirit in prayer prefatory note by the editor preface to the reader the use of prayer and the work
- page: 6; hit_ratio: 0.5; sample: unto whom the holy spirit is promised and given as comforter or the object of his acting in this office inhabitation of the spirit the first thing promised

## Missing Top-Of-Page Body Windows

- page: 35; sample: wisdom before all the world, Deuteronomy 4:6-8. Now, we shall not need to consider what were the first attempts of other nations in

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 44; sample: testimony may rationally be supposed to be so far influenced by self- interest as to be of little validity.
- page: 93; sample: let it be observed, that what we assert respects the revelation itself, the Scripture, the writing, th<n grafh>n, and not merely the things written or
- page: 150; sample: out of thy law. — Psalm 119:18. Give me understanding, and I shall live. — <19B9144>Psalm 119:144.
- page: 219; sample: understanding, and I shall keep thy law," Psalm 119:34. So the apostle speaks to Timothy,
- page: 365; sample: its proper place, as a consequent and fruit of his death and resurrection, verse 35. And there he is said simply ejntugca>nein? but the Spirit here is
- page: 413; sample: aJrpasqei<v h{ ejnqousia>sav hJsuch~ ejn ejrh>mw| katasta>sei gege>nhtai ajtremei~, th~| aujtou~ oujsi>a| oujdamou~ ajpokli>nwn, oujde<
- page: 513; sample: expressed in every place where there is mention made of it: 2 Corinthians 1:22, Dou<v to<n ajrjrJazw~na tou~ Pneu>matov? — "The earnest
- page: 532; sample: Again; with respect unto the manner of their communication, they are called merismoi< tou~ Pneu>matov aJgi>ou, Hebrews 2:4, "distributions,"
- page: 621; sample: [3.] Both these are directed unto one general issue. It is all eijv oijkodomh<n tou~ sw>matov tou~ Cristou~, — "unto the edification of the body of

## Possible Paragraph Splits

- file: EPUB/ch029.xhtml; previous: Its general nature is considered, — prayer having been defined to be a spiritual faculty of exercising Christian graces in the way of vocal requests and supplications to God,; next: IV.
- file: EPUB/ch029.xhtml; previous: on of our spiritual wants; acquainting us with the promises of grace and mercy for our relief; and leading us to express desires for any blessing in order to right and proper ends,; next: V.
- file: EPUB/ch029.xhtml; previous: planting holy and gracious desires after the objects sought; giving us delight in God as the object of prayer; and keeping us intent on Christ, as the way and ground of acceptance,; next: VI.
- file: EPUB/ch029.xhtml; previous: The manner of prayer is farther considered with special reference to [Ephesians 6:18]; next: VII.
- file: EPUB/ch044.xhtml; previous: In regard to his effects on believers, it is first proved that his effectual consolations are the privilege of believers exclusively,; next: III.
- file: EPUB/ch045.xhtml; previous: (1.) Extraordinary gifts constituted extraordinary officers — apostles, evangelists, and prophets,; next: III.
- file: EPUB/ch045.xhtml; previous: ction, from its original acquisition, from the immediate cause of its actual communication, from its own nature, from the variety of offices in it, and from the end designed by it,; next: VI.
- file: EPUB/ch045.xhtml; previous: the Spirit is promised, administered, and continued; the plain assertions of Scripture; the indispensable necessity for them; and from the actual enjoyment and experience of them,; next: VII.
- file: EPUB/ch057.xhtml; previous: e, another a hand, another a foot, in the body, by virtue of peculiar gifts: for "unto every one of us is given grace according to the measure of the gift of Christ," Ephesians 4:7; next: These gifts are not saving, sanctifying graces; those were not so in themselves which made the most glorious and astonishing appearance in the world, and which were most eminently

## Inline Structural Marker Candidates

- file: EPUB/ch016.xhtml; text: 2. Into the especial nature of the Spirit's work in enlightening us into a knowledge of the mind of God in Scripture. Its nature is first considered by a reference to several scriptural expressions descriptive of it, such as "opening the...
- file: EPUB/ch024.xhtml; text: Nor do I believe that any one who doth and can thus pray as he ought, in a conscientious study of the word, shall ever be left unto the final prevalency of any pernicious error or the ignorance of any fundamental truth. None utterly misc...
- file: EPUB/ch037.xhtml; text: I say, therefore, — 1. That the things insisted on are in some degree and measure necessary unto all acceptable prayer. The Scripture assigns them thereunto, and believers find them so by their own experience. For we discourse not about ...
- file: EPUB/ch044.xhtml; text: Among the special benefits indicated are, — 1. The unction of the Spirit, 5; 2. sealing of the Spirit, expounded in a brief comment on [Ephesians 1:13] 4:30, VI.; and, 3. The Spirit as an earnest, considered in reference to [2 Corinthian...
- file: EPUB/ch052.xhtml; text: What remains is, to inquire, — 1. What benefit or advantage we have by this unction; 2. How this belongs unto our consolation, seeing the Holy Spirit is thus bestowed on us as he is promised to be the comforter of the church.
- file: EPUB/ch062.xhtml; text: Designing to treat of the spiritual gifts bestowed on the ministry of the church, I have thus far diverted unto the consideration of the ministry itself as it is a gift of Christ, and shall shut it up with a few corollaries, As, 1. Where...

## Overlong Heading Candidates

- file: EPUB/ch047.xhtml; tag: h3; text: The Holy Ghost the comforter of the church by way of office — How he is the church's advocate — John 14:16; 1 John 2:1, 2; John 16:8-11 opened.

## Short Fragments

- file: EPUB/ch005.xhtml; text: May 11, 1677.
- file: EPUB/ch010.xhtml; text: Isaiah 8:19, 20,
- file: EPUB/ch016.xhtml; text: I.
- file: EPUB/ch029.xhtml; text: I.
- file: EPUB/ch029.xhtml; text: II.
- file: EPUB/ch029.xhtml; text: IV.
- file: EPUB/ch029.xhtml; text: V.
- file: EPUB/ch029.xhtml; text: VI.
- file: EPUB/ch029.xhtml; text: VII.
- file: EPUB/ch035.xhtml; text: I answer, —

## Enumerator Sequence Candidates

- file: EPUB/ch021.xhtml; marker: (2.); family: paren_decimal; context: (2.) Moreover, the effect of this work of the Holy Spirit on the minds of men doth evidence of what nature it is, And this, also, is variously expressed; as, —

## Repeated Windows

- phrase: we believe the scripture to be the word of god; count: 21
- phrase: to believe the scripture to be the word of god; count: 16
- phrase: believe the scripture to be the word of god with; count: 9
- phrase: the mind and will of god as revealed in the; count: 9
- phrase: to be the word of god with faith divine and; count: 7
- phrase: mind and will of god as revealed in the scripture; count: 7
- phrase: be the word of god with faith divine and supernatural; count: 6
- phrase: believe the scripture to be the word of god in; count: 6
- phrase: of the mind and will of god as revealed in; count: 6
- phrase: of the holy spirit in the illumination of our minds; count: 5

## Missing Word Samples

- word: self; pdf: 7; epub: 2
- word: 14-17; pdf: 4; epub: 0
- word: editor; pdf: 4; epub: 1
- word: 16-18; pdf: 3; epub: 1

## Excess Word Samples

- word: chapter; pdf: 48; epub: 92
- word: psalms; pdf: 7; epub: 30
- word: digital; pdf: 0; epub: 10
- word: modern; pdf: 4; epub: 13
- word: greek; pdf: 8; epub: 16
- word: edition; pdf: 3; epub: 9
- word: footnotes; pdf: 0; epub: 6

## Untagged Latin Word Samples

- word: nor; epub: 488; tagged: 0
- word: jesus; epub: 175; tagged: 0
- word: thereunto; epub: 160; tagged: 0
- word: whereas; epub: 139; tagged: 0
- word: immediate; epub: 137; tagged: 0
- word: yea; epub: 114; tagged: 0
- word: hereunto; epub: 76; tagged: 0
- word: distinct; epub: 52; tagged: 0
- word: elsewhere; epub: 51; tagged: 0
- word: whereunto; epub: 47; tagged: 0

## Untranslated Latin Samples

- phrase: continuing in the Son, and in the Father.
- phrase: witnesses in Jerusalem, and in all Judea, and in Samaria, and unto the uttermost part of the earth;

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
