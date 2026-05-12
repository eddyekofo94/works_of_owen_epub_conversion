# Text Integrity Audit: Volume 3

- Status: **WARN**
- Warnings: 10
- PDF pages: 820
- EPUB text files: 45
- EPUB paragraphs/headings: 2623

## Coverage

- PDF content tokens: 288667
- EPUB content tokens: 285566
- Approximate PDF-to-EPUB coverage ratio: 0.9878
- Pages checked: 818
- Weak page matches: 14
- Dense source windows checked: 30948
- Missing dense source-window pages: 113
- Top-of-page body windows checked: 796
- Top-of-page windows skipped as unstable: 37
- Missing top-of-page body windows: 6
- Bottom-of-page body windows checked: 775
- Bottom-of-page windows skipped as unstable: 36
- Missing bottom-of-page body windows: 16

## Paragraphs

- Body paragraphs checked: 2368
- Possible faulty paragraph splits: 19
- Structural starts excluded from split warnings: 423
- Short fragments: 20
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 18
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 6
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 626
- EPUB enumerator markers: 559
- Missing enumerator marker forms: 2
- Enumerator sequence candidates: 1

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 12; sample: books embraced in this volume to all of them the general designation pneumatologia is
- page: 15; sample: reference to the father as giving sending him etc and in reference to his
- page: 16; sample: imparts no supernatural strength is not all we pray for when we pray for
- page: 30; sample: things themselves of the gospel in their own nature it is enmity against them
- page: 41; sample: far were they transported with vain-glory and desire of self advancement as that they
- page: 48; sample: of reasons of the importance use and necessity of the doctrine proposed to be
- page: 50; sample: unknown unto other men they in the meantime really finding themselves acted by power
- page: 59; sample: present undertaking is the open and horrible opposition that is made unto the spirit
- page: 61; sample: it is therefore the things themselves and not the pretences pretended that are the
- page: 66; sample: was preached concerning them was looked on as cunningly devised and artificially-framed fables to

## Missing Top-Of-Page Body Windows

- page: 139; sample: spiritual habit, permanent and abiding in the soul. But in neither of these senses can we be said to receive the Spirit of God, nor God to give him, if
- page: 335; sample: not; yet this darkness is no less effectual to bind them in a state of sin, without the powerful illumination of the Holy Ghost, than it is in the
- page: 408; sample: think that all the depravation of our nature consists in that of the sensitive part of the soul, or our affections; the vanity and folly of which opinion
- page: 429; sample: (1.) It is with most an immediate product of the power of their own lust. Especially is it so with them who together with their convictions receive
- page: 504; sample: If there were any other way or means whereby men might be sanctified or made holy, he would not have confined it unto the "faith that is in him;" at
- page: 779; sample: stormy and troubled; and they are all evil, "only evil continually," Genesis 6:5. Herein doth it "cast up mire and dirt." And those who

## Missing Bottom-Of-Page Body Windows

- page: 101; sample: Leviticus 9:24. they shouted, and fell on their faces,"
- page: 134; sample: oppression they were; for although they had permission and encouragement from Cyrus for their work, yet immediately upon his death
- page: 163; sample: 2 Epist. 1:20, 21, "Knowing this first, testimony of the apostle Peter:
- page: 173; sample: Genesis 18:1, 2; angels. Thus three men appeared unto Abraham,
- page: 194; sample: John 14:27. But he gives particular you, my peace I give unto you,"
- page: 327; sample: Isaiah 53:1-3. Suppose a man of good reputation for rejected by them,
- page: 392; sample: 2 Thessalonians 3:2, but it is peculiar to the or "all have not faith,"
- page: 406; sample: 1 Corinthians 4:7. Neither can any purpose of God the apostle,
- page: 407; sample: sins of the flesh," as the apostle speaks, the flesh, with the affections and lusts" thereof. Some men are inclined to
- page: 408; sample: word of God, which liveth and abideth for ever." John 1:13,

## Possible Paragraph Splits

