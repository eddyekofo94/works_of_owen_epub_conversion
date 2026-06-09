# Text Integrity Audit: Volume 11

- Status: **WARN**
- Warnings: 15
- PDF pages: 815
- EPUB text files: 31
- EPUB paragraphs/headings: 2077

## Coverage

- PDF content tokens: 303982
- EPUB content tokens: 297400
- Approximate PDF-to-EPUB coverage ratio: 0.9762
- Pages checked: 809
- Weak page matches: 4
- Dense source windows checked: 36957
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 2
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 791
- Top-of-page windows skipped as unstable: 28
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 791
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 10

## Paragraphs

- Body paragraphs checked: 1771
- Possible faulty paragraph splits: 14
- Structural starts excluded from split warnings: 276
- Short fragments: 23
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 8
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 1
- Overlong heading candidates: 1
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 263
- EPUB enumerator markers: 267
- Missing enumerator marker forms: 3
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 2084
- EPUB Greek words: 2080
- Greek word coverage ratio: 0.9931
- PDF Hebrew words: 0
- EPUB Hebrew words: 0
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 117
- Missing Greek clauses: 1
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 7075
- EPUB Latin words: 7005
- EPUB Tagged Latin words: 355
- Latin word coverage ratio: 0.9864
- Latin word tagging ratio: 0.0507
- Latin clauses checked: 416
- Missing Latin clauses: 0
- Tagged Latin runs checked: 34
- Translated Latin runs: 25
- Latin translation ratio: 0.7353

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
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: explained and confirmed prefatory note by the editor the dedication the epistle dedicatory preface
- page: 4; sample: of them evinced in sundry instances of vocation justification and sanctification isaiah 27-31 opened
- page: 5; sample: samuel farther considered and its unsuitableness to illustrate romans 28-31 proved interpretation of scripture
- page: 6; sample: chapter argument from the covenant of grace an entrance into the consideration of the
- page: 7; sample: who intended in that promise not judas the accomplishment of the premise the testimony
- page: 8; sample: and fountain of all goodness to his people in his own good pleasure the
- page: 9; sample: the death of christ and the necessity of faith and obedience reconciled sundry considerations
- page: 10; sample: effects ascribed in the scripture to his so doing as union with christ union
- page: 11; sample: the argument and of the first part of this treatise chapter the improvement of
- page: 12; sample: promises more particularly and more largely insisted on chapter arguments against the doctrine considered

## Missing Top-Of-Page Body Windows

