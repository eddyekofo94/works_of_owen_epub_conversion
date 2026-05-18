# Text Integrity Audit: Volume 4

- Status: **WARN**
- Warnings: 13
- PDF pages: 653
- EPUB text files: 71
- EPUB paragraphs/headings: 2410

## Coverage

- PDF content tokens: 222359
- EPUB content tokens: 222838
- Approximate PDF-to-EPUB coverage ratio: 0.9951
- Pages checked: 644
- Weak page matches: 34
- Dense source windows checked: 777
- Missing dense source-window pages: 627
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 624
- Top-of-page windows skipped as unstable: 29
- Missing top-of-page body windows: 2
- Bottom-of-page body windows checked: 607
- Bottom-of-page windows skipped as unstable: 17
- Missing bottom-of-page body windows: 3

## Paragraphs

- Body paragraphs checked: 2177
- Possible faulty paragraph splits: 22
- Structural starts excluded from split warnings: 408
- Short fragments: 24
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 2
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 30
- Overlong heading candidates: 1
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 416
- EPUB enumerator markers: 375
- Missing enumerator marker forms: 3
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 786
- EPUB Greek words: 779
- Greek word coverage ratio: 0.9817
- PDF Hebrew words: 111
- EPUB Hebrew words: 109
- Hebrew word coverage ratio: 0.3303
- Greek clauses checked: 42
- Missing Greek clauses: 42
- Hebrew clauses checked: 17
- Missing Hebrew clauses: 17

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_hebrew_word_coverage`: EPUB Hebrew word coverage against PDF extraction is lower than expected
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB
- `missing_hebrew_clauses`: Some dense Hebrew passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 3; sample: contents πηευματολογια or discourse concerning the holy spirit continued book vi part the reason
- page: 10; sample: 10 fanatical excesses which they sought to rebuke they stated the question in such
- page: 11; sample: 11 itself substantiates such claim in his behalf it is the first recognition of
- page: 12; sample: 12 preface having added brief account of the design order and method of the
- page: 13; sample: 13 the consciences of men immediately and the way whereby they may come to
- page: 15; sample: 15 the reason of faith or the grounds whereon the scripture is believed to
- page: 16; sample: 16 first supernatural revelation is the only objective cause and means of supernatural illumination
- page: 17; sample: 17 that it did sufficiently evidence itself to be from god unto the minds
- page: 18; sample: 18 of his will πολυμερως by sundry parts and degrees yet so that every
- page: 19; sample: 19 before the call of moses during which time all things went into darkness

## Missing Top-Of-Page Body Windows

- page: 16; sample: First, Supernatural revelation is the only objective cause and means of supernatural illumination. These things are commensurate. There is a
- page: 35; sample: wisdom before all the world, Deuteronomy 4:6-8. Now, we shall not need to consider what were the first attempts of other nations in

## Missing Bottom-Of-Page Body Windows

- page: 15; sample: declaration we at present design, reserving the latter unto a distinct discourse by itself also. Unto the former some things may be premised: —
- page: 44; sample: testimony may rationally be supposed to be so far influenced by self- interest as to be of little validity.
- page: 367; sample: matter of it, namely, "mercy" and "grace," and by the only object of it, "God on a throne of grace."

## Possible Paragraph Splits

- file: EPUB/ch006.xhtml; previous: THE principal design of that discourse whereof the ensuing treatise is a; next: part, is to declare the work of the Holy Ghost in the illumination of the
- file: EPUB/ch006.xhtml; previous: part, is to declare the work of the Holy Ghost in the illumination of the; next: minds of men, — for this work is particularly and eminently ascribed unto
- file: EPUB/ch006.xhtml; previous: minds of men, — for this work is particularly and eminently ascribed unto; next: him, — or the efficacy of the grace of God by him dispensed, Ephesians
- file: EPUB/ch006.xhtml; previous: him, — or the efficacy of the grace of God by him dispensed, Ephesians; next: 1:17,18; Hebrews 6:4; Luke 2:32; Acts 13:47, 16:14, 26:18; 2
- file: EPUB/ch006.xhtml; previous: 1:17,18; Hebrews 6:4; Luke 2:32; Acts 13:47, 16:14, 26:18; 2; next: Corinthians 4:4; 1 Peter 2:9. The objective cause and outward means of
- file: EPUB/ch006.xhtml; previous: Corinthians 4:4; 1 Peter 2:9. The objective cause and outward means of; next: it are the subjects at present designed unto consideration; and it will issue
- file: EPUB/ch006.xhtml; previous: it are the subjects at present designed unto consideration; and it will issue; next: in these two inquiries: —
- file: EPUB/ch006.xhtml; previous: in these two inquiries: —; next: the word of God with faith divine and supernatural, as it is required of us
- file: EPUB/ch006.xhtml; previous: the word of God with faith divine and supernatural, as it is required of us; next: in a way of duty?
- file: EPUB/ch006.xhtml; previous: God in the Scripture, or the revelations that are made unto us of his mind; next: and will therein?

## Inline Structural Marker Candidates

- file: EPUB/ch024.xhtml; text: 1. Spiritual; 2. Disciplinary; 3. Ecclesiastical. Some instances on each head will farther clear what I intend.
- file: EPUB/ch034.xhtml; text: 1. We know not our own wants; 2. We know not the plies of them that are expressed in the promises of God; and, 3. We know not the end whereunto what we pray for is to be directed, which I add unto the former. Without the knowledge and un...

## Roman Heading Candidates

- file: EPUB/ch007.xhtml; text: II. That there are external arguments of the divine original of the Scripture, which are effectual motives to persuade us to give an unfeigned assent thereunto:
- file: EPUB/ch007.xhtml; text: III. That yet, moreover, God requires of us that we believe them to be his word with faith divine, supernatural, and infallible:
- file: EPUB/ch007.xhtml; text: IV. Evidence the grounds and reasons whereon we do so believe, and ought so to do.
- file: EPUB/ch013.xhtml; text: II. This being the substance of what is declared and pleaded for in the preceding treatise, to prevent the obloquy of some and confirm the judgment of others, I shall add the suffrage of ancient and modern writers given
- file: EPUB/ch016.xhtml; text: I. The Holy, Spirit is represented as the EFFICIENT CAUSE, and an inquiry follows: —
- file: EPUB/ch018.xhtml; text: II. That as to the right understanding of the mind of God in the Scripture, or our coming unto the riches of the full assurance of understanding in the acknowledgment of the mystery of God, we do not, nor need to depend
- file: EPUB/ch018.xhtml; text: III. That in the mere exercise of our own natural reason and understanding, with the help of external means, we cannot attain that knowledge of the mind and wfil of God in the Scripture, of the sense and meaning of the H
- file: EPUB/ch018.xhtml; text: V. That hereby alone is that full assurance of understanding in the knowledge of the mystery of God, his truth and grace, to be obtained, whereby any man may answer the mind and will of God, or comply with his own duty i
- file: EPUB/ch018.xhtml; text: VII. That whereas the means of the right interpretation of the Scripture, and understanding of the mind of God therein, are of two sorts, — first, such as are prescribed unto us in a way of duty, as prayer, meditation on
- file: EPUB/ch024.xhtml; text: II. The means designed for the improvement hereof, or our profitable use of it, are of three sorts: —

## Overlong Heading Candidates

- file: EPUB/ch047.xhtml; tag: h3; text: The Holy Ghost the comforter of the church by way of office — How he is the church's advocate — John 14:16; 1 John 2:1, 2; John 16:8-11 opened.

## Short Fragments

- file: EPUB/ch001.xhtml; text: Appendix.
- file: EPUB/ch005.xhtml; text: May 11, 1677.
- file: EPUB/ch006.xhtml; text: in these two inquiries: —
- file: EPUB/ch006.xhtml; text: in a way of duty?
- file: EPUB/ch006.xhtml; text: and will therein?
- file: EPUB/ch013.xhtml; text: Wherefore, —
- file: EPUB/ch016.xhtml; text: — ED.
- file: EPUB/ch018.xhtml; text: ΣΨΝΕΣΙΣ ΠΝΕΨΜΑΤΙΚΗ .
- file: EPUB/ch034.xhtml; text: For, —
- file: EPUB/ch035.xhtml; text: I answer, —

## Missing Enumerator Markers

- marker: [1st.]; pdf: 2; epub: 0; examples: [{'location': 'pdf:p212', 'context': 's of their minds, which hinder them from receiving instruction." But ff it be so, then, — [1st.] It is supposed that man also in their teachings can give us an understanding as well as the Son of God...
- marker: [2dly.]; pdf: 1; epub: 0; examples: [{'location': 'pdf:p212', 'context': 'learn, and have no darling lusts or vicious habits of mind to hinder them from learning. [2dly.] Seeing he hath taken this work on himself, and designs its accomplishment, cannot the Son of God by hi...
- marker: [3dly.]; pdf: 1; epub: 0; examples: [{'location': 'pdf:p214', 'context': 'and condition with the conceptions of every one that will pretend unto this inspiration. [3dly.] The pretense visibly confutes itself in the manifold mutual contradictions of them that pretend unto i...

## Repeated Windows

- phrase: we believe the scripture to be the word of god; count: 21
- phrase: to believe the scripture to be the word of god; count: 17
- phrase: the mind and will of god as revealed in the; count: 11
- phrase: believe the scripture to be the word of god with; count: 9
- phrase: to be the word of god with faith divine and; count: 8
- phrase: be the word of god with faith divine and supernatural; count: 7
- phrase: mind and will of god as revealed in the scripture; count: 7
- phrase: of the holy spirit in the illumination of our minds; count: 6
- phrase: the right understanding of the mind of god in the; count: 6
- phrase: believe the scripture to be the word of god in; count: 6

## Missing Word Samples

- word: 1st; pdf: 27; epub: 9
- word: 2dly; pdf: 27; epub: 10
- word: עןףְלָאוֹט; pdf: 5; epub: 0
- word: self; pdf: 7; epub: 3
- word: 14-17; pdf: 4; epub: 0
- word: חָ־ןִ; pdf: 3; epub: 0
- word: ־טחֲןוּעןים; pdf: 3; epub: 0
- word: 10-12; pdf: 3; epub: 1
- word: ; pdf: 3; epub: 1
- word: 16-18; pdf: 3; epub: 1

## Excess Word Samples

- word: psalms; pdf: 7; epub: 37
- word: dly; pdf: 0; epub: 23
- word: st; pdf: 2; epub: 20

## Missing Hebrew Word Samples

- word: עןףְלָאוֹט; pdf: 5; epub: 0
- word: חָ־ןִ; pdf: 3; epub: 0
- word: ־טחֲןוּעןים; pdf: 3; epub: 0
- word: ־נלאעעי־ןי; pdf: 2; epub: 0
- word: תוֹרָה; pdf: 2; epub: 0
- word: עחִ; pdf: 2; epub: 0
- word: ־םתָןוֹט; pdf: 2; epub: 0

## Missing Greek Clauses

- page: 107; word_count: 8; sample: τὸ γνωστὸν τοῦ θεοῦ φανερόν ἐστιν ἐν αὐτοῖς
- page: 141; word_count: 26; sample: εχομεν γὰρ τὴν ἀρχὴν τῆς διδασκαλίας τὸν κύριον διά τε τῶν προφητῶν
- page: 141; word_count: 9; sample: εἴτις ἐτέρου δεῖσθαι ὑπολάζοι οὐκέτ ἄν ὄντως ἀρχὴ φυλαχθείη
- page: 141; word_count: 46; sample: μὲν οῦν ἐξ ἑαυτοῦ πιστὸς τῇ κυριακῇ γραφῇ τε καὶ φωνῇ ἀξιόπιστος
- page: 142; word_count: 41; sample: εἰκότως τοίνυν πίστει περιλαζόντες ἀναπόδεικτον τὴν ἀρχὴν ἐκ περιουσίας καὶ τὰς ἀποδείξεις
- page: 142; word_count: 26; sample: οὐκ ἀρκεῖ μόνον ἁπλῶς εἰπεῖν τὸ δόξαν ἀλλὰ πιστώσασθαι δεῖ τὸ λεχθὲν
- page: 142; word_count: 20; sample: μόνη ἀπόδειξις οῦσα τυγχάνει οὕτως οῦν καὶ ἡμεῖς ἀπ αὐτῶν περὶ αὐτῶν
- page: 143; word_count: 11; sample: ὑπὲρ τὰς λογικὰς μεθάδους τὴν ψυχὴν εἰς συγκατάθεσιν ἕλκουσα πίστις οὐκ
- page: 143; word_count: 5; sample: ταῖς τοῦ πνεύματος ἐνεργείαις ἐγγινομένη
- page: 143; word_count: 13; sample: τῶν ζείων λογίων διδασκαλία τὸ πιστὸν ἀφ ἑαυτῆς ἔχουσα διὰ τὸ ζεόπνευστον

## Missing Hebrew Clauses

- page: 16; word_count: 3; sample: ־נלאעעי־ןי באףא גליטא
- page: 23; word_count: 3; sample: עפ־טחאדְּבָ ריו יָעאיר
- page: 28; word_count: 5; sample: ־האֲעםיןוּ ־בּיהוָֹה ־אלֹעהי ךם וְעטאָעםןוּ
- page: 166; word_count: 9; sample: ־נלאעעי־ןי וְ־אבּיטָה עןףְלָאוֹט עםתוֹרָ טו תוֹרָה כְטוּעבים תוֹרָה ןְעבעאים
- page: 167; word_count: 7; sample: עןףְלָאוֹט פָלָא עןףְלָאוֹט עךי עיפָעלא עםמְו דָבָר
- page: 167; word_count: 6; sample: לא רעבּו תוֹרָעטי כְםוֹ זָר עןףְלָאוֹט
- page: 171; word_count: 7; sample: ־ה וֹט ־ה וֹט וְ־ה־מע ךָה ־הנְסוּךָה
- page: 265; word_count: 4; sample: דְּבְערי ־א םט ךָטוּב
- page: 269; word_count: 3; sample: עס ףר יְהֹוָה
- page: 325; word_count: 4; sample: רוּ־ח עח עחִ חָ־ןִ

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