- file: EPUB/ch008.xhtml; previous: uncians in homines Christum suum;" which Hierom rectified into "Formans montes, et creans ventum, et annuntians homini eloquium suum," discovering in his comment the mistake of the; next: But it is certain that, from the ambiguity of the word רוּ æח in this place, with the corrupt translations making mention of Christ in the next words, some who of old denied the de
- file: EPUB/ch011.xhtml; previous: s, because in the communication of internal grace unto us, we contribute nothing to the procurement of it, but are merely capable recipient subjects. And this grace is a quality or; next: Now, this giving of the Spirit, as it is the act of him by whom he is given, denotes authority, freedom, and bounty; and, on the part of them that receive him, privilege and advant
- file: EPUB/ch021.xhtml; previous: ned in the gospel as have their foundation in the law and light of nature. Such are all the moral duties which are taught therein. And two things may be observed concerning them: —; next: (1st.) That they are in some measure known unto men aliunde from other principles. The inbred concreated light of nature doth, though obscurely, teach and confirm them. So the apos
- file: EPUB/ch021.xhtml; previous: In this estate the gospel superadds two things unto the minds of men: —; next: (1st.) It directs us unto a right performance of these things, from a right principle, by a right rule, and to a right end and purpose; so that they, and we in them, may obtain acc
- file: EPUB/ch024.xhtml; previous: a person so convinced. is, — 1st, To inquire after and to receive the revelation of Jesus Christ, and the righteousness of God in him, John 1:12. And in order hereunto, he ought, —; next: (1st.) To own the sentence of the law under which he suffereth, justifying God in his righteousness and the law in its holiness, whatever be the issue of this dispensation towards
- file: EPUB/ch024.xhtml; previous: 2 dly . It is the duty of persons in such a condition to beware of entangling temptations; as, —; next: (1st.) That they have not attained such a degree of sorrow for sin and humiliation as is necessary unto them that are called to believe in Jesus Christ. There was, indeed, more rea
- file: EPUB/ch031.xhtml; previous: , then, in general premised, I shall comprise what I have farther to offer in the declaration and vindication of gospel sanctification and holiness in the two ensuing assertions: —; next: There is wrought and preserved in the minds and souls of all believers, by the Spirit of God, a supernatural principle or habit of grace and holiness, whereby they are made meet fo
- file: EPUB/ch031.xhtml; previous: l ordinance unto the increase of holiness in us, so his holy obedience, as proposed unto us, hath a peculiar efficacy unto that purpose beyond all other instituted examples; for, —; next: (1st.) We are often called to behold Christ, and to look upon him, or it is promised that we shall do so, Isaiah 45:22; Zechariah 12:10.
- file: EPUB/ch031.xhtml; previous: 1, may through faith in him be justified from all our sins, and saved from the wrath to come. But this we intend not; for, 1 Peter 2:24, and "receiving the atonement" made thereby,; next: (2dly.) He is of God proposed unto us in the gospel as the great pattern and exemplar of holiness, so as that, by God's appointment, our beholding and looking on him, in the way me
- file: EPUB/ch031.xhtml; previous: efficacy, by the way of motive, in the example of Christ, to incline us unto the imitation of him, that is not to be found in any other example, on any occasion whatever; because,; next: (1st.) Whatever is proposed unto us, in what he was or what he did, as our pattern and example, he was it, and did it, not for his own sake, but out of free and mere love unto us.

## Inline Structural Marker Candidates

- file: EPUB/ch001.xhtml; text: 3. — Divine Nature And Personality Of The Holy Spirit Proved And Vindicated. — Ends of our consideration of the dispensation of the Spirit — Principles premised thereunto — The nature of God the foundation of all religion — Divine revela...
- file: EPUB/ch001.xhtml; text: 2. By internal purification — Holiness peculiar to the gospel and its truth — Not discernible to the eye of carnal reason — Hardly understood by believers themselves — It passeth over into eternity — Hath in it a present glory — Is all t...
- file: EPUB/ch001.xhtml; text: 2. Power; the nature thereof; or what power is required in believers unto holy obedience; with its properties and effects in readiness and facility — Objections thereunto answered, and an inquiry on these principles after true holiness i...
- file: EPUB/ch010.xhtml; text: 1. Those of nature; 2. Those of grace; — or the works of the old and new creation. And we must inquire what are the especial operations of the Holy Spirit in and about these works, which shall be distinctly explained.
- file: EPUB/ch010.xhtml; text: And thus was it also in the earth. God first out of nothing created the earth, which comprised the whole inferior globe, which afterward divided itself into seas and dry land, as the heavens contain in that expression of their creation a...
- file: EPUB/ch011.xhtml; text: Now, this giving of the Spirit, as it is the act of him by whom he is given, denotes authority, freedom, and bounty; and, on the part of them that receive him, privilege and advantage. 1. Authority. He that gives anything hath authority ...
- file: EPUB/ch013.xhtml; text: 1. Voices; 2. Dreams; 3. Visions. And the accidental adjuncts of it are two: —
- file: EPUB/ch013.xhtml; text: 1. Symbolical actions; 2. Local mutations. The schoolmen, after Aquinas,
- file: EPUB/ch013.xhtml; text: 1. By our external senses; 2. By impressions on the fantasy or imagination;
- file: EPUB/ch017.xhtml; text: Christ the head of the new creation — Things premised in general unto the remaining work of the Spirit — Things presupposed unto the work of the Spirit towards the church — The love and grace of Father and Son — The whole work of the bui...

