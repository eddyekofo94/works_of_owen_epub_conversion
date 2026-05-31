# Text Integrity Audit: Volume 13

- Status: **WARN**
- Warnings: 11
- PDF pages: 749
- EPUB text files: 82
- EPUB paragraphs/headings: 2280

## Coverage

- PDF content tokens: 252246
- EPUB content tokens: 257539
- Approximate PDF-to-EPUB coverage ratio: 0.9962
- Pages checked: 738
- Weak page matches: 10
- Dense source windows checked: 845
- Missing dense source-window pages: 724
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 722
- Top-of-page windows skipped as unstable: 20
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 681
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 3

## Paragraphs

- Body paragraphs checked: 1839
- Possible faulty paragraph splits: 92
- Structural starts excluded from split warnings: 128
- Short fragments: 29
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 8
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 7
- Overlong heading candidates: 10
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 80
- EPUB enumerator markers: 94
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1049
- EPUB Greek words: 1061
- Greek word coverage ratio: 0.9922
- PDF Hebrew words: 12
- EPUB Hebrew words: 12
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 59
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
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 3; sample: among the patriarchs before the law of the same among the jews and of
- page: 4; sample: epistle the state of the church of corinth in those days εχχλησια παροικουσα κορινθον
- page: 5; sample: of schism the ground of sin and disorder objections against the former discourse proposed
- page: 7; sample: of elijah the last objection waived inferences upon the whole review of the true
- page: 9; sample: alleged evils from the free exercise of conscience charges of parker against noncomformists mischief
- page: 11; sample: 11 the duty of pastors and people distinguished or brief discourse touching the administration
- page: 12; sample: 12 prefatory note the title-page of the following treatise indicates that it was published
- page: 14; sample: 14 to the truly noble and my ever honored friend sir edward scot of
- page: 15; sample: 15 of potent enemy prevailing in the neighbor county at both which times besides
- page: 16; sample: 16 preface the glass of our lives seems to run and keep pace with

## Missing Top-Of-Page Body Windows

- page: 14; sample: TO THE TRULY NOBLE AND MY EVER HONORED FRIEND, SIR EDWARD SCOT,

## Missing Bottom-Of-Page Body Windows

- page: 9; sample: PREFATORY NOTE BY THE EDITOR, The Grounds and Reasons, etc.,
- page: 32; sample: places; to which add uJphre>tai, 1 Corinthians 4:1, a word though of
- page: 247; sample: Acts 22:5,6, and his design was pro<v to< ge>nov. That by the "church," mentioned

## Possible Paragraph Splits

- file: EPUB/ch006.xhtml; previous: uty: concerning each of which we have both the precept and the practice, God's command and their performance. The one in that injunction given unto the priest, Deuteronomy 31:11-13; next: All which we find punctually performed on both sides, Nehemiah 8:1-8. Ezra the priest, standing on a pulpit of wood, read the law and gave the meaning of it; and the "ears of all t
- file: EPUB/ch006.xhtml; previous: ning of it; and the "ears of all the people were attentive to the book of the law." Which course continued until there was an end put to the observances of that law; as Acts 15:21,; next: On which ground, not receding from their ancient observations, the people assembled to hear our Savior teaching with authority, Luke 21:38; and St Paul divers times took advantage
- file: EPUB/ch006.xhtml; previous: ary assemblies to preach the gospel unto them. For the other, which concerns their own searching into the law and studying of the word, we have a strict command, Deuteronomy 6:6-9,; next: Which strict charge is again repeated, chapter 11:18, summarily comprehending all ways whereby they might become exercised in the law.
- file: EPUB/ch006.xhtml; previous: s belonged to that kind of public teaching which was necessary under that administration of the covenant. But instead of many, I will name one not liable to exception: Malachi 2:7,; next: — where both a recital of his own duty, that he should be full of knowledge to instruct; the intimation to the people, that they should seek unto him, or give heed to his teaching;
- file: EPUB/ch006.xhtml; previous: 6:2,3, than him because he did. There are, indeed, many sharp reproofs in the Old Testament of those who undertook to be God's messengers without his warrant; as Jeremiah 22:21,22,; next: — to which, and the like places, it may satisfactorily be answered, that howsoever, by the way of analogy, they may be drawn into rule for these times of the gospel, yet they were
- file: EPUB/ch007.xhtml; previous: 16:5, — chosen by a particular calling "ad munus," to the office of the ritual priesthood; so in regard of that other kind, comparatively so called, it is said of the whole people,; next: Their approaching nigh unto God made them all a nation of priests, in comparison of those "dogs" and unclean Gentiles that were out of the covenant. Now, this prerogative is often
- file: EPUB/ch007.xhtml; previous: Now, they are of divers sorts, though all in general eucharistical; — as, first, Of prayers and thanksgivings: Psalm 116:17,; next: Fourthly, The sweet incense of martyrdom: "Yea, and if I be offered upon the sacrifice and service of your faith, etc., Philippians 50:17 2:17. Now, these and sundry other services
- file: EPUB/ch007.xhtml; previous: ork of the ministry; as the slaying of men's lusts, and the offering up of them, being converted by the preaching of the gospel, unto God. So St Paul of his ministry, Romans 15:16,; next: Ministers preaching the gospel to the conversion of souls are said to kill men's lusts, and offer them up unto God as the fruit of their calling, as Abel brought unto him an accept
- file: EPUB/ch008.xhtml; previous: o him, Who hath made man's mouth? have not I the LORD?" So also was it with the prophet Jeremiah. When God told him that he had ordained him a prophet unto the nations, he replies,; next: Nothing can excuse any from going on His message who can perfect his praise out of the mouths of babes and sucklings. This the prophet Amos rested upon when he was questioned, alth
- file: EPUB/ch009.xhtml; previous: and to shake the faith that is built upon it? Surely the prophet Jeremiah had an infallible assurance of the author of his message, when he pleaded for himself before the princes,; next: He must be both blind and mad that shall mistake wheat for chaff, and on the contrary. What some men speak of a hidden instinct from God moving the minds of men, yet so as they kno

