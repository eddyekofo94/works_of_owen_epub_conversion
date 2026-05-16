# Text Integrity Audit: Volume 4

- Status: **WARN**
- Warnings: 10
- PDF pages: 653
- EPUB text files: 71
- EPUB paragraphs/headings: 2342

## Coverage

- PDF content tokens: 221791
- EPUB content tokens: 223108
- Approximate PDF-to-EPUB coverage ratio: 0.9982
- Pages checked: 644
- Weak page matches: 3
- Dense source windows checked: 24388
- Missing dense source-window pages: 232
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 624
- Top-of-page windows skipped as unstable: 29
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 607
- Bottom-of-page windows skipped as unstable: 17
- Missing bottom-of-page body windows: 2

## Paragraphs

- Body paragraphs checked: 2062
- Possible faulty paragraph splits: 34
- Structural starts excluded from split warnings: 386
- Short fragments: 25
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 8
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 26
- Roman heading candidates: 9
- Overlong heading candidates: 1
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 370
- EPUB enumerator markers: 375
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 3; sample: continued book vi part the reason of faith refatory ote by the ditor preface
- page: 9; sample: prefatory note he subject of this treatise belongs to the office of the holy
- page: 12; sample: preface aving added brief account of the design order and method of the ensuing
- page: 15; sample: of god with faith divine and supernaural chapter the subject stated preliminary remarks he
- page: 16; sample: warning and instruction of others jude 14 15 and to noah who became thereby
- page: 17; sample: being and power this they do undeniably and infallibly psalm 19 romans 19-21 yet
- page: 19; sample: devil of the ways means and degrees whereof have discoursed elsewhere f1 hereon god
- page: 20; sample: and testimony with threatening of curse unto the contrary malachi 4-6 so the writings
- page: 21; sample: is the only repository of all divine supernatural revelation psalm 19 isaiah 20 timothy
- page: 22; sample: the word see matthew 14 15 corinthians 18-20 ephesians 11-15 timothy 15 the church

## Missing Top-Of-Page Body Windows

- page: 35; sample: wisdom before all the world, Deuteronomy 4:6-8. Now, we shall not need to consider what were the first attempts of other nations in

## Missing Bottom-Of-Page Body Windows

- page: 44; sample: testimony may rationally be supposed to be so far influenced by self- interest as to be of little validity.
- page: 367; sample: matter of it, namely, "mercy" and "grace," and by the only object of it, "God on a throne of grace."

## Possible Paragraph Splits

