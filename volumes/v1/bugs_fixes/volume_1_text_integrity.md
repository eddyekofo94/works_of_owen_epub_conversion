# Text Integrity Audit: Volume 1

- Status: **WARN**
- Warnings: 9
- PDF pages: 644
- EPUB text files: 84
- EPUB paragraphs/headings: 2756

## Coverage

- PDF content tokens: 208263
- EPUB content tokens: 207584
- Approximate PDF-to-EPUB coverage ratio: 0.9895
- Pages checked: 633
- Weak page matches: 39
- Dense source windows checked: 13850
- Missing dense source-window pages: 421
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 597
- Top-of-page windows skipped as unstable: 21
- Missing top-of-page body windows: 6
- Bottom-of-page body windows checked: 547
- Bottom-of-page windows skipped as unstable: 6
- Missing bottom-of-page body windows: 14

## Paragraphs

- Body paragraphs checked: 2326
- Possible faulty paragraph splits: 116
- Structural starts excluded from split warnings: 156
- Short fragments: 52
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 12
- Roman heading candidates: 0
- Overlong heading candidates: 1
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 313
- EPUB enumerator markers: 313
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
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 9; sample: temptation and the danger of apostasy mark uncommon depths of exploring the secretes of
- page: 10; sample: most of the impression his work which bears the title qeologoymena pantodaiia etc originally
- page: 11; sample: whose literary industry the church of christ had been se largely indebted it would
- page: 19; sample: cristologia christologia or declaration of the glorious mystery of the person of christ god
- page: 20; sample: prefatory note to object of dr owen in this treatise is to illustrate the
- page: 21; sample: events ensued which justified these apprehensions of own prolonged controversy on the subject of
- page: 22; sample: unto the church for he was child born son given unto us isaiah that
- page: 23; sample: shall glory isaiah for israel shall be saved in the lord with an everlasting
- page: 29; sample: unto them by the great apostle acts timothy timothy and wherein any of them
- page: 33; sample: promise and prediction of our blessed savior in matthew the place insisted on to

## Missing Top-Of-Page Body Windows

- page: 49; sample: being nothing but the "ajnakefalaiwsiv" mentioned by the apostle, Ephesians 1:10 — and he here affirms, that, unto this end, the Lord was
- page: 200; sample: lovest thou me? Feed my lambs," John 21:15-17. Three times did he
- page: 224; sample: like that of a "husband unto a wife," Ephesians 5:25, 26, or a holy
- page: 377; sample: what we are conversant withal. See Philippians 3:7-11. A defect herein
- page: 451; sample: fullness of the Godhead, Colossians 2:9. This glory was now presented
- page: 609; sample: Hebrews 1:8; 1 Timothy 3:16; secondly, of the Son of God,

## Missing Bottom-Of-Page Body Windows

