# Text Integrity Audit: Volume 12

- Status: **WARN**
- Warnings: 14
- PDF pages: 822
- EPUB text files: 61
- EPUB paragraphs/headings: 3518

## Coverage

- PDF content tokens: 270738
- EPUB content tokens: 272724
- Approximate PDF-to-EPUB coverage ratio: 0.9991
- Pages checked: 815
- Weak page matches: 2
- Dense source windows checked: 30713
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 3
- Missing front CONTENTS pages: 1
- Top-of-page body windows checked: 793
- Top-of-page windows skipped as unstable: 47
- Missing top-of-page body windows: 3
- Bottom-of-page body windows checked: 740
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 14

## Paragraphs

- Body paragraphs checked: 3081
- Possible faulty paragraph splits: 35
- Structural starts excluded from split warnings: 433
- Short fragments: 48
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 3
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 450
- EPUB enumerator markers: 460
- Missing enumerator marker forms: 1
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 2593
- EPUB Greek words: 2593
- Greek word coverage ratio: 0.9992
- PDF Hebrew words: 222
- EPUB Hebrew words: 221
- Hebrew word coverage ratio: 0.9955
- Greek clauses checked: 133
- Missing Greek clauses: 0
- Hebrew clauses checked: 7
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 10596
- EPUB Latin words: 10733
- EPUB Tagged Latin words: 6394
- Latin word coverage ratio: 0.9975
- Latin word tagging ratio: 0.5957
- Latin clauses checked: 776
- Missing Latin clauses: 3
- Tagged Latin runs checked: 1658
- Translated Latin runs: 668
- Latin translation ratio: 0.4029

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 4; sample: evincing the death of christ to be punishment properly so called digression concerning the
- page: 5; sample: vindicated and socinianism examined in the consideration and confutation of catechism called scripture catechism
- page: 6; sample: first among that splendid catena of divines bull waterland horsley magee fuller pye smith
- page: 7; sample: son and of the spirit and similar doctrines biddle had well nigh fallen martyr
- page: 8; sample: by their brethren of the same creed the task was devolved on valentine smalcius
- page: 9; sample: of the latter to the socinian crellius see page is the difference between those
- page: 11; sample: to the right worshipful his reverend learned and worthy friends and brethren the heads
- page: 14; sample: of his inclinations that way some parcels of letter of his to crellius some
- page: 15; sample: the socinians and oftentimes consist in the very words of socinus and smalcius and
- page: 16; sample: let bellarmine on the one hand and beza on the other evince and as

## Missing Front CONTENTS Pages

- page: 5; hit_ratio: 0.5; sample: vindiciae evangelicae or the mystery of the gospel vindicated and socinianism examined in the consideration and confutation of catechism called scripture catechism written by biddle and the catechism

## Missing Top-Of-Page Body Windows

- page: 11; sample: TO THE RIGHT WORSHIPFUL, HIS REVEREND, LEARNED, AND WORTHY FRIENDS AND BRETHREN,
- page: 136; sample: CHAPTER 3. Of the drape and bodily visible figure of God.
- page: 445; sample: Exodus 33:11, in the Hebrew is µyniP;Ala, µyniP;, panim el That which,

## Missing Bottom-Of-Page Body Windows

