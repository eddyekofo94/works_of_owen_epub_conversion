# Text Integrity Audit: Volume 12

- Status: **WARN**
- Warnings: 11
- PDF pages: 822
- EPUB text files: 58
- EPUB paragraphs/headings: 3516

## Coverage

- PDF content tokens: 275563
- EPUB content tokens: 274978
- Approximate PDF-to-EPUB coverage ratio: 0.9958
- Pages checked: 815
- Weak page matches: 26
- Dense source windows checked: 993
- Missing dense source-window pages: 806
- Front CONTENTS pages checked: 3
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 798
- Top-of-page windows skipped as unstable: 48
- Missing top-of-page body windows: 5
- Bottom-of-page body windows checked: 746
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 14

## Paragraphs

- Body paragraphs checked: 3115
- Possible faulty paragraph splits: 276
- Structural starts excluded from split warnings: 367
- Short fragments: 46
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 3
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 5
- Roman heading candidates: 0
- Overlong heading candidates: 5
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 450
- EPUB enumerator markers: 445
- Missing enumerator marker forms: 3
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 2593
- EPUB Greek words: 2593
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 222
- EPUB Hebrew words: 221
- Hebrew word coverage ratio: 0.9955
- Greek clauses checked: 133
- Missing Greek clauses: 0
- Hebrew clauses checked: 7
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 4; sample: of christ to be punishment properly so called 25 digression concerning the 53d chapter
- page: 5; sample: from the animad versions of mr μηδε εμοι τω ταυτα λεγοντι απλως πιστευσης εαν
- page: 7; sample: the son and of the spirit and similar doctrines biddle had well nigh fallen
- page: 11; sample: 11 to the right worshipful his reverend learned and worthy friends and brethren the
- page: 12; sample: 12 the like nature which to my thoughts did then occur not prevailing with
- page: 13; sample: 13 maresius professor at groningen man well known by his works published goes farther
- page: 14; sample: 14 from thence whence in the thoughts of some am most likely to suffer
- page: 15; sample: 15 that be men of what religion soever that is professed in the world
- page: 16; sample: 16 given to that sacred truth which is not wrested to another sense or
- page: 17; sample: 17 their business to despise what is done by others shall very little trouble

## Missing Top-Of-Page Body Windows

- page: 11; sample: TO THE RIGHT WORSHIPFUL, HIS REVEREND, LEARNED, AND WORTHY FRIENDS AND BRETHREN,
- page: 131; sample: Neither can that of the prophet Isaiah, chap. 66:1, be otherwise
- page: 229; sample: Luke 1:35;" f235 — the place insisted on the Son of God, as we read in
- page: 258; sample: himself abundantly hath manifested to be otherwise. Of 1 Corinthians
- page: 445; sample: Exodus 33:11, in the Hebrew is µyniP;Ala, µyniP;, panim el That which,

## Missing Bottom-Of-Page Body Windows

- page: 145; sample: Cwrei~te qnhtw~n to<n Qeo<n kai< mh< do>kei. Omoion aujtw~| sarkiko<n kaqesta>nai.
- page: 175; sample: propositions: — (1.) That God hath so foretold the free actions of men.
- page: 209; sample: explained. The words are, Oti oJ Qeo<v e]ktise to<n a]nqrwton ejp ajfqarsi>a| kai< eijko>na th~v ijdi>av ijdio>thtov ejpoi>hsen aujto>n Fqo>nw|
- page: 335; sample: expressed in the enumeration foregoing or no; all things were created by him. They were created for him eijv aujto>n, as it is said of the Father,
- page: 373; sample: chap. 16:19, ajnelh>fqh, — that is, ajnelh>fqh ejn do>xh|, "he was taken up into heaven,"
- page: 399; sample: vocis aperture est, et istud hBer]µæl], Isaiah 9:6, clausum est?
- page: 438; sample: 1 Timothy 2:6, "in whom we have redemption redemption for us,
- page: 514; sample: chap. 9:12, "He entered by his own blood into the holy place, aijwni>an lu>trwsin euJra>menov," — "after he had obtained eternal
- page: 526; sample: the LXX. constantly render it by apolutrou~n and sometimes lutrw>sasqai, otherwise by rju>omai, and the like.
- page: 660; sample: 1 Timothy 2:5, 6, gives us this fully. He is the mediator, and as such he gave himself ajnti>lutron, a price of redemption to God.

## Possible Paragraph Splits