- page: 87; sample: Zechariah 6:13,) or the originally between Jehovah and the Branch, (
- page: 99; sample: Exodus 33:18. Moses had Moses: "I beseech thee, show me thy glory:"
- page: 105; sample: John 1:1. "The Word was God," in with God, and the Word was God:"
- page: 156; sample: suffered, being tempted, he is touched with a feeling of our infirmities, and knows how to have compassion on them that are out of the way,
- page: 195; sample: Matthew 3:17, "Lo, a voice from heaven, saying, heaven afterwards,
- page: 289; sample: Colossians 1:18, 19. And I shall herein wholly avoid the eminence,"
- page: 318; sample: 1:11, — and the "heaven must receive him," chap. 3:21; not these aspectable heavens which we behold, — for in his ascension "he passed
- page: 325; sample: solemn worship. So is it represented, the whole number of the saints above that have passed through the
- page: 380; sample: 1 Corinthians 1:21-25. Not to see the wisdom apostle declares at large,
- page: 385; sample: 2 Corinthians 3:18. may have with open face, though yet "as in a glass!"

## Possible Paragraph Splits

- file: EPUB/ch001.xhtml; previous: **GENERAL PREFACE.**; next: IT would be presumption to enter upon any commendation of John Owen as an author and divine. His works will continue to gather round them the respect and admiration of the Church o
- file: EPUB/ch005.xhtml; previous: **A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST**; next: **CHAPTER 1**
- file: EPUB/ch005.xhtml; previous: **CHAPTER 1**; next: **PETER'S CONFESSION; Matthew 16:16MATTHEW 16:16 — CONCEITS OF THE PAPISTS THEREON — THE SUBSTANCE AND EXCELLENCY OF THAT CONFESSION**
- file: EPUB/ch005.xhtml; previous: **PETER'S CONFESSION; Matthew 16:16MATTHEW 16:16 — CONCEITS OF THE PAPISTS THEREON — THE SUBSTANCE AND EXCELLENCY OF THAT CONFESSION**; next: Our blessed Savior, inquiring of his disciples their apprehensions concerning his person, and their faith in him, Simon Peter — as he was usually the forwardest on all such occasio
- file: EPUB/ch011.xhtml; previous: But —; next: There was yet more required thereunto, or to render his offices effectual unto their proper ends. Not one of them could have been so, had he been no more than a man — had he had no
- file: EPUB/ch011.xhtml; previous: And he discharged this office four ways: —; next: (1st,) By personal appearances in the likeness of human nature, in the shape of a man, as an indication of his future incarnation; and under those appearances instructing the churc
- file: EPUB/ch011.xhtml; previous: ls was subordinate unto him; and whatever instruction was thereby given unto the church in the mind and will of God, it was immediately from him, as the great prophet of the church; next: (3rdly,) By sending his Holy Spirit to inspire, act, and guide the prophets, by whom God would reveal himself. God spoke unto them by the "mouth of his holy prophets, which have be
- file: EPUB/ch013.xhtml; previous: eunto. Hence is that expression, "He bowed down his head and worshipped," [ Genesis 24:26Genesis 24:26;] see [ αλσὄ Psalms 95:6Psalm 95:6. And these external signs are of two sorts; next: (1st,) Such as are natural and occasional;
- file: EPUB/ch013.xhtml; previous: ofession of the gospel, are another season rendering this peculiar invocation of Christ both comely and necessary. Two things will befall the minds of believers in such a season; —; next: [1st,] that their thoughts will be neatly exercised about him, and conversant with him. They cannot but continually think and meditate on him for whom they suffer. None ever suffer
- file: EPUB/ch022.xhtml; previous: There can be but two senses of these words; next: (1st,) That the Word ceased to be what it was, and was substantially turned into flesh

## Inline Structural Marker Candidates

- file: EPUB/ch019.xhtml; text: Whatever men may fancy to the contrary, it is the design of the apostle, in sundry places of his writings, to prove that they did so, especially Romans 1; 1 Corinthians 1. Wherefore, it was an infinite condescension of divine wisdom and ...

## Suspicious Large-Number Starts

- file: EPUB/ch004.xhtml; text: 13. — "Upon this rock which thou hast confessed — upon myself, the God of the living God — I WILL build my church I WILL build thee upon myself, and not myself on thee." And he more fully declareth his mind: (Tract. 124,
- file: EPUB/ch004.xhtml; text: 78. The like difference immediately fell out between the Grecians and Latins about "hypostasis" and "persona". For the Latins rendered "hypostasis" by "substantia," and " πρόσωπον " by "persona." Hereof Jerome complains,
- file: EPUB/ch004.xhtml; text: 71. And Augustine gives an account of the same difference: De Trinitate, lib. 5 cap. 8, 9. Athanasius endeavored the composing of this difference, and in a good measure effected it, as Gregory Nazianzen affirms in his or
- file: EPUB/ch004.xhtml; text: 14. " Ονομα δὲ κοινὸν τῶν τριῶν ἕν , ἡ θεότηψ ". — "The one name common to the three is the Deity:" Gregor. Nazianzen, Orat.
- file: EPUB/ch004.xhtml; text: 40. Hence Augustine gives it as a rule, in speaking of the Holy Trinity: "Quando unus trium in aliquo opere nominatur, universa operari trinitas intelligitur:" Enchirid., cap.
- file: EPUB/ch004.xhtml; text: 38. — "When one person of the three is named in any work, the whole Trinity is to be understood to effect it." "There is one Lord, one faith, one baptism," according to the Scriptures. Wherefore, as there is one faith in
- file: EPUB/ch004.xhtml; text: 32. And this they professed themselves to hold and believe, in that ancient doxology which was first invented to decry the Arian heresy: "Glory be to the Father, and to the Son, and to the Holy Ghost." The same glory, in
- file: EPUB/ch022.xhtml; text: 10. But that is true only in this one respect, that the Son is not so in the Father as to become one person with him. In all other respects it must be granted that the in-being of the Son in the Father — the union betwee
- file: EPUB/ch024.xhtml; text: 22. O that my soul might abide and abound in this exercise of faith! — that I might yet enjoy a clearer prospect of this glory, and inspection into the beauty and order of this blessed assembly! How inconceivable is the
- file: EPUB/ch024.xhtml; text: 38. He has made atonement for them in the blood of his oblation, and they appear not in the presence of God. Through the second, or the efficacy of his intercession, he gives acceptance unto our prayers and holy worship,

## Overlong Heading Candidates

- file: EPUB/ch049.xhtml; tag: h4; text: A. His decrees, and his works. — Chapter 4. Q. What are the decrees of God concerning us? A. His eternal purposes, of saving some by Jesus Christ, for the praise of

## Short Fragments

- file: EPUB/ch001.xhtml; text: **GENERAL PREFACE.**
- file: EPUB/ch001.xhtml; text: ΧΡΙΣΤΟΛΟΓΙΑ :
- file: EPUB/ch005.xhtml; text: **CHAPTER 1**
- file: EPUB/ch006.xhtml; text: For,
- file: EPUB/ch006.xhtml; text: As,
- file: EPUB/ch009.xhtml; text: Wherefore —
- file: EPUB/ch009.xhtml; text: And —
- file: EPUB/ch009.xhtml; text: All this himself instructs us in.
- file: EPUB/ch011.xhtml; text: This must be declared.
- file: EPUB/ch011.xhtml; text: For —

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

- word: ft; pdf: 124; epub: 0
- word: kai; pdf: 40; epub: 0
- word: tou; pdf: 33; epub: 0
- word: th; pdf: 38; epub: 9
- word: oj; pdf: 23; epub: 0
- word: ou; pdf: 17; epub: 0
- word: lo; pdf: 26; epub: 10
- word: ejn; pdf: 14; epub: 0
- word: qeo; pdf: 14; epub: 0
- word: tw; pdf: 13; epub: 0

## Excess Word Samples

- word: corinthians; pdf: 181; epub: 333
- word: hebrews; pdf: 182; epub: 330
- word: ephesians; pdf: 146; epub: 269
- word: isaiah; pdf: 110; epub: 203
- word: psalms; pdf: 2; epub: 66
- word: colossians; pdf: 56; epub: 109
- word: philippians; pdf: 56; epub: 107
- word: timothy; pdf: 45; epub: 84
- word: proverbs; pdf: 26; epub: 53
- word: solomon; pdf: 23; epub: 43

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
