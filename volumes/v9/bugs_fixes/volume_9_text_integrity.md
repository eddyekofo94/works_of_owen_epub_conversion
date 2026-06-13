# Text Integrity Audit: Volume 9

- Status: **WARN**
- Warnings: 10
- PDF pages: 778
- EPUB text files: 102
- EPUB paragraphs/headings: 3511

## Coverage

- PDF content tokens: 254653
- EPUB content tokens: 254435
- Approximate PDF-to-EPUB coverage ratio: 0.9961
- Pages checked: 771
- Weak page matches: 3
- Dense source windows checked: 31520
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 5
- Missing front CONTENTS pages: 4
- Top-of-page body windows checked: 751
- Top-of-page windows skipped as unstable: 27
- Missing top-of-page body windows: 9
- Bottom-of-page body windows checked: 697
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 2

## Paragraphs

- Body paragraphs checked: 3023
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 406
- Short fragments: 38
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 1
- Roman heading candidates: 4
- Overlong heading candidates: 9
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 834
- EPUB enumerator markers: 842
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 4

## Greek / Hebrew

- PDF Greek words: 140
- EPUB Greek words: 140
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 34
- EPUB Hebrew words: 34
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 3
- Missing Greek clauses: 0
- Hebrew clauses checked: 1
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 597
- EPUB Latin words: 635
- EPUB Tagged Latin words: 90
- Latin word coverage ratio: 0.9933
- Latin word tagging ratio: 0.1417
- Latin clauses checked: 13
- Missing Latin clauses: 0
- Tagged Latin runs checked: 43
- Translated Latin runs: 3
- Latin translation ratio: 0.0698

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 3; sample: contents of vol part sermon published prefatory note by the editor seasonable words for
- page: 4; sample: discourse seeing the act of closing with christ is secret and hidden and the
- page: 5; sample: the excellency of christ the use and advantage of faith in time of public
- page: 6; sample: lord's death till he come corinthians 23-26 discourses and if be lifted up from
- page: 7; sample: part sermon published prefatory note the following is the first of owen's posthumous sermons
- page: 8; sample: that city and country are crying watchman what of the night watchman what of
- page: 10; sample: unto idolatry secondly their idolatry the idolatry that there began consisted in image worship
- page: 26; sample: posthumous sermons part sermons published prefatory note under the second division of the posthumous
- page: 29; sample: affirmation is laid down the promises the promises of god the promises of god
- page: 42; sample: glorified as god as our god he that gives him that gives him what

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.25; sample: contents of vol part sermon published prefatory note by the editor seasonable words for english protestants part sermons published prefatory note by the editor the strength of faith
- page: 4; hit_ratio: 0.25; sample: discourse seeing the act of closing with christ is secret and hidden and the special times and seasons of our conversion unto god are unknown unto most what
- page: 5; hit_ratio: 0.5; sample: the excellency of christ the use and advantage of faith in time of public calamity the use of faith under reproaches and persecutions the use of faith if
- page: 6; hit_ratio: 0.5; sample: also he took the cup when he had supped saying this cup is the new testament in my blood this do ye as oft as ye drink it

## Missing Top-Of-Page Body Windows

- page: 151; sample: Philippians 4:11, "I have learned it," saith he; This was Paul's frame,
- page: 273; sample: SERMON 17. F16 THE DIVINE POWER OF THE GOSPEL.
- page: 370; sample: SERMON 24. F26 GOD'S WITHDRAWING HIS PRESENCE, THE CORRECTION OF
- page: 385; sample: SERMON 25. F27 THE BEAUTY AND STRENGTH OF ZION.
- page: 419; sample: SERMON 27. F31 THE CHRISTIAN'S WORK OF DYING DAILY.
- page: 441; sample: SERMON 30. F37 THE EVIL AND DANGER OF OFFENCES.
- page: 612; sample: SERMON 10.F64 THE USE AND ADVANTAGE OF FAITH
- page: 622; sample: SERMON 11.F65 THE USE OF FAITH UNDER REPROACHES AND
- page: 705; sample: are invited to feast upon the sacrifice. The sacrifice is offered; Christ is the sacrifice, — God's passover; God makes a feast upon it, and invites his

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 4; sample: Ministerial Endowments The Work Of The Spirit. The Duty Of A Pastor.

## Suspicious Large-Number Starts

- file: EPUB/ch023.xhtml; text: 18 I shall now give the reasons why we ought not in any thing to be ashamed of the gospel of Christ. I speak unto persons that are under a conviction that such and such things belong unto the gospel. If we are not, what

## Roman Heading Candidates

- file: EPUB/ch006.xhtml; text: I. As to the former of these, —
- file: EPUB/ch045.xhtml; text: II. I shall now proceed to show when a corruption is habitually prevalent. And here is a large field before me, but I shall only speak some few things: 1. When a man doth choose, or willingly embrace, known occasions of
- file: EPUB/ch060.xhtml; text: I. The subject treated of: —
- file: EPUB/ch071.xhtml; text: III. We may see three things concerning ourselves: —

## Overlong Heading Candidates

