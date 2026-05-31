# Text Integrity Audit: Volume 1

- Status: **WARN**
- Warnings: 9
- PDF pages: 633
- EPUB text files: 82
- EPUB paragraphs/headings: 2730

## Coverage

- PDF content tokens: 208214
- EPUB content tokens: 208118
- Approximate PDF-to-EPUB coverage ratio: 0.9968
- Pages checked: 624
- Weak page matches: 17
- Dense source windows checked: 741
- Missing dense source-window pages: 612
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 591
- Top-of-page windows skipped as unstable: 13
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 538
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 2

## Paragraphs

- Body paragraphs checked: 2263
- Possible faulty paragraph splits: 101
- Structural starts excluded from split warnings: 126
- Short fragments: 7
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 10
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 310
- EPUB enumerator markers: 310
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 812
- EPUB Greek words: 812
- Greek word coverage ratio: 0.9987
- PDF Hebrew words: 20
- EPUB Hebrew words: 20
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 38
- Missing Greek clauses: 0
- Hebrew clauses checked: 1
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 3; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ
- page: 4; sample: note by the editor preface to the reader the explication of the text john
- page: 5; sample: under the old testament the glory of christ in his intimate conjunction with the
- page: 6; sample: of corrupted nature of the incarnation of christ 10 of the person of jesus
- page: 9; sample: embraces the most comprehensive view of this vitally-important subject his exposition of psalm 130
- page: 10; sample: 10 dutch divines the most favorable mention is made of the various treatises of
- page: 11; sample: 11 ushered under their auspices into public notice there was large body of subscribers
- page: 12; sample: 12 the edition was comprised in twenty-one octavo volumes the first however consisting of
- page: 13; sample: 13 that the theologoumena had been much disfigured with errors nobis praelo capite ad
- page: 14; sample: 14 the punctuation has undergone thorough revisal passages which from negligence in this respect

## Missing Top-Of-Page Body Windows

- page: 613; sample: A. In that for us he underwent the punishment due to our sin. Isaiah

## Missing Bottom-Of-Page Body Windows

