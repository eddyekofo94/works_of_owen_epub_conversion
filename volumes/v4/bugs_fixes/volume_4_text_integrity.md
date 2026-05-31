# Text Integrity Audit: Volume 4

- Status: **WARN**
- Warnings: 10
- PDF pages: 650
- EPUB text files: 69
- EPUB paragraphs/headings: 2168

## Coverage

- PDF content tokens: 221655
- EPUB content tokens: 222385
- Approximate PDF-to-EPUB coverage ratio: 0.9967
- Pages checked: 641
- Weak page matches: 12
- Dense source windows checked: 742
- Missing dense source-window pages: 625
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 622
- Top-of-page windows skipped as unstable: 28
- Missing top-of-page body windows: 2
- Bottom-of-page body windows checked: 605
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 8

## Paragraphs

- Body paragraphs checked: 1813
- Possible faulty paragraph splits: 75
- Structural starts excluded from split warnings: 313
- Short fragments: 13
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 2
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 3
- Overlong heading candidates: 8
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 416
- EPUB enumerator markers: 416
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 713
- EPUB Greek words: 713
- Greek word coverage ratio: 0.9971
- PDF Hebrew words: 99
- EPUB Hebrew words: 99
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 38
- Missing Greek clauses: 0
- Hebrew clauses checked: 7
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 4; sample: objections answered corinthians 13-18 isaiah 27 explained luke 24 44 45 opened ephesians 17-19
- page: 8; sample: be the word of god with the causes and nature of that faith wherewith
- page: 10; sample: 10 fanatical excesses which they sought to rebuke they stated the question in such
- page: 11; sample: 11 itself substantiates such claim in his behalf it is the first recognition of
- page: 12; sample: 12 preface having added brief account of the design order and method of the
- page: 13; sample: 13 the consciences of men immediately and the way whereby they may come to
- page: 15; sample: 15 the reason of faith or the grounds whereon the scripture is believed to
- page: 16; sample: 16 first supernatural revelation is the only objective cause and means of supernatural illumination
- page: 17; sample: 17 that it did sufficiently evidence itself to be from god unto the minds
- page: 18; sample: 18 of his will πολυμερως by sundry parts and degrees yet so that every

## Missing Top-Of-Page Body Windows

