# Text Integrity Audit: Volume 4

- Status: **WARN**
- Warnings: 8
- PDF pages: 653
- EPUB text files: 72
- EPUB paragraphs/headings: 2317

## Coverage

- PDF content tokens: 220247
- EPUB content tokens: 220482
- Approximate PDF-to-EPUB coverage ratio: 0.9942
- Pages checked: 644
- Weak page matches: 3
- Dense source windows checked: 24832
- Missing dense source-window pages: 64
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 624
- Top-of-page windows skipped as unstable: 29
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 607
- Bottom-of-page windows skipped as unstable: 22
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 2015
- Possible faulty paragraph splits: 30
- Structural starts excluded from split warnings: 326
- Short fragments: 26
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 9
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 3
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 416
- EPUB enumerator markers: 375
- Missing enumerator marker forms: 3
- Enumerator sequence candidates: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 9; sample: prefatory note the subject of this treatise belongs to the office of the holy
- page: 13; sample: authority of the scripture which they frequently meet withal and that many know not
- page: 25; sample: scripture to be the word of god affirmed my design requires that should confine
- page: 27; sample: been so instructed by them whom they have sufficient reason to give credit unto
- page: 64; sample: were accused to have followed cunningly devised fables they appealed unto moses and the
- page: 74; sample: called faith with respect unto divine revelation and is accepted with god as such
- page: 79; sample: neither do we nor can we rationally answer by it unto this question why
- page: 95; sample: is what he requireth it unto it is to this law to this law
- page: 148; sample: quam ulla argumenta persuadet ut ad firmiter credendum trahi se intelligant tom in thom
- page: 156; sample: infallible conduct in these things but probably the near ap preach of the daily-expected

## Possible Paragraph Splits

- file: EPUB/ch007.xhtml; previous: M Y design requires that I should confine my discourse unto as narrow bounds as possible, and I shall so do, showing, —; next: What it is in general infallibly to believe the Scripture to be the word of God, and what is the ground and reason of our so doing; or, what it is to believe the Scripture to be th
- file: EPUB/ch013.xhtml; previous: As to the first part of the design, the things that follow are proposed: —; next: Unto the inquiry, on what grounds, or for what reason, we believe the Scripture to be the word of God, many things supposed, as on all hands agreed upon, whose demonstration or pro
- file: EPUB/ch016.xhtml; previous: ed; the question considered is declared to relate to the method by which we attain to a right perception of the mind of God in Scripture, and this method is described as twofold: —; next: Through a principal efficient cause; and,
- file: EPUB/ch016.xhtml; previous: The Holy, Spirit is represented as the EFFICIENT CAUSE, and an inquiry follows: —; next: Into the evidence of the work of the Spirit in the communication of spiritual understanding; — various testimonies from Scripture are adduced, involving a minute discussion of Psal
- file: EPUB/ch016.xhtml; previous: l scriptural expressions descriptive of it, such as "opening the eyes," "translating out of darkness into light," "giving understanding," "teaching," and "shining into our hearts,"; next: As preparatory to what follows in explanation of the Spirit's work in enlightening the mind, a digression is introduced on the causes of spiritual ignorance, which are classified i
- file: EPUB/ch016.xhtml; previous: removal of all those causes of spiritual ignorance, by communicating spiritual light, purging from corrupt affections, and implanting spiritual habits and principles, is explained,; next: His work for the production of the same effect by means of Scripture itself next comes under review; and under this head three points in regard,
- file: EPUB/ch016.xhtml; previous: (3.) Ecclesiastical, under which the deference due to catholic tradition, the consent of the fathers, and pious authorship, is estimated,; next: — ED.
- file: EPUB/ch018.xhtml; previous: d apprehend his mind and will as revealed in the Scripture, and without which we cannot so do. The substance, therefore, of the ensuing discourse may be reduced unto these heads: —; next: That we stand not in need of any new divine afflations, or immediate prophetical inspirations, to enable us to understand the Scripture, or the mind and will of God as revealed the
- file: EPUB/ch018.xhtml; previous: Wherefore, principally, it is asserted, —; next: That there is an especial work of the Holy Spirit, in the supernatural illumination of our minds, needful unto the end proposed, — namely, that we may aright, and according unto ou
- file: EPUB/ch018.xhtml; previous: reby any man may answer the mind and will of God, or comply with his own duty in all that he may be called to do or suffer in this world in his especial circumstances. Wherefore, —; next: The certainty and assurance that we may have and ought to have of our right understanding the mind of God in the Scripture, either in general or as to any especial doctrine, doth n

## Inline Structural Marker Candidates