- page: 26; sample: oijkodomh>sw mou th<n ejhkklhsi>an, kai< pu>lai a[|dou ouj katiscu>sousin aujth~v".
- page: 293; sample: of God. Such are "ejnsa>rkwsiv", "incarnation;" "ejnswma>twsiv", "embodying," "ejnanqrw>phsiv", "inhumanation;" "hJ despotikh<

## Possible Paragraph Splits

- file: EPUB/ch004.xhtml; previous: on, the Only-begotten, the First-begotten, the Door, the Way, the Arrow, Wisdom, and sundry other things." And Ennodius has, as it were, turned this passage of Jerome into verse: —; next: Chap. IV. That he was the foundation of all the holy counsels of God, with respect unto the vocation, sanctification, justification, and eternal salvation of the church, is, in the
- file: EPUB/ch009.xhtml; previous: nswer hereunto God tells him, that he cannot see his face and live; none can have either bodily sight or direct mental intuition of the Divine Being. But this I will do, saith God,; next: This is all that God would grant, viz, such external representations of himself, in the proclamation of his name, and created appearances of his glory, as we have of a man whose ba
- file: EPUB/ch009.xhtml; previous: he being of God, his infinite wisdom, power, and goodness — viz., in the impressions and characters of them on the things that were made — in their own representations of him, they; next: Wherefore this common presumption — that there was no way to attain a due sense of the Divine Being but by some representation of it — though true in itself, yet, by the craft of S
- file: EPUB/ch009.xhtml; previous: This was the testimony which the apostles gave concerning him, when he dwelt among them in the days of his flesh. They saw; next: The divine glory was manifest in him, and in him they saw the glory of the Father. So the same apostle witnesses again, who recorded this testimony:
- file: EPUB/ch010.xhtml; previous: wisdom and knowledge of God — in his counsels concerning the vocation, sanctification, and salvation, of the church — concerning which the apostle falls into that holy admiration,; next: And they are called "treasures" on a twofold account, both mentioned together by the Psalmist. "How precious are thy thoughts unto me, O Lord; how great is the sum of them!" They a
- file: EPUB/ch011.xhtml; previous: is power and care for the church, that is so expressed. These were from the beginning the first foundation of the church, in answer unto his everlasting counsels, Zechariah 2:8, 9,; next: He who is sent calleth himself "The Lord of hosts," and affirms that he will destroy the nations by the shaking of his hand; who can be no other but God himself. That is, it was th
- file: EPUB/ch011.xhtml; previous: tion, so it is not only intended. He was so before Abraham, as that the care of the church was then and always from the beginning on him. And he discharged this office four ways: —; next: (1st,) By personal appearances in the likeness of human nature, in the shape of a man, as an indication of his future incarnation; and under those appearances instructing the churc
- file: EPUB/ch011.xhtml; previous: ls was subordinate unto him; and whatever instruction was thereby given unto the church in the mind and will of God, it was immediately from him, as the great prophet of the church; next: (3rdly,) By sending his Holy Spirit to inspire, act, and guide the prophets, by whom God would reveal himself. God spoke unto them by the "mouth of his holy prophets, which have be
- file: EPUB/ch011.xhtml; previous: hed unto those that were disobedient in the days of Noah, who are now in prison for their disobedience, 1 Peter 3:19, 20. For he was so to prophet of the church always as to tender; next: John 1:9, by one way or other communicating to them some notices of God and his will; for his light shineth in, or irradiates darkness itself — that darkness which is come on the m
- file: EPUB/ch011.xhtml; previous: not only received divine truth by parcel, but comprehended not the depths of the revelations made unto them, 1 Peter 1:11, 12. To this purpose is that divine testimony, John 1:18,; next: It is of all the prophets concerning whom it is affirmed, that no man has seen God at any time. So is it evident in the antithesis between Moses the principal of them, and the Lord

## Inline Structural Marker Candidates

- file: EPUB/ch031.xhtml; text: In the susception of this office we may behold the glory of Christ, — I. In his condescension; II. In his love.

## Roman Heading Candidates

- file: EPUB/ch033.xhtml; text: I. 1. What he did, what obedience he yielded unto the law of God in the discharge of his office (with respect whereunto he said, "Lo, I come to do thy will, O God; yea, thy law is in my heart"), it was all on his own fre

## Overlong Heading Candidates

- file: EPUB/ch019.xhtml; tag: h4; text: IV. The last thing proposed concerning the person of Christ, was the use of it unto believers, in the whole of their relation unto God and duty towards him.
- file: EPUB/ch024.xhtml; tag: h4; text: III. The third and last thing which we proposed unto consideration, in our inquiry into the present state and condition of the person of Christ in heaven, is the exercise and discharge of his mediatory once in behalf of the church; espec...
- file: EPUB/ch027.xhtml; tag: h4; text: IV. He it is who in himself has given us a pledge of the capacity of our nature to inhabit those blessed regions of light, which are far above these aspectable heavens.
- file: EPUB/ch029.xhtml; tag: h4; text: I. Since men fell from God by sin, it is no small part of their misery and punishment, that they are covered with thick darkness and ignorance of the nature of God.
- file: EPUB/ch029.xhtml; tag: h4; text: II. This darkness in the minds of men, this ignorance of God, his nature and his will, was the original of all evil unto the world, and yet continues so to be. For, —
- file: EPUB/ch036.xhtml; tag: h4; text: III. There is a greater, a more intimate conjunction, a nearer relation, a higher mutual interest, between Christ and the church, than ever was or can be between any other persons or relations in the world, whereon it became just and equ...
- file: EPUB/ch041.xhtml; tag: h4; text: I. In the view which we have here of the glory of Christ by faith, we gather things, as it were, one by one, in several parts and parcels out of the Scripture; and comparing them together in our minds, they become the object of our prese...
- file: EPUB/ch045.xhtml; tag: h4; text: II. The second thing proposed is, that notwithstanding all this provision for the growth of spiritual life in us, believers, especially in a long course of profession, are subject to decays, such as may cast them into great perplexities,...
- file: EPUB/ch045.xhtml; tag: h4; text: III. But I come to that which was proposed in the third place, — namely, to show that this at present is the state of many professors of religion, that they are fallen under those spiritual decays, and do not enjoy the effects of the pro...
- file: EPUB/ch045.xhtml; tag: h4; text: IV. I proceed unto that which was proposed in the fourth or last place, — namely, the way and means whereby believers may be delivered from these decays, and come to thrive and flourish in the inward principle and outward fruits of spiri...

## Short Fragments

- file: EPUB/ch009.xhtml; text: All this himself instructs us in.
- file: EPUB/ch026.xhtml; text: - Teron and Aspasio, vol. 3 p. 75.
- file: EPUB/ch031.xhtml; text: There is not
- file: EPUB/ch035.xhtml; text: The sum is,
- file: EPUB/ch037.xhtml; text: And, —
- file: EPUB/ch041.xhtml; text: END.
- file: EPUB/ch049.xhtml; text: Glory be to God on high!

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
- phrase: unto us child is born unto us son is given; count: 6

## Missing Word Samples

- word: faithfullness; pdf: 7; epub: 0
- word: pre; pdf: 6; epub: 2
- word: eminence; pdf: 5; epub: 1
- word: mindedness; pdf: 3; epub: 0

## Excess Word Samples

- word: faithfulness; pdf: 5; epub: 12
- word: digital; pdf: 0; epub: 6

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
