# Text Integrity Audit: Volume 16

- Status: **WARN**
- Warnings: 14
- PDF pages: 672
- EPUB text files: 82
- EPUB paragraphs/headings: 2653

## Coverage

- PDF content tokens: 217723
- EPUB content tokens: 218950
- Approximate PDF-to-EPUB coverage ratio: 0.9992
- Pages checked: 662
- Weak page matches: 1
- Dense source windows checked: 28539
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 5
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 630
- Top-of-page windows skipped as unstable: 34
- Missing top-of-page body windows: 3
- Bottom-of-page body windows checked: 602
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 5

## Paragraphs

- Body paragraphs checked: 2300
- Possible faulty paragraph splits: 2
- Structural starts excluded from split warnings: 275
- Short fragments: 20
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 8
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 3
- Roman heading candidates: 1
- Overlong heading candidates: 1
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 509
- EPUB enumerator markers: 519
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1037
- EPUB Greek words: 1042
- Greek word coverage ratio: 0.995
- PDF Hebrew words: 268
- EPUB Hebrew words: 268
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 51
- Missing Greek clauses: 0
- Hebrew clauses checked: 19
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 4907
- EPUB Latin words: 4942
- EPUB Tagged Latin words: 2001
- Latin word coverage ratio: 0.9988
- Latin word tagging ratio: 0.4049
- Latin clauses checked: 221
- Missing Latin clauses: 0
- Tagged Latin runs checked: 583
- Translated Latin runs: 246
- Latin translation ratio: 0.422

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py
- `flat_analysis_chapters`: 1 ANALYSIS chapter(s) appear under-structured — fewer outline markers than expected. Check extraction quality for these chapters.

## Missing Dense Source Windows

- page: 6; sample: formerly asserted by others reasons of the opposition made to them of the putty
- page: 10; sample: the true nature of gospel church and its government the second part wherein these
- page: 19; sample: separation is proper and inseparable adjunct thereof the apostle speaks of church member-ship corinthians
- page: 25; sample: not be tolerated at least not approved in well governed kingdom or commonwealth of
- page: 27; sample: covetous oppressors and the like who shall not inherit the kingdom of god corinthians
- page: 28; sample: even deride the necessity of the same things in present church members or the
- page: 33; sample: the things ascribed unto those who are to be esteemed the proper subject matter
- page: 34; sample: things as to deny that the members of the church ought to be visibly
- page: 43; sample: chapter of the formal cause of particular church the way or means whereby such
- page: 48; sample: useful unto the ends of church edification jointly giving up themselves unto the lord

## Missing Top-Of-Page Body Windows