- file: EPUB/ch001.xhtml; text: 8. - The duty of external prayer by virtue of a spiritual gift explained and vindicated 9. - Duties inferred from the preceding discourse.
- file: EPUB/ch001.xhtml; text: 2. - General adjuncts or properties of the office of a comforter, as exercised by the Holy Spirit 3. - Unto whom the Holy Spirit is promised and given as a comforter, or the object of his acting in this office.
- file: EPUB/ch001.xhtml; text: 1. - Spiritual gifts, their names and signification 2. - Differences between spiritual gifts and saying grace.
- file: EPUB/ch007.xhtml; text: That yet, moreover, God requires of us that we believe them to be his word with faith divine, supernatural, and infallible: IV. Evidence the grounds and reasons whereon we do so believe, and ought so to do.
- file: EPUB/ch024.xhtml; text: 1. Spiritual; 2. Disciplinary; 3. Ecclesiastical. Some instances on each head will farther clear what I intend.
- file: EPUB/ch026.xhtml; text: 2. Consent of the fathers; 3. The endeavors of any persons holy and learned who have gone before us in the investigation of the truth, and expressed their minds in writing, for the edification of others, whether of old or of late. These ...
- file: EPUB/ch034.xhtml; text: 1. We know not our own wants; 2. We know not the plies of them that are expressed in the promises of God; and, 3. We know not the end whereunto what we pray for is to be directed, which I add unto the former. Without the knowledge and un...
- file: EPUB/ch053.xhtml; text: 2. It is for the safe-keeping or preservation of that which a seal is set upon. So things precious and highly valuable are sealed up, that they may be kept safe and inviolable. So, on the other hand, when Job expressed his apprehension t...
- file: EPUB/ch062.xhtml; text: [1.] The evil which we are hereby delivered from is, the danger of being perniciously and destructively deceived by false doctrines, errors, and heresies; which then began, and have ever since, in all ages, continued to infest the church...

## Suspicious Large-Number Starts

- file: EPUB/ch023.xhtml; text: 16. And our Savior assures us that heavenly things are much more above our comprehension than earthly, John 3:12. Such as these are, the Trinity, or the subsistence of one single divine nature in three persons; the incar
- file: EPUB/ch059.xhtml; text: 11. But whereas our Savior, in that commission by virtue whereof they were to act after his resurrection, had extended their office and power expressly to "all nations," Matthew 28:19, or to "every creature in all the wo
- file: EPUB/ch062.xhtml; text: 11. And it was appointed by him to be the ministry of that peace between God and man which was made therein and thereby, Ephesians 2:14,16,17; for when he had made this peace by the blood of the cross, he preached it in

## Roman Heading Candidates

- file: EPUB/ch016.xhtml; text: II. As to the MEANS for the understanding of Scripture, two kinds are specified: —

## Short Fragments

- file: EPUB/ch001.xhtml; text: CONTENTS ΠΗΕΥΜΑΤΟΛΟΓΙΑ ?
- file: EPUB/ch001.xhtml; text: The Preface
- file: EPUB/ch001.xhtml; text: The Preface.
- file: EPUB/ch005.xhtml; text: May 11, 1677.
- file: EPUB/ch013.xhtml; text: APPENDIX.
- file: EPUB/ch013.xhtml; text: Wherefore, —
- file: EPUB/ch016.xhtml; text: — ED.
- file: EPUB/ch018.xhtml; text: ΣΥΝΕΣΙΣ ΠΝΕΥΜΑΤΙΚΗ .
- file: EPUB/ch034.xhtml; text: For, —
- file: EPUB/ch037.xhtml; text: I say, therefore, —

## Missing Enumerator Markers

- marker: [1st.]; pdf: 2; epub: 0; examples: [{'location': 'pdf:p212', 'context': 's of their minds, which hinder them from receiving instruction." But ff it be so, then, — [1st.] It is supposed that man also in their teachings can give us an understanding as well as the Son of God...
- marker: [2dly.]; pdf: 1; epub: 0; examples: [{'location': 'pdf:p212', 'context': 'learn, and have no darling lusts or vicious habits of mind to hinder them from learning. [2dly.] Seeing he hath taken this work on himself, and designs its accomplishment, cannot the Son of God by hi...
- marker: [3dly.]; pdf: 1; epub: 0; examples: [{'location': 'pdf:p214', 'context': 'and condition with the conceptions of every one that will pretend unto this inspiration. [3dly.] The pretense visibly confutes itself in the manifold mutual contradictions of them that pretend unto i...

## Repeated Windows

- phrase: we believe the scripture to be the word of god; count: 21
- phrase: to believe the scripture to be the word of god; count: 17
- phrase: the mind and will of god as revealed in the; count: 11
- phrase: believe the scripture to be the word of god with; count: 9
- phrase: to be the word of god with faith divine and; count: 8
- phrase: be the word of god with faith divine and supernatural; count: 7
- phrase: mind and will of god as revealed in the scripture; count: 7
- phrase: of the holy spirit in the illumination of our minds; count: 6
- phrase: the right understanding of the mind of god in the; count: 6
- phrase: believe the scripture to be the word of god in; count: 6

## Missing Word Samples

- word: th; pdf: 31; epub: 2
- word: tou; pdf: 29; epub: 0
- word: ft; pdf: 23; epub: 0
- word: tw; pdf: 20; epub: 0
- word: kai; pdf: 16; epub: 0
- word: pneu; pdf: 13; epub: 0
- word: ou; pdf: 12; epub: 0
- word: av; pdf: 10; epub: 0
- word: lo; pdf: 10; epub: 1
- word: ejn; pdf: 9; epub: 0

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