- file: EPUB/ch004.xhtml; previous: The Holy Ghost tells us that we are; next: And thus do all they become the house of Christ "who hold fast the confidence and the rejoicing of the hope firm unto the end," Hebrews 3:6. In this house of God there are daily bu
- file: EPUB/ch004.xhtml; previous: house of God there are daily builders, according as new living stones are to be fitted to their places therein; and continual oppositions have there been made thereto, and will be,; next: In this work of building are some employed by Jesus Christ, and will be so to the end of the world, Matthew 28:19, 20, Ephesians 4:11, 12; and some employ themselves at least in a
- file: EPUB/ch004.xhtml; previous: and not be believed. See Calvin's epistles, about the year 1561. But the man on this occasion being sent to the meeting at Pinckzow (as Statorius), he subscribes this confession: —; next: This did the wretched man think meet to do, that he might preserve the good esteem of his patron and reserve himself for a fitter opportunity of doing mischief; which also he did,
- file: EPUB/ch004.xhtml; previous: of Grotius, time will evidence. Now, because this man's creed is such as is not to be paralleled, perhaps some may be contented to take it in his own words, which are as follow: —; next: To this issue did Satan drive the Socinian principles in this man and sundry others, even to a full and peremptory denial of the Lord that bought them. In answering this man, it fe
- file: EPUB/ch004.xhtml; previous: is day the Papists continue in the same idolatry (to touch that by the way), I shall give you, for your refreshment, a copy of a verse or two, whose poetry does much outgo the old,; next: The other is of Franciscus de Mendoza, in Viridario Utriusque Eruditionis, lib. 2 prob. 2, as ensueth: —
- file: EPUB/ch004.xhtml; previous: The other is of Franciscus de Mendoza, in Viridario Utriusque Eruditionis, lib. 2 prob. 2, as ensueth: —; next: And this their idolatry is objected to them by Soeinus, 94 who marvels at the impudence of Bellarmine closing his books of controversies (as is the manner of the men of that Societ
- file: EPUB/ch005.xhtml; previous: are not owned by the Scripture, so neither the things contained in them. How excellent, therefore, was that advice of Paul to Timothy in his second epistle to him, 2 Timothy 1:13,; next: JOHN BIDDLE.
- file: EPUB/ch006.xhtml; previous: y of God's essence or being is manifest from his absolute independence and firstness in being and operation, which God often insists upon in the revelation of himself: Isaiah 44:6,; next: Secondly, God is absolutely and perfectly one and the same, and nothing differs from his essence in it: "The LORD our God is one LORD," Deuteronomy 6:4; "Thou art the same," Psalm
- file: EPUB/ch008.xhtml; previous: with his master, who will not allow any such thing to be asserted in these words of our Savior. His words are (Fragment. Disput. de Adorat. Christi cure Christiano Franken, p. 60),; next: Vorstius also follows him, Not. ad Disput. 3, p. 200. Because the verb substantive "is" is not in the original expressed (than the omission whereof nothing being more frequent, tho
- file: EPUB/ch008.xhtml; previous: n which way thou wilt, thou shalt see God meeting thee. Nothing is empty of him: he fills his own work." 138 "All things are full of God," says the poet; 139 and another of them: —; next: Of this presence of God, I say, with and unto all things, of the infinity of his essence, the very heathens themselves, by the light of nature (which Mr B. herein opposes), had a k

## Inline Structural Marker Candidates

- file: EPUB/ch040.xhtml; text: Now, both these were lost at once. The heavens were darkened when it might be expected, in an ordinary course, that the sun should have shone in its full beauty, Matthew 27:45, Luke 23:44, 45; and the earth lost its stability, and shook ...
- file: EPUB/ch040.xhtml; text: He suffered, — [1.] In his person; [2.] In his name; [3.] In his friends; [4.] In his goods; as the curse of the law extended to all, and that universally in all these: —
- file: EPUB/ch047.xhtml; text: These Mr B. would oppose, and from the assertion of the one argue to the destruction of the other, though they sweetly and eminently comply in our communion with God. The other righteousness was before evinced. Even our sanctification al...

## Suspicious Large-Number Starts

- file: EPUB/ch011.xhtml; text: 11. Crellius is something more candid, as he pretends, but indeed infected with the same venom with the other; for after he hath disputed for sundry pages to prove the foreknowledge of God, he concludes at last that for
- file: EPUB/ch017.xhtml; text: 18. Acts 13:32, 33; Revelation 1:5; 4. His exaltation, Hebrews 5:5; Romans 8:29. For the removal of all this from prejudicing the eternal sonship of Jesus Christ there is an abundant sufficiency, arising from the conside
- file: EPUB/ch019.xhtml; text: 24. Simile loquendi genua Sic Legem fuisse ante mundum aiunt Hebraei." Again, " Παρὰ σοί , refer ad illud εῖχον , et intellige, ut diximus, in decreto tuo." But what intends the learned man by those places o 1 Peter 1:20
- file: EPUB/ch039.xhtml; text: 52. The words of that verse are, —
- file: EPUB/ch042.xhtml; text: 12. And that may be the sense of the word ἐπιλαμβάνεται , if not in the effect, yet in the cause, Hebrews 2:16.

## Overlong Heading Candidates

- file: EPUB/ch017.xhtml; tag: h4; text: II. That he is and is termed the Son of God solely on this account, and not upon the reasons mentioned by Mr B. and explained from his companions, is with equal clearness evinced.
- file: EPUB/ch018.xhtml; tag: h4; text: III. ALTHOUGH the testimonies and arguments for the deity of Christ might be urged and handled to a better advantage, if liberty might be used to insist upon them in the method that seems most natural for the clearing and confirmation of...
- file: EPUB/ch036.xhtml; tag: h4; text: I. THE death of Christ in this business is a PRICE, and that properly so called: 1 Corinthians 6:20, ' Ηγοράσθητε τιμῆς , — "Ye are bought with a price." And if we will know what that price was with which we are bought, the Holy Ghost in...
- file: EPUB/ch036.xhtml; tag: h4; text: II. It was a SACRIFICE; and what sacrifice it was shall be declared: — That Christ offered a sacrifice is abundantly evident from what was said before, in the consideration of the time and place when and wherein Christ was a high priest.
- file: EPUB/ch044.xhtml; tag: h4; text: III. THE third consideration of the death of Christ was of it as it was penal, as therein he underwent punishment for us, or that punishment which for sin was due to us.

## Short Fragments

- file: EPUB/ch005.xhtml; text: JOHN BIDDLE.
- file: EPUB/ch009.xhtml; text: MR BIDDLE'S question: —
- file: EPUB/ch009.xhtml; text: Whereunto answers that in Cato: —
- file: EPUB/ch009.xhtml; text: Ομοιον αὐτῷ σαρκικὸν καθεστάναι .
- file: EPUB/ch011.xhtml; text: Ans.
- file: EPUB/ch013.xhtml; text: Ans. Genesis 1:1
- file: EPUB/ch016.xhtml; text: Ans. Ephesians 4:5.
- file: EPUB/ch017.xhtml; text: EXAMINATION.
- file: EPUB/ch017.xhtml; text: He adds, 12th,
- file: EPUB/ch019.xhtml; text: Thus, then, they proceed: —

## Missing Enumerator Markers

- marker: (1.); pdf: 110; epub: 107; examples: [{'location': 'pdf:p51', 'context': 'them to Palaeologus. f75 By this course of behavior, the man had these two advantages: — (1.) He kept fair with all parties amongst them, and provoked not any by joining with them with whom they could...
- marker: (3.); pdf: 54; epub: 53; examples: [{'location': 'pdf:p87', 'context': 'he several particulars as they shall occur in the method wherein by him they are handled. (3.) What can be concluded of the mind of God in the Scripture, by cutting off any place or places of it from ...
- marker: [4.]; pdf: 7; epub: 6; examples: [{'location': 'pdf:p296', 'context': 'f many nations," and not as a proper name, whereof in Scripture there is not any example. [4.] It is horribly wrested, — 1st. In making the words "I am" elliptical, whereas there is neither need of n...

## Enumerator Sequence Candidates

- file: EPUB/ch011.xhtml; marker: (8.); family: paren_decimal; context: (8.) By this prerogative of certain predictions in reference to things to come, God vindicates his own deity; and from the want of it evinces the vanity of the idols of the Gentiles, a
- file: EPUB/ch027.xhtml; marker: (2.); family: paren_decimal; context: (2.) Omniscience, 1 Corinthians 2:10; John 16:13. His omnipotency and eternity are both manifest from the creation.

## Repeated Windows

- phrase: made of the seed of david according to the flesh; count: 5
- phrase: that they which commit sin are worthy of death romans; count: 5
- phrase: they which commit sin are worthy of death romans 32; count: 5
- phrase: the lord hath laid on him the iniquity of us; count: 5
- phrase: lord hath laid on him the iniquity of us all; count: 5
- phrase: known unto god are all his works from the beginning; count: 4
- phrase: unto god are all his works from the beginning of; count: 4
- phrase: god are all his works from the beginning of the; count: 4
- phrase: are all his works from the beginning of the world; count: 4
- phrase: the son of god is come and hath given us; count: 4

## Missing Word Samples

- word: chap; pdf: 142; epub: 35
- word: pre; pdf: 4; epub: 0
- word: ; pdf: 3; epub: 1

## Excess Word Samples

- word: 5chap; pdf: 0; epub: 14
- word: 1chap; pdf: 0; epub: 9
- word: psalms; pdf: 3; epub: 11
- word: 6chap; pdf: 0; epub: 8
- word: 13chap; pdf: 0; epub: 7
- word: digital; pdf: 0; epub: 6
- word: onlybegotten; pdf: 0; epub: 6
- word: 9chap; pdf: 0; epub: 6

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
