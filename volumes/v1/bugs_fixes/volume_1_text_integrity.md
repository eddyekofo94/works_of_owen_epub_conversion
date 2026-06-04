# Text Integrity Audit: Volume 1

- Status: **WARN**
- Warnings: 11
- PDF pages: 633
- EPUB text files: 84
- EPUB paragraphs/headings: 2703

## Coverage

- PDF content tokens: 204998
- EPUB content tokens: 205763
- Approximate PDF-to-EPUB coverage ratio: 0.9992
- Pages checked: 622
- Weak page matches: 4
- Dense source windows checked: 27225
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
- Structural starts excluded from split warnings: 117
- Short fragments: 11
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 15
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 310
- EPUB enumerator markers: 467
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 88

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
- EPUB Latin words: 3457
- EPUB Tagged Latin words: 0
- Latin word coverage ratio: 0.9971
- Latin word tagging ratio: 0.0
- Latin clauses checked: 149
- Missing Latin clauses: 1
- Tagged Latin runs checked: 0
- Translated Latin runs: 0
- Latin translation ratio: 1.0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 3; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ
- page: 4; sample: person of christ which is love its truth and reality vindicated chapter the nature
- page: 5; sample: the accomplishment of the work of mediation in this world representations of the glory
- page: 6; sample: of the holy trinity of the works of god and first of those that
- page: 9; sample: embraces the most comprehensive view of this vitally-important subject his exposition of psalm exhibits
- page: 11; sample: whose literary industry the church of christ had been se largely indebted it would
- page: 20; sample: prefatory note to object of dr owen in this treatise is to illustrate the
- page: 21; sample: events ensued which justified these apprehensions of own prolonged controversy on the subject of
- page: 26; sample: the shepherd wherein he has respect unto this testimony and origin expressly denies the
- page: 27; sample: inquit petram quam confessus es aedificabo eccleaism meam petra enim erat christus super quod

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.0; sample: contents of χριστολογια or declaration of the glorious mystery of the person of christ prefatory note preface chapter peter's confession matthew conceits of the papists thereon the substance
- page: 4; hit_ratio: 0.5; sample: chapter the especial principle of obedience unto the person of christ which is love its truth and reality vindicated chapter the nature operations and causes of divine love
- page: 5; hit_ratio: 0.5; sample: the glory of christ in his exaltation after the accomplishment of the work of mediation in this world representations of the glory of christ under the old testament
- page: 6; hit_ratio: 0.25; sample: of the holy trinity of the works of god and first of those that are internal and immanent of the works of god that outwardly are of him

## Missing Bottom-Of-Page Body Windows

- page: 26; sample: oijkodomh>sw mou th<n ejhkklhsi>an, kai< pu>lai a[|dou ouj katiscu>sousin aujth~v".
- page: 293; sample: of God. Such are "ejnsa>rkwsiv", "incarnation;" "ejnswma>twsiv", "embodying," "ejnanqrw>phsiv", "inhumanation;" "hJ despotikh<

## Possible Paragraph Splits

- file: EPUB/ch004.xhtml; previous: nim erat Christus, super quod fundamentum etiam ipse aedificatus est Petrus. Fundamentum quippe aliud nemo potest ponere, praeter id quod positum est, quod est Jesus Christus". [1]; next: — "He (Christ) meant the universal church, which in this world is shaken with divers temptations, as with showers, floods, and tempests, yet falleth not, because it is built on the
- file: EPUB/ch004.xhtml; previous: rtium coelu, ineffabilia dicit, quomodo nos exprimere possumus paternae generationis arcanum, quod nec sentire potuimus nec audire? Quid te ista questionum tormenta delectant?" [2]; next: — "I inquire of you when and how the Son was begotten? Impossible it is to me to know the mystery of this generation. My mind faileth, my voice is silent — and not only mine, but o
- file: EPUB/ch004.xhtml; previous: To the same purpose. speaks Eusebius at large: Demonstratio Evang., lib. 5 cap. 2. [47]; next: Leo well adds hereunto the consideration of his incarnation, in these excellent words: (Serm. 9, De Nativit.:) [73] "Quia in Christo Jesus Filio Dei non solum ad divinam essentiam,
- file: EPUB/ch004.xhtml; previous: veniret utriusque diversitas, ut unus idemque sit filius, qui se, et secundum quod verus est homo, Patre dicit minorem, et secundum quod verus est Deus Patrise profitetur aequalem"; next: — "Human nature is assumed into the society of the Creator, not that he should be the inhabitant, and that the habitation," (that is, by an inhabitation in the effects of his power
- file: EPUB/ch004.xhtml; previous: image of God, even the Father, who by him is represented unto us. See the same book, chap. 7, to the same purpose; also, De Ecclesiast. Theol. contra Marcell., lib. 2 cap. 17. [27]; next: Clemens abounds much in the affirmation of this truth concerning the person of Christ, and we may yet add, from a multitude to the same purpose, one or more testimonies from him. T
- file: EPUB/ch004.xhtml; previous: to the same purpose: (lib. 5 cap. 1:) [90] "Neque enim vere esset sanguinem et carnem habens, per quam nos redemit, nisi antiquam plasmationem Adae in seipsum recapitulasset". [12]; next: That which these passages give testimony unto, is what we have discoursed concerning the necessity of our redemption in and by the nature that sinned; and yet withal, that it shoul
- file: EPUB/ch004.xhtml; previous: non aeriae, non alterius cujusquam putes esse naturae, sed ejus coujus est omnium caro; id est, quam ipse Deus, homini primo de terra plasmavit, et caeteris hominibus plasmat." [4]; next: — "So believe Christ the Son of God, that is, one person of the Trinity, to be the true God, that you doubt not but that his divinity was born" (thy eternal generation) "of the nat
- file: EPUB/ch004.xhtml; previous: tantum; at qui erat in divinitate Dei Patris Filius, ipse fieret in homine hominis matris Filius; ne Filii nomen ad alterum transiret, qui non esset eterna nativitate filius". [6]; next: — "The Father did not assume flesh, nor the Holy Spirit, but the Son only; that he who in the Deity was the Son of the Father, should be made the Son of man, in his mother of human
- file: EPUB/ch004.xhtml; previous: amnatione justissima derelictis, ostenderetur, quod meruisset universa conspersio, et quo etiam istos debitum judicium Dei duceret, nisi ejus indebita misericordia subveniret." [3]; next: — "Behold, the whole race of mankind, by the just judgment of God, so condemned in the apostatical root, that if no one were thence delivered, yet no man could rightly complain of
- file: EPUB/ch009.xhtml; previous: affirm] we know not; only we declare what we believe and adore. "Neque sensus est ejus, neque phantsia, neque opinio, nec ratio, nec scientia", says Dionys. De Divan. Nomine,1. [1]; next: We have no means — no corporeal, no intellectual instrument or power — for the comprehension of him; nor has any other creature: " Επεὶ αὐτὸ ὅπε ? ρ ἐστιν ὁ Θεὸς , οὐ μόνον προφῆτα

