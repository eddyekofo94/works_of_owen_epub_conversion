# Text Integrity Audit: Volume 1

- Status: **WARN**
- Warnings: 10
- PDF pages: 633
- EPUB text files: 84
- EPUB paragraphs/headings: 2706

## Coverage

- PDF content tokens: 204998
- EPUB content tokens: 205862
- Approximate PDF-to-EPUB coverage ratio: 0.9992
- Pages checked: 622
- Weak page matches: 4
- Dense source windows checked: 27185
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 4
- Top-of-page body windows checked: 586
- Top-of-page windows skipped as unstable: 13
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 534
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 2

## Paragraphs

- Body paragraphs checked: 2255
- Possible faulty paragraph splits: 19
- Structural starts excluded from split warnings: 116
- Short fragments: 11
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 5
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 310
- EPUB enumerator markers: 320
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 812
- EPUB Greek words: 811
- Greek word coverage ratio: 0.9987
- PDF Hebrew words: 20
- EPUB Hebrew words: 20
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 38
- Missing Greek clauses: 0
- Hebrew clauses checked: 1
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3418
- EPUB Latin words: 3459
- EPUB Tagged Latin words: 1154
- Latin word coverage ratio: 0.9974
- Latin word tagging ratio: 0.3336
- Latin clauses checked: 149
- Missing Latin clauses: 0
- Tagged Latin runs checked: 290
- Translated Latin runs: 160
- Latin translation ratio: 0.5517

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ
- page: 4; sample: person of christ which is love its truth and reality vindicated chapter the nature
- page: 5; sample: the accomplishment of the work of mediation in this world representations of the glory
- page: 6; sample: of the holy trinity of the works of god and first of those that
- page: 8; sample: man to himself with peculiar closeness of application stripping in of his false dependencies
- page: 9; sample: embraces the most comprehensive view of this vitally-important subject his exposition of psalm exhibits
- page: 10; sample: as his own john nesbitt matthew clarke thomas ridgley and thomas bradbury eminent independent
- page: 11; sample: whose literary industry the church of christ had been se largely indebted it would
- page: 20; sample: prefatory note to object of dr owen in this treatise is to illustrate the
- page: 21; sample: events ensued which justified these apprehensions of own prolonged controversy on the subject of

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.0; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ prefatory note preface chapter peter's confession matthew conceits of the papists thereon the substance
- page: 4; hit_ratio: 0.5; sample: chapter the especial principle of obedience unto the person of christ which is love its truth and reality vindicated chapter the nature operations and causes of divine love
- page: 5; hit_ratio: 0.5; sample: the glory of christ in his exaltation after the accomplishment of the work of mediation in this world representations of the glory of christ under the old testament
- page: 6; hit_ratio: 0.25; sample: of the holy trinity of the works of god and first of those that are internal and immanent of the works of god that outwardly are of him

## Missing Bottom-Of-Page Body Windows

