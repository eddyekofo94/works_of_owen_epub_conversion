# Text Integrity Audit: Volume 1

- Status: **WARN**
- Warnings: 9
- PDF pages: 644
- EPUB text files: 83
- EPUB paragraphs/headings: 3170

## Coverage

- PDF content tokens: 210900
- EPUB content tokens: 214356
- Approximate PDF-to-EPUB coverage ratio: 0.9981
- Pages checked: 635
- Weak page matches: 6
- Dense source windows checked: 25724
- Missing dense source-window pages: 170
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 602
- Top-of-page windows skipped as unstable: 21
- Missing top-of-page body windows: 2
- Bottom-of-page body windows checked: 555
- Bottom-of-page windows skipped as unstable: 6
- Missing bottom-of-page body windows: 22

## Paragraphs

- Body paragraphs checked: 2863
- Possible faulty paragraph splits: 81
- Structural starts excluded from split warnings: 176
- Short fragments: 100
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 1
- Roman heading candidates: 33
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 313
- EPUB enumerator markers: 317
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
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 3; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ
- page: 4; sample: and discourses on the glory of christ refatory ote he ditor reface he eader
- page: 5; sample: heaven meditations and discourses concerning the glory of christ applied etc riginal reface application
- page: 7; sample: general preface would be presumption to enter upon any commendation of john owen as
- page: 9; sample: embraces the most comprehensive view of this vitally-important subject his exposition of psalm 130
- page: 10; sample: learned puritan we are informed by dr steven f2 that his exposition of the
- page: 11; sample: whose literary industry the church of christ had been se largely indebted it would
- page: 12; sample: russell dissenting minister in the neighborhood of london as the first attempt f4 to
- page: 19; sample: χριστολογια christologia or declaration of the glorious mystery of the person of christ god
- page: 20; sample: prefatory note to object of dr owen in this treatise is to illustrate the

## Missing Top-Of-Page Body Windows

- page: 157; sample: Hebrews 2:18; 4:15; 5:2. So is he also, as he alone who is able to succor, to relieve, and to deliver them. "He is able to succor them that are
- page: 619; sample: A. No; essentially they are but one,f91 differing only in some outward administrations.

## Missing Bottom-Of-Page Body Windows