## Inline Structural Marker Candidates

- file: EPUB/ch001.xhtml; text: They have repeatedly appeared in the language of Holland; and by the Dutch divines the most favorable mention is made of the various treatises of our pious and learned Puritan. We are informed by Dr Steven, 2 that his Exposition of the E...
- file: EPUB/ch004.xhtml; text: We may take an instance hereof with respect unto the Nestorian heresy, condemned in the first Ephesian Council, and afterwards in that at Chalcedon. Cyril of Alexandria, a man learned and vehement, designed by all means to be unto it wha...
- file: EPUB/ch004.xhtml; text: As he is in his divine person his eternal, essential image; so, in his incarnation, as the teacher of men, he is the representative image of God unto the church, as is afterwards declared. So also Jerome expresseth his mind herein: (Comm...
- file: EPUB/ch004.xhtml; text: Clemens abounds much in the affirmation of this truth concerning the person of Christ, and we may yet add, from a multitude to the same purpose, one or more testimonies from him. Treating of Christ as the teacher of all men, his " παιδαγ...
- file: EPUB/ch004.xhtml; text: Herein we consider the incarnation of the Son of God, with respect unto the recovery and salvation of the church alone. Some have contended that he should have been incarnate, had man never fallen or sinned. Of these are Rupertus, lib. 3...
- file: EPUB/ch009.xhtml; text: Still it is supposed that the glory of God, as essentially in him, is invisible unto us, and incomprehensible by us. Yet is there a knowledge of it necessary unto us, that we may live unto him, and come unto the enjoyment of him. This we...
- file: EPUB/ch009.xhtml; text: It may be said, that the Scripture itself is sufficient for this end of the declaration of God unto us, so that there is no need of any other representation of him; and [that] these things serve only to turn the minds of men from learnin...
- file: EPUB/ch013.xhtml; text: In the confirmation hereof it will appear what judgment ought to be passed on that inquiry — which, after the uninterrupted profession of the catholic church for so many ages of a faith unto the contrary, is begun to be made by some amon...
- file: EPUB/ch017.xhtml; text: The faith and love of believers is not to be regulated by the ignorance and boldness of them who have neither the one nor the other. The title of the 45th Psalm is, " שִׁיר יְדִידְֹת ", [2] "A song of loves;" — that is, of the mutual lov...
- file: EPUB/ch029.xhtml; text: The glory of Christ is the glory of the person of Christ So he calls it " Τὴν δόξαν τὴν ἐμὴν ", [2] John 17:24, "That glory which is mine," which belongeth to me, unto my person.

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

## Enumerator Sequence Candidates

- file: EPUB/ch001.xhtml; marker: [4]; family: bracket_decimal; context: rculated most of the impression His work which bears the title, ΘΕΟΛΟΓΟΥΜΕΝΑ ΠΑΝΤΟΔΑΙΙΑ , [4] etc., originally published at Oxford in 1661, must have been highly esteemed abroad, as it was reprinted at Bremen in 1684, and at Franeker in ...
- file: EPUB/ch001.xhtml; marker: [3]; family: bracket_decimal; context: l as to indicate, perhaps, the special difficulty which may have prevented the same honor [3] and service being rendered to his memory by the publication of his collected works, when we bear in mind that one of them, his Exposition of th...
- file: EPUB/ch004.xhtml; marker: [45]; family: bracket_decimal; context: υσα ηοσος , ηε πετρα , ηε κλεις , ηε ποιμεν ", etc, saith Ignatius: Epist. ad Philadelph. [45] — "He" (that is, Christ) "is the way leading unto the Father, the rock, the key, the shepherd" — wherein he has respect unto this testimony. A...
- file: EPUB/ch004.xhtml; marker: [94]; family: bracket_decimal; context: Origen expressly denies the words to be spoken of Peter, in Matthew 16:1 16: (Tract. 1:) [94] "Quod si super unum illum Petrum tantum existimees totam eclesiam aedificar, quid dicturus es de Johanne, et apostolorum unoquoque? Num audebim...
- file: EPUB/ch004.xhtml; marker: [42]; family: bracket_decimal; context: unto in the name of all the rest of the apostles. Euseb. Preparat. Evang., lib. 1 cap. 3: [42] [41] " Ητε ὀνομαστὶ προθεσπισθεῖσα ἐκκλησία αὐτοῦ ἕστηκε κατὰ βάθους ἐῤῥιζωμένη , καὶ μέχρις οὐρανίων ἁψίδων εὐχηαῖς ὀσίων καὶ θεοφιλῶν ἀνδρῶν...
- file: EPUB/ch004.xhtml; marker: [41]; family: bracket_decimal; context: in the name of all the rest of the apostles. Euseb. Preparat. Evang., lib. 1 cap. 3: [42] [41] " Ητε ὀνομαστὶ προθεσπισθεῖσα ἐκκλησία αὐτοῦ ἕστηκε κατὰ βάθους ἐῤῥιζωμένη , καὶ μέχρις οὐρανίων ἁψίδων εὐχηαῖς ὀσίων καὶ θεοφιλῶν ἀνδρῶν μετε...
- file: EPUB/ch004.xhtml; marker: [72]; family: bracket_decimal; context: lix fidei Petra, Petri ore confessa, Tu es filius Dei vivi," says Hilary de Trin., lib. 2 [72] — "This is the only immovable foundation, this is the blessed rock of faith confessed by Peter, Thou art the Son of the living God". And Epiph...
- file: EPUB/ch004.xhtml; marker: [69]; family: bracket_decimal; context: f faith confessed by Peter, Thou art the Son of the living God". And Epiphanius, Haer.29: [69] " Επὶ τῇ πέτρᾳ ταυτῃ τῆς ἀσφαλοῦς πίστεως οἰκοδομήσω μοῦ τὴν ἐκκλεσίαν ". [22] — "Upon this rock" of assured faith "I will build my church". F...
- file: EPUB/ch004.xhtml; marker: [22]; family: bracket_decimal; context: , Haer.29: [69] " Επὶ τῇ πέτρᾳ ταυτῃ τῆς ἀσφαλοῦς πίστεως οἰκοδομήσω μοῦ τὴν ἐκκλεσίαν ". [22] — "Upon this rock" of assured faith "I will build my church". For many thought that faith itself was metonymically called the Rock, because of...
- file: EPUB/ch004.xhtml; marker: [11]; family: bracket_decimal; context: sum filium Dei vivi, aedificabo ecclesiam meam. Super me aedificabo te, non me super te:" [11] De Verbis Dom., Serm. 13. [68] — "Upon this rock which thou hast confessed — upon myself, the God of the living God — I will build my church I...

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
- word: modern; pdf: 4; epub: 13
- word: greek; pdf: 9; epub: 17
- word: faithfulness; pdf: 5; epub: 12
- word: hebrew; pdf: 3; epub: 10
- word: footnotes; pdf: 0; epub: 6

## Untagged Latin Word Samples

- word: nor; epub: 352; tagged: 0
- word: jesus; epub: 254; tagged: 0
- word: yea; epub: 97; tagged: 0
- word: immediate; epub: 97; tagged: 0
- word: distinct; epub: 86; tagged: 0
- word: thereunto; epub: 73; tagged: 0
- word: mere; epub: 66; tagged: 0
- word: hereunto; epub: 63; tagged: 0
- word: et; epub: 62; tagged: 0
- word: whereas; epub: 60; tagged: 0

## Missing Latin Clauses

- page: 51; word_count: 4; sample: de ecclesiastica dogmatibus cap

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
