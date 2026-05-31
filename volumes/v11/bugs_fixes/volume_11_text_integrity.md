# Text Integrity Audit: Volume 11

- Status: **WARN**
- Warnings: 12
- PDF pages: 815
- EPUB text files: 29
- EPUB paragraphs/headings: 2091

## Coverage

- PDF content tokens: 307709
- EPUB content tokens: 300847
- Approximate PDF-to-EPUB coverage ratio: 0.9763
- Pages checked: 809
- Weak page matches: 22
- Dense source windows checked: 883
- Missing dense source-window pages: 793
- Front CONTENTS pages checked: 2
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 795
- Top-of-page windows skipped as unstable: 29
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 796
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 9

## Paragraphs

- Body paragraphs checked: 1797
- Possible faulty paragraph splits: 143
- Structural starts excluded from split warnings: 296
- Short fragments: 26
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 4
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 3
- Roman heading candidates: 2
- Overlong heading candidates: 4
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 263
- EPUB enumerator markers: 255
- Missing enumerator marker forms: 4
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 2086
- EPUB Greek words: 2080
- Greek word coverage ratio: 0.997
- PDF Hebrew words: 0
- EPUB Hebrew words: 0
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 117
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

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

## Missing Dense Source Windows

- page: 3; sample: contents of the doctrine of the saints perseverance explained and confirmed prefatory note by
- page: 4; sample: principles the close of the vindication of this first argument chapter the immutability of
- page: 5; sample: produced samuel 30 farther considered and its unsuitableness to illustrate romans 28-31 proved interpretation
- page: 6; sample: chapter argument from the covenant of grace an entrance into the consideration of the
- page: 7; sample: promise not judas the accomplishment of the premise the testimony of peter martyr considered
- page: 8; sample: and fountain of all goodness to his people in his own good pleasure the
- page: 9; sample: the death of christ and the necessity of faith and obedience reconciled sundry considerations
- page: 10; sample: 10 the saints as in temple corinthians 16 19 the indwelling of the spirit
- page: 11; sample: 11 farther objections answered christ not the minister of sin by this doctrine supposals
- page: 12; sample: 12 both precepts on the one hand and promises exhortations threatenings on the other

## Missing Top-Of-Page Body Windows

