# Text Integrity Audit: Volume 2

- Status: **WARN**
- Warnings: 9
- PDF pages: 555
- EPUB text files: 47
- EPUB paragraphs/headings: 2365

## Coverage

- PDF content tokens: 189781
- EPUB content tokens: 189073
- Approximate PDF-to-EPUB coverage ratio: 0.9953
- Pages checked: 550
- Weak page matches: 9
- Dense source windows checked: 835
- Missing dense source-window pages: 539
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 542
- Top-of-page windows skipped as unstable: 29
- Missing top-of-page body windows: 3
- Bottom-of-page body windows checked: 507
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 15

## Paragraphs

- Body paragraphs checked: 2023
- Possible faulty paragraph splits: 201
- Structural starts excluded from split warnings: 251
- Short fragments: 36
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 2
- Roman heading candidates: 0
- Overlong heading candidates: 5
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 478
- EPUB enumerator markers: 478
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 450
- EPUB Greek words: 449
- Greek word coverage ratio: 0.9977
- PDF Hebrew words: 88
- EPUB Hebrew words: 89
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 25
- Missing Greek clauses: 0
- Hebrew clauses checked: 11
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 8; sample: the doctrine of distinct communion with the divine persons to be new fangled one
- page: 10; sample: 10 of communion with god the father son and holy ghost each person distinctly
- page: 11; sample: 11 prefatory note the reader may be referred to the life of dr owen
- page: 12; sample: 12 part ii the reality of communion with christ is proved chap and the
- page: 13; sample: 13 part chapter that the saints have communion with god john considered to that
- page: 14; sample: 14 by nature since the entrance of sin no man hath any communion with
- page: 15; sample: 15 access with confidence to god ephesians 12 this boldness and access with confidence
- page: 16; sample: 16 they had communion in that cruel act of revenge and murder our communion
- page: 17; sample: 17 perfect and complete in the full fruition of his glory and total giving
- page: 18; sample: 18 chapter that the saints have this communion distinctly with the father son and

## Missing Top-Of-Page Body Windows

- page: 25; sample: wherein the saints have communion with God. f19 As all the spiritual ascendings of their souls are assigned unto them respectively, so all their
- page: 155; sample: Two things are required, that we may pray for the things in the promise, as they are in the promise: —
- page: 344; sample: are not themselves altogether insensible. Among the things which this sort of men sought to make an advantage of against me, I found that two or

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 39; sample: John 1:16. Though the love of the might receive, and grace for grace,"
- page: 57; sample: Ephesians 5:2; so from the graces wherewith the blood of his atonement,
- page: 59; sample: Isaiah 32:2. From the power of corruptions, rock in a weary land,"
- page: 128; sample: Romans 9:31,32, they have this issue, the apostle witnesseth,
- page: 156; sample: Song of Solomon 2:3. And down under his shadow with great delight,
- page: 194; sample: John 17:9. There were not worse in the world, really and evidently, than many of them that crucified him; yet, as a man, subject to the law, he
- page: 214; sample: and that only. Now, this is most evident: — (1.) What he did, he did for us, and not for himself:
- page: 268; sample: 1 Peter 2:5; — a "chosen it. It is composed of "living stones,"
- page: 314; sample: Acts 13:2; he furnisheth them work, and they are separated unto him,

## Possible Paragraph Splits

- file: EPUB/ch002.xhtml; previous: Reader, I am Thy servant in Christ Jesus; next: DANIEL BURGESS
- file: EPUB/ch008.xhtml; previous: n what the peculiar appropriation of this distinct communion unto the several persons doth consist, must, in the first place, be made manifest. 14 1 John 5:7, the apostle tells us,; next: In heaven they are, and bear witness to us. And what is it that they bear witness unto? Unto the sonship of Christ, and the salvation of believers in his blood. Of the carrying on
- file: EPUB/ch008.xhtml; previous: Sometimes the Son only is spoken of, as to this purpose. 1 Corinthians 1:9,; next: — of which place afterward.
- file: EPUB/ch008.xhtml; previous: Sometimes the Spirit alone is mentioned. 2 Corinthians 13:14,; next: This distinct communion, then, of the saints with the Father, Son, and Spirit, is very plain in the Scripture; but yet it may admit of farther demonstration Only this caution I mus
- file: EPUB/ch008.xhtml; previous: er: these graces as acted in prayer and praises, and as clothed with instituted worship, are peculiarly directed unto him. "Ye call on the Father," 1 Peter 1:17, Ephesians 3:14,15,; next: Bowing the knee compriseth the whole worship of God, both that which is moral, in the universal obedience he requireth, and those peculiar ways of carrying it on which are by him a
- file: EPUB/ch008.xhtml; previous: therefore the same apostle doth, in another place, expressly conjoin, and yet as expressly distinguish, the Father and the Son in directing his supplications, 1 Thessalonians 3:11,; next: The like precedent, also, have you of thanksgiving, Ephesians 1:3,4, "Blessed be the God and Father of our Lord Jesus Christ," etc. I shall not add those very many places wherein t
- file: EPUB/ch008.xhtml; previous: on hath everlasting life," verse 36. "This is the work of God, that ye believe on him whom he hath sent," John 6:29,40; 1 John 5:10. The foundation of the whole is laid, John 5:23,; next: But of this honor and worship of the Son I have treated at large elsewhere; 18 and shall not in general insist upon it again. For love, I shall only add that solemn apostolical ben
- file: EPUB/ch008.xhtml; previous: 2:22-24, 1 John 5:10-13; Hebrews 1:6; Philippians 29:10 2:10; John 5:23.) and distinctly directed unto the Son, is abundantly manifest from that solemn doxology, Revelation 1:5,6,; next: Which yet is set forth with more glory, chapter 5:8,
- file: EPUB/ch008.xhtml; previous: Which yet is set forth with more glory, chapter 5:8,; next: and verses 13,14, "Every creature which is in heaven, and on the earth, and under the earth, and such as are in the sea, and all that are in them, heard I saying, Blessing, and hon
- file: EPUB/ch008.xhtml; previous: And you have distinct mention of the love of the Splint, Romans 15:30. The apostle also peculiarly directs his supplication to him in that solemn benediction, 2 Corinthians 13:14,; next: And such benedictions are originally supplications. He is likewise entitled unto all instituted worship, from the appointment of the administration of baptism in his name, Matthew

