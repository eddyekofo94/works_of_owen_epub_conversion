# Text Integrity Audit: Volume 12

- Status: **WARN**
- Warnings: 12
- PDF pages: 822
- EPUB text files: 59
- EPUB paragraphs/headings: 3294

## Coverage

- PDF content tokens: 275563
- EPUB content tokens: 259266
- Approximate PDF-to-EPUB coverage ratio: 0.9381
- Pages checked: 815
- Weak page matches: 79
- Dense source windows checked: 920
- Missing dense source-window pages: 808
- Front CONTENTS pages checked: 3
- Missing front CONTENTS pages: 3
- Top-of-page body windows checked: 798
- Top-of-page windows skipped as unstable: 48
- Missing top-of-page body windows: 48
- Bottom-of-page body windows checked: 746
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 59

## Paragraphs

- Body paragraphs checked: 2948
- Possible faulty paragraph splits: 257
- Structural starts excluded from split warnings: 331
- Short fragments: 42
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 6
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 450
- EPUB enumerator markers: 569
- Missing enumerator marker forms: 1
- Enumerator sequence candidates: 38

## Greek / Hebrew

- PDF Greek words: 2593
- EPUB Greek words: 2342
- Greek word coverage ratio: 0.8979
- PDF Hebrew words: 222
- EPUB Hebrew words: 221
- Hebrew word coverage ratio: 0.9955
- Greek clauses checked: 133
- Missing Greek clauses: 20
- Hebrew clauses checked: 7
- Missing Hebrew clauses: 0

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
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 3; sample: contents of vindiciae evangelicae or the mystery of the gospel vindicated and socinianism examined
- page: 4; sample: office and how he dischargeth it 21 of the death of christ the causes
- page: 5; sample: vindicated and socinianism examined in the consideration and confutation of catechism called scripture catechism
- page: 7; sample: the son and of the spirit and similar doctrines biddle had well nigh fallen
- page: 9; sample: he is claimed alike by socinians arminians and papists the learned jesuit peta-vius said
- page: 11; sample: 11 to the right worshipful his reverend learned and worthy friends and brethren the
- page: 12; sample: 12 the like nature which to my thoughts did then occur not prevailing with
- page: 13; sample: 13 maresius professor at groningen man well known by his works published goes farther
- page: 14; sample: 14 from thence whence in the thoughts of some am most likely to suffer
- page: 15; sample: 15 that be men of what religion soever that is professed in the world

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.25; sample: contents of vindiciae evangelicae or the mystery of the gospel vindicated and socinianism examined prefatory note by the editor dedication epistle dedicatory preface to the reader mr biddle's
- page: 4; hit_ratio: 0.5; sample: 20 of the priestly office of christ how he was priest when he entered on his office and how he dischargeth it 21 of the death of christ
- page: 5; hit_ratio: 0.5; sample: vindiciae evangelicae or the mystery of the gospel vindicated and socinianism examined in the consideration and confutation of catechism called scripture catechism written by biddle and the catechism

## Missing Top-Of-Page Body Windows

- page: 11; sample: TO THE RIGHT WORSHIPFUL, HIS REVEREND, LEARNED, AND WORTHY FRIENDS AND BRETHREN,
- page: 131; sample: Neither can that of the prophet Isaiah, chap. 66:1, be otherwise
- page: 229; sample: Luke 1:35;" f235 — the place insisted on the Son of God, as we read in
- page: 258; sample: himself abundantly hath manifested to be otherwise. Of 1 Corinthians
- page: 445; sample: Exodus 33:11, in the Hebrew is µyniP;Ala, µyniP;, panim el That which,
- page: 749; sample: engage in this now in hand; of the necessity whereof I shall give the reader a brief account. That as to the matter of the contest between Mr B. and
- page: 750; sample: But why must my arguments be answered and myself confuted? Two reasons hereof are given. The first by very many insinuations, namely, that
- page: 751; sample: are answered in reference to another, and that this is the sum of Mr B.'s discourse against me, I shall only recommend to them some verses of old
- page: 752; sample: than he, that he have more illumination and grace than he; that is, that he be a better, wiser, more holy, and learned man than Mr B. Now, if we may
- page: 753; sample: That he hath been able to discern the positions he opposes in the beginning of his eighth chapter to be contained in any writings of mine, as maintained

## Missing Bottom-Of-Page Body Windows

