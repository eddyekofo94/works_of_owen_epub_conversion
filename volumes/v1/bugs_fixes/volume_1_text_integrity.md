# Text Integrity Audit: Volume 1

- Status: **WARN**
- Warnings: 9
- PDF pages: 644
- EPUB text files: 83
- EPUB paragraphs/headings: 3083

## Coverage

- PDF content tokens: 211474
- EPUB content tokens: 213785
- Approximate PDF-to-EPUB coverage ratio: 0.9963
- Pages checked: 635
- Weak page matches: 23
- Dense source windows checked: 794
- Missing dense source-window pages: 620
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 602
- Top-of-page windows skipped as unstable: 21
- Missing top-of-page body windows: 3
- Bottom-of-page body windows checked: 555
- Bottom-of-page windows skipped as unstable: 6
- Missing bottom-of-page body windows: 18

## Paragraphs

- Body paragraphs checked: 2750
- Possible faulty paragraph splits: 35
- Structural starts excluded from split warnings: 164
- Short fragments: 49
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 0
- Overlong heading candidates: 11
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 313
- EPUB enumerator markers: 316
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 824
- EPUB Greek words: 835
- Greek word coverage ratio: 0.9987
- PDF Hebrew words: 20
- EPUB Hebrew words: 20
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 44
- Missing Greek clauses: 44
- Hebrew clauses checked: 1
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 3; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ
- page: 9; sample: embraces the most comprehensive view of this vitally-important subject his exposition of psalm 130
- page: 10; sample: 10 dutch divines the most favorable mention is made of the various treatises of
- page: 11; sample: 11 ushered under their auspices into public notice there was large body of subscribers
- page: 12; sample: 12 the edition was comprised in twenty-one octavo volumes the first however consisting of
- page: 13; sample: 13 that the theologoumena had been much disfigured with errors nobis praelo capite ad
- page: 14; sample: 14 the punctuation has undergone thorough revisal passages which from negligence in this respect
- page: 15; sample: 15 were printed when he was himself alive here abound in errors to degree
- page: 16; sample: 16 sometimes at loss to judge of the treatise of an old author whether
- page: 17; sample: 17 which belongs to the library of the college and from which the portrait

## Missing Top-Of-Page Body Windows

- page: 157; sample: Hebrews 2:18; 4:15; 5:2. So is he also, as he alone who is able to succor, to relieve, and to deliver them. "He is able to succor them that are
- page: 613; sample: A. In that for us he underwent the punishment due to our sin. Isaiah
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
- page: 380; sample: 1 Corinthians 1:21-25. Not to see the wisdom apostle declares at large,
- page: 397; sample: Colossians 3:10. the saving knowledge of him does,

## Possible Paragraph Splits

- file: EPUB/ch005.xhtml; previous: PETER'S CONFESSION; MATTHEW 16:16 — CONCEITS OF THE PAPISTS THEREON — THE SUBSTANCE AND EXCELLENCY OF THAT CONFESSION; next: Our blessed Savior, inquiring of his disciples their apprehensions concerning his person, and their faith in him, Simon Peter — as he was usually the forwardest on all such occasio
- file: EPUB/ch006.xhtml; previous: OPPOSITION MADE UNTO THE CHURCH AS BUILT UPON THE PERSON OF CHRIST; next: There are in the words of our Savior unto Peter concerning the foundation of the church, a promise of its preservation, and a prediction of the opposition that should be made there
- file: EPUB/ch007.xhtml; previous: THE PERSON OF CHRIST THE MOST INEFFABLE EFFECT OF DIVINE WISDOM AND GOODNESS — THENCE THE NEXT CAUSE OF ALL TRUE RELIGION — IN WHAT SENSE IT IS SO; next: The person of Christ is the most glorious and ineffable effect of divine wisdom, grace, and power; and therefore is the next foundation of all acceptable religion and worship. The
- file: EPUB/ch008.xhtml; previous: TO PERSON OF CHRIST THE FOUNDATION OF ALL THE COUNSELS OF GOD; next: Secondly, The person of Christ is the foundation of all the counsels of God, as unto his own eternal glory in the vocation, sanctification, and salvation of the church. That which
- file: EPUB/ch009.xhtml; previous: THE PERSON OF CHRIST THE GREAT REPRESENTATIVE OF GOD AND HIS WILL; next: What may be known of God, is, — his nature and existence, with the holy counsels of his will. A representation of them unto us is the foundation of all religion, and the means of o
- file: EPUB/ch011.xhtml; previous: POWER AND EFFICACY COMMUNICATED UNTO THE OFFICE OF CHRIST, FOR THE SALVATION OF THE CHURCH, FROM HIS PERSON; next: It is by the exercise and discharge of the office of Christ — as the king, priest, and prophet of the church — that we are redeemed, sanctified, and saved. Thereby does he immediat
- file: EPUB/ch011.xhtml; previous: And he discharged this office four ways: —; next: (1st,) By personal appearances in the likeness of human nature, in the shape of a man, as an indication of his future incarnation; and under those appearances instructing the churc
- file: EPUB/ch011.xhtml; previous: ls was subordinate unto him; and whatever instruction was thereby given unto the church in the mind and will of God, it was immediately from him, as the great prophet of the church; next: (3rdly,) By sending his Holy Spirit to inspire, act, and guide the prophets, by whom God would reveal himself. God spoke unto them by the "mouth of his holy prophets, which have be
- file: EPUB/ch012.xhtml; previous: THE FAITH OF THE CHURCH UNDER THE OLD TESTAMENT IN AND CONCERNING THE PERSON OF CHRIST; next: A brief view of the faith of the church under the Old Testament concerning the divine person of Christ, shall close these discourses, and make way for those that ensue, wherein our
- file: EPUB/ch013.xhtml; previous: HONOR DUE TO THE PERSON OF CHRIST — THE NATURE AND CAUSES OF IT; next: Many other considerations of the same nature with those foregoing, relating unto the glory and honor of the person of Christ, may be taken from all the fundamental principles of re

