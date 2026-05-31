# Text Integrity Audit: Volume 7

- Status: **WARN**
- Warnings: 12
- PDF pages: 683
- EPUB text files: 62
- EPUB paragraphs/headings: 2379

## Coverage

- PDF content tokens: 232551
- EPUB content tokens: 233372
- Approximate PDF-to-EPUB coverage ratio: 0.9968
- Pages checked: 679
- Weak page matches: 4
- Dense source windows checked: 852
- Missing dense source-window pages: 665
- Front CONTENTS pages checked: 5
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 667
- Top-of-page windows skipped as unstable: 16
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 632
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 1

## Paragraphs

- Body paragraphs checked: 2013
- Possible faulty paragraph splits: 126
- Structural starts excluded from split warnings: 285
- Short fragments: 16
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 3
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 1
- Roman heading candidates: 6
- Overlong heading candidates: 26
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 381
- EPUB enumerator markers: 386
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 325
- EPUB Greek words: 325
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 26
- EPUB Hebrew words: 26
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 18
- Missing Greek clauses: 0
- Hebrew clauses checked: 3
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
- `flat_analysis_chapters`: 1 ANALYSIS chapter(s) appear under-structured — fewer outline markers than expected. Check extraction quality for these chapters.

## Missing Dense Source Windows

- page: 8; sample: in an exposition of hebrews 4-6 with an inquiry into the causes and reasons
- page: 10; sample: 10 strain of solemn appeal appropriate to work written according to its author amid
- page: 11; sample: 11 of the zealous orthodoxy of the reformation the rise of arminianism and socinianism
- page: 12; sample: 12 national vices ignorance of the spiritual beauty of religion the operations of satan
- page: 13; sample: 13 to the reader some brief account of the occasion and design of the
- page: 14; sample: 14 pleasures of it with readiness for the cross are all so overgrown and
- page: 15; sample: 15 professors it will not long abide the shock of that opposition which it
- page: 16; sample: 16 the corrupt worldly conversation of the generality of the members of its communion
- page: 17; sample: 17 it should get ground and enlarge its territories unless it be among them
- page: 18; sample: 18 things in the world by the confident use of this artifice and the

## Missing Top-Of-Page Body Windows

- page: 183; sample: 12:39-41, and that of the apostles, Acts 28:25-27, and is expounded,

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53

## Possible Paragraph Splits

- file: EPUB/ch001.xhtml; previous: EDITED BY; next: WILLIAM H. GOOLD
- file: EPUB/ch001.xhtml; previous: WILLIAM H. GOOLD; next: NATURE AND CAUSES OF APOSTASY FROM THE GOSPEL.
- file: EPUB/ch003.xhtml; previous: rked the reign of Charles II has often been the subject of speculation and inquiry. Mr Macaulay thus confirms our author's estimate of the rapid decline of morality at this time: —; next: The historian, dealing with the surface of affairs rather than with the springs of conduct, may account the vulgar theory of a reaction against enforced strictness sufficient to ex
- file: EPUB/ch005.xhtml; previous: each shall be, if they endeavor not to prevent it with their utmost diligence, and the open hazard of all their earthly concerns. A learned writer of the church of England affirms,; next: And after he had declared that "ministers of the gospel may deny Christ, or manifest their being ashamed of the gospel, by not opposing his word at they ought unto the sins of men,
- file: EPUB/ch007.xhtml; previous: Certainly the Lord Christ may say to the churches and nations among whom his name is yet owned in the world, what God said of old concerning that of the Jews, then his only church,; next: Yea, to most of them as in another place,
- file: EPUB/ch007.xhtml; previous: Yea, to most of them as in another place,; next: The greatness of the evil complained of, the secret mystery of its accomplishment, the unreasonableness, folly, and ingratitude of the fact, the strangeness of the event, make the
- file: EPUB/ch007.xhtml; previous: kedness in its relinquishment as to its principles and obedience, may well be expressed as God doth in the inferior instance of the apostasy of the Jewish church: Jeremiah 2:11,12,; next: Yet thus is it, and no otherwise, as we shall afterward manifest, amongst the generality of them that are called Christians in the world.
- file: EPUB/ch007.xhtml; previous: y thought sufficient to repel the charge of the prophets, to vindicate their innocency, and secure their peace. The reply of the prophet unto them will equally serve in both cases,; next: A plea of innocency and hope of impunity, under an evident guilt of the highest immoralities and the vilest of superstitions, do equally participate of folly and impudence.
- file: EPUB/ch007.xhtml; previous: bedience, which the gospel requireth. But this is no other but an account of the true nature of that apostasy of the latter times which is foretold by the apostle, 2 Timothy 3:1-5,; next: Under the power of the most filthy and outrageous lusts, men frame to themselves an outward shape, image, and representation of holiness; they delineate a form of religion by a sub
- file: EPUB/ch008.xhtml; previous: n Timothy to be careful herein, manifest both the weight he laid upon it, the difficulty that was in it, and the danger of miscarriage wherewith it was attended: 1 Timothy 6:20,21,; next: And the same apostle expressly mentions the proneness of some to relinquish the truth of the gospel; whom, therefore, he would have rebuked sharply,

## Inline Structural Marker Candidates

- file: EPUB/ch006.xhtml; text: They may taste, — 1. Of the word in its truth, not its power; 2. Of the worship of the church in its outward order, not in its inward beauty; 3. Of the gifts of the church, not its graces.
- file: EPUB/ch021.xhtml; text: An inquiry follows into the objects of spiritual thoughts; which are, — 1. The dispensations of Providence; 2. Special trials and temptations; and 3. Heavenly and eternal realities. In regard to the latter, —
- file: EPUB/ch022.xhtml; text: An inquiry follows into the objects of spiritual thoughts; which are, — 1. The dispensations of Providence; 2. Special trials and temptations; and 3. Heavenly and eternal realities. In regard to the latter, —