## Suspicious Large-Number Starts

- file: EPUB/ch008.xhtml; text: 14. But why, then, is he not called the "Spirit of God" also on this reason, because the prophets that spake by him treated wholly of God, the things and the will of God? This they will not say, for they acknowledge him
- file: EPUB/ch011.xhtml; text: 342. Whatever trouble befalls the minds of men upon the account of a sense of the guilt of sin; whatever darkness and disconsolation they may undergo through the displeasure of God, and his withdrawing of the wonted infl
- file: EPUB/ch013.xhtml; text: 22. q. 174, a. 1, do commonly reduce the means of revelation unto three heads. For whereas there are three ways whereby we come to know anything, —
- file: EPUB/ch021.xhtml; text: 344. 89 I confess these are the words of one who seems not much to consider what he says, so as that it may serve his present turn in reviling and reproaching other men; for he considers not that, by this description of
- file: EPUB/ch024.xhtml; text: 10. Those who were thus converted unto God in the primitive times of the church were, upon their confession or profession hereof, admitted into church-society and to a participation of all the mysteries thereof. And this
- file: EPUB/ch036.xhtml; text: 11. And a supposition hereof lies at the bottom of that blessed exhortation of our apostle, Colossians 3:12, 13, "Put on therefore, as the elect of God, holy and beloved, bowels of mercies, kindness, humbleness of mind,

## Short Fragments

- file: EPUB/ch017.xhtml; text: Thus,
- file: EPUB/ch019.xhtml; text: Therefore,
- file: EPUB/ch019.xhtml; text: And,
- file: EPUB/ch020.xhtml; text: For,
- file: EPUB/ch021.xhtml; text: Hence it follows: —
- file: EPUB/ch023.xhtml; text: For, —
- file: EPUB/ch024.xhtml; text: And sorrow always accompanieth it.
- file: EPUB/ch024.xhtml; text: 30.
- file: EPUB/ch024.xhtml; text: 1.
- file: EPUB/ch026.xhtml; text: And in this place, —

## Missing Enumerator Markers

- marker: [1st.]; pdf: 6; epub: 1; examples: [{'location': 'pdf:p439', 'context': 'hings which will present themselves in such a case as means of relief are of two sorts: — [1st.] Such as the fears and superstitions of men have suggested or will suggest. That which hath raised all ...
- marker: [2dly.]; pdf: 7; epub: 1; examples: [{'location': 'pdf:p439', 'context': 'stition consists in endeavors to quiet and charm the consciences of men convinced of sin. [2dly.] That which is pressed with most vehemency and plausibility, being suggested by the law itself, in a w...

## Enumerator Sequence Candidates

- file: EPUB/ch007.xhtml; marker: [18]; family: bracket_decimal; context: before them, — namely, the old scoffing heathens; for so doth Lucian, in his Philopatris [18], speak in imitation of a Christian by way of scorn, Λέγε παρὰ τοῦ Πνεύματος δύναμιν τοῦ λόγου λαβών — "Speak out now, receiving power or abilit...

## Repeated Windows

- phrase: both to will and to do of his good pleasure; count: 7
- phrase: the name of the father and of the son and; count: 6
- phrase: in us both to will and to do of his; count: 6
- phrase: us both to will and to do of his good; count: 6
- phrase: work of the spirit of god in the new creation; count: 5
- phrase: name of the father and of the son and of; count: 5
- phrase: of the father and of the son and of the; count: 5
- phrase: the father and of the son and of the holy; count: 5
- phrase: father and of the son and of the holy ghost; count: 5
- phrase: the new man which after god is created in righteousness; count: 5

## Missing Word Samples

- word: ft; pdf: 141; epub: 0
- word: pneu; pdf: 94; epub: 0
- word: kai; pdf: 93; epub: 0
- word: ma; pdf: 75; epub: 0
- word: th; pdf: 73; epub: 4
- word: tou; pdf: 66; epub: 0
- word: ta; pdf: 41; epub: 0
- word: wr; pdf: 33; epub: 0
- word: tw; pdf: 32; epub: 0
- word: ou; pdf: 31; epub: 0

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