- page: 25; sample: Matthew 16:18:) whereon the church is built: (
- page: 87; sample: Zechariah 6:13,) or the originally between Jehovah and the Branch, (
- page: 98; sample: John 1:18; the Father, he has declared him:"
- page: 99; sample: Exodus 33:18. Moses had Moses: "I beseech thee, show me thy glory:"
- page: 105; sample: John 1:1. "The Word was God," in with God, and the Word was God:"
- page: 156; sample: suffered, being tempted, he is touched with a feeling of our infirmities, and knows how to have compassion on them that are out of the way,
- page: 195; sample: Matthew 3:17, "Lo, a voice from heaven, saying, heaven afterwards,
- page: 241; sample: Ecclesiastes 7:29; unto. Wherein it did consist, see
- page: 302; sample: Hebrews 1:3. These things are all spoken of the person of Christ, but belong unto it on account of his divine nature. So is it said of him, "Unto
- page: 318; sample: 1:11, — and the "heaven must receive him," chap. 3:21; not these aspectable heavens which we behold, — for in his ascension "he passed

## Possible Paragraph Splits

- file: EPUB/ch004.xhtml; previous: their personality, are the formal object and term of divine worship; but in the worship of one, they are all worshipped as one God over all, blessed for ever. See Aquin. 22 q., 81,; next: a. 3, ad prim., and q., 84,
- file: EPUB/ch004.xhtml; previous: a. 3, ad prim., and q., 84,; next: a. 1, ad tertium; Alexand. Alens. p. 3, q. 30,
- file: EPUB/ch004.xhtml; previous: m. 1,; next: a. 3.
- file: EPUB/ch005.xhtml; previous: PETER'S CONFESSION; MATTHEW 16:16 — CONCEITS OF THE PAPISTS THEREON — THE SUBSTANCE AND EXCELLENCY OF THAT CONFESSION; next: Our blessed Savior, inquiring of his disciples their apprehensions concerning his person, and their faith in him, Simon Peter — as he was usually the forwardest on all such occasio
- file: EPUB/ch006.xhtml; previous: OPPOSITION MADE UNTO THE CHURCH AS BUILT UPON THE PERSON OF CHRIST; next: There are in the words of our Savior unto Peter concerning the foundation of the church, a promise of its preservation, and a prediction of the opposition that should be made there
- file: EPUB/ch007.xhtml; previous: THE PERSON OF CHRIST THE MOST INEFFABLE EFFECT OF DIVINE WISDOM AND GOODNESS — THENCE THE NEXT CAUSE OF ALL TRUE RELIGION — IN WHAT SENSE IT IS SO; next: The person of Christ is the most glorious and ineffable effect of divine wisdom, grace, and power; and therefore is the next foundation of all acceptable religion and worship. The
- file: EPUB/ch008.xhtml; previous: TO PERSON OF CHRIST THE FOUNDATION OF ALL THE COUNSELS OF GOD; next: Secondly, The person of Christ is the foundation of all the counsels of God, as unto his own eternal glory in the vocation, sanctification, and salvation of the church. That which
- file: EPUB/ch009.xhtml; previous: THE PERSON OF CHRIST THE GREAT REPRESENTATIVE OF GOD AND HIS WILL; next: What may be known of God, is, — his nature and existence, with the holy counsels of his will. A representation of them unto us is the foundation of all religion, and the means of o
- file: EPUB/ch011.xhtml; previous: POWER AND EFFICACY COMMUNICATED UNTO THE OFFICE OF CHRIST, FOR THE SALVATION OF THE CHURCH, FROM HIS PERSON; next: It is by the exercise and discharge of the office of Christ — as the king, priest, and prophet of the church — that we are redeemed, sanctified, and saved. Thereby does he immediat
- file: EPUB/ch011.xhtml; previous: And he discharged this office four ways: —; next: (1st,) By personal appearances in the likeness of human nature, in the shape of a man, as an indication of his future incarnation; and under those appearances instructing the churc

## Inline Structural Marker Candidates

- file: EPUB/ch078.xhtml; text: A. M. of Northampton, 1781. FT4 A statement occurs in the "Encyclopaedia Britannica" that Owen's works are printed in seven folio volumes. If it be meant that there are seven folio volumes of Owen's works, there is a sense in which the s...

## Suspicious Large-Number Starts

- file: EPUB/ch070.xhtml; text: 12. Matthew 5:20;, 8:1Romans, 8:1,2; Ephesians 4:22, 23; Titus 2:12.

## Roman Heading Candidates

- file: EPUB/ch011.xhtml; text: I. The first of these is, that he should have a nature provided for him, which originally was not his own. For in his divine nature, singly considered, he had no such relation unto them for whom he was to discharge his o
- file: EPUB/ch013.xhtml; text: IV. The use we make of him, for the attaining and receiving of all Gospel privileges — all grace and glory.
- file: EPUB/ch013.xhtml; text: I. The person of Christ is the object of divine honor and worship. The formal object and reason hereof is the divine nature, and its essential infinite excellencies. For they are nothing but that respect unto the Divine
- file: EPUB/ch019.xhtml; text: IV. The last thing proposed concerning the person of Christ, was the use of it unto believers, in the whole of their relation unto God and duty towards him. And the things belonging thereunto may be reduced unto these ge
- file: EPUB/ch022.xhtml; text: II. The union of the two natures in that single person which is consequential thereon.
- file: EPUB/ch022.xhtml; text: III. The mutual communication of those distinct natures, the divine and human, by virtue of that union.
- file: EPUB/ch022.xhtml; text: IV. The enunciations or predications concerning the person of Christ, which follow on that union and communion.
- file: EPUB/ch022.xhtml; text: I. The first thing in the divine constitution of the person of Christ as God and man, is assumption. That ineffable divine act I intend whereby the person of the Son of God assumed our nature, or took it into a personal
- file: EPUB/ch022.xhtml; text: II. That which followeth hereon, is the union of the two natures in the same person, or the hypostatical union. This is included and asserted in a multitude of divine testimonies.
- file: EPUB/ch022.xhtml; text: III. Concurrent with, and in part consequent unto, this union, is the communion of the distinct natures of Christ hypostatically united. And herein we may consider, —

## Short Fragments

- file: EPUB/ch006.xhtml; text: For,
- file: EPUB/ch006.xhtml; text: As,
- file: EPUB/ch009.xhtml; text: Wherefore —
- file: EPUB/ch009.xhtml; text: And —
- file: EPUB/ch009.xhtml; text: All this himself instructs us in.
- file: EPUB/ch011.xhtml; text: This must be declared.
- file: EPUB/ch011.xhtml; text: For —
- file: EPUB/ch011.xhtml; text: For —
- file: EPUB/ch013.xhtml; text: 2ndly, Invocation.
- file: EPUB/ch014.xhtml; text: Or —

## Repeated Windows

- phrase: the glory of god in the face of jesus christ; count: 12
- phrase: between our beholding the glory of christ by faith in; count: 6
- phrase: our beholding the glory of christ by faith in this; count: 6
- phrase: beholding the glory of christ by faith in this world; count: 6
- phrase: the glory of christ by faith in this world and; count: 6
- phrase: glory of christ by faith in this world and by; count: 6
- phrase: of christ by faith in this world and by sight; count: 6
- phrase: christ by faith in this world and by sight in; count: 6
- phrase: by faith in this world and by sight in heaven; count: 6
- phrase: of the glory of god in the face of jesus; count: 6

## Missing Word Samples

- word: faithfullness; pdf: 7; epub: 0
- word: pre; pdf: 6; epub: 2
- word: eminence; pdf: 5; epub: 1
- word: ote; pdf: 3; epub: 0
- word: reface; pdf: 3; epub: 0
- word: mindedness; pdf: 3; epub: 0

## Excess Word Samples

- word: psalms; pdf: 2; epub: 16
- word: faithfulness; pdf: 5; epub: 12

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