## Suspicious Large-Number Starts

- file: EPUB/ch006.xhtml; text: 23. Let them beware by whom they are despised.

## Roman Heading Candidates

- file: EPUB/ch004.xhtml; text: I. Apostasy from the doctrines of the gospel is illustrated by facts in the history of the ancient church, and by the predictions of the a apostles, who foretold, —
- file: EPUB/ch004.xhtml; text: II. Apostasy from the holiness of the gospel is next considered theoretically, in reference, —
- file: EPUB/ch004.xhtml; text: III. Apostasy from purity of worship is exhibited, in the neglect of what God has appointed, and by additions which he has not appointed, in the ordinances of the gospel,
- file: EPUB/ch047.xhtml; text: I. 1. That spiritual life whereof we are made partakers in this world is threefold, or there are three gospel privileges or graces so expressed: —
- file: EPUB/ch050.xhtml; text: I. As to the nature of this dominion, — 1. It is evil and perverse, (1.) as usurped, and (2.) as exercised to evil ends. 2. It implies no force contrary to the human will
- file: EPUB/ch050.xhtml; text: II. As to the evidence of this dominion, —

## Overlong Heading Candidates

- file: EPUB/ch006.xhtml; tag: h4; text: II. The Holy Ghost, for the remission of the mysteries of the gospel, and the institution of the ordinances of spiritual worship, is the great gift of God under the new testament.
- file: EPUB/ch006.xhtml; tag: h4; text: III. There is a goodness and excellency in this heavenly gift which may be tasted or experienced in some measure by such as never receive them in their life, power, and efficacy.
- file: EPUB/ch006.xhtml; tag: h4; text: IV. A rejection of the gospel, its truth and worship, after some experience had of their worth and excellency, is a high aggravation of sin, and a certain presage of destruction.
- file: EPUB/ch006.xhtml; tag: h4; text: I. There is a goodness and excellency in the word of God able to attract and affect the minds of men who yet never arrive at sincere obedience unto it.
- file: EPUB/ch009.xhtml; tag: h4; text: I. That rooted enmity which is in the minds of men by nature unto spiritual things, abiding uncured under the profession of the gospel, is the original and first spring of this apostasy.
- file: EPUB/ch010.xhtml; tag: h4; text: II. THE second spring or cause of defection from the gospel in any kind, is that spiritual darkness and ignorance which abides in the minds of men under the profession of the truth.
- file: EPUB/ch011.xhtml; tag: h4; text: III. THE innate pride and vanity of the minds of men is another means whereby they are disposed and inclined unto an apostasy from the profession of evangelical truth.
- file: EPUB/ch013.xhtml; tag: h4; text: II. Again; others confine the _whole_ of their obedience unto _morality,_ and deride whatever is pleaded as above it and beyond it, under the name of evangelical grace, as "enthusiastical folly." And the truth is, if those persons who pl...
- file: EPUB/ch013.xhtml; tag: h4; text: III. Some there are who, as unto themselves, pretend they have attained unto _perfection_ already in this world; such a perfection in all degrees of holiness as the gospel is but an introduction towards.
- file: EPUB/ch014.xhtml; tag: h4; text: I. The first occasion hereof, in all ages, hath been given by or taken from the public readers, guides, or leaders of the people in the matter of religion.

## Short Fragments

- file: EPUB/ch001.xhtml; text: EDITED BY
- file: EPUB/ch001.xhtml; text: WILLIAM H. GOOLD
- file: EPUB/ch002.xhtml; text: SEARCH THE SCRIPTURES — JOHN 5:39.
- file: EPUB/ch002.xhtml; text: LONDON: 1676.
- file: EPUB/ch006.xhtml; text: And, —
- file: EPUB/ch006.xhtml; text: Ans.
- file: EPUB/ch014.xhtml; text: Verse 20,
- file: EPUB/ch018.xhtml; text: I answer, —
- file: EPUB/ch028.xhtml; text: I answer, —
- file: EPUB/ch047.xhtml; text: And this it doth several ways: —

## Enumerator Sequence Candidates

- file: EPUB/ch031.xhtml; marker: (2.); family: paren_decimal; context: (2.) WE have treated in general before of the proper objects of our spiritual thoughts as unto our present duty. That which we were last engaged in is an especial instance in heavenly
- file: EPUB/ch031.xhtml; marker: [3.]; family: bracket_decimal; context: [3.] Again; meditate and think of the glory of heaven so as to compare it with the opposite state of death and eternal misery. Few men care to think much of hell, and the everlasting t

## Repeated Windows

- phrase: nature of this grace and duty of being spiritually minded; count: 4
- phrase: the true notion and consideration of spiritual and heavenly things; count: 4
- phrase: dominion of sin which we are freed from and discharged; count: 4
- phrase: of sin which we are freed from and discharged of; count: 4
- phrase: sin which we are freed from and discharged of by; count: 4
- phrase: which we are freed from and discharged of by grace; count: 4
- phrase: what is the assurance given us and what are the; count: 4
- phrase: is the assurance given us and what are the grounds; count: 4
- phrase: that we are not under the law but under grace; count: 4
- phrase: the good word of god and the powers of the; count: 4

## Excess Word Samples

- word: digital; pdf: 0; epub: 6

## Flat ANALYSIS Chapters

**1 ANALYSIS chapter(s)** appear under-structured — fewer outline markers than expected.  Extraction may have failed to parse the outline.

## Flat Analysis Details

- file: EPUB/ch022.xhtml; paragraph_count: 7; structural_line_count: 2; note: ANALYSIS chapter appears flat — fewer structural outline lines than expected. Check extraction quality.

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