- file: EPUB/ch002.xhtml; tag: h3; text: "To the Reader — Upon the desire of some interested in the publication of this sermon, I have perused it, and do communicate these my thoughts concerning it. "There appear unto me in it those two things, which do above all others commend...
- file: EPUB/ch044.xhtml; tag: h1; text: DISCOURSE 7. 44 Question. When our own faith is weakened as to the hearing of our prayers — when we ourselves are hindered within ourselves from believing the answer of our prayers, have no ground to expect we should be heard, or no grou...
- file: EPUB/ch053.xhtml; tag: h3; text: "To The Reader, — The following Discourses were preached by that truly venerable divine in the last century, Dr John Owen: and, in order to be fully satisfied they are genuine, Mrs Cooke of Stoke Newington, by this means informs the read...
- file: EPUB/ch060.xhtml; tag: h1; text: SERMON 7. 61 "My heart is inditing a good matter: I speak of the things which I have made touching the King; my tongue is the pen of a ready writer. Thou art fairer than the children of men; grace is poured into thy lips: therefore God h...
- file: EPUB/ch072.xhtml; tag: h1; text: DISCOURSE 2. 69 "The cup of blessing which we bless, is it not the communion of the blood of Christ? The bread which we break, is it not the communion of the body of Christ?" — 1 Corinthians 10:16.
- file: EPUB/ch073.xhtml; tag: h1; text: DISCOURSE 3. 70 "The cup of blessing which we bless, is it not the communion of the blood of Christ? The bread which we break, is it not the communion of the body of Christ?" — 1 Corinthians 10:16.
- file: EPUB/ch078.xhtml; tag: h1; text: DISCOURSE 8. 76 "Christ also hath once suffered for sins, the just for the unjust, that he might bring us to God; being put to death in the flesh, but quickened by the Spirit." — 1 Peter 3:18.
- file: EPUB/ch080.xhtml; tag: h1; text: DISCOURSE 10. 78 "Teaching them to observe all things whatsoever I have commanded you: and, lo, I am with you alway, even unto the end of the world." — Matthew 28:20.
- file: EPUB/ch089.xhtml; tag: h1; text: DISCOURSE 19. 86 "I am crucified with Christ: nevertheless I live; yet not I, but Christ liveth in me: and the life which I now live in the flesh I live by the faith of the Son of God, who loved me, and gave himself for me." — Galatians ...

## Short Fragments

- file: EPUB/ch008.xhtml; text: To this end, —
- file: EPUB/ch014.xhtml; text: The grounds of it are: —
- file: EPUB/ch015.xhtml; text: The grounds hereof are, —
- file: EPUB/ch016.xhtml; text: Come we now to the uses.
- file: EPUB/ch017.xhtml; text: Use 1. Of trial or examination.
- file: EPUB/ch017.xhtml; text: Jehu's spirit spoiled his work.
- file: EPUB/ch020.xhtml; text: WE shall now proceed to the uses.
- file: EPUB/ch020.xhtml; text: Use all diligence in this matter.
- file: EPUB/ch020.xhtml; text: Use your day.
- file: EPUB/ch022.xhtml; text: I answer, In two things: —

## Enumerator Sequence Candidates

- file: EPUB/ch013.xhtml; marker: (2.); family: paren_decimal; context: (2.) I come now to show what it is to humble ourselves to the law of his providence.
- file: EPUB/ch018.xhtml; marker: (2.); family: paren_decimal; context: (2.) That which in the next place is considerable, is the proposing of the ingredients that lie in the motive to holiness, here expressed by the apostle, "Seeing that these things shal
- file: EPUB/ch020.xhtml; marker: (2.); family: paren_decimal; context: (2.) The second thing that God doth, in giving up an unhealed land unto barrenness, is his judicial hardening of them, or leaving them to hardness and impenitency, that so they may fil
- file: EPUB/ch025.xhtml; marker: [2.]; family: bracket_decimal; context: [2.] There are some distresses that, in their own nature, refuse all relief that you can tender them, but only what is derived from the fountain itself, — the nature of God. Zion's dis

## Repeated Windows

- phrase: discourse discourse discourse discourse discourse discourse discourse discourse discourse discourse; count: 16
- phrase: loved us and washed us from our sins in his; count: 6
- phrase: us and washed us from our sins in his own; count: 6
- phrase: and washed us from our sins in his own blood; count: 6
- phrase: is so filled with sin against the holy one of; count: 5
- phrase: so filled with sin against the holy one of israel; count: 5
- phrase: and the gates of hell shall not prevail against it; count: 5
- phrase: who loved us and washed us from our sins in; count: 5
- phrase: land is filled with sin against the holy one of; count: 4
- phrase: is filled with sin against the holy one of israel; count: 4

## Missing Word Samples

- word: editor; pdf: 5; epub: 1
- word: sufficiency; pdf: 3; epub: 1

## Excess Word Samples

- word: psalms; pdf: 8; epub: 19
- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 2; epub: 11
- word: historical; pdf: 0; epub: 8
- word: greek; pdf: 8; epub: 15
- word: footnotes; pdf: 0; epub: 7
- word: modern; pdf: 0; epub: 7
- word: hebrew; pdf: 7; epub: 13
- word: edition; pdf: 5; epub: 11

## Untagged Latin Word Samples

- word: iii; epub: 33; tagged: 0
- word: door; epub: 28; tagged: 0
- word: alas; epub: 24; tagged: 2
- word: undergo; epub: 16; tagged: 0
- word: communicate; epub: 15; tagged: 0
- word: ultimate; epub: 14; tagged: 0
- word: relate; epub: 13; tagged: 0
- word: meditate; epub: 10; tagged: 0
- word: splendor; epub: 9; tagged: 0
- word: incarnate; epub: 9; tagged: 0

## Untranslated Latin Samples

- phrase: Quis talia fando
- phrase: anguis in herba
- phrase: Gloria est
- phrase: de aliquo fama cum
- phrase: laus bonorum, incorrupta
- phrase: bene judicantium de excellenti
- phrase: is "peccata missa facere
- phrase: water break out in the wilderness, and streams in the desert,
- phrase: Amici, dum vivimus, vivamus
- phrase: Marcus ‡ Brutus

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