- page: 145; sample: Cwrei~te qnhtw~n to<n Qeo<n kai< mh< do>kei. Omoion aujtw~| sarkiko<n kaqesta>nai.
- page: 175; sample: propositions: — (1.) That God hath so foretold the free actions of men.
- page: 209; sample: explained. The words are, Oti oJ Qeo<v e]ktise to<n a]nqrwton ejp ajfqarsi>a| kai< eijko>na th~v ijdi>av ijdio>thtov ejpoi>hsen aujto>n Fqo>nw|
- page: 335; sample: expressed in the enumeration foregoing or no; all things were created by him. They were created for him eijv aujto>n, as it is said of the Father,
- page: 373; sample: chap. 16:19, ajnelh>fqh, — that is, ajnelh>fqh ejn do>xh|, "he was taken up into heaven,"
- page: 399; sample: vocis aperture est, et istud hBer]µæl], Isaiah 9:6, clausum est?
- page: 438; sample: 1 Timothy 2:6, "in whom we have redemption redemption for us,
- page: 483; sample: invocation of Christ, that others as well as God may be worshipped and invocated, in his third epistle to Volkelius, where he labors to answer the
- page: 514; sample: chap. 9:12, "He entered by his own blood into the holy place, aijwni>an lu>trwsin euJra>menov," — "after he had obtained eternal
- page: 526; sample: the LXX. constantly render it by apolutrou~n and sometimes lutrw>sasqai, otherwise by rju>omai, and the like.

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: gst you, that, according to your several degrees, you would take it into your patronage or use, affording him in his daily labors the benefit of your prayers at the throne of grace; next: who is your unworthy fellow-laborer
- file: EPUB/ch003.xhtml; previous: who is your unworthy fellow-laborer; next: John Owen
- file: EPUB/ch003.xhtml; previous: John Owen; next: OXON. CH. CH. COLL., April 1 [1655.]
- file: EPUB/ch010.xhtml; previous: ry about the nature of God respects the attribution of several affections and passions unto him in the Scriptures, of whose sense and meaning he thus expresseth his apprehension: —; next: Ques. Are there not, according to the perpetual tenor of the Scriptures, affections and passions in God, as anger, fury, zeal, wrath, love, hatred, mercy, grace, jealousy, repentan
- file: EPUB/ch011.xhtml; previous: ution thereof, in order to a discovery of what God himself hath revealed concerning his knowledge of all things, is the next part of our employment. Thus, then, it may be framed: —; next: Ques. Doth not God know all things, whether past, present, or to come, all the ways and actions of men, even before their accomplishment, or is any thing hid from him? What says th
- file: EPUB/ch014.xhtml; previous: nd discourse, let us also propose a few questions as to the matter under consideration, and see what answer the Scripture will positively give in to our inquiries: — First, then, —; next: Ques. 1. In what state and condition was man at first created?
- file: EPUB/ch018.xhtml; previous: Their first question and answer are: —; next: Ques. Declare now to me what I ought to know concerning Jesus Christ?
- file: EPUB/ch018.xhtml; previous: ns 15:21; such a one as God of old promised by the prophets, and such as the creed, commonly called the Apostles', witnesseth him to be; which, with us, all Christians embrace. 259; next: Ans. That Jesus Christ was a true man, in his nature like unto us, sin only excepted, we believe, and do abhor the abominations of Paracelsus, Wigelius , etc., and the Familists am
- file: EPUB/ch018.xhtml; previous: t bring other causes, which thou wilt afterward find in the person of Christ, which most evidently declare that the Lord Jesus can by no means be esteemed a pure (or mere) man. 260; next: Ans. 1. But I have abundantly demonstrated that Christ neither was nor was called the Son of God upon the account here mentioned, nor any other whatever intimated in the close of t
- file: EPUB/ch018.xhtml; previous: But as the divine nature by itself constitutes a person, so it is necessary that the human nature should do. 263; next: Ans. 1. In what sense it may be said that Christ, that is, the person of Christ, consisteth of a divine and human nature, was before declared. The person of the Son of God assumed

## Inline Structural Marker Candidates

- file: EPUB/ch040.xhtml; text: He suffered, — [1.] In his person; [2.] In his name; [3.] In his friends; [4.] In his goods; as the curse of the law extended to all, and that universally in all these: —
- file: EPUB/ch047.xhtml; text: I answer, The words there are used in a law sense, and are declarative of the righteousness of God in rewarding the keepers of the law of nature, or the moral law, according to the law of the covenant of works. This is evident from the w...
- file: EPUB/ch047.xhtml; text: These Mr B. would oppose, and from the assertion of the one argue to the destruction of the other, though they sweetly and eminently comply in our communion with God. The other righteousness was before evinced. Even our sanctification al...

## Suspicious Large-Number Starts

- file: EPUB/ch011.xhtml; text: 11. Johannes Crellius is something more candid, as he pretends, but indeed infected with the same venom with the other; for after he hath disputed for sundry pages to prove the foreknowledge of God, he concludes at last
- file: EPUB/ch019.xhtml; text: 24. Simile loquendi genua Sic Legem fuisse ante mundum aiunt Hebraei." Again, " Παρὰ σοί , refer ad illud εῖχον , et intellige, ut diximus, in decreto tuo ." But what intends the learned man by those places of 1 Peter 1:
- file: EPUB/ch039.xhtml; text: 52. The words of that verse are, —
- file: EPUB/ch042.xhtml; text: 12. And that may be the sense of the word ἐπιλαμβάνεται , if not in the effect, yet in the cause, Hebrews 2:16.