## Inline Structural Marker Candidates

- file: EPUB/ch009.xhtml; text: Now, three ways may a man receive, and be assured that he hath received, this divine mission, or know that he is called of God to the preaching of the word; I mean not that persuasion of divine concurrence which is necessary also for the...
- file: EPUB/ch016.xhtml; text: Explication III. The greatness of the work (for which who is sufficient? 2 Corinthians 2:16); — the strength of the opposition which lies against it, 1 Corinthians 16:9; Revelation 12:12; 2 Timothy 4:3-5; — the concernment of men's souls...
- file: EPUB/ch016.xhtml; text: Let motives hereunto be, — 1. God's command. 2. Our own preservation from sin and protection from punishment, that with others we be not infected and plagued. 3. Christ's delight in the purity of his ordinances.
- file: EPUB/ch016.xhtml; text: Now, to a right performance of this duty, and in the discharge of it, are required, — 1. A due valuation, strong desire, and high esteem of the church's prosperity, in every member of it, Psalm 122:6. 2. Bowels of compassion as a fruit o...
- file: EPUB/ch016.xhtml; text: Motives to this duty are: — 1. The love of God unto us, 1 John 3: 16. 2. The glory of the gospel, exceedingly exalted thereby, Titus 3:8,14; Matthew 5:7.
- file: EPUB/ch016.xhtml; text: Now, to a close adhering to the church wherein we walk in fellowship, in all conditions whatsoever, without dismission attained upon just and equitable grounds, for the embracing of communion in some other churches. Motives are, — 1. The...
- file: EPUB/ch016.xhtml; text: Motives hereunto are, — 1. Christ's example; 2. Scripture precepts; 3. God's not accepting persons; 4. Joint participation of the same common faith, hope, etc; 5. The unprofitableness of all causes of outward differences in the things of...
- file: EPUB/ch016.xhtml; text: These and the like things being duly weighed, let every brother, with Christian courage, admonish from the word every one whom he judgeth to walk disorderly in any particular whatsoever, not to suffer sin upon him, being ready to receive...

## Suspicious Large-Number Starts

- file: EPUB/ch005.xhtml; text: 12. ae. quest.
- file: EPUB/ch022.xhtml; text: 10. I no way doubt of the perpetual existence of innumerable believers in every age, and such as made the profession that is absolutely necessary to salvation, one way or other, though I question a regular association of
- file: EPUB/ch022.xhtml; text: 22. In what sense this church is visible was before declared. Men elected, redeemed, justified, as such, are not visible, for that which makes them so is not; but this hinders not but they may be so upon the other consid
- file: EPUB/ch023.xhtml; text: 29. There being, then, in the world a great multitude, which no man can number, of all nations, kindreds, people, and language, professing the doctrine of the gospel, not tied to mountains or hills, John 4:21, 23, but wo

## Roman Heading Candidates

- file: EPUB/ch030.xhtml; text: C. hardly refrain from calling a man Satan for speaking the truth? It is well if we know of what Spirit we are.
- file: EPUB/ch032.xhtml; text: C. knows how easy it were to make his own words dress him up in all those ornaments wherein he labors to make me appear in the world, by such glosses, inversions, additions, and interpositions, as he is pleased to make u
- file: EPUB/ch039.xhtml; text: C. himself is bound to come into it, and yet I do not think that his not so doing makes him a schismatic; and as for relinquishment, I assert no more than what he himself concludes to be lawful. And thus, Christian reade
- file: EPUB/ch057.xhtml; text: II. From the law of nations. For, —
- file: EPUB/ch057.xhtml; text: V. From the promises of gospel times. For, —
- file: EPUB/ch057.xhtml; text: VI. From the equity of gospel rules For, —
- file: EPUB/ch059.xhtml; text: IV. The payment of tithes, — 1. Before the law, Genesis 14:20, Hebrews 7:4,5; with, 2. The like usage amongst all nations living according to the light of nature; 3. Their establishing under the law; with, 4. The express

## Overlong Heading Candidates