- page: 4; sample: A SECOND CONSIDERATION OF THE ANNOTATIONS OF HUGO GROTIUS, EPISTLES OF GROTIUS TO CRELLIUS,
- page: 145; sample: Cwrei~te qnhtw~n to<n Qeo<n kai< mh< do>kei. Omoion aujtw~| sarkiko<n kaqesta>nai.
- page: 175; sample: propositions: — (1.) That God hath so foretold the free actions of men.
- page: 209; sample: explained. The words are, Oti oJ Qeo<v e]ktise to<n a]nqrwton ejp ajfqarsi>a| kai< eijko>na th~v ijdi>av ijdio>thtov ejpoi>hsen aujto>n Fqo>nw|
- page: 335; sample: expressed in the enumeration foregoing or no; all things were created by him. They were created for him eijv aujto>n, as it is said of the Father,
- page: 373; sample: chap. 16:19, ajnelh>fqh, — that is, ajnelh>fqh ejn do>xh|, "he was taken up into heaven,"
- page: 399; sample: vocis aperture est, et istud hBer]µæl], Isaiah 9:6, clausum est?
- page: 438; sample: 1 Timothy 2:6, "in whom we have redemption redemption for us,
- page: 514; sample: chap. 9:12, "He entered by his own blood into the holy place, aijwni>an lu>trwsin euJra>menov," — "after he had obtained eternal
- page: 526; sample: the LXX. constantly render it by apolutrou~n and sometimes lutrw>sasqai, otherwise by rju>omai, and the like.

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: gst you, that, according to your several degrees, you would take it into your patronage or use, affording him in his daily labors the benefit of your prayers at the throne of grace; next: who is your unworthy fellow-laborer
- file: EPUB/ch003.xhtml; previous: who is your unworthy fellow-laborer; next: John Owen
- file: EPUB/ch003.xhtml; previous: John Owen; next: OXON. CH. CH. COLL., April 1 [1655.]
- file: EPUB/ch004.xhtml; previous: house of God there are daily builders, according as new living stones are to be fitted to their places therein; and continual oppositions have there been made thereto, and will be,; next: In this work of building are some employed by Jesus Christ, and will be so to the end of the world, Matthew 28:19, 20, Ephesians 4:11, 12; and some employ themselves at least in a
- file: EPUB/ch004.xhtml; previous: and not be believed. See Calvin's epistles, about the year 1561. But the man on this occasion being sent to the meeting at Pinckzow (as Statorius), he subscribes this confession: —; next: This did the wretched man think meet to do, that he might preserve the good esteem of his patron and reserve himself for a fitter opportunity of doing mischief; which also he did,
- file: EPUB/ch004.xhtml; previous: of Grotius, time will evidence. Now, because this man's creed is such as is not to be paralleled, perhaps some may be contented to take it in his own words, which are as follow: —; next: To this issue did Satan drive the Socinian principles in this man and sundry others, even to a full and peremptory denial of the Lord that bought them. In answering this man, it fe
- file: EPUB/ch004.xhtml; previous: ne day send him again to Jerusalem, there to take upon him a kingdom, and to rule as the kings of this world do or have done." — Thes. Francisci David de Adorat. Jes. Christi. [10]; next: The reminding of these abominations gives occasion, by the way, to complain of the carnal apprehensions of a kingdom of Christ , which too many amongst ourselves have filled their
- file: EPUB/ch004.xhtml; previous: , nam ratio vocabuli non patitur, ut quis dicatur sine matre pater: et si Logos filius erat, natus ex patre sine matre; dic mihi quomodo peporit eum, per ventrem an per latus." [2]; next: To this height of atheism and blasphemy had Satan wrought up the spirit of the man; so that I must say he is the only person in the world, that I ever read or heard of, that ever d
- file: EPUB/ch004.xhtml; previous: is day the Papists continue in the same idolatry (to touch that by the way), I shall give you, for your refreshment, a copy of a verse or two, whose poetry does much outgo the old,; next: and whose blasphemy comes not at all short of it. The first is of Clarus Bonarus the Jesuit, lib. 3 Amphitrial. Honor. lib. 3 cap. ult. ad Divinam Hallensem et Puerum Jesum, as fol
- file: EPUB/ch004.xhtml; previous: blasphemy comes not at all short of it. The first is of Clarus Bonarus the Jesuit, lib. 3 Amphitrial. Honor. lib. 3 cap. ult. ad Divinam Hallensem et Puerum Jesum, as followeth: —; next: The other is of Franciscus de Mendoza, in Viridario Utriusque Eruditionis, lib. 2 prob. 2, as ensueth: —

## Inline Structural Marker Candidates