- page: 19; sample: WITH SOME DIGRESSIONS CONCERNING 1. The Immediate effects of the Death of Christ.

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 18; sample: In a Full Answer to the Discourse of Mr. JOHN GOODWIN against it, in his Book Entituled REdemption .Redeemed.
- page: 53; sample: aujtai~v ajkoai~v th~v ejnqe>ou sofi>av ejpakou~sai kathxiwme>nwn, thnikau~ta th~v ajqe>ou pla>nhv th<n ajrch<n ejla>mzanen hJ su>stasiv,
- page: 68; sample: ko>smou panto<v swthri>av, (as was Jesus Christ). And it is added: Eij ga<r oJ basileu~sin ejpegeiro>menov, kola>sewv a]xiov dikai>wv
- page: 77; sample: prosene>gkontav ta< dw~ra th~v ejpiskoph~v ajpoza>lwmen. Maka>rioi oJi proodoiporh>santev preszu>teroi, — namely, because they were in
- page: 79; sample: and for the first epistle, it is directed not only to the church of Corinth, chap. 1, verse 2, but also pa~si toi~v ejpikaloume>noiv to< o]noma tou~
- page: 172; sample: good thoughts and actings whatsoever. ( Romans 7:8-24; 2 Corinthians 3:5.)
- page: 268; sample: pleasure? ( John 1:16; 1 Corinthians 12:13; Ephesians 1:23, 2:20- 22, 4:15, 16; Galatians 2:20; Colossians 1:17-19, 2:19.) What is it,
- page: 586; sample: him be brought forth to this purpose time will show. But if he be able to make JO Qeo>v ejstin oJ ejnergw~n ejn uJmi~n, "God is working in you to will
- page: 793; sample: chap. 6:4, where it is said that they were a[pax fwtisqe>ntev, "once enlightened;" whence he thus argues: —

## Possible Paragraph Splits

- file: EPUB/ch005.xhtml; previous: ak to deal so harshly with some of them with whom he hath to do. And it is still feared that "Parata tollit cornua; Qualis Lycambae spretus infido gener, Aut acer hostis Bupalo." 3; next: It might, indeed, be the more excusable if evident provocation were always ready at hand to be charged with the blame of this procedure, if he said only,
- file: EPUB/ch005.xhtml; previous: st of a crooked and perverse generation, knowing that it is but yet a little while, and he that shall come will come, and will not tarry. Yea, come, Lord Jesus, come. So prays your; next: unworthy fellow-laborer and brother in our dear Lord Jesus
- file: EPUB/ch005.xhtml; previous: unworthy fellow-laborer and brother in our dear Lord Jesus; next: John Owen
- file: EPUB/ch006.xhtml; previous: o make the matter more clear, cap. 13, he disputes, that " Auxilium sine quo nullus perseverat, et per quod quilibet perseverat, est Spiritus Sanctus, divina bonitas et voluntas. "; next: Every cause of bringing sinful man to God is called by them "auxilium.' In these three, "Spiritus Sanctus, divina bonitas, et voluntas," he compriseth the chief causes of persevera
- file: EPUB/ch008.xhtml; previous: of many in these days — The great offense given and taken thereby, with the provision made for its removal — The nature of that offense and temptation thence arising considered _—; next: Answer to some arguings of Mr. G., chap. 9, from thence against the truth proposed — The use of trials and shakings — Grounds of believers' assurance that they are so — The same fa
- file: EPUB/ch010.xhtml; previous: n, at least before their calling, are as liable to be deceived or seduced as other men. This is their own confession; and Paul says that they were sometimes deceived, [Titus 3:3] "; next: Ans. An exception, doubtless, unworthy him that makes it; who, had he not resolved to say all that ever had been said by any to the business in hand, would scarcely, I presume, hav
- file: EPUB/ch011.xhtml; previous: rt, that they shall not depart from me,' may be as well rendered, ' That they may not depart from me;' and so it is said in the verse foregoing, ' That they may fear me for ever.'"; next: Ans. Suppose the words may be thus rendered, what inconvenience will ensue? Either way they evidently and beyond exception design out the end aimed at by God; and when God intends
- file: EPUB/ch013.xhtml; previous: e;' in which words of 'hearing' and 'following' him he intimateth or includeth their perseverance, as appeareth by the words immediately following, 'And I give them eternal life.'"; next: Ans. This, I confess, is to the purpose, if it be true; but being so contrary to what hath been (I had almost said universally) received concerning the mind of Christ in this place
- file: EPUB/ch014.xhtml; previous: ever, and yet every present member thereof lose his interest and part in him; yea, the abiding of the Spirit in the apostles themselves was not absolutely promised, [John 15:10] "; next: Ans. 1. The design of this discourse is to prove that this promise is not made to believers in general, or those who through the word are brought to believe in Christ in all genera
- file: EPUB/ch014.xhtml; previous: also. That the sealing mentioned depends upon the faith of the sealed is evident, because it is said, 'In whom also, after ye believed, ye were sealed with the Spirit of promise.'"; next: Ans. I dare say there is no honest man that would take it well at the hand of Mr. Goodwin, or any else, that should attempt, by distinctions, or any other way, to alleviate or take

## Inline Structural Marker Candidates

- file: EPUB/ch010.xhtml; text: All these things, to the falling of a hair or the withering of a [blade of] grass, hath he determined from of old. Now, this divine fore-appointment of all things the Scripture assigns sometimes to the knowledge and understanding, someti...
- file: EPUB/ch010.xhtml; text: I shall only add that, — 1. When Mr. Goodwin shall make good that order and series of decrees here by him mentioned from the Scripture, or with solid reason from the nature of the things themselves, suitably to the properties of Him whos...
- file: EPUB/ch012.xhtml; text: Gospel promises, then, are, — 1. The free and gracious dispensations, and, 2. discoveries of God's good-will and love, to, 3. sinners, 4. through Christ, 5. in a covenant of grace; 6. wherein, upon his truth and faithfulness, he engageth...
- file: EPUB/ch013.xhtml; text: The former argument confirmed by an induction of particular instances — [Joshua 1:5] opened — The concernment of all believers in that promise proved by the apostle, Hebrews 42:5. — The general interest of all believers in all the promis...
- file: EPUB/ch022.xhtml; text: As to the matter in hand, this is evident by the light of this single consideration, that in such an ecclesiastical body of Christ there are always, or may be, — and Christ himself, in the rules and laws that he hath given for the govern...
- file: EPUB/ch022.xhtml; text: That they should be saved by Christ, and yet not washed in his blood, not sanctified by his Spirit (which to be is to be regenerate), is another new notion of the new gospel The countenance which Mr. Goodwin would beg to his doctrine fro...
- file: EPUB/ch022.xhtml; text: The proposition is ready at hand in the words, "He that is born of God doth not, cannot commit sin." The reason of the proposition confirming the truth thereof is twofold: — 1. Because he is born of God; 2. Because His seed, whereof he i...
- file: EPUB/ch023.xhtml; text: Mr. G.'s seventh argument, about the tendency of the doctrine of the saints' apostasy as to their consolation, proposed, considered — What that doctrine offereth for the consolation of the saints stated — The impossibility of its affordi...

## Suspicious Large-Number Starts

- file: EPUB/ch006.xhtml; text: 29. Whatever be the judgment of our doctor concerning this man (as some there are of whom a learned bishop in this nation long ago complained, that they are still opening their mouths against Calvin, who helped them to m
- file: EPUB/ch006.xhtml; text: 24. It seems, moreover, that those bishops and deacons in those days, as was observed, were appointed to the office by and with the consent of the people, or whole body of the church; no loss do these words import, Συνευ
- file: EPUB/ch006.xhtml; text: 23. Deln epistola ista Antiocheme ecclesiae reddita, vet.
- file: EPUB/ch006.xhtml; text: 30. Paulus tandem et Silas Syriam et Cilieiam peragrantes, ver. 41, cap. 16:4, δόγματα κεκριμένα ὑπὸ τῶν ἀποστόλων , singulis elvitatibus observanda tradiderunt, ut quae ad hanc Antiochiae metropolin, ut totidem subordin

## Roman Heading Candidates

- file: EPUB/ch007.xhtml; text: M. Pacho secured possession of another copy in 1847, which afterwards came under the examination of Mr. Cureton.

## Overlong Heading Candidates

- file: EPUB/ch004.xhtml; tag: h3; text: HIS HIGHNESS OLIVER, LORD-PROTECTOR OF THE COMMONWEALTH OF ENGLAND, SCOTLAND, AND IRELAND, WITH THE DOMINIONS THEREOF. SIR, THE wise man tells us that "no man knoweth love or hatred by all that is before him." The great variety wherein G...

## Short Fragments

- file: EPUB/ch004.xhtml; text: TO
- file: EPUB/ch005.xhtml; text: John Owen
- file: EPUB/ch006.xhtml; text: De Correptione et Gratia, cap. 14,
- file: EPUB/ch006.xhtml; text: And cap. 12,
- file: EPUB/ch006.xhtml; text: And a little after:
- file: EPUB/ch006.xhtml; text: And farther in the same chapter,
- file: EPUB/ch006.xhtml; text: And again,
- file: EPUB/ch006.xhtml; text: And,
- file: EPUB/ch006.xhtml; text: He concludes,
- file: EPUB/ch006.xhtml; text: Prosper, ad cap. 7 Gal.:

## Missing Enumerator Markers

- marker: (1.); pdf: 63; epub: 62; examples: [{'location': 'pdf:p10', 'context': 'Union with Christ by the indwelling of the same Spirit in him and us — This proved from, (1.) Scriptural declarations of it — 2 Peter 1:4, how we are made partakers of the divine nature — Union expres...
- marker: (2.); pdf: 65; epub: 62; examples: [{'location': 'pdf:p10', 'context': 'disciples, John 17:2l — The union of the persons in the Trinity with themselves — (2.) Scriptural illustrations for the manifestation of union — The union of head and members, what it is, and wherein ...
- marker: (3.); pdf: 24; epub: 23; examples: [{'location': 'pdf:p11', 'context': 'g it on work, faith — (2.) In the manner of doing it, eyeing both precepts and promises — (3.) The end aimed at in it, the glory of God as a rewarder, Hebrews 11:6; Romans 4:4 — The principle in us wh...

## Enumerator Sequence Candidates

- file: EPUB/ch017.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) There are promises of what good and great things God will farther do unto and for them who obey him; as, that he will keep them and preserve them that they shall not be lost, that

## Repeated Windows

- phrase: both to will and to do of his good pleasure; count: 9
- phrase: law in their inward parts and write it in their; count: 5
- phrase: in their inward parts and write it in their hearts; count: 5
- phrase: all things work together for good to them that love; count: 4
- phrase: he wrought in christ when he raised him from the; count: 4
- phrase: wrought in christ when he raised him from the dead; count: 4
- phrase: will put my law in their inward parts and write; count: 4
- phrase: put my law in their inward parts and write it; count: 4
- phrase: my law in their inward parts and write it in; count: 4
- phrase: in them both to will and to do of his; count: 4

## Missing Word Samples

- word: 19-22; pdf: 9; epub: 3
- word: 3-5; pdf: 7; epub: 3
- word: 31-34; pdf: 7; epub: 3
- word: 27-29; pdf: 6; epub: 2
- word: g's; pdf: 4; epub: 0
- word: 27-31; pdf: 5; epub: 2
- word: 17-20; pdf: 5; epub: 2
- word: 28-30; pdf: 5; epub: 2
- word: 16-18; pdf: 4; epub: 1
- word: 2-4; pdf: 3; epub: 0

## Excess Word Samples

- word: psalms; pdf: 1; epub: 56
- word: digital; pdf: 0; epub: 10
- word: modern; pdf: 4; epub: 13
- word: hebrew; pdf: 2; epub: 9
- word: footnotes; pdf: 0; epub: 6

## Missing Greek Word Samples

- word: ὅπερ; pdf: 3; epub: 1

## Missing Greek Clauses

- page: 68; word_count: 34; sample: κυριος ανευ του πατρος ουδεν ποιει ου δυναμαι γαρ φησι ποιειν εμαυτου

## Missing Latin Word Samples

- word: semi; pdf: 3; epub: 0

## Untagged Latin Word Samples

- word: nor; epub: 450; tagged: 0
- word: jesus; epub: 217; tagged: 0
- word: yea; epub: 211; tagged: 0
- word: et; epub: 170; tagged: 20
- word: thereunto; epub: 134; tagged: 0
- word: non; epub: 140; tagged: 14
- word: whereunto; epub: 101; tagged: 0
- word: persevere; epub: 95; tagged: 0
- word: de; epub: 82; tagged: 7
- word: sum; epub: 75; tagged: 0

## Untranslated Latin Samples

- phrase: put his law in their inward parts, and write it in their hearts;
- phrase: in loving-kindness and in mercies,
- phrase: in its proper place. What he adds in the last place, namely,
- phrase: abide in me, and I in you.
- phrase: is in the other, in equivalent terms, called
- phrase: Ye believe in God, believe also in me,
- phrase: blessed with all spiritual blessings in heavenly places in him
- phrase: though brought in illatively, in respect of what was said before,
- phrase: in him, that is, in his flesh, dwelt no good,

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