## Suspicious Large-Number Starts

- file: EPUB/ch035.xhtml; text: 280. "As for example," saith he, "Christ is called a husband, the church his spouse; and now all the invitations of the gospel are Christ's wooing and making love to his spouse; — and what other men call believing the go
- file: EPUB/ch035.xhtml; text: 14. And it is strange to apprehend how he came to imagine that I said he did it not as our mediator, but as a private man. That which, possibly, might cast his thoughts into this disorder was, that he knew not that Chris

## Overlong Heading Candidates

- file: EPUB/ch013.xhtml; tag: h4; text: II. Having manifested that the saints hold peculiar fellowship with the Lord Jesus, it neatly follows that we show wherein it is that they have this peculiar communion with him.
- file: EPUB/ch016.xhtml; tag: h4; text: II. For the knowledge of ourselves, which is the SECOND part of our wisdom, this consists in these three things, which our Savior sends his Spirit to convince the world of, — even "sin, righteousness, and judgement," John 16:8.
- file: EPUB/ch018.xhtml; tag: h4; text: II. Christ values his saints, values believers (which is the second branch of that conjugal affection he bears towards them), having taken them into the relation whereof we speak.
- file: EPUB/ch021.xhtml; tag: h4; text: I. Communion with Christ in purchased grace, as unto acceptation with God, from the obedience of his life and efficacy of his death, is the first thing we inquire into.
- file: EPUB/ch022.xhtml; tag: h4; text: II. Our communion with the Lord Jesus as to that grace of sanctification and purification whereof we have made mention, in the several distinctions and degrees thereof, formerly, is neatly to be considered.

## Short Fragments

- file: EPUB/ch002.xhtml; text: DANIEL BURGESS
- file: EPUB/ch008.xhtml; text: — of which place afterward.
- file: EPUB/ch009.xhtml; text: John 16:26,27, saith our Savior,
- file: EPUB/ch016.xhtml; text: Hebrews 1:3; of which before.
- file: EPUB/ch016.xhtml; text: Wherefore, —
- file: EPUB/ch018.xhtml; text: Afflictions.
- file: EPUB/ch019.xhtml; text: Hereof, then, are two parts: —
- file: EPUB/ch020.xhtml; text: Of which in the ensuing chapters.
- file: EPUB/ch021.xhtml; text: Therefore, —
- file: EPUB/ch021.xhtml; text: [2ndly.] Peace.

## Enumerator Sequence Candidates

- file: EPUB/ch014.xhtml; marker: (2.); family: paren_decimal; context: (2.) The next thing that comes under consideration is, the way whereby we hold communion with the Lord Christ, in respect of that personal grace whereof we have spoken. Now, this the S

## Repeated Windows

- phrase: bare our sins in his own body on the tree; count: 7
- phrase: is with the father and with his son jesus christ; count: 6
- phrase: pleased the father that in him should all fullness dwell; count: 6
- phrase: the father that in him should all fullness dwell colossians; count: 6
- phrase: father that in him should all fullness dwell colossians 19; count: 6
- phrase: our fellowship is with the father and with his son; count: 5
- phrase: fellowship is with the father and with his son jesus; count: 5
- phrase: it pleased the father that in him should all fullness; count: 5
- phrase: to be propitiation through faith in his blood to declare; count: 5
- phrase: be propitiation through faith in his blood to declare his; count: 5

## Missing Word Samples

- word: cant; pdf: 3; epub: 1

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