- file: EPUB/ch007.xhtml; previous: MY design requires that I should confine my discourse unto as narrow bounds as possible, and I shall so do, showing, —; next: What it is in general infallibly to believe the Scripture to be the word of God, and what is the ground and reason of our so doing; or, what it is to believe the Scripture to be th
- file: EPUB/ch013.xhtml; previous: As to the first part of the design, the things that follow are proposed: —; next: Unto the inquiry, on what grounds, or for what reason, we believe the Scripture to be the word of God, many things supposed, as on all hands agreed upon, whose demonstration or pro
- file: EPUB/ch016.xhtml; previous: ed; the question considered is declared to relate to the method by which we attain to a right perception of the mind of God in Scripture, and this method is described as twofold: —; next: Through a principal efficient cause; and,
- file: EPUB/ch016.xhtml; previous: The Holy, Spirit is represented as the EFFICIENT CAUSE, and an inquiry follows: —; next: Into the evidence of the work of the Spirit in the communication of spiritual understanding; — various testimonies from Scripture are adduced, involving a minute discussion of [Psa
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
- file: EPUB/ch016.xhtml; text: Into the evidence of the work of the Spirit in the communication of spiritual understanding; — various testimonies from Scripture are adduced, involving a minute discussion of [Psalms 119:18] Psalm 119:18, 2 Corinthians 3:13-18, Isaiah 2...
- file: EPUB/ch024.xhtml; text: 1. Spiritual; 2. Disciplinary; 3. Ecclesiastical. Some instances on each head will farther clear what I intend.
- file: EPUB/ch034.xhtml; text: 1. We know not our own wants; 2. We know not the plies of them that are expressed in the promises of God; and, 3. We know not the end whereunto what we pray for is to be directed, which I add unto the former. Without the knowledge and un...
- file: EPUB/ch053.xhtml; text: 2. It is for the safe-keeping or preservation of that which a seal is set upon. So things precious and highly valuable are sealed up, that they may be kept safe and inviolable. So, on the other hand, when Job expressed his apprehension t...
- file: EPUB/ch062.xhtml; text: [1.] The evil which we are hereby delivered from is, the danger of being perniciously and destructively deceived by false doctrines, errors, and heresies; which then began, and have ever since, in all ages, continued to infest the church...

## Suspicious Large-Number Starts

- file: EPUB/ch007.xhtml; text: 23. But if, moreover, we are asked a reason of our faith or hope, or why we believe the things we do profess, as God to be one in three persons, Jesus Christ to be the Son of God, we do not answer, "Because so it is, for
- file: EPUB/ch008.xhtml; text: 21. On this account, and no other, did they themselves receive the Scripture, as also believe and yield obedience unto the things contained in it. Neither would they admit that their testimony was received if the whole w
- file: EPUB/ch010.xhtml; text: 18. This gave them, indeed, sufficient assurance; but whereinto shall they resolve their faith who heard not this testimony?
- file: EPUB/ch011.xhtml; text: 25. An invasion may be made on the outward duties that conscience disposeth unto, but none can be so upon its internal actings. No power under heaven can cause conscience to think, act, or judge otherwise than it doth by
- file: EPUB/ch019.xhtml; text: 27. Speaking unto these very persons, that is, the leaders of them, he saith, "I have kept back nothing that was profitable unto you, but declared unto you all the counsel of God," — namely, "what is the hope of his call
- file: EPUB/ch019.xhtml; text: 23. And with respect hereunto doth the apostle give that advice unto us as our duty, "Let no man deceive himself. If any man among you seemeth to be wise in this world, let him become a fool, that he may be wise," 1 Cori
- file: EPUB/ch019.xhtml; text: 40. It proved no otherwise, and that to their eternal ruin. Yet do I not judge all them to be practically blind who do not doctrinally own the receiving of this wisdom and light from above; for although we make not ourse
- file: EPUB/ch021.xhtml; text: 18. And the expression, though in part metaphorical, is eminently instructive in the nature of this work; for suppose the nearest and best-disposed proposition of any object unto our bodily eyes, with an external light p
- file: EPUB/ch021.xhtml; text: 11. Hence they so frequently and fervently prayed for understanding, as we have seen in the instance of David. Wherefore,
- file: EPUB/ch023.xhtml; text: 16. And our Savior assures us that heavenly things are much more above our comprehension than earthly, John 3:12. Such as these are, the Trinity, or the subsistence of one single divine nature in three persons; the incar

## Roman Heading Candidates

- file: EPUB/ch011.xhtml; text: did. It is, therefore, folly to pretend that things so made known of God are not infallibly true and certain, because they are not obvious unto the first conceptions of natural light, without the due exercise of reason,
- file: EPUB/ch016.xhtml; text: II. As to the MEANS for the understanding of Scripture, two kinds are specified: —
- file: EPUB/ch018.xhtml; text: mill. Whatever we know, be it of what sort it will, we know it in and by the use of our reason; and what we conceive, we do it by our own understanding: only the inquiry is, whether there be not an especial work of the H
- file: EPUB/ch019.xhtml; text: did. And we find that the apostle reneweth his prayer for them again unto the same purpose with great fervency, [Ephesians 3:14] -19. All the difference ariseth from hence, that the apostle judgeth that over and above th
- file: EPUB/ch019.xhtml; text: did. Whoever, therefore, hath this ability to know the mysteries of the gospel, he hath it by free gift or donation from God. He hath received it, and may not boast as if it were from himself, and that he had not receive
- file: EPUB/ch020.xhtml; text: mill. The Scripture we own as the only rule of our faith, as the only treasury of all sacred truths. The knowledge we aim at is, the "full assurance of understanding" in the mind and will of God, revealed therein. The so
- file: EPUB/ch021.xhtml; text: did. Wherefore, although there be in the gospel and the doctrine of it an illustrious representation of the glory of God in Christ, yet are we not able of ourselves to discern it, until the Holy Spirit by an act of his a
- file: EPUB/ch041.xhtml; text: did. In the meantime, I do yet judge that the use of them is in itself obstructive of all the principal ends of prayer and sacred worship. Where they are alone used, they are opposite to the edification of the church; an
- file: EPUB/ch059.xhtml; text: did. But whereas their ministry was subordinate unto that of the apostles, they were by them guided as to the particular places wherein they were to exercise their power and discharge their office for a season. This is e

## Overlong Heading Candidates

- file: EPUB/ch047.xhtml; tag: h3; text: The Holy Ghost the comforter of the church by way of office — How he is the church's advocate — John 14:16; 1 John 2:1, 2; John 16:8-11 opened.

## Short Fragments

- file: EPUB/ch001.xhtml; text: Appendix.
- file: EPUB/ch005.xhtml; text: May 11, 1677.
- file: EPUB/ch013.xhtml; text: Wherefore, —
- file: EPUB/ch016.xhtml; text: — ED.
- file: EPUB/ch018.xhtml; text: ΣΨΝΕΣΙΣ ΠΝΕΨΜΑΤΙΚΗ.
- file: EPUB/ch034.xhtml; text: For, —
- file: EPUB/ch037.xhtml; text: I say, therefore, —
- file: EPUB/ch039.xhtml; text: And,
- file: EPUB/ch039.xhtml; text: Again,
- file: EPUB/ch043.xhtml; text: and

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

- word: ord; pdf: 67; epub: 0
- word: self; pdf: 7; epub: 3
- word: econdly; pdf: 4; epub: 0
- word: hat; pdf: 4; epub: 0
- word: 14-17; pdf: 4; epub: 0
- word: od; pdf: 5; epub: 2
- word: irst; pdf: 3; epub: 0
- word: hirdly; pdf: 3; epub: 0
- word: 10-12; pdf: 3; epub: 1
- word: 16-18; pdf: 3; epub: 1

## Excess Word Samples

- word: psalms; pdf: 7; epub: 37
- word: ed; pdf: 1; epub: 16
- word: note; pdf: 8; epub: 15
- word: prefatory; pdf: 7; epub: 14

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