## Inline Structural Marker Candidates

- file: EPUB/ch078.xhtml; text: A.M. of Northampton, 1781. FT4 A statement occurs in the "Encyclopaedia Britannica" that Owen's works are printed in seven folio volumes. If it be meant that there are seven folio volumes of Owen's works, there is a sense in which the st...

## Overlong Heading Candidates

- file: EPUB/ch019.xhtml; tag: h4; text: IV. The last thing proposed concerning the person of Christ, was the use of it unto believers, in the whole of their relation unto God and duty towards him.
- file: EPUB/ch020.xhtml; tag: h4; text: ill. For what he so does is due in and for itself; and to suppose that satisfaction will be made for a former fault by that whose omission would have been another, had the former never been committed, is madness.
- file: EPUB/ch024.xhtml; tag: h4; text: III. The third and last thing which we proposed unto consideration, in our inquiry into the present state and condition of the person of Christ in heaven, is the exercise and discharge of his mediatory once in behalf of the church; espec...
- file: EPUB/ch027.xhtml; tag: h4; text: IV. He it is who in himself has given us a pledge of the capacity of our nature to inhabit those blessed regions of light, which are far above these aspectable heavens.
- file: EPUB/ch029.xhtml; tag: h4; text: I. Since men fell from God by sin, it is no small part of their misery and punishment, that they are covered with thick darkness and ignorance of the nature of God.
- file: EPUB/ch029.xhtml; tag: h4; text: II. This darkness in the minds of men, this ignorance of God, his nature and his will, was the original of all evil unto the world, and yet continues so to be.
- file: EPUB/ch036.xhtml; tag: h4; text: III. There is a greater, a more intimate conjunction, a nearer relation, a higher mutual interest, between Christ and the church, than ever was or can be between any other persons or relations in the world, whereon it became just and equ...
- file: EPUB/ch041.xhtml; tag: h4; text: I. In the view which we have here of the glory of Christ by faith, we gather things, as it were, one by one, in several parts and parcels out of the Scripture; and comparing them together in our minds, they become the object of our prese...
- file: EPUB/ch045.xhtml; tag: h4; text: II. The second thing proposed is, that notwithstanding all this provision for the growth of spiritual life in us, believers, especially in a long course of profession, are subject to decays, such as may cast them into great perplexities,...
- file: EPUB/ch045.xhtml; tag: h4; text: III. But I come to that which was proposed in the third place, — namely, to show that this at present is the state of many professors of religion, that they are fallen under those spiritual decays, and do not enjoy the effects of the pro...

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
- phrase: unto us child is born unto us son is given; count: 6

## Missing Word Samples

- word: faithfullness; pdf: 7; epub: 0
- word: pre; pdf: 6; epub: 2
- word: eminence; pdf: 5; epub: 1
- word: mindedness; pdf: 3; epub: 0

## Excess Word Samples

- word: faithfulness; pdf: 5; epub: 12

## Missing Greek Clauses

- page: 26; word_count: 54; sample: υτος εστιν ηε προς τον πατερα αγουσα ηοσος ηε πετρα ηε κλεις
- page: 27; word_count: 11; sample: επὶ τῇ πέτρᾳ ταυτῃ τῆς ἀσφαλοῦς πίστεως οἰκοδομήσω μοῦ τὴν ἐκκλεσίαν
- page: 31; word_count: 5; sample: πρόσωπον ὁμοιούσιος ἑτερούσιος ἐξ οὐκ
- page: 32; word_count: 13; sample: ὑπόστατις φύσις μίαν φύσιν ὅτι κατ ἀλήθειαν ἐστὶ μία φύσις τοῦ λόγου
- page: 36; word_count: 31; sample: τὸν θεοῦ μεσίτην καὶ ἀνθρώπων κατὰ τὰς γραφὰς συγκεῖσθαι φάμεν ἔκ τε
- page: 37; word_count: 5; sample: ἔνωσιν φυσικὴν ἕνωσιν κατὰ σύνθεσιν
- page: 37; word_count: 11; sample: υἱὸς θεοῦ ὑιὸς ἀνθρώπου γίνεται οὕτω δὲ φωτὸς ἡλίου μία καὶ
- page: 37; word_count: 22; sample: αὐτὴ προσβολὴ ὁμοῦ καὶ κατὰ τὸ αὐτὸ καταυγάζει μὲν ἀέρα φωτίζει δὲ
- page: 37; word_count: 37; sample: εἰ γοῦν ὥς ἐν ὑποθέσει λόγου καθεὶς οὐρανόθεν αὐτὸς ἑαυτὸν παμφαὴς ἥλιος
- page: 40; word_count: 13; sample: χριστὸς καὶ τοῦ εῖναι πάλαι ἡμᾶς ῆν γὰρ ἐν θεῷ καὶ τοῦ

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
