# Text Integrity Audit: Volume 12

- Status: **WARN**
- Warnings: 14
- PDF pages: 822
- EPUB text files: 61
- EPUB paragraphs/headings: 3532

## Coverage

- PDF content tokens: 275563
- EPUB content tokens: 276599
- Approximate PDF-to-EPUB coverage ratio: 0.996
- Pages checked: 815
- Weak page matches: 31
- Dense source windows checked: 961
- Missing dense source-window pages: 807
- Front CONTENTS pages checked: 3
- Missing front CONTENTS pages: 1
- Top-of-page body windows checked: 798
- Top-of-page windows skipped as unstable: 48
- Missing top-of-page body windows: 5
- Bottom-of-page body windows checked: 746
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 14

## Paragraphs

- Body paragraphs checked: 3094
- Possible faulty paragraph splits: 276
- Structural starts excluded from split warnings: 342
- Short fragments: 48
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 5
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 450
- EPUB enumerator markers: 513
- Missing enumerator marker forms: 1
- Enumerator sequence candidates: 14

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
- EPUB Latin words: 10658
- EPUB Tagged Latin words: 6303
- Latin word coverage ratio: 0.9982
- Latin word tagging ratio: 0.5914
- Latin clauses checked: 787
- Missing Latin clauses: 45
- Tagged Latin runs checked: 1615
- Translated Latin runs: 497
- Latin translation ratio: 0.3077

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

- page: 4; sample: of christ to be punishment properly so called 25 digression concerning the 53d chapter
- page: 5; sample: vindicated and socinianism examined in the consideration and confutation of catechism called scripture catechism
- page: 7; sample: the son and of the spirit and similar doctrines biddle had well nigh fallen
- page: 9; sample: he is claimed alike by socinians arminians and papists the learned jesuit peta-vius said
- page: 11; sample: 11 to the right worshipful his reverend learned and worthy friends and brethren the
- page: 12; sample: 12 the like nature which to my thoughts did then occur not prevailing with
- page: 13; sample: 13 maresius professor at groningen man well known by his works published goes farther
- page: 14; sample: 14 from thence whence in the thoughts of some am most likely to suffer
- page: 15; sample: 15 that be men of what religion soever that is professed in the world
- page: 16; sample: 16 given to that sacred truth which is not wrested to another sense or

## Missing Front CONTENTS Pages

- page: 5; hit_ratio: 0.5; sample: vindiciae evangelicae or the mystery of the gospel vindicated and socinianism examined in the consideration and confutation of catechism called scripture catechism written by biddle and the catechism

## Missing Top-Of-Page Body Windows

- page: 11; sample: TO THE RIGHT WORSHIPFUL, HIS REVEREND, LEARNED, AND WORTHY FRIENDS AND BRETHREN,
- page: 131; sample: Neither can that of the prophet Isaiah, chap. 66:1, be otherwise
- page: 136; sample: CHAPTER 3. Of the drape and bodily visible figure of God.
- page: 229; sample: Luke 1:35;" f235 — the place insisted on the Son of God, as we read in
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

