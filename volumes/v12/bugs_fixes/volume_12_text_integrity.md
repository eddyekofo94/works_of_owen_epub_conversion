# Text Integrity Audit: Volume 12

- Status: **WARN**
- Warnings: 12
- PDF pages: 822
- EPUB text files: 61
- EPUB paragraphs/headings: 3619

## Coverage

- PDF content tokens: 270737
- EPUB content tokens: 272543
- Approximate PDF-to-EPUB coverage ratio: 0.9991
- Pages checked: 815
- Weak page matches: 0
- Dense source windows checked: 32888
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 3
- Missing front CONTENTS pages: 1
- Top-of-page body windows checked: 793
- Top-of-page windows skipped as unstable: 47
- Missing top-of-page body windows: 3
- Bottom-of-page body windows checked: 740
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 13

## Paragraphs

- Body paragraphs checked: 3182
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 443
- Short fragments: 53
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
- Missing enumerator marker forms: 2
- Enumerator sequence candidates: 0

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
- EPUB Latin words: 10668
- EPUB Tagged Latin words: 6309
- Latin word coverage ratio: 0.998
- Latin word tagging ratio: 0.5914
- Latin clauses checked: 776
- Missing Latin clauses: 1
- Tagged Latin runs checked: 1617
- Translated Latin runs: 668
- Latin translation ratio: 0.4131

## Warnings

- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 4; sample: evincing the death of christ to be punishment properly so called digression concerning the
- page: 5; sample: vindicated and socinianism examined in the consideration and confutation of catechism called scripture catechism
- page: 6; sample: first among that splendid catena of divines bull waterland horsley magee fuller pye smith
- page: 7; sample: son and of the spirit and similar doctrines biddle had well nigh fallen martyr
- page: 11; sample: to the right worshipful his reverend learned and worthy friends and brethren the heads
- page: 17; sample: hammond's answer to my animadversions on his dissertations about episcopacy mr baxter's objections against
- page: 29; sample: he became the patron of all the antitrini tarians of all sorts throughout poland
- page: 30; sample: at morden anno and there acquitted with testimonial 15a but in the year at
- page: 32; sample: and cunning as beza says of him 18a incredibly furnished for contradiction and sophism
- page: 41; sample: is since published this was before his going into poland in the year 52a

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
- page: 514; sample: chap. 9:12, "He entered by his own blood into the holy place, aijwni>an lu>trwsin euJra>menov," — "after he had obtained eternal
- page: 526; sample: the LXX. constantly render it by apolutrou~n and sometimes lutrw>sasqai, otherwise by rju>omai, and the like.
- page: 660; sample: 1 Timothy 2:5, 6, gives us this fully. He is the mediator, and as such he gave himself ajnti>lutron, a price of redemption to God.

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: gst you, that, according to your several degrees, you would take it into your patronage or use, affording him in his daily labors the benefit of your prayers at the throne of grace; next: who is your unworthy fellow-laborer
- file: EPUB/ch003.xhtml; previous: who is your unworthy fellow-laborer; next: John Owen
- file: EPUB/ch003.xhtml; previous: John Owen; next: OXON. CH. CH. COLL., April 1 [1655.]
- file: EPUB/ch004.xhtml; previous: of old opposed the doctrine of the Trinity, especially of the deity of Christ, his person and natures, may be referred to three heads, and of them and their ways this is the sum: —; next: The first sort of them may be reckoned to be those who are commonly esteemed to be followers of Simon Magus, known chiefly by the names of Gnostics and Valentinians. These, with th
- file: EPUB/ch004.xhtml; previous: ince of Transylvania, who had then cast David into prison for his blasphemy. 58 To give a little account, by the way, of the end of this man, with his contempt of the Lord Jesus: —; next: In the year 1579, in the beginning of the month of June, he was cast into prison by the prince of Transylvania, and lived until the end of November. 59 That he was cast into prison
- file: EPUB/ch004.xhtml; previous: glad.), and that of the Athenians, by the advice of Epimenides Θεοῖς Ασίας καὶ Ευρώπης καὶ Λιβύης , Θεῷ ἀγνώστῳ καὶ Ξένῳ both of them being suitable to the counsel of Pythagoras: —; next: Αθανάτους μὲν πρῶτα θεοὺς νόμῳ ὡς διάκειται Τίμα καὶ σέβου ὅρκον ἔπειθ ἥρωας ἀγανούς Τούς τε καταχθονίους οέβε δαίμονας ἕννομα ῥέζων Let them be sure to worship all sorts, that the
- file: EPUB/ch006.xhtml; previous: comprehended, compounded; he believes there is no trinity of persons in the Godhead, — that Christ is not the eternal Son of God. The following parts of it are of the same kind: —; next: The eternal procession of the Holy Ghost is nextly rejected. The Holy Ghost being constantly termed the "Spirit of God," the "Spirit of the Father," and the "Spirit of the Son" (be
- file: EPUB/ch006.xhtml; previous: Some things I shall remark upon that discourse, and shut up these considerations of his preface: —; next: For his own success, he tells us "That being otherwise of no great abilities, yet searching the Scriptures impartially, he hath detected many errors, and hath presented the reader
- file: EPUB/ch008.xhtml; previous: Let us all, then, supply our catechumens, in the room of Mr B.'s, with this question, expressly leading to the things inquired after: —; next: What says the Scripture concerning the essence and presence of God? is it confined and limited to a certain place, or is he infinitely and equally present everywhere?
- file: EPUB/ch008.xhtml; previous: nt, ipsum se colere , afrmant, verum hoc sibi placere, ut Jupiter nominetur," lib. 1:cap. 2.); which, as Servius on the place observes, he had taken from Aratus, whose words are: —; next: Εκ διὸς ἀρχώμεσθα τὸν οὐδὲ ποτ ἄνδρες ἐῶμεν Αῤῥητον μεσταὶ δὲ διὸς πᾶσαι μὲν ἁγυιαὶ Πᾶσαι δ ἀνθρώπων ἀγοραὶ μεστὴ δὲ θάλασσα Καὶ λιμένες πάντη δὲ διὸς κεχρήμεθα πάντες — giving a f

## Inline Structural Marker Candidates

- file: EPUB/ch040.xhtml; text: He suffered, — [1.] In his person; [2.] In his name; [3.] In his friends; [4.] In his goods; as the curse of the law extended to all, and that universally in all these: —
- file: EPUB/ch047.xhtml; text: I answer, The words there are used in a law sense, and are declarative of the righteousness of God in rewarding the keepers of the law of nature, or the moral law, according to the law of the covenant of works. This is evident from the w...
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
- file: EPUB/ch017.xhtml; text: etc.
- file: EPUB/ch017.xhtml; text: He adds, 12th,

## Missing Enumerator Markers

- marker: (1.); pdf: 110; epub: 109; examples: [{'location': 'pdf:p51', 'context': 'them to Palaeologus. f75 By this course of behavior, the man had these two advantages: — (1.) He kept fair with all parties amongst them, and provoked not any by joining with them with whom they could...
- marker: (8.); pdf: 1; epub: 0; examples: [{'location': 'pdf:p178', 'context': 'f is as high a pitch of blasphemy as any creature in this world can possibly arrive unto. (8.) By this prerogative of certain predictions in reference to things to come, God vindicates his own deity;...

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
- word: sod; pdf: 3; epub: 0

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 4; epub: 13
- word: psalms; pdf: 3; epub: 11
- word: historical; pdf: 0; epub: 8
- word: modern; pdf: 7; epub: 14
- word: footnotes; pdf: 0; epub: 7
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

- page: 593; word_count: 6; sample: oppressus et affiictus fuit et non

## Untranslated Latin Samples

- phrase: HUGO GROTIUS
- phrase: Vindiciae Evangelicae
- phrase: Faustus Socinus
- phrase: Statorius, ‡ junior
- phrase: as "quantilla causa
- phrase: Valentinus Smalcius
- phrase: Nicolaus Arnoldus
- phrase: Maresius, ‡ professor
- phrase: Dionysius ‡ Petavius
- phrase: Socinus, Smalcius, Crellius

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