## Short Fragments

- file: EPUB/ch003.xhtml; text: John Owen
- file: EPUB/ch005.xhtml; text: JOHN BIDDLE.
- file: EPUB/ch009.xhtml; text: Whereunto answers that in Cato: —
- file: EPUB/ch009.xhtml; text: Ομοιον αὐτῷ σαρκικὸν καθεστάναι .
- file: EPUB/ch011.xhtml; text: Ans.
- file: EPUB/ch013.xhtml; text: Ans. Genesis 1:1
- file: EPUB/ch014.xhtml; text: EXAMINATION.
- file: EPUB/ch016.xhtml; text: Ans. Ephesians 4:5.
- file: EPUB/ch017.xhtml; text: etc.
- file: EPUB/ch017.xhtml; text: He adds, 12th,

## Missing Enumerator Markers

- marker: (1.); pdf: 110; epub: 109; examples: [{'location': 'pdf:p51', 'context': 'them to Palaeologus. f75 By this course of behavior, the man had these two advantages: — (1.) He kept fair with all parties amongst them, and provoked not any by joining with them with whom they could...

## Enumerator Sequence Candidates

- file: EPUB/ch011.xhtml; marker: (8.); family: paren_decimal; context: (8.) By this prerogative of certain predictions in reference to things to come, God vindicates his own deity; and from the want of it evinces the vanity of the idols of the Gentiles, a

## Repeated Windows

- phrase: made of the seed of david according to the flesh; count: 5
- phrase: that they which commit sin are worthy of death romans; count: 5
- phrase: the lord hath laid on him the iniquity of us; count: 5
- phrase: lord hath laid on him the iniquity of us all; count: 5
- phrase: known unto god are all his works from the beginning; count: 4
- phrase: unto god are all his works from the beginning of; count: 4
- phrase: god are all his works from the beginning of the; count: 4
- phrase: are all his works from the beginning of the world; count: 4
- phrase: the son of god is come and hath given us; count: 4
- phrase: son of god is come and hath given us an; count: 4

## Missing Word Samples

- word: pre; pdf: 4; epub: 0
- word: schlusselburgius; pdf: 3; epub: 0
- word: sod; pdf: 3; epub: 0
- word: gerlachius; pdf: 3; epub: 0

## Excess Word Samples

- word: johannes; pdf: 10; epub: 60
- word: valentinus; pdf: 11; epub: 49
- word: christianus; pdf: 6; epub: 23
- word: theodore; pdf: 0; epub: 16
- word: george; pdf: 1; epub: 13
- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 4; epub: 13
- word: christophorus; pdf: 0; epub: 9
- word: psalms; pdf: 3; epub: 11
- word: historical; pdf: 0; epub: 8

## Missing Latin Word Samples

- word: schlusselburgius; pdf: 3; epub: 0
- word: gerlachius; pdf: 3; epub: 0

## Untagged Latin Word Samples

- word: nor; epub: 438; tagged: 15
- word: jesus; epub: 397; tagged: 3
- word: grotius; epub: 197; tagged: 20
- word: mediator; epub: 148; tagged: 5
- word: yea; epub: 139; tagged: 3
- word: socinus; epub: 169; tagged: 36
- word: abraham; epub: 93; tagged: 2
- word: thereunto; epub: 73; tagged: 2
- word: annotator; epub: 69; tagged: 1
- word: mere; epub: 65; tagged: 2

## Missing Latin Clauses

- page: 27; word_count: 6; sample: georgius blandrata petrus statorius franciscus lismaninus
- page: 116; word_count: 4; sample: socinus smalcius crellius etc
- page: 593; word_count: 6; sample: oppressus et affiictus fuit et non

## Untranslated Latin Samples

- phrase: HUGO GROTIUS
- phrase: Vindiciae Evangelicae
- phrase: Faustus Socinus
- phrase: Statorius, ‡ junior
- phrase: Valentinus Smalcius
- phrase: as "quantilla causa
- phrase: Nicolaus Arnoldus
- phrase: Maresius, ‡ professor
- phrase: Dionysius ‡ Petavius
- phrase: Socinus, Valentinus Smalcius

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