- page: 43; sample: CHAPTER 2. OF THE FORMAL CAUSE OF A PARTICULAR CHURCH.
- page: 333; sample: OF INFANT BAPTISM AND DIPPING. OF INFANT BAPTISM.
- page: 363; sample: TO MY REVEREND AND WORTHY FRIENDS, THE PREBENDS OF CHRIST CHURCH COLLEGE

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 365; sample: of it (which how vast and extensive it is no man knows; — for the Jews have given us their deuterw>seiv in their Mishna and Gemara; these kept
- page: 372; sample: Rabbins; and the other, that without them the understanding of the Hebrew is ejk tw~n ajduna>twn: though they look diverse ways, there is a
- page: 398; sample: determined the times before appointed, and the bounds of their habitation," zhtei~n to<n Ku>rion eji a]rage yhlafh>seian aujto<n kai<
- page: 593; sample: And there is another word that signifies also what weight he lays on it, We have rendered it here, "Furthermore then." It is to< loipo<n ou+n, — "for

## Possible Paragraph Splits

- file: EPUB/ch032.xhtml; previous: plum ipsis quoque fiens; deinde et usque ad mortem pervenit, ut sit primogenitus ex mortuis , ipse primatum tenens in omnibus, princeps vitae, prior omnium, et praecedens omnes." †; next: Lib. 1: cap. 18: Οσοι γάρ εἰσι ταύτης τῆς γνώμης μυσταγωγοὶ , τοσαῦται καὶ ἀπολυτρώσεις . Οτι μὲν εἰς ἐξάρνησιν τοῦ βαπτισ́ματος τῆς εἰς Θεὸν ἀναγεννήσεως , καὶ πάσης τῆς πίστεως ἀ
- file: EPUB/ch058.xhtml; previous: cam veritatem, ut interim fatear illos non admodum peritos fuisse linguae Hebraicae id vel quod inviti cogimur fateri , alioquin in plurimis locis non tam fcede lapsi fuissent ." †; next: If, moreover, the ability be granted, what security have we of their principles and honesty? Cardinal Ximenes, in his preface to the edition of the Complutensian Bibles, tells us (

## Inline Structural Marker Candidates

- file: EPUB/ch004.xhtml; text: The neglect of this duty brings inconceivable prejudice unto churches, and if continued in will prove their ruin; for they are not to be preserved, propagated, and continued, at the easy rate of a constant supply by the carnal baptized p...
- file: EPUB/ch006.xhtml; text: Unto the attaining of this wisdom are required, — 1. Fervent prayer for it, James 1:5. 2. Diligent study of the Scripture, to find out and understand the rules given by Christ unto this purpose, Ezra 7:10; 2 Timothy 2:1, 15. 3. Humble wa...
- file: EPUB/ch013.xhtml; text: The whole of what we plead for is here exemplified; as, — [1.] The cause of excommunication, which is a scandalous sin unrepented of. [2.] The preparation for its execution, which is the church's sense of the sin and scandal, with humili...
- file: EPUB/ch027.xhtml; text: (2.) Admit of none unto this sacrament by virtue of their communion with any other church, or any churches not of their own constitution; nor, (3.) Will administer it unto any hut those whom they claim to be their own, as living in their...
- file: EPUB/ch029.xhtml; text: Secondly, If the innocent party upon a divorce be not set at liberty, then, 1. He is deprived of his right by the sin of another; which is against the law of nature; — and so every wicked woman hath it in her power to deprive her husband...
- file: EPUB/ch033.xhtml; text: But I say, — 1. It doth not signify properly "to dip" or "plunge," for that in Greek is ἐμζάπτω and ἐμζαπτίζω . 2. it nowhere signifies "to dip," but as a mode of and in order to washing. 3. It signifies the "dipping" of a finger, or the...
- file: EPUB/ch058.xhtml; text: The industry of learned men of old, and of late Jews and Christians, has been well exercised in the interpretation and reconciliation of them: by one or other a fair and probable account is given of them all. Where we cannot reach the ut...
- file: EPUB/ch063.xhtml; text: Then we have the adjuncts of this vision, which I will but name: — 1. It is certain: "Write it." It is a certain vision. 2. It is evident: "Make it plain upon tables, that he may run that readeth it." 3. It is determined: "The vision is ...

## Suspicious Large-Number Starts

- file: EPUB/ch007.xhtml; text: 124. in Johan.: "Peter the apostle bare, in a general figure, the person of the church; for as unto what belonged unto himself, he was by nature one man, by grace one Christian, and of special, more abounding grace one a
- file: EPUB/ch055.xhtml; text: 14. Let any man consider those two racks of the Rabbins and swords of Judaical unbelief, Isaiah 53 and Daniel 9, as they are now pointed and accented in our Bibles, and compare them with the translation of the LXX, and t
- file: EPUB/ch057.xhtml; text: 22. But this is only to question whether Ezra, Nehemiah, Joshua, Zechariah, Haggai, and the rest of the leaders of the people, on their return from the captivity, did set a sanhedrim, according to the institution of God,

## Roman Heading Candidates

- file: EPUB/ch056.xhtml; text: L. One, none, note, etc. — oe velca. O rotund.

## Overlong Heading Candidates

- file: EPUB/ch024.xhtml; tag: h3; text: QUESTION 1. WHETHER persons who have engaged unto reformation and another way of divine worship, according to the word of God, as they believe, may lawfully go unto and attend on the us of the prayer book in divine worship?

## Short Fragments

- file: EPUB/ch004.xhtml; text: I answer, therefore, —
- file: EPUB/ch013.xhtml; text: I answer, —
- file: EPUB/ch016.xhtml; text: I.
- file: EPUB/ch016.xhtml; text: II.
- file: EPUB/ch021.xhtml; text: I.
- file: EPUB/ch026.xhtml; text: QUESTION 2.
- file: EPUB/ch027.xhtml; text: QUESTION 2.
- file: EPUB/ch044.xhtml; text: So Job 37-39, throughout.
- file: EPUB/ch056.xhtml; text: Double. Diphthongs.
- file: EPUB/ch056.xhtml; text: Shi, di; thy, my.

## Enumerator Sequence Candidates

- file: EPUB/ch011.xhtml; marker: [2.]; family: bracket_decimal; context: [2.] Personal holiness, in gracious moral obedience.
- file: EPUB/ch013.xhtml; marker: (2dly.); family: paren_ordinal; context: unto it for its administration in the name of our Lord Jesus Christ, and with his power; (2dly.) The declarative cause of the equity of this sentence, which was the spirit of the apostle, or the authoritative declaration of his judgment ...

## Repeated Windows

- phrase: the various readings of ben asher and ben naphtali of; count: 4
- phrase: various readings of ben asher and ben naphtali of the; count: 4
- phrase: of ben asher and ben naphtali of the eastern and; count: 4
- phrase: ben asher and ben naphtali of the eastern and western; count: 4
- phrase: asher and ben naphtali of the eastern and western jews; count: 4
- phrase: will say unto me and what shall answer when am; count: 4
- phrase: say unto me and what shall answer when am reproved; count: 4
- phrase: let this mind be in you which was also in; count: 4
- phrase: this mind be in you which was also in christ; count: 4
- phrase: mind be in you which was also in christ jesus; count: 4

## Missing Word Samples

- word: pre; pdf: 5; epub: 0
- word: eminence; pdf: 5; epub: 0

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 1; epub: 10
- word: historical; pdf: 3; epub: 11
- word: modern; pdf: 8; epub: 15
- word: footnotes; pdf: 0; epub: 7

## Untagged Latin Word Samples

- word: nor; epub: 430; tagged: 7
- word: jesus; epub: 166; tagged: 0
- word: yea; epub: 116; tagged: 2
- word: distinct; epub: 101; tagged: 1
- word: whereas; epub: 99; tagged: 2
- word: poor; epub: 98; tagged: 2
- word: thereunto; epub: 93; tagged: 1
- word: whereunto; epub: 65; tagged: 1
- word: prolegomena; epub: 48; tagged: 1
- word: morinus; epub: 50; tagged: 4

## Untranslated Latin Samples

- phrase: Biblia Polyglotta
- phrase: Prolegomena enumerate
- phrase: Arias Montanus
- phrase: Morinus, Junius
- phrase: Elias Levita
- phrase: Arias Montaus
- phrase: in rerum natura
- phrase: undergo; whereas
- phrase: malae fidei
- phrase: nor communicate

## Flat ANALYSIS Chapters

**1 ANALYSIS chapter(s)** appear under-structured — fewer outline markers than expected.  Extraction may have failed to parse the outline.

## Flat Analysis Details

- file: EPUB/ch042.xhtml; paragraph_count: 4; structural_line_count: 2; note: ANALYSIS chapter appears flat — fewer structural outline lines than expected. Check extraction quality.

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