- file: EPUB/ch003.xhtml; previous: gst you, that, according to your several degrees, you would take it into your patronage or use, affording him in his daily labors the benefit of your prayers at the throne of grace; next: who is your unworthy fellow-laborer
- file: EPUB/ch003.xhtml; previous: who is your unworthy fellow-laborer; next: John Owen
- file: EPUB/ch003.xhtml; previous: John Owen; next: OXON. CH. CH. COLL., April 1 [1655.]
- file: EPUB/ch004.xhtml; previous: house of God there are daily builders, according as new living stones are to be fitted to their places therein; and continual oppositions have there been made thereto, and will be,; next: In this work of building are some employed by Jesus Christ, and will be so to the end of the world, Matthew 28:19, 20, Ephesians 4:11, 12; and some employ themselves at least in a
- file: EPUB/ch004.xhtml; previous: and not be believed. See Calvin's epistles, about the year 1561. But the man on this occasion being sent to the meeting at Pinckzow (as Statorius), he subscribes this confession: —; next: This did the wretched man think meet to do, that he might preserve the good esteem of his patron and reserve himself for a fitter opportunity of doing mischief; which also he did,
- file: EPUB/ch004.xhtml; previous: of Grotius, time will evidence. Now, because this man's creed is such as is not to be paralleled, perhaps some may be contented to take it in his own words, which are as follow: —; next: To this issue did Satan drive the Socinian principles in this man and sundry others, even to a full and peremptory denial of the Lord that bought them. In answering this man, it fe
- file: EPUB/ch004.xhtml; previous: one day send him again to Jerusalem, there to take upon him a kingdom, and to rule as the kings of this world do or have done." — Thes. Francisci David de Adorat. Jes. Christi. [1]; next: The reminding of these abominations gives occasion, by the way, to complain of the carnal apprehensions of a kingdom of Christ , which too many amongst ourselves have filled their
- file: EPUB/ch004.xhtml; previous: is day the Papists continue in the same idolatry (to touch that by the way), I shall give you, for your refreshment, a copy of a verse or two, whose poetry does much outgo the old,; next: and whose blasphemy comes not at all short of it. The first is of Clarus Bonarus the Jesuit, lib. 3 Amphitrial. Honor. lib. 3 cap. ult. ad Divinam Hallensem et Puerum Jesum , as fo
- file: EPUB/ch004.xhtml; previous: blasphemy comes not at all short of it. The first is of Clarus Bonarus the Jesuit, lib. 3 Amphitrial. Honor. lib. 3 cap. ult. ad Divinam Hallensem et Puerum Jesum , as followeth: —; next: The other is of Franciscus de Mendoza, in Viridario Utriusque Eruditionis, lib. 2 prob. 2, as ensueth: —
- file: EPUB/ch004.xhtml; previous: The other is of Franciscus de Mendoza, in Viridario Utriusque Eruditionis, lib. 2 prob. 2, as ensueth: —; next: And this their idolatry is objected to them by Soeinus, 94 who marvels at the impudence of Bellarmine closing his books of controversies (as is the manner of the men of that Societ

## Inline Structural Marker Candidates

- file: EPUB/ch008.xhtml; text: — "All things are disposed of by the virtue of one infinite mind." And Plutarch, expressing the same thing, says he is νοῦς καθαρὸς καὶ ἄρκρατος ἐμμεμιγμένος πᾶσι , — "a pure and sincere mind, mixing itself, and mixed" (so they expressed...
- file: EPUB/ch017.xhtml; text: The intendment of these questions being the application of what is spoken of Christ, either as mediator or as man, unto his person, to the exclusion of any other consideration, namely, that of a divine nature therein, the whole of Mr B.'...
- file: EPUB/ch022.xhtml; text: The first they propose is taken from Hebrews 1:3, where the words spoken of Christ are, Φέρων τε τὰ πάντα τῷ ῥήματι τῆς δυνάμεως αὑτοῦ , [1] — "Upholding all things by the word of his power."
- file: EPUB/ch040.xhtml; text: He suffered, — [1.] In his person; [2.] In his name; [3.] In his friends; [4.] In his goods; as the curse of the law extended to all, and that universally in all these: —
- file: EPUB/ch047.xhtml; text: These Mr B. would oppose, and from the assertion of the one argue to the destruction of the other, though they sweetly and eminently comply in our communion with God. The other righteousness was before evinced. Even our sanctification al...

## Suspicious Large-Number Starts

- file: EPUB/ch011.xhtml; text: 11. Crellius is something more candid, as he pretends, but indeed infected with the same venom with the other; for after he hath disputed for sundry pages to prove the foreknowledge of God, he concludes at last that for
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
- file: EPUB/ch017.xhtml; text: EXAMINATION.
- file: EPUB/ch017.xhtml; text: He adds, 12th,

## Missing Enumerator Markers

- marker: (1.); pdf: 110; epub: 109; examples: [{'location': 'pdf:p51', 'context': 'them to Palaeologus. f75 By this course of behavior, the man had these two advantages: — (1.) He kept fair with all parties amongst them, and provoked not any by joining with them with whom they could...

## Enumerator Sequence Candidates

- file: EPUB/ch004.xhtml; marker: [7]; family: bracket_decimal; context: , lib. 1 tom. 2; and Augustine, in his book of Heresies, 5 "ad quod vult deus manifeste." [7] To these may be added Tatianus, Cerdo , Marcion, and their companions (of whom see Tertullian at large, and Eusebius, in their respective place...
- file: EPUB/ch004.xhtml; marker: [6]; family: bracket_decimal; context: municated on that account by Victor, as Eusebius relates, Hist. Eccles. lib. 5 cap. ult., [6] where he gives also an account of his associates in judgment, Artemon, Asclepiodotus, Natalius , etc.; and the books written against him are th...
- file: EPUB/ch004.xhtml; marker: [5]; family: bracket_decimal; context: stantly boast. Of Samosatenus and his heresy, see Euseb. Hist. Eccles. lib. 7 cap. 29, 30 [5] and Hilary, De Synodis ; of Photinus, Socrat. Eccles. Hist. lib. 2 cap. 24, 25. [4] And with these do our present Socinians expressly agree in ...
- file: EPUB/ch004.xhtml; marker: [4]; family: bracket_decimal; context: 9, 30 [5] and Hilary, De Synodis ; of Photinus, Socrat. Eccles. Hist. lib. 2 cap. 24, 25. [4] And with these do our present Socinians expressly agree in the matter of the person of Christ. 7 To the third head I refer that deluge of ARIAN...
- file: EPUB/ch008.xhtml; marker: [4]; family: bracket_decimal; context: do concerning the presence of God. "He is," saith he, "in heaven, as in a certain place." [4] That which is in a certain place is finite and limited, as, from the nature of a place and the manner of any thing's being in a place, shall be...
- file: EPUB/ch008.xhtml; marker: [3]; family: bracket_decimal; context: is more than insinuated in the expression that he is "in a certain place in the heavens," [3] I ask why he dwells in one part of the heavens rather than another? 134 or whether he ever removes or takes a journey, as Elijah speaks of Baal...
- file: EPUB/ch008.xhtml; marker: [2]; family: bracket_decimal; context: psum se colere , afrmant, verum hoc sibi placere, ut Jupiter nominetur," lib. 1:cap. 2.); [2] which, as Servius on the place observes, he had taken from Aratus, whose words are: — Εκ διὸς ἀρχώμεσθα τὸν οὐδὲ ποτ ἄνδρες ἐῶμεν [1] Αῤῥητον μ...
- file: EPUB/ch009.xhtml; marker: [2]; family: bracket_decimal; context: schylus, in the same place of Clemens, Strom. 5: — Χωρεῖτε θνητῶν τὸν Θεὸν καὶ μὴ δόκει . [2]
- file: EPUB/ch011.xhtml; marker: (8.); family: paren_decimal; context: (8.) By this prerogative of certain predictions in reference to things to come, God vindicates his own deity; and from the want of it evinces the vanity of the idols of the Gentiles, a
- file: EPUB/ch017.xhtml; marker: [2]; family: bracket_decimal; context: s sufficiently already disappointed. It is true, there is an order, yea, a subordination, [2] in the persons of the Trinity themselves, whereby the son, as to his personality, may be said to depend on the Father, being begotten of him; b...

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
- word: sod; pdf: 3; epub: 0
- word: ; pdf: 3; epub: 1

## Excess Word Samples

- word: 5chap; pdf: 0; epub: 14
- word: digital; pdf: 0; epub: 10
- word: modern; pdf: 7; epub: 16
- word: 1chap; pdf: 0; epub: 9
- word: psalms; pdf: 3; epub: 11
- word: 6chap; pdf: 0; epub: 8
- word: theological; pdf: 4; epub: 11
- word: 13chap; pdf: 0; epub: 7
- word: footnotes; pdf: 0; epub: 6
- word: onlybegotten; pdf: 0; epub: 6

## Untagged Latin Word Samples

- word: nor; epub: 438; tagged: 15
- word: jesus; epub: 397; tagged: 3
- word: grotius; epub: 197; tagged: 20
- word: mediator; epub: 148; tagged: 5
- word: yea; epub: 139; tagged: 3
- word: socinus; epub: 169; tagged: 40
- word: abraham; epub: 93; tagged: 2
- word: thereunto; epub: 73; tagged: 2
- word: annotator; epub: 69; tagged: 1
- word: mere; epub: 65; tagged: 2

## Missing Latin Clauses

- page: 48; word_count: 8; sample: quia etiam mihi a deo datus est non
- page: 123; word_count: 6; sample: sed repetendum verbum quod paulo ante
- page: 153; word_count: 11; sample: quod res sunt futurae a voluntate dei est effectiva vel permissiva
- page: 231; word_count: 7; sample: illud quod a deo creatum et cum
- page: 231; word_count: 5; sample: quia non a viro profectum
- page: 263; word_count: 5; sample: is purus homo a mere
- page: 303; word_count: 9; sample: origo ipsi ab olim a temporibus longis id est
- page: 347; word_count: 4; sample: is a seipso or
- page: 365; word_count: 4; sample: jacobus a porta fidei
- page: 372; word_count: 4; sample: as a malefactor a

## Untranslated Latin Samples

- phrase: HUGO GROTIUS
- phrase: Vindiciae Evangelicae
- phrase: Faustus Socinus
- phrase: Statorius, junior
- phrase: as "quantilla causa
- phrase: Valentinus Smalcius
- phrase: Nicolaus Arnoldus
- phrase: Maresius, professor
- phrase: Dionysius Petavius
- phrase: Socinus, Smalcius, Crellius

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
