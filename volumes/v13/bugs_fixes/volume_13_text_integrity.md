# Text Integrity Audit: Volume 13

- Status: **WARN**
- Warnings: 16
- PDF pages: 749
- EPUB text files: 84
- EPUB paragraphs/headings: 1979

## Coverage

- PDF content tokens: 250071
- EPUB content tokens: 226985
- Approximate PDF-to-EPUB coverage ratio: 0.9014
- Pages checked: 737
- Weak page matches: 30
- Dense source windows checked: 29743
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 2
- Top-of-page body windows checked: 720
- Top-of-page windows skipped as unstable: 20
- Missing top-of-page body windows: 86
- Bottom-of-page body windows checked: 679
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 40

## Paragraphs

- Body paragraphs checked: 1543
- Possible faulty paragraph splits: 9
- Structural starts excluded from split warnings: 90
- Short fragments: 22
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 3
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 4
- Overlong heading candidates: 2
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 80
- EPUB enumerator markers: 76
- Missing enumerator marker forms: 6
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1046
- EPUB Greek words: 1020
- Greek word coverage ratio: 0.9521
- PDF Hebrew words: 12
- EPUB Hebrew words: 12
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 59
- Missing Greek clauses: 1
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 4940
- EPUB Latin words: 4550
- EPUB Tagged Latin words: 179
- Latin word coverage ratio: 0.904
- Latin word tagging ratio: 0.0393
- Latin clauses checked: 215
- Missing Latin clauses: 14
- Tagged Latin runs checked: 26
- Translated Latin runs: 23
- Latin translation ratio: 0.8846

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
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
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 3; sample: contents of the duty of pastors and people distinguished preface of the administration of
- page: 4; sample: of schism aggravations of the evil of schism from the authority of the ancients
- page: 5; sample: of schism the ground of sin and disorder objections against the former discourse proposed
- page: 6; sample: their apostasy proved by instances their grand argument in this case proposed answered consequences
- page: 7; sample: of elijah the last objection waived inferences upon the whole review of the true
- page: 8; sample: an answer etc brief vindication of the nonconformists from the charge of schism prefatory
- page: 9; sample: alleged evils from the free exercise of conscience charges of parker against noncomformists mischief
- page: 11; sample: the duty of pastors and people distinguished or brief discourse touching the administration of
- page: 12; sample: and independency he afterwards changed his views on church government but in the work
- page: 14; sample: to the truly noble and my ever honored friend sir edward scot of scot's

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.25; sample: contents of the duty of pastors and people distinguished preface of the administration of holy things among the patriarchs before the law of the same among the jews
- page: 8; hit_ratio: 0.5; sample: an answer etc brief vindication of the nonconformists from the charge of schism prefatory note by the editor brief vindication etc truth and innocence vindicated prefatory note by

## Missing Top-Of-Page Body Windows