- file: EPUB/ch023.xhtml; tag: h4; text: II. THE second general notion of the church, as it is usually taken, signifies the universality of men professing the doctrine of the gospel and obedience to God in Christ, according to it, throughtout the world.
- file: EPUB/ch025.xhtml; tag: h4; text: III. I NOW descend to the last consideration of a church, in the most usual acceptation of that name in the New Testament, — that is, of a particular instituted church.
- file: EPUB/ch049.xhtml; tag: h3; text: [Inconsistent expressions of Parker in regard to the power of the magistrate and the rights of conscience — The design of his discourse to prove the magistrate's authority to govern the consciences of his subjects in affairs of religion ...
- file: EPUB/ch050.xhtml; tag: h3; text: [Alleged power of the magistrate over the conscience in matters of morality refuted — Distinction between moral virtue and grace — Meaning of the terms — Four propositions of Parker on grace and virtue considered — Agreement between the ...
- file: EPUB/ch057.xhtml; tag: h4; text: VIII. From the confession of those, in particular, who suffer in the world on the account of the largeness of their principles as to toleration and forbearance, the Independents, whose words in their Confession are as followeth: —
- file: EPUB/ch059.xhtml; tag: h4; text: III. Where God, by providential dispensations, hath laid things in a nation in a subserviency to an institution of Christ, according to his promise, Psalm 2:8, Isaiah 49:23, as he hath done in this case, to oppose that order of things se...
- file: EPUB/ch059.xhtml; tag: h4; text: V. A maintenance, by a participation in men's temporals, for those who preach the gospel, being expressly appointed by Jesus Christ, and reference for the proportion being directly made by the apostle unto the proportion allotted by God ...
- file: EPUB/ch059.xhtml; tag: h4; text: VI. To deprive preachers of the gospel, when sent out into their Master's harvest, and attending unto their work, according to the best of the light which the present age enjoyeth, with visible and glorious success, of the portion, hire,...
- file: EPUB/ch059.xhtml; tag: h4; text: VII. Wherever, or in what nation soever, there hath been a removal of the maintenance provided in the providence of God for the necessary supportment of the public dispensers of the word, the issue hath been a fatal and irrecoverable dis...
- file: EPUB/ch059.xhtml; tag: h4; text: VIII. An alteration of the way of payment of that revenue which is provided in the providence of God for public preachers, by the way of tithes, into some other way of payment, continuing the present right, is not obnoxious or liable to ...

## Short Fragments

- file: EPUB/ch002.xhtml; text: M AY 11, 1644.
- file: EPUB/ch002.xhtml; text: JOSEPH CARYL.
- file: EPUB/ch007.xhtml; text: Whence I conclude, —
- file: EPUB/ch012.xhtml; text: Τῷ Θεῷ ἀριστομεγίστῳ δόζα .
- file: EPUB/ch016.xhtml; text: 17.
- file: EPUB/ch016.xhtml; text: 2 Thessalonians 3:1,2,
- file: EPUB/ch016.xhtml; text: 1 Timothy 1:16-18,
- file: EPUB/ch016.xhtml; text: Song of Solomon 6:4,
- file: EPUB/ch016.xhtml; text: Acts 18:26,
- file: EPUB/ch016.xhtml; text: Motives hereunto are, —

## Enumerator Sequence Candidates

- file: EPUB/ch023.xhtml; marker: (2.); family: paren_decimal; context: (2.) That doing so, in the course of our lives we manifest and declare a principle that is utterly inconsistent with the belief of those truths which outwardly we profess; or, —
- file: EPUB/ch042.xhtml; marker: [16]; family: bracket_decimal; context: Nor did I, as is pretended, plead for their presbyterian way in the year [16]46; all the ministers almost in the county of Essex know the contrary, one especially, being a man of great ability and moderation of spirit, and for his knowle...

## Repeated Windows

- phrase: the grounds and reasons on which protestant dissenters desire their; count: 6
- phrase: ii word of advice to the citizens of london this; count: 6
- phrase: word of advice to the citizens of london this tract; count: 6
- phrase: of advice to the citizens of london this tract only; count: 6
- phrase: advice to the citizens of london this tract only appeared; count: 6
- phrase: to the citizens of london this tract only appeared in; count: 6
- phrase: the citizens of london this tract only appeared in print; count: 6
- phrase: citizens of london this tract only appeared in print in; count: 6
- phrase: of london this tract only appeared in print in 1721; count: 6
- phrase: london this tract only appeared in print in 1721 in; count: 6

## Missing Word Samples

- word: self; pdf: 13; epub: 6
- word: fellow; pdf: 3; epub: 0
- word: re; pdf: 3; epub: 1

## Excess Word Samples

- word: volume; pdf: 6; epub: 26
- word: london; pdf: 14; epub: 27
- word: penalty; pdf: 11; epub: 24
- word: ; pdf: 8; epub: 21
- word: bill; pdf: 7; epub: 17
- word: citizens; pdf: 9; epub: 18
- word: conventicle; pdf: 5; epub: 14
- word: folio; pdf: 2; epub: 11
- word: ; pdf: 2; epub: 11
- word: renewed; pdf: 9; epub: 17

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