- page: 183; sample: "I will put my fear in their hearts," Jeremiah 32:40; which Ezekiel 36:27 calls the "putting his Spirit in them," who is the author of that grace

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 51; sample: Acts. 2:47, 13:48; Romans 6:14, 8:1, 16, 17, 28-34, etc.; 1 Corinthians 1:8, 9, 10:13, 14, 15:49, 58; 2 Corinthians 1:21, 22;
- page: 53; sample: aujtai~v ajkoai~v th~v ejnqe>ou sofi>av ejpakou~sai kathxiwme>nwn, thnikau~ta th~v ajqe>ou pla>nhv th<n ajrch<n ejla>mzanen hJ su>stasiv,
- page: 68; sample: ko>smou panto<v swthri>av, (as was Jesus Christ). And it is added: Eij ga<r oJ basileu~sin ejpegeiro>menov, kola>sewv a]xiov dikai>wv
- page: 77; sample: prosene>gkontav ta< dw~ra th~v ejpiskoph~v ajpoza>lwmen. Maka>rioi oJi proodoiporh>santev preszu>teroi, — namely, because they were in
- page: 79; sample: and for the first epistle, it is directed not only to the church of Corinth, chap. 1, verse 2, but also pa~si toi~v ejpikaloume>noiv to< o]noma tou~
- page: 172; sample: good thoughts and actings whatsoever. ( Romans 7:8-24; 2 Corinthians 3:5.)
- page: 586; sample: him be brought forth to this purpose time will show. But if he be able to make JO Qeo>v ejstin oJ ejnergw~n ejn uJmi~n, "God is working in you to will
- page: 793; sample: chap. 6:4, where it is said that they were a[pax fwtisqe>ntev, "once enlightened;" whence he thus argues: —

## Possible Paragraph Splits

- file: EPUB/ch001.xhtml; previous: OR, THE; next: DOCTRINE OF THE
- file: EPUB/ch001.xhtml; previous: DOCTRINE OF THE; next: SAINTS PERSEVERANCE _Explained and Confirmed._ **THE CERTAIN PERMANENCY OF THEIR**
- file: EPUB/ch004.xhtml; previous: TO; next: Your Highness's most humble and most faithful servant, John Owen
- file: EPUB/ch005.xhtml; previous: ll manner of signal improvements that may render it keen or pleasant, according to his intendment or desire. What the Latin lyric said of the Grecian poets may be applied to him: —; next: And he is hereby plainly possessed of not a few advantages. It is true that when the proof of his opinion by argument, and the orderly pursuit of it, is incumbent on him (a course
- file: EPUB/ch005.xhtml; previous: ak to deal so harshly with some of them with whom he hath to do. And it is still feared that "Parata tollit cornua; Qualis Lycambae spretus infido gener, Aut acer hostis Bupalo." 3; next: It might, indeed, be the more excusable if evident provocation were always ready at hand to be charged with the blame of this procedure, if he said only,
- file: EPUB/ch005.xhtml; previous: It might, indeed, be the more excusable if evident provocation were always ready at hand to be charged with the blame of this procedure, if he said only,; next: But for a man to warm himself by casting about his own pen until it be so filled with indignation and scorn as to blur every page and almost every line, is a course that will never
- file: EPUB/ch006.xhtml; previous: eems to have been, who is followed by sundry of the schoolmen, with many of the divines of the reformed churches. Hence is that conclusion of Alvarez, De Auxil., lib. 10 disp. 103,; next: And of this proposition he says, "In hac omnes catholici conveniunt." Of the same judgment was his master, Thomas, lib. 3 Con. Genesis cap. ely.; where, also, he gives this reason
- file: EPUB/ch006.xhtml; previous: o be a superadded gift to saving grace, which, as before was observed, he denied, but to manifest that it was immediately and wholly from God. His words are, lib. 2 cap. 8, Corol.,; next: The same schoolmen also (a generation of men exceeding ready to speak of any thing, though they know not what they speak nor whereof they affirm) go yet farther, some of them, and
- file: EPUB/ch006.xhtml; previous: Add, in the next place, the most ancient of the Latins, TERTULLIAN, that great storehouse of all manner of leaning and knowledge. Saith; next: The certain salvation of the whole body of Christ, with whom he hath that communion as to give them his Spirit, as he took their flesh (for he took upon him flesh and blood, becaus
- file: EPUB/ch006.xhtml; previous: CYPRIAN is express to our purpose. Saith he,; next: The whole doctrine we contend for is plainly and clearly asserted, and bottomed on a text of Scripture; which in a special manner (as we have cause) we do insist upon. All that is

## Inline Structural Marker Candidates

- file: EPUB/ch012.xhtml; text: Gospel promises, then, are, — 1. The free and gracious dispensations, and, 2. discoveries of God's good-will and love, to, 3. sinners, 4. through Christ, 5. in a covenant of grace;
- file: EPUB/ch022.xhtml; text: That they should be saved by Christ, and yet not washed in his blood, not sanctified by his Spirit (which to be is to be regenerate), is another new notion of the new gospel The countenance which Mr. Goodwin would beg to his doctrine fro...
- file: EPUB/ch022.xhtml; text: The proposition is ready at hand in the words, "He that is born of God doth not, cannot commit sin." The reason of the proposition confirming the truth thereof is twofold: — 1. Because he is born of God; 2. Because His seed, whereof he i...
- file: EPUB/ch023.xhtml; text: Mr. G.'s seventh argument, about the tendency of the doctrine of the saints' apostasy as to their consolation, proposed, considered — What that doctrine offereth for the consolation of the saints stated — The impossibility of its affordi...

## Suspicious Large-Number Starts

- file: EPUB/ch006.xhtml; text: 29. Whatever be the judgment of our doctor concerning this man (as some there are of whom a learned bishop in this nation long ago complained, that they are still opening their mouths against Calvin, who helped them to m
- file: EPUB/ch006.xhtml; text: 23. Deln epistola ista Antiocheme ecclesiae reddita, vet.
- file: EPUB/ch006.xhtml; text: 30. Paulus tandem et Silas Syriam et Cilieiam peragrantes, ver. 41, cap. 16:4, δόγματα κεκριμένα ὑπὸ τῶν ἀποστόλων , singulis elvitatibus observanda tradiderunt, ut quae ad hanc Antiochiae metropolin, ut totidem subordin

## Roman Heading Candidates

- file: EPUB/ch007.xhtml; text: M. Pacho secured possession of another copy in 1847, which afterwards came under the examination of Mr. Cureton.
- file: EPUB/ch015.xhtml; text: II. 1. The first signal issue and effect which is ascribed to this indwelling of the Spirit is union; not a personal union with himself, which is impossible.

## Overlong Heading Candidates

- file: EPUB/ch004.xhtml; tag: h3; text: HIS HIGHNESS OLIVER, LORD-PROTECTOR OF THE COMMONWEALTH OF ENGLAND, SCOTLAND, AND IRELAND, WITH THE DOMINIONS THEREOF. SIR, THE wise man tells us that "no man knoweth love or hatred by all that is before him." The great variety wherein G...
- file: EPUB/ch010.xhtml; tag: h4; text: I. By the purposes of God I mean, as I said before, the eternal acts of his will concerning all things that outwardly are of him; which are the rules, if I may so speak, of all his following operations, — all external, temporary products...
- file: EPUB/ch010.xhtml; tag: h4; text: II. This foundation being laid, I come to what was secondly proposed, — namely, to manifest, by an induction of particular instances, the engagement of these absolute and immutable purposes of God as to the preservation of the saints in ...
- file: EPUB/ch015.xhtml; tag: h4; text: I. 1. The indwelling of the Spirit is the great and solemn promise of the covenant of grace; the manner of it we shall afterward evince: [Ezekiel 36:27] "I will put my Spirit within you, and cause you to walk: in my statutes." In the ver...

## Short Fragments

- file: EPUB/ch001.xhtml; text: OR, THE
- file: EPUB/ch001.xhtml; text: DOCTRINE OF THE
- file: EPUB/ch001.xhtml; text: ETERNALL PRINCIPLES
- file: EPUB/ch001.xhtml; text: ANNO DOM: 1654.
- file: EPUB/ch004.xhtml; text: TO
- file: EPUB/ch006.xhtml; text: De Correptione et Gratia, cap. 14,
- file: EPUB/ch006.xhtml; text: And cap. 12,
- file: EPUB/ch006.xhtml; text: And a little after:
- file: EPUB/ch006.xhtml; text: And farther in the same chapter,
- file: EPUB/ch006.xhtml; text: And again,

## Missing Enumerator Markers

- marker: (1); pdf: 1; epub: 0; examples: [{'location': 'pdf:p11', 'context': 'gospel obedience in the hearts of these true believers — 1. By removing discouragements — (1) Perplexing fears, which impair their faith; (2.) Hard thoughts of God, which weaken their love: without wh...
- marker: (1.); pdf: 63; epub: 61; examples: [{'location': 'pdf:p10', 'context': 'Union with Christ by the indwelling of the same Spirit in him and us — This proved from, (1.) Scriptural declarations of it — 2 Peter 1:4, how we are made partakers of the divine nature — Union expres...
- marker: (2.); pdf: 65; epub: 61; examples: [{'location': 'pdf:p10', 'context': 'disciples, John 17:2l — The union of the persons in the Trinity with themselves — (2.) Scriptural illustrations for the manifestation of union — The union of head and members, what it is, and wherein ...
- marker: (3.); pdf: 24; epub: 23; examples: [{'location': 'pdf:p11', 'context': 'g it on work, faith — (2.) In the manner of doing it, eyeing both precepts and promises — (3.) The end aimed at in it, the glory of God as a rewarder, Hebrews 11:6; Romans 4:4 — The principle in us wh...

## Enumerator Sequence Candidates

- file: EPUB/ch017.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) There are promises of what good and great things God will farther do unto and for them who obey him; as, that he will keep them and preserve them that they shall not be lost, that

## Repeated Windows

- phrase: both to will and to do of his good pleasure; count: 9
- phrase: all things work together for good to them that love; count: 5
- phrase: law in their inward parts and write it in their; count: 5
- phrase: in their inward parts and write it in their hearts; count: 5
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
- word: 17-20; pdf: 5; epub: 2
- word: 28-30; pdf: 5; epub: 2
- word: 2-4; pdf: 3; epub: 0
- word: 21-36; pdf: 3; epub: 0
- word: semi; pdf: 3; epub: 0

## Excess Word Samples

- word: psalms; pdf: 1; epub: 56
- word: digital; pdf: 0; epub: 6

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