- page: 26; sample: oijkodomh>sw mou th<n ejhkklhsi>an, kai< pu>lai a[|dou ouj katiscu>sousin aujth~v".
- page: 293; sample: of God. Such are "ejnsa>rkwsiv", "incarnation;" "ejnswma>twsiv", "embodying," "ejnanqrw>phsiv", "inhumanation;" "hJ despotikh<

## Possible Paragraph Splits

- file: EPUB/ch004.xhtml; previous: καὶ θεοφιλῶν ἀνδρῶν μετεωριζομένη — διὰ μίαν ἐκείνην , ἥν αὐτὸς ἀπεφήνατο λέξιν , εἴπων , Επὶ τὴν πέτραν οἰκοδομήσω μου τὴν ἐηκκλησίαν , καὶ πύλαι ᾅδου οὐ κατισχύσουσιν αὐτῆς ". †; next: He proves the verity of divine predictions from the glorious accomplishment of that word, and the promise of our Savior, that he would build his church on the rock, (that is, himse
- file: EPUB/ch004.xhtml; previous: enim erat Christus, super quod fundamentum etiam ipse aedificatus est Petrus. Fundamentum quippe aliud nemo potest ponere, praeter id quod positum est, quod est Jesus Christus ". †; next: — "He (Christ) meant the universal church, which in this world is shaken with divers temptations, as with showers, floods, and tempests, yet falleth not, because it is built on the
- file: EPUB/ch004.xhtml; previous: tertium coelu, ineffabilia dicit, quomodo nos exprimere possumus paternae generationis arcanum, quod nec sentire potuimus nec audire? Quid te ista questionum tormenta delectant?" †; next: — "I inquire of you when and how the Son was begotten? Impossible it is to me to know the mystery of this generation. My mind faileth, my voice is silent — and not only mine, but o
- file: EPUB/ch004.xhtml; previous: αὴς ἥλιος σὺν ἀνθρώποις ἐπὶ γῆς πολιτευοίτο , οὐδένα τῶν ἑπὶ τῆς γῆς μείναι ἆν ἀδιάφορον , πάντων συλλήβδην ἐμψύχων ὁμοῦ καὶ ἀψύχων ἀθρόᾳ τῃ τοῦ φωτὸς προσβολῇ διαφθαρησομένων ". †; next: The sense of which words, with some that follow in the same place, is unto this purpose: By the beams of the sunlight, and life, and heat, unto the procreation, sustentation, refre
- file: EPUB/ch004.xhtml; previous: veniret utriusque diversitas, ut unus idemque sit filius, qui se, et secundum quod verus est homo, Patre dicit minorem, et secundum quod verus est Deus Patrise profitetur aequalem"; next: — "Human nature is assumed into the society of the Creator, not that he should be the inhabitant, and that the habitation," (that is, by an inhabitation in the effects of his power
- file: EPUB/ch004.xhtml; previous: ν ἠδυνήθη μετασχεῖν τῆς ἀφθαρσίας . Εδει γὰρ τὸν μεσίτην τοῦ Θεοῦ τε καὶ ἀνθρώπων , διὰ τῆς ἰδίας πρὸς ἑκατέρους οἰκειότητος εις φιλίαν καὶ ὁμόνοιαν τοῦς ἀμφοτέρους συναγαγεῖν ". †; next: Words plainly divine; an illustrious testimony of the faith of the ancient church, and expressive of the principal mystery of the gospel! "Wherefore, as we said before, he united m
- file: EPUB/ch004.xhtml; previous: And to the same purpose: (lib. 5 cap. 1:) "Neque enim vere esset sanguinem et carnem habens, per quam nos redemit, nisi antiquam plasmationem Adae in seipsum recapitulasset". †; next: That which these passages give testimony unto, is what we have discoursed concerning the necessity of our redemption in and by the nature that sinned; and yet withal, that it shoul
- file: EPUB/ch004.xhtml; previous: , non aeriae, non alterius cujusquam putes esse naturae, sed ejus coujus est omnium caro; id est, quam ipse Deus, homini primo de terra plasmavit, et caeteris hominibus plasmat." †; next: — "So believe Christ the Son of God, that is, one person of the Trinity, to be the true God, that you doubt not but that his divinity was born" (thy eternal generation) "of the nat
- file: EPUB/ch004.xhtml; previous: ccato ceciderat. Utraque operatus est filius Verbum Dei existens, a Patre descendens et incarnatus, et usque ad mortem descendens, et dispensationem consummans salutis nostrae ". †; next: — "Being the Son of God always with the Father, and being made man, he reconciled or gathered up in himself the long-continued exposing of men," (unto sin and judgment,) "bringing
- file: EPUB/ch004.xhtml; previous: tantum ; at qui erat in divinitate Dei Patris Filius , ipse fieret in homine hominis matris Filius; ne Filii nomen ad alterum transiret, qui non esset eterna nativitate filius ". †; next: — "The Father did not assume flesh, nor the Holy Spirit, but the Son only; that he who in the Deity was the Son of the Father, should be made the Son of man, in his mother of human

## Inline Structural Marker Candidates

- file: EPUB/ch013.xhtml; text: In the confirmation hereof it will appear what judgment ought to be passed on that inquiry — which, after the uninterrupted profession of the catholic church for so many ages of a faith unto the contrary, is begun to be made by some amon...
- file: EPUB/ch031.xhtml; text: That which we inquire after at present, is, the glory of Christ herein, and how we may behold that glory. And there are three things wherein we may take a prospect of it. 1. In his susception of this office. 2. In his discharge of it. 3....
- file: EPUB/ch031.xhtml; text: In the susception of this office we may behold the glory of Christ, — I. In his condescension; II. In his love.
- file: EPUB/ch040.xhtml; text: Two things we must here speak unto. 1. Why does the Lord Christ, at any time, thus hide himself in his glory from the faith of believers, that they cannot behold him? 2. How we may perceive and know that he does so withdraw himself from ...
- file: EPUB/ch045.xhtml; text: The second thing proposed is, that notwithstanding all this provision for the growth of spiritual life in us, believers, especially in a long course of profession, are subject to decays, such as may cast them into great perplexities, and...

## Roman Heading Candidates

- file: EPUB/ch033.xhtml; text: I. 1. What he did, what obedience he yielded unto the law of God in the discharge of his office (with respect whereunto he said, "Lo, I come to do thy will, O God; yea, thy law is in my heart"), it was all on his own fre

## Short Fragments

- file: EPUB/ch001.xhtml; text: Edinburgh, August 1850
- file: EPUB/ch009.xhtml; text: All this himself instructs us in.
- file: EPUB/ch011.xhtml; text: This must be declared.
- file: EPUB/ch027.xhtml; text: Christian Reader,
- file: EPUB/ch035.xhtml; text: The sum is,
- file: EPUB/ch037.xhtml; text: And, —
- file: EPUB/ch041.xhtml; text: END.
- file: EPUB/ch042.xhtml; text: To The Reader
- file: EPUB/ch045.xhtml; text: END OF PART 2.
- file: EPUB/ch048.xhtml; text: J.O.

## Repeated Windows

- phrase: the glory of god in the face of jesus christ; count: 12
- phrase: unto us child is born unto us son is given; count: 6
- phrase: of the glory of god in the face of jesus; count: 6
- phrase: us child is born unto us son is given and; count: 5
- phrase: the brightness of his glory and the express image of; count: 5
- phrase: brightness of his glory and the express image of his; count: 5
- phrase: of his glory and the express image of his person; count: 5
- phrase: are changed into the same image from glory to glory; count: 5
- phrase: both which are in heaven and which are on earth; count: 5
- phrase: the only-begotten son who is in the bosom of the; count: 5

## Missing Word Samples

- word: faithfullness; pdf: 7; epub: 0
- word: pre; pdf: 6; epub: 2
- word: eminence; pdf: 5; epub: 1
- word: mindedness; pdf: 3; epub: 0

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 2; epub: 11
- word: historical; pdf: 2; epub: 10
- word: faithfulness; pdf: 5; epub: 12
- word: modern; pdf: 4; epub: 11
- word: footnotes; pdf: 0; epub: 7
- word: hebrew; pdf: 3; epub: 9

## Untagged Latin Word Samples

- word: nor; epub: 352; tagged: 5
- word: jesus; epub: 254; tagged: 7
- word: yea; epub: 97; tagged: 1
- word: immediate; epub: 97; tagged: 2
- word: distinct; epub: 86; tagged: 1
- word: thereunto; epub: 73; tagged: 3
- word: mere; epub: 66; tagged: 0
- word: hereunto; epub: 63; tagged: 2
- word: whereas; epub: 60; tagged: 0
- word: adam; epub: 52; tagged: 3

## Untranslated Latin Samples

- phrase: bias — in an inveterate
- phrase: quarto (Amsterdam
- phrase: Clarae, Thomas
- phrase: operis absentibus
- phrase: Salus Electorum Sauguis
- phrase: quam conspici
- phrase: contemplate a separate
- phrase: Quod si super unum illum Petrum tantum
- phrase: totam eclesiam
- phrase: quid dicturus

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