- page: 8; sample: An Answer, etc., A BRIEF VINDICATION OF THE NONCONFORMISTS FROM
- page: 14; sample: TO THE TRULY NOBLE AND MY EVER HONORED FRIEND, SIR EDWARD SCOT,
- page: 77; sample: those, as bestowed on them, who are to be called to office of ministration: and may be, in several degrees and measures, in such as are never set apart
- page: 79; sample: the ways of God, and his worship by them administered (as hath fallen out in the Old Testament,
- page: 80; sample: 2 Thessalonians 3:1,2, "Brethren, pray for us, that the word of the Lord may have free course and be glorified; and that we may be
- page: 81; sample: RULE IV. Reverential estimation of him, with submission unto him for his work's sake.
- page: 82; sample: RULE V. Maintenance for them and their families, by the administration of earthly things suitable to the state and condition of the churches, is
- page: 83; sample: giving portions and granting privileges to churches and their pastors. It is so in many places in the days wherein we live. On this ground, where
- page: 84; sample: 1 Timothy 1:16-18, "The Lord give mercy unto the house of Onesiphorus; for he oft refreshed me, and was not ashamed of my
- page: 85; sample: encouragement to the work; saying also unto them, "Take heed to the ministry ye have received in the Lord, that ye fulfill it,"

## Missing Bottom-Of-Page Body Windows

- page: 3; sample: Rules to be observed by those who walk in fellowship and considered, to stir up their remembrance in things of mutual duty one towards another,
- page: 9; sample: PREFATORY NOTE BY THE EDITOR, The Grounds and Reasons, etc.,
- page: 32; sample: places; to which add uJphre>tai, 1 Corinthians 4:1, a word though of
- page: 76; sample: 1 Timothy 3:2-7, Titus 1:6-9, and many other places, is required to be previously in
- page: 77; sample: 1. The name wherein they speak and administer, 2 Corinthians 5:20.
- page: 78; sample: Matthew 5:16, is eminently exacted; and this not only that no offense be taken at
- page: 79; sample: me, that I may open my mouth boldly, to make known the mystery of the gospel, for which I am an ambassador."
- page: 81; sample: them and cut them off in a month, Zechariah 11:8.
- page: 82; sample: those committed to them. The fruit of this promise the churches in many ages have enjoyed; laws by supreme and kingly power have been enacted,
- page: 83; sample: but all men forsook me: I pray God that it may not be laid to their charge."

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: ays of mercy and grace which are necessary to carry you along through all your engagements, until you arrive at the haven of everlasting glory, where you would be. I rest your most; next: obliged servant in Jesus Christ, our common Master
- file: EPUB/ch003.xhtml; previous: obliged servant in Jesus Christ, our common Master; next: John Owen
- file: EPUB/ch015.xhtml; previous: To The Reader; next: THERE are, Christian reader, certain principles in church affairs generally consented unto by all men aiming at reformation and the furtherance of the power of godliness therein, h
- file: EPUB/ch026.xhtml; previous: h and making profession of Christianity, may claim admission into the society of Christians within those bounds, and enjoy the privileges and ordinances which are there dispensed,"; next: Ans. of Commit., p. 105. This is also pursued by the authors of Jus Divinum Ministerii Anglicani, pp. 9,10, where, after the repetition of the words first mentioned, they add, that
- file: EPUB/ch029.xhtml; previous: To The Reader; next: CHRISTIAN READER,
- file: EPUB/ch029.xhtml; previous: CHRISTIAN READER,; next: IT is now about three weeks since that there was sent unto me a book entitle, "Independency a Great Schism;" as the frontispiece farther promiseth, undertaken to be managed against
- file: EPUB/ch039.xhtml; previous: ll as the doctrine, and that we are all departed from it, and so are schismatical; for we hold communion with them," he says, " in the same doctrine, but not in the same worship. "; next: Ans. 1. His first exception ariseth from the advantage he makes use of from his large use of the word "Independent;" which will serve him, in his sense, for what end he pleaseth. I
- file: EPUB/ch048.xhtml; previous: uld be restrained. It is far from my purpose to return him any answer in the like manner to these things; to do it " — opus est mangone perito Qui Smithfieldensi polleat eloquio. "; next: Yet some instances of prodigious excesses in this kind will, in our process, be reflected on; and it may be the repetition of them may make an appearance, unto some less considerat
- file: EPUB/ch059.xhtml; previous: Yours; next: J.O.

## Inline Structural Marker Candidates

- file: EPUB/ch009.xhtml; text: Now, three ways may a man receive, and be assured that he hath received, this divine mission, or know that he is called of God to the preaching of the word; I mean not that persuasion of divine concurrence which is necessary also for the...
- file: EPUB/ch031.xhtml; text: Thus, in general, to take a view of some particular passages in the appendix destined to this good work: The first section tries, with much wit and rhetoric, to improve the pretended alteration of judgment to the blemishing of my reputat...
- file: EPUB/ch059.xhtml; text: The reasonableness of this gospel institution is manifested by the Holy Ghost: — 1. From the law of nature, Luke 10:7; 1 Corinthians 9:7, 11. 2. From the law of nations, in the same place. 3. From the tendency and equity of Mosaical inst...

## Suspicious Large-Number Starts

- file: EPUB/ch005.xhtml; text: 12. ae. quest.
- file: EPUB/ch022.xhtml; text: 10. I no way doubt of the perpetual existence of innumerable believers in every age, and such as made the profession that is absolutely necessary to salvation, one way or other, though I question a regular association of
- file: EPUB/ch022.xhtml; text: 22. In what sense this church is visible was before declared. Men elected, redeemed, justified, as such, are not visible, for that which makes them so is not; but this hinders not but they may be so upon the other consid
- file: EPUB/ch023.xhtml; text: 29. There being, then, in the world a great multitude, which no man can number, of all nations, kindreds, people, and language, professing the doctrine of the gospel, not tied to mountains or hills, John 4:21, 23, but wo

## Roman Heading Candidates

- file: EPUB/ch030.xhtml; text: C. hardly refrain from calling a man Satan for speaking the truth? It is well if we know of what Spirit we are.
- file: EPUB/ch032.xhtml; text: C. knows how easy it were to make his own words dress him up in all those ornaments wherein he labors to make me appear in the world, by such glosses, inversions, additions, and interpositions, as he is pleased to make u
- file: EPUB/ch039.xhtml; text: C. himself is bound to come into it, and yet I do not think that his not so doing makes him a schismatic; and as for relinquishment, I assert no more than what he himself concludes to be lawful. And thus, Christian reade
- file: EPUB/ch059.xhtml; text: IV. The payment of tithes, — 1. Before the law, Genesis 14:20, Hebrews 7:4, 5; with, 2. The like usage amongst all nations living according to the light of nature; 3. Their establishing under the law; with, 4. The expres

## Overlong Heading Candidates

- file: EPUB/ch049.xhtml; tag: h3; text: [Inconsistent expressions of Parker in regard to the power of the magistrate and the rights of conscience — The design of his discourse to prove the magistrate's authority to govern the consciences of his subjects in affairs of religion ...
- file: EPUB/ch050.xhtml; tag: h3; text: [Alleged power of the magistrate over the conscience in matters of morality refuted — Distinction between moral virtue and grace — Meaning of the terms — Four propositions of Parker on grace and virtue considered — Agreement between the ...

## Short Fragments

- file: EPUB/ch002.xhtml; text: M AY 11, 1644.
- file: EPUB/ch002.xhtml; text: JOSEPH CARYL.
- file: EPUB/ch003.xhtml; text: John Owen
- file: EPUB/ch007.xhtml; text: and again,
- file: EPUB/ch007.xhtml; text: Whence I conclude, —
- file: EPUB/ch011.xhtml; text: to which add that of the apostle,
- file: EPUB/ch012.xhtml; text: Τῷ Θεῷ ἀριστομεγίστῳ δόζα .
- file: EPUB/ch015.xhtml; text: To The Reader
- file: EPUB/ch025.xhtml; text: I say, then, —
- file: EPUB/ch029.xhtml; text: To The Reader

## Missing Enumerator Markers

- marker: (1.); pdf: 21; epub: 17; examples: [{'location': 'pdf:p34', 'context': '34 (1.) All faithful ministers of the gospel, inasmuch as they are ingrafted into Christ and are true believers, may, as all other true Christians, be called priests; but this inasmuch as'}, {'locatio...
- marker: (2.); pdf: 22; epub: 17; examples: [{'location': 'pdf:p35', 'context': 'us Christ hath purchased for every one that is sanctified with the blood of the covenant. (2.) We have an interest in this appellation of priests by virtue of our union with Christ. Being one with our...
- marker: (3.); pdf: 15; epub: 12; examples: [{'location': 'pdf:p36', 'context': "an is crucified with him, that the body of sin might be destroyed,'' Romans 6:6. (3.) We are priests as we are Christians, or partakers of a holy unction, whereby we are anointed to the participation ...
- marker: (4.); pdf: 9; epub: 7; examples: [{'location': 'pdf:p37', 'context': 'te communion with him in all his glorious offices; and in that regard are called priests. (4.) The sacrifices we are enjoined to offer give ground to this appellation. Now, they are of divers sorts, t...
- marker: (5.); pdf: 4; epub: 3; examples: [{'location': 'pdf:p226', 'context': 'o be reduced unto it, is of the same importance, Acts 14:23; Titus 1:5. (5.) Christ\'s institution of officers for them, Ephesians 4:11, 1 Corinthians 12:28; calling such a church his "body," verse 2...
- marker: (6.); pdf: 3; epub: 2; examples: [{'location': 'pdf:p226', 'context': 'and for order, — evince from whom they are, and what is our duty in reference unto them. (6.) The judging and condemning them by the Holy Ghost as disorderly, blamable persons, who are to be avoided,...

## Enumerator Sequence Candidates

- file: EPUB/ch023.xhtml; marker: (2.); family: paren_decimal; context: (2.) That doing so, in the course of our lives we manifest and declare a principle that is utterly inconsistent with the belief of those truths which outwardly we profess; or, —
- file: EPUB/ch042.xhtml; marker: [16]; family: bracket_decimal; context: [16] 46; all the ministers almost in the county of Essex know the contrary, one especially, being a man of great ability and moderation of spirit, and for his knowledge in those things

## Repeated Windows

- phrase: the grounds and reasons on which protestant dissenters desire their; count: 7
- phrase: grounds and reasons on which protestant dissenters desire their liberty; count: 6
- phrase: the state of the kingdom with respect to the present; count: 5
- phrase: state of the kingdom with respect to the present bill; count: 5
- phrase: of the kingdom with respect to the present bill against; count: 5
- phrase: an account of the grounds and reasons on which protestant; count: 4
- phrase: account of the grounds and reasons on which protestant dissenters; count: 4
- phrase: of the grounds and reasons on which protestant dissenters desire; count: 4
- phrase: the kingdom with respect to the present bill against conventicles; count: 4
- phrase: posthumous the state of the kingdom etc the following statement; count: 4

## Missing Word Samples

- word: ye; pdf: 127; epub: 32
- word: brethren; pdf: 79; epub: 38
- word: matthew; pdf: 61; epub: 26
- word: timothy; pdf: 42; epub: 10
- word: edification; pdf: 49; epub: 18
- word: hebrews; pdf: 50; epub: 23
- word: thessalonians; pdf: 31; epub: 10
- word: explication; pdf: 27; epub: 6
- word: galatians; pdf: 28; epub: 10
- word: brother; pdf: 25; epub: 8

## Excess Word Samples

- word: volume; pdf: 6; epub: 22
- word: ii; pdf: 15; epub: 28
- word: london; pdf: 14; epub: 26
- word: bill; pdf: 7; epub: 18
- word: digital; pdf: 0; epub: 10
- word: penalty; pdf: 11; epub: 20
- word: citizens; pdf: 9; epub: 18
- word: modern; pdf: 5; epub: 14
- word: greek; pdf: 2; epub: 10
- word: oppression; pdf: 8; epub: 15

## Missing Greek Clauses

- page: 263; word_count: 5; sample: δουλον κυριου ου δει μαχεσθαι

## Missing Latin Word Samples

- word: communicate; pdf: 13; epub: 5
- word: affectionate; pdf: 4; epub: 0
- word: judea; pdf: 6; epub: 2
- word: aquila; pdf: 5; epub: 2
- word: vos; pdf: 4; epub: 1
- word: galatia; pdf: 3; epub: 1
- word: macedonia; pdf: 3; epub: 1
- word: paulus; pdf: 3; epub: 1
- word: samaria; pdf: 3; epub: 1

## Untagged Latin Word Samples

- word: nor; epub: 471; tagged: 0
- word: magistrate; epub: 229; tagged: 0
- word: jesus; epub: 178; tagged: 0
- word: thereunto; epub: 104; tagged: 0
- word: yea; epub: 98; tagged: 0
- word: plea; epub: 71; tagged: 0
- word: whereas; epub: 71; tagged: 0
- word: et; epub: 75; tagged: 12
- word: dissent; epub: 60; tagged: 0
- word: debate; epub: 51; tagged: 0

## Missing Latin Clauses

- page: 389; word_count: 7; sample: coitio christianorum merito sane illicita si illicitis
- page: 389; word_count: 16; sample: merito damnanda si quis de ea queritur eo titulo quo de factionibus
- page: 389; word_count: 13; sample: aliquando convenimus hoc sumus congregati quod et dispersi hoc universi quod et
- page: 389; word_count: 4; sample: quum probi cum boni
- page: 389; word_count: 11; sample: cum pii cum casti congregantur non est factio dicenda sed curia
- page: 398; word_count: 5; sample: in maenia si nilus non
- page: 398; word_count: 4; sample: in arva si coelum
- page: 416; word_count: 4; sample: in a sincere endeavor
- page: 435; word_count: 5; sample: vos aequo animo aequa noscere
- page: 435; word_count: 7; sample: si vos voltis perhiberi probos ter ad

## Untranslated Latin Samples

- phrase: doctrine and fellowship, and in breaking of bread, and in prayers,
- phrase: some decays in true grace in the members of this church,
- phrase: in the same doctrine, but not in the same worship.

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