- page: 35; sample: wisdom before all the world, Deuteronomy 4:6-8. Now, we shall not need to consider what were the first attempts of other nations in
- page: 164; sample: V. That hereby alone is that full assurance of understanding in the knowledge of the mystery of God, his truth and grace, to be obtained,

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 44; sample: testimony may rationally be supposed to be so far influenced by self- interest as to be of little validity.
- page: 93; sample: let it be observed, that what we assert respects the revelation itself, the Scripture, the writing, th<n grafh>n, and not merely the things written or
- page: 365; sample: its proper place, as a consequent and fruit of his death and resurrection, verse 35. And there he is said simply ejntugca>nein? but the Spirit here is
- page: 413; sample: aJrpasqei<v h{ ejnqousia>sav hJsuch~ ejn ejrh>mw| katasta>sei gege>nhtai ajtremei~, th~| aujtou~ oujsi>a| oujdamou~ ajpokli>nwn, oujde<
- page: 513; sample: expressed in every place where there is mention made of it: 2 Corinthians 1:22, Dou<v to<n ajrjrJazw~na tou~ Pneu>matov? — "The earnest
- page: 532; sample: Again; with respect unto the manner of their communication, they are called merismoi< tou~ Pneu>matov aJgi>ou, Hebrews 2:4, "distributions,"
- page: 621; sample: [3.] Both these are directed unto one general issue. It is all eijv oijkodomh<n tou~ sw>matov tou~ Cristou~, — "unto the edification of the body of

## Possible Paragraph Splits

- file: EPUB/ch001.xhtml; previous: EDITED BY; next: WILLIAM H. GOOLD
- file: EPUB/ch001.xhtml; previous: WILLIAM H. GOOLD; next: ΠΗΕΥΜΑΤΟΛΟΓΙΑ ? OR A DISCOURSE CONCERNING THE HOLY SPIRIT — CONTINUED. [BOOK VI., PART I.] THE REASON OF FAITH. PREFATORY NOTE BY THE EDITOR
- file: EPUB/ch001.xhtml; previous: 4. - Extraordinary spiritual gifts, [1 Corinthians 12:5] -; next: 11.
- file: EPUB/ch007.xhtml; previous: we do believe; and the reason why we do believe them is, because they are proposed in the Scripture. Thus the apostle expresseth the whole of what we intend: 1 Corinthians 15:3, 4,; next: Christ's death, and burial, and resurrection, are the things proposed unto us to be believed, and so the object of our faith; but the reason why we believe them is, because they ar
- file: EPUB/ch008.xhtml; previous: o deservedly, for where it is absolute it is unquestionable; that which is most ancient in any kind is most true. God himself makes use of this plea against idols: Isaiah 43:10-12,; next: That which he asserts is, that he alone is God, and no other: this he calls the people to testify by this argument, that he was among them as God, — that is, in the church, — befor
- file: EPUB/ch008.xhtml; previous: rship of idols, but a sedate, unprejudiced consideration of the revelation of these things in the books of the Scripture. We may say, therefore, to all the world, with our prophet,; next: And this, also, plainly manifests the Scripture to be of a divine original: for if this declaration of God, this revelation of himself and his will, is incomparably the greatest an
- file: EPUB/ch008.xhtml; previous: of them, severally and jointly, witnessed that what they wrote was received by inspiration from God. This is pleaded by the apostle Peter in the name of them all: 2 Peter 1:16-21,; next: This is the concurrent testimony of the writers both of the Old Testament and the New, — namely, that as they had certain knowledge of the things they wrote, so their writing was b
- file: EPUB/ch009.xhtml; previous: the word of God, in the way and manner which God requireth, without a supernatural work of the Holy Spirit upon our minds in the illumination of them. So David prays that God would; next: The communication of this light unto us the Scripture calleth revealing and revelation: Matthew 11:25, "Thou hast hid these things from the wise and prudent, and hast revealed them
- file: EPUB/ch009.xhtml; previous: e kingdom of heaven, when they were preached unto them. And "no man knoweth the Father, but he to whom the Son will reveal him," verse 27. So the apostle prayeth for the Ephesians,; next: It is true, these Ephesians were already believers, or considered by the apostle as such; but if he judged it necessary to pray for them that they might have "the Spirit of wisdom
- file: EPUB/ch009.xhtml; previous: and revelation to enlighten the eyes of their understanding," with respect unto farther degrees of faith and knowledge, or, as he speaks in another place, that they might come unto; next: But as a pretense hereof hath been abused, as we shall see afterward, so the pleading of it is liable to be mistaken; for some are ready to apprehend that this retreat unto a Spiri

## Inline Structural Marker Candidates

- file: EPUB/ch044.xhtml; text: Among the special benefits indicated are, — 1. The unction of the Spirit, 5; 2. sealing of the Spirit, expounded in a brief comment on [Ephesians 1:13] 4:30, VI.; and, 3. The Spirit as an earnest, considered in reference to [2 Corinthian...
- file: EPUB/ch052.xhtml; text: What remains is, to inquire, — 1. What benefit or advantage we have by this unction; 2. How this belongs unto our consolation, seeing the Holy Spirit is thus bestowed on us as he is promised to be the comforter of the church.

## Roman Heading Candidates

- file: EPUB/ch016.xhtml; text: I. The Holy, Spirit is represented as the EFFICIENT CAUSE, and an inquiry follows: —
- file: EPUB/ch029.xhtml; text: I. The evidence of its reality consists in a minute explanation of two passages in Scripture, Zechariah 12:10, and Galatians 4:6, 2, 3.
- file: EPUB/ch029.xhtml; text: II. Its general nature is considered, — prayer having been defined to be a spiritual faculty of exercising Christian graces in the way of vocal requests and supplications to God,

## Overlong Heading Candidates

- file: EPUB/ch013.xhtml; tag: h4; text: II. This being the substance of what is declared and pleaded for in the preceding treatise, to prevent the obloquy of some and confirm the judgment of others, I shall add the suffrage of ancient and modern writers given unto the principa...
- file: EPUB/ch018.xhtml; tag: h4; text: IV. That there is an especial work of the Holy Spirit, in the supernatural illumination of our minds, needful unto the end proposed, — namely, that we may aright, and according unto our duty, understand the mind of God in the Scripture o...
- file: EPUB/ch018.xhtml; tag: h4; text: V. That hereby alone is that full _assurance of understanding in the_ _knowledge of the mystery of God,_ his truth and grace, to be obtained, whereby any man may answer the mind and will of God, or comply with his own duty in all that he...
- file: EPUB/ch018.xhtml; tag: h4; text: VI. The certainty and assurance that we may have and ought to have of our right understanding the mind of God in the Scripture, either in general or as to any especial doctrine, doth not depend upon, is not resolved into, any immediate i...
- file: EPUB/ch018.xhtml; tag: h4; text: VII. That whereas the means of the right interpretation of the Scripture, and understanding of the mind of God therein, are of two sorts, — first, such as are prescribed unto us in a way of duty, as _prayer, meditation_ on the word itsel...
- file: EPUB/ch043.xhtml; tag: h4; text: XI. The discourse on Spiritual Gifts, though comparatively short, is the second part of the main.body of the whole work on the Spirit; and, from various allusions to it in other works of the author, he seems to trove attached considerabl...
- file: EPUB/ch047.xhtml; tag: h3; text: The Holy Ghost the comforter of the church by way of office — How he is the church's advocate — John 14:16; 1 John 2:1, 2; John 16:8-11 opened.
- file: EPUB/ch064.xhtml; tag: h4; text: I. In our inquiry after the first, or what are the gifts whereby men are fitted and enabled for the ministry, we wholly set aside the consideration of all those gracious qualifications of faith, love, zeal, compassion, careful tender wat...

## Short Fragments

- file: EPUB/ch001.xhtml; text: EDITED BY
- file: EPUB/ch001.xhtml; text: WILLIAM H. GOOLD
- file: EPUB/ch001.xhtml; text: Appendix.
- file: EPUB/ch001.xhtml; text: 11.
- file: EPUB/ch005.xhtml; text: May 11, 1677.
- file: EPUB/ch010.xhtml; text: Isaiah 8:19,20,
- file: EPUB/ch035.xhtml; text: I answer, —
- file: EPUB/ch037.xhtml; text: I say, therefore, —
- file: EPUB/ch043.xhtml; text: See vol. 15 p. 249.
- file: EPUB/ch044.xhtml; text: I.

## Enumerator Sequence Candidates

- file: EPUB/ch021.xhtml; marker: (2.); family: paren_decimal; context: (2.) Moreover, the effect of this work of the Holy Spirit on the minds of men doth evidence of what nature it is, And this, also, is variously expressed; as, —

## Repeated Windows

- phrase: we believe the scripture to be the word of god; count: 21
- phrase: to believe the scripture to be the word of god; count: 17
- phrase: the mind and will of god as revealed in the; count: 11
- phrase: believe the scripture to be the word of god with; count: 9
- phrase: to be the word of god with faith divine and; count: 7
- phrase: mind and will of god as revealed in the scripture; count: 7
- phrase: of the holy spirit in the illumination of our minds; count: 6
- phrase: the right understanding of the mind of god in the; count: 6
- phrase: be the word of god with faith divine and supernatural; count: 6
- phrase: believe the scripture to be the word of god in; count: 6

## Missing Word Samples

- word: self; pdf: 7; epub: 3
- word: 14-17; pdf: 4; epub: 0
- word: 16-18; pdf: 3; epub: 1

## Excess Word Samples

- word: psalms; pdf: 7; epub: 30
- word: ohn; pdf: 0; epub: 7
- word: digital; pdf: 0; epub: 6

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