- file: EPUB/ch017.xhtml; text: The intendment of these questions being the application of what is spoken of Christ, either as mediator or as man, unto his person, to the exclusion of any other consideration, namely, that of a divine nature therein, the whole of Mr B.'...
- file: EPUB/ch022.xhtml; text: The first they propose is taken from Hebrews 1:3, where the words spoken of Christ are, Φέρων τε τὰ πάντα τῷ ῥήματι τῆς δυνάμεως αὑτοῦ , [1] — "Upholding all things by the word of his power."
- file: EPUB/ch032.xhtml; text: Of the same judgment with him is Volk. de Vera Relig. lib. 4:cap. 11: [2] de Christi invocatione, Schlichting. ad Meisner., pp. 206, 207, and generally the rest of them; which again how consistent it is with what they affirm in the Racov...
- file: EPUB/ch040.xhtml; text: He suffered, — [1.] In his person; [2.] In his name; [3.] In his friends; [4.] In his goods; as the curse of the law extended to all, and that universally in all these: —
- file: EPUB/ch047.xhtml; text: I answer, The words there are used in a law sense, and are declarative of the righteousness of God in rewarding the keepers of the law of nature, or the moral law, according to the law of the covenant of works. This is evident from the w...
- file: EPUB/ch047.xhtml; text: These Mr B. would oppose, and from the assertion of the one argue to the destruction of the other, though they sweetly and eminently comply in our communion with God. The other righteousness was before evinced. Even our sanctification al...

## Suspicious Large-Number Starts

- file: EPUB/ch011.xhtml; text: 11. Crellius is something more candid, as he pretends, but indeed infected with the same venom with the other; for after he hath disputed for sundry pages to prove the foreknowledge of God, he concludes at last that for
- file: EPUB/ch019.xhtml; text: 24. Simile loquendi genua Sic Legem fuisse ante mundum aiunt Hebraei." Again, " Παρὰ σοί , refer ad illud εῖχον , et intellige, ut diximus, in decreto tuo." But what intends the learned man by those places o 1 Peter 1:20
- file: EPUB/ch039.xhtml; text: 52. The words of that verse are, —
- file: EPUB/ch042.xhtml; text: 12. And that may be the sense of the word ἐπιλαμβάνεται , if not in the effect, yet in the cause, Hebrews 2:16.

## Short Fragments

- file: EPUB/ch003.xhtml; text: John Owen
- file: EPUB/ch005.xhtml; text: JOHN BIDDLE.
- file: EPUB/ch009.xhtml; text: MR BIDDLE'S question: —
- file: EPUB/ch009.xhtml; text: Whereunto answers that in Cato: —
- file: EPUB/ch009.xhtml; text: Ομοιον αὐτῷ σαρκικὸν καθεστάναι .
- file: EPUB/ch011.xhtml; text: Ans.
- file: EPUB/ch013.xhtml; text: Ans. Genesis 1:1
- file: EPUB/ch014.xhtml; text: EXAMINATION.
- file: EPUB/ch016.xhtml; text: Ans. Ephesians 4:5.
- file: EPUB/ch017.xhtml; text: EXAMINATION.

## Missing Enumerator Markers

