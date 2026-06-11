# Text Integrity Audit: Volume h3

- Status: **WARN**
- Warnings: 7
- PDF pages: 10
- EPUB text files: 30
- EPUB paragraphs/headings: 4509

## Coverage

- PDF content tokens: 242491
- EPUB content tokens: 452611
- Approximate PDF-to-EPUB coverage ratio: 0.9997
- Pages checked: 9
- Weak page matches: 0
- Dense source windows checked: 0
- Missing dense source-window pages: 0
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 0
- Top-of-page windows skipped as unstable: 0
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 0
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 4370
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 471
- Short fragments: 89
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 17
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 2
- Roman heading candidates: 4
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 672
- EPUB enumerator markers: 1215
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 3772
- EPUB Greek words: 7133
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 1229
- EPUB Hebrew words: 2172
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 165
- Missing Greek clauses: 0
- Hebrew clauses checked: 118
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3601
- EPUB Latin words: 6623
- EPUB Tagged Latin words: 2776
- Latin word coverage ratio: 1.0
- Latin word tagging ratio: 0.4191
- Latin clauses checked: 182
- Missing Latin clauses: 0
- Tagged Latin runs checked: 854
- Translated Latin runs: 87
- Latin translation ratio: 0.1019

## Warnings

- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Possible Paragraph Splits

- file: EPUB/ch002.xhtml; previous: " Mundos," "secula ." לְעָלְמֵא , Syr., "the ages," "times," "worlds." In the remaining words there is no difficulty, as to the grammatical signification; we shall then read them,—; next: Ver. 1, 2.—By sundry parts, and in divers manners, God having formerly [or, of old] spoken unto the fathers in the prophets, hath in these last days spoken unto us in the Son, whom
- file: EPUB/ch002.xhtml; previous: nfounds the שכינה , or 'divine Majesty,' with רוח הקדוש , 'the Holy Ghost,' contradicting the Gemara. The commonly approved order is that of the author of Aruch, in the root כבד :—; next: " ארון כפורת וכרוב אחד ,—'the ark, propitiatory, and cherubim, one.'
- file: EPUB/ch002.xhtml; previous: הנביאים האחרונים חגי זכריה ומלאכי נסתלקה רוח הקודש מישראל ;—'After the death of the latter prophets, Haggai, Zechariah, and Malachi, the Holy Spirit was taken away from Israel.' "; next: It is, then, confessed "that God ceased to speak to the church in prophets, as to their oral teaching and writing, after the days of Malachi; which season of the want of vision, th
- file: EPUB/ch002.xhtml; previous: into their pristine condition. Let us then see what course they do or have taken to countenance themselves in their infidelity. Two ways to relieve themselves they have fixed on:—; next: "1. Granting that the Messiah was to come to their government and worship, they laboured to keep them up, and to restore them being cast down, that so they might prolong their expe
- file: EPUB/ch002.xhtml; previous: unto them whilst they were a state and church, seeing they were so, by their own confession, only for his sake? This puts their later masters to their last miserable shifts; for,—; next: "2. Contrary to the evident nature of all things relating to them from the appropriating of the promise to the family of Abraham, contrary to the whole design of the Scripture, and
- file: EPUB/ch002.xhtml; previous: s whole dominion, seeing the consideration of it will not again so directly occur unto us. That which is the intendment of the words, in the interpretation given of them, is this:—; next: God the Father, in the pursuit of the sovereign purpose of his will, hath granted unto the Son as incarnate, and mediator of the new covenant, according to the eternal counsel betw
- file: EPUB/ch002.xhtml; previous: Both these sorts, or all mankind, is the lordship of Christ extended to, and to each of them respectively:—; next: He is Lord over all flesh, John 17:2; both living and dead, Rom. 14:9; Phil 2:9, 10.
- file: EPUB/ch002.xhtml; previous: ———; next: Δι ʼ οὗ καὶ τοὺς αἰῶνας ἐποίησεν ,—"By whom also he made the worlds."
- file: EPUB/ch002.xhtml; previous: efore mentions light in particular, because of an allusion to the light at first created by God, when of all other things, whereto there is no such allusion, he maketh no mention,"; next: Ans. [1.] The new creation granted by the men of this persuasion being only a moral suasion of the minds of men by the outward doctrine of the gospel, I know not what allusion can
- file: EPUB/ch002.xhtml; previous: ρακτὴρ τῆς ὑποστάσεως αὐτοῦ , φέρων τε τὰ πάντα τῷ ῥήματι τῆς δυνάμεως αὑτοῦ , δι ʼ ἑαυτοῦ καθαρισμὸν ποιησάμενος τῶν ἁμαρτιῶν ἡμῶν , ἐκάθισεν ἐν δεξιᾷ τῆς μεγαλωσύνης ἐν ὑψηλοῖς ‚; next: Δι ʼ ἑαυτοῦ is wanting in MS. T.; but the sense requires the words, and all other ancient copies retain them. Ἡμῶν is wanting in some copies; and one or two for ἐκάθισε have καθίζε