- marker: (1.); pdf: 110; epub: 108; examples: [{'location': 'pdf:p51', 'context': 'them to Palaeologus. f75 By this course of behavior, the man had these two advantages: — (1.) He kept fair with all parties amongst them, and provoked not any by joining with them with whom they could...

## Enumerator Sequence Candidates

- file: EPUB/ch004.xhtml; marker: [18]; family: bracket_decimal; context: , lib. 1 tom. 2; and Augustine, in his book of Heresies, 5 "ad quod vult deus manifeste." [18] To these may be added Tatianus, Cerdo, Marcion, and their companions (of whom see Tertullian at large, and Eusebius, in their respective place...
- file: EPUB/ch004.xhtml; marker: [9]; family: bracket_decimal; context: affirmed by Epiphanius, Haer. 51. "Hieronymus de Seriptoribus Ecclesiasticis de Johanne." [9] The same abomination was again revived by Theodotus, called Coriarius (who, having once denied Christ, was resolved to do so always); excommuni...
- file: EPUB/ch004.xhtml; marker: [17]; family: bracket_decimal; context: municated on that account by Victor, as Eusebius relates, Hist. Eccles. lib. 5 cap. ult., [17] where he gives also an account of his associates in judgment, Artemon, Asclepiodotus, Natalius, etc.; and the books written against him are th...
- file: EPUB/ch004.xhtml; marker: [16]; family: bracket_decimal; context: stantly boast. Of Samosatenus and his heresy, see Euseb. Hist. Eccles. lib. 7 cap. 29, 30 [16] and Hilary, De Synodis; of Photinus, Socrat. Eccles. Hist. lib. 2 cap. 24, 25. [14] And with these do our present Socinians expressly agree in...
- file: EPUB/ch004.xhtml; marker: [14]; family: bracket_decimal; context: 9, 30 [16] and Hilary, De Synodis; of Photinus, Socrat. Eccles. Hist. lib. 2 cap. 24, 25. [14] And with these do our present Socinians expressly agree in the matter of the person of Christ. 7 To the third head I refer that deluge of ARIA...
- file: EPUB/ch004.xhtml; marker: [6]; family: bracket_decimal; context: "Defensio Fidei Catholicae de Satisfactione Christi, adversus Faustum Socinum Senensem." [6] Immediately upon the coming out of that book, animadversions were put forth against it by Harmanus Ravenspergerus, approved, as it seems, by our...
- file: EPUB/ch004.xhtml; marker: [3]; family: bracket_decimal; context: sia, seu rege illo promisso, et haec est mea religio, quam coram vobis ingenue profiteor. [3] " — Martin. Seidelius Olaviensis Silesius.
- file: EPUB/ch004.xhtml; marker: [13]; family: bracket_decimal; context: defense of Socinus against Grotius' treatise, "De Causis Morris Christi, de Effectu SS.," [13] his comments and ethics, declare his abilities and industry in his way. After him arose Jonas Schlichtingius, a man no whit behind any of the ...
- file: EPUB/ch004.xhtml; marker: [2]; family: bracket_decimal; context: erat, natus ex patre sine matre; dic mihi quomodo peporit eum, per ventrem an per latus." [2]
- file: EPUB/ch004.xhtml; marker: [8]; family: bracket_decimal; context: rmine, in his book, "De Christo,' lays it to the charge of Bullinger, that in his book, " [8] De Scripturae et Ecclesiae Authoritate," he wrote that there were three persons in the Deity, "non statu, sed gradu, non subsistentia, sed form...

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

- word: chap; pdf: 142; epub: 31
- word: justification; pdf: 145; epub: 68
- word: jus; pdf: 45; epub: 1
- word: myself; pdf: 69; epub: 33
- word: ex; pdf: 54; epub: 25
- word: elect; pdf: 47; epub: 23
- word: deo; pdf: 42; epub: 20
- word: nobis; pdf: 42; epub: 20
- word: opera; pdf: 23; epub: 1
- word: esse; pdf: 39; epub: 18

## Excess Word Samples

- word: 5chap; pdf: 0; epub: 14
- word: digital; pdf: 0; epub: 10
- word: veniam; pdf: 1; epub: 10
- word: 1chap; pdf: 0; epub: 9
- word: modern; pdf: 7; epub: 15
- word: psalms; pdf: 3; epub: 11
- word: 6chap; pdf: 0; epub: 8
- word: 13chap; pdf: 0; epub: 7
- word: footnotes; pdf: 0; epub: 6
- word: onlybegotten; pdf: 0; epub: 6

## Missing Greek Word Samples

- word: ζητήσεις; pdf: 3; epub: 0

## Missing Greek Clauses

- page: 63; word_count: 21; sample: αθανατους μεν πρωτα θεους νομω ως διακειται τιμα και σεβου ορκον επειθ
- page: 748; word_count: 7; sample: γινεται φθονος ερις βλασφημιαι υπονοιαι πονηραι παραδιατριβαι
- page: 748; word_count: 7; sample: το γινεσθαι πατερα παιδων λυπη φοβος φροντις
- page: 749; word_count: 7; sample: φιλει γαρ οκειν πραγμ ανηρ πρασσων μεγα
- page: 749; word_count: 5; sample: ως ουχ υπαρχων αλλα τιμωρουμενος
- page: 750; word_count: 6; sample: μικρα προφασις εστι του πραξαι κακως
- page: 750; word_count: 14; sample: ειδε παν εχει καλως τω παιγνιω δοτε κροτον και παντες υμεις μετα
- page: 751; word_count: 7; sample: και ταυτα πρασσων φασκ ανηρ ουδεν ποιων
- page: 752; word_count: 8; sample: ουθεις επ αυτου τα κακα συνορα σαφως ετερου
- page: 753; word_count: 6; sample: εγω ειμι μονος των ημων εμος

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