## Inline Structural Marker Candidates

- file: EPUB/ch002.xhtml; text: 1. The ark, with the propitiatory and cherubim; 2. The fire from heaven, which answers the third, or wood of disposition, in the former order; 3. The divine Majesty, in the room of the anointing oil; 4. The Holy Ghost; 5. Urim and Thummi...
- file: EPUB/ch006.xhtml; text: Wherefore he adds, (3.) what is direct to his pretension, "That all the words, or things signified by them, in any testimony, which are firstly spoken of one, and then are, for some of the causes mentioned" (that is, conveniency, similit...
- file: EPUB/ch006.xhtml; text: Concerning this person, or the "Lord," he affirms two things, or attributes two things unto him. 1. The creation of heaven and earth; 2. The abolition or change of them. From that attribution he proceeds to a comparison between him and t...
- file: EPUB/ch009.xhtml; text: Wherefore he adds, (3.) what is direct to his pretension, "That all the words, or things signified by them, in any testimony, which are firstly spoken of one, and then are, for some of the causes mentioned" (that is, conveniency, similit...
- file: EPUB/ch009.xhtml; text: Concerning this person, or the "Lord," he affirms two things, or attributes two things unto him. 1. The creation of heaven and earth; 2. The abolition or change of them. From that attribution he proceeds to a comparison between him and t...
- file: EPUB/ch013.xhtml; text: Εἰ γάρ , "si enim," "etenim," "and if," "for if." Ὁ λόγος λαληθεὶς , " sermo dictus ;" נֶילְתָא דֵּאתְמֵלַלֵת , Syr., " sermo qui dictus est," or "pronuntiatus ," "the word which was spoken or pronounced,"—properly, as we shall see. Δι ʼ...
- file: EPUB/ch013.xhtml; text: The design of the apostle in these three verses is to confirm and enforce the inference and exhortation laid down in the first, as that which arose from the discourses of the former chapter. The way he proceeds in for this end, is by int...
- file: EPUB/ch013.xhtml; text: 1. The subject-matter spoken of,—"so great salvation," 2. A further description of it; (1.) From its principal author,—it "began to be spoken by the Lord;" (2.) From the manner of its propagation,—it "was confirmed unto us by them that h...
- file: EPUB/ch013.xhtml; text: He further describes the gospel, (2.) From the way and means of its conveyance unto us. It was "confirmed unto us by them that heard him." And herein also he prevents an objection that might arise in the minds of the Hebrews, inasmuch as...
- file: EPUB/ch014.xhtml; text: Εἰ γάρ , "si enim," "etenim," "and if," "for if." Ὁ λόγος λαληθεὶς , " sermo dictus ;" נֶילְתָא דֵּאתְמֵלַלֵת , Syr., " sermo qui dictus est," or "pronuntiatus ," "the word which was spoken or pronounced,"—properly, as we shall see. Δι ʼ...

## Suspicious Large-Number Starts

- file: EPUB/ch020.xhtml; text: 49. כי עבד נאמן קראתלו כליל תפארת בראשו נתת בעמדו לפניך על הר סיני ושני לוחוח אבנים הוריד בידו וכתוב בה שמירת שבת ;—"Thou calledst him thy faithful servant; and didst put a glorious crown on his head, when he stood befor
- file: EPUB/ch022.xhtml; text: 49. כי עבד נאמן קראתלו כליל תפארת בראשו נתת בעמדו לפניך על הר סיני ושני לוחוח אבנים הוריד בידו וכתוב בה שמירת שבת ;—"Thou calledst him thy faithful servant; and didst put a glorious crown on his head, when he stood befor

## Roman Heading Candidates

- file: EPUB/ch014.xhtml; text: I. ii. 28,—
- file: EPUB/ch015.xhtml; text: I. ii. 28,—
- file: EPUB/ch016.xhtml; text: II. The Lord Christ suffered under all his temptations, sinned in none.
- file: EPUB/ch020.xhtml; text: II. The Lord Christ suffered under all his temptations, sinned in none.

## Short Fragments

- file: EPUB/ch002.xhtml; text: And the first is this,—
- file: EPUB/ch002.xhtml; text: Κεκληρονόμηκε .
- file: EPUB/ch004.xhtml; text: Κεκληρονόμηκε .
- file: EPUB/ch006.xhtml; text: The sum of all is, that,—
- file: EPUB/ch006.xhtml; text: Use the world, but live on Christ.
- file: EPUB/ch009.xhtml; text: The sum of all is, that,—
- file: EPUB/ch009.xhtml; text: Use the world, but live on Christ.
- file: EPUB/ch009.xhtml; text: Λειτουργικά .
- file: EPUB/ch009.xhtml; text: Εἰς διακονίαν ἀποστελλόμενα .
- file: EPUB/ch009.xhtml; text: 8.

## Repeated Windows

- phrase: for whom are all things and by whom are all; count: 17
- phrase: whom are all things and by whom are all things; count: 17
- phrase: the brightness of his glory and the express image of; count: 14
- phrase: brightness of his glory and the express image of his; count: 14
- phrase: of his glory and the express image of his person; count: 14
- phrase: unto which of the angels said he at any time; count: 13
- phrase: will be to him father and he shall be to; count: 8
- phrase: be to him father and he shall be to me; count: 8
- phrase: to him father and he shall be to me son; count: 8
- phrase: down at the right hand of the majesty on high; count: 6

## Missing Word Samples

- word: διʼ; pdf: 40; epub: 0
- word: επʼ; pdf: 11; epub: 0
- word: παρʼ; pdf: 8; epub: 0
- word: κατʼ; pdf: 7; epub: 0

## Excess Word Samples

- word: the; pdf: 20888; epub: 38596
- word: of; pdf: 14560; epub: 26992
- word: and; pdf: 11646; epub: 21755
- word: in; pdf: 7137; epub: 13285
- word: to; pdf: 5936; epub: 10996
- word: is; pdf: 5696; epub: 10745
- word: it; pdf: 4092; epub: 7746
- word: his; pdf: 4168; epub: 7767
- word: he; pdf: 4051; epub: 7530
- word: be; pdf: 2728; epub: 5164

## Untagged Latin Word Samples

- word: cor; epub: 350; tagged: 0
- word: isa; epub: 225; tagged: 3
- word: mediator; epub: 141; tagged: 0
- word: abraham; epub: 128; tagged: 0
- word: elsewhere; epub: 111; tagged: 2
- word: immediate; epub: 100; tagged: 0
- word: poor; epub: 93; tagged: 0
- word: mere; epub: 77; tagged: 0
- word: adam; epub: 69; tagged: 0
- word: nowhere; epub: 60; tagged: 2

## Untranslated Latin Samples

- phrase: Multis vicibus," Beza
- phrase: is "sortior," "divido
- phrase: alternis vicibus
- phrase: is "Olim," "quondam," "pridem," "jamdudum
- phrase: Ultimis diebus
- phrase: ultimis diebus istis
- phrase: diebus istis
- phrase: in extremo dierum istorum
- phrase: Mundos," "secula
- phrase: Rabbi Bechai

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
