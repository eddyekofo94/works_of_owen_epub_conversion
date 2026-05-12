# Text Integrity Audit: Volume 2

- Status: **WARN**
- Warnings: 9
- PDF pages: 558
- EPUB text files: 51
- EPUB paragraphs/headings: 2061

## Coverage

- PDF content tokens: 187844
- EPUB content tokens: 187059
- Approximate PDF-to-EPUB coverage ratio: 0.9933
- Pages checked: 553
- Weak page matches: 5
- Dense source windows checked: 20562
- Missing dense source-window pages: 80
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 544
- Top-of-page windows skipped as unstable: 30
- Missing top-of-page body windows: 3
- Bottom-of-page body windows checked: 510
- Bottom-of-page windows skipped as unstable: 29
- Missing bottom-of-page body windows: 13

## Paragraphs

- Body paragraphs checked: 1909
- Possible faulty paragraph splits: 61
- Structural starts excluded from split warnings: 240
- Short fragments: 27
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 5
- Roman heading candidates: 0
- Overlong heading candidates: 3
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 478
- EPUB enumerator markers: 484
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 1

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 9; sample: he was manichee testifying in so many words that his error was his very
- page: 20; sample: assertion in hand shall farther declare by particular instances for the father faith love
- page: 22; sample: the father of our lord jesus christ and therefore the same apostle doth in
- page: 23; sample: of god is most frequently pressed john god that is the father so loved
- page: 24; sample: divine worship and honor for ever and ever and therefore stephen in his solemn
- page: 26; sample: one is your master even christ to the spirit john the comforter he shall
- page: 29; sample: up by an induction of instances to manifest what it is and wherein the
- page: 42; sample: what is in and of the world whose whole portion lies in evil ndly
- page: 44; sample: place that our love was one day equal towards god and thus these agreements
- page: 49; sample: in the blood of jesus and this will be exceeding effectual to endear thy

## Missing Top-Of-Page Body Windows

- page: 90; sample: the Holy Ghost to regenerate us, and to create all the habitual grace, with the daily supplies thereof, in our hearts, that we are made partakers of.
- page: 155; sample: Two things are required, that we may pray for the things in the promise, as they are in the promise: —
- page: 250; sample: (3rdly.) For actual grace, or that influence or power whereby the saints are enabled to perform particular duties according to the mind of God, there is

## Missing Bottom-Of-Page Body Windows

- page: 57; sample: Ephesians 5:2; so from the graces wherewith the blood of his atonement,
- page: 59; sample: Isaiah 32:2. From the power of corruptions, rock in a weary land,"
- page: 79; sample: Jeremiah 23:6. In the thereof. He is "Jehovah our Righteousness,"
- page: 144; sample: Isaiah 8:9,10, "Go about your counsels," saith the disappointment,
- page: 156; sample: Song of Solomon 2:3. And down under his shadow with great delight,
- page: 187; sample: of Solomon 5:1. If in any things, then, we are straitened, it is in ourselves; Christ deals bountifully with us Indeed, the great sin of believers is, that
- page: 194; sample: Luke 23:34; — some things as mediator; so he prayed for his elect only, John 17:9. There were not worse in the world, really and evidently, than
- page: 218; sample: Isaiah 42:6; and a "leader," be given "for a covenant of the people,"
- page: 268; sample: 1 Peter 2:5; — a "chosen it. It is composed of "living stones,"
- page: 314; sample: Acts 13:2; he furnisheth them work, and they are separated unto him,

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: OF; next: "Tell me, O thou whom my soul loveth, where they feedest.' — Song of Solomon l:7.
- file: EPUB/ch004.xhtml; previous: art I. - The fact of communion with God is asserted, CHAP. I Passages in Scripture are quoted to show that special mention is made of communion with all the persons of the Trinity,; next: Communion with the FATHER is described,
- file: EPUB/ch004.xhtml; previous: Communion with the FATHER is described,; next: and practical inferences deduced from it, IV.
- file: EPUB/ch005.xhtml; previous: art I. - The fact of communion with God is asserted, CHAP. I Passages in Scripture are quoted to show that special mention is made of communion with all the persons of the Trinity,; next: Communion with the FATHER is described,
- file: EPUB/ch005.xhtml; previous: Communion with the FATHER is described,; next: and practical inferences deduced from it, IV.
- file: EPUB/ch005.xhtml; previous: Part II . — The reality of communion with CHRIST is proved, CHAP. I.; and the nature of it is subsequently considered,; next: It is shown to consist in grace; and then the grace of Christ is exhibited under three divisions: — his personal grace, III. — VI.; and under this branch are two long digressions,
- file: EPUB/ch005.xhtml; previous: under three divisions: — his personal grace, III. — VI.; and under this branch are two long digressions, designed to unfold the glory and loveliness of Christ; — purchased grace ,; next: — X.; in which the mediatorial work of Christ is fully considered, in reference to our acceptance with God, VII., VIII.; sanctification, IX.; and the privileges of the covenant, X.
- file: EPUB/ch009.xhtml; previous: (1st.) The love of the Father unto us is an antecedent love, and that in two respects: —; next: [1st.] It is antecedent in respect of our love, 1 John 4:10, "Herein is love, not that we loved God, but that he loved us." His love goes before ours. The father loves the child, w
- file: EPUB/ch009.xhtml; previous: (2ndly.) Our love is consequential in both these regards: —; next: [1st.] In respect of the love of God. Never did creature turn his affections towards God, if the heart of God were not first set upon him.
- file: EPUB/ch009.xhtml; previous: ng; that cannot be heightened by any act of ours, that cannot be lessened by any thing in us. I say, in itself it is thus; otherwise, in a twofold regard, it may admit of change: —; next: [1st.] In respect of its fruits. It is, as I said, a fruitful love, a love of bounty. In reference unto those fruits, it may sometimes be greater, sometimes less; its communication

## Suspicious Large-Number Starts

- file: EPUB/ch035.xhtml; text: 43. What this farther acquaintance with the person of Christ should mean, I do not well understand: it may be, any more acquaintance with respect unto some that is necessary; — it may be, without any more ado as to an ac
- file: EPUB/ch035.xhtml; text: 74. He quotes my words, "That 'the soul consents to take Christ on his own terms, to save him in his own way; and saith, Lord, I would have had thee and salvation in my way, that it might have been partly of mine endeavo
- file: EPUB/ch035.xhtml; text: 203. "That I distinguish the graces of Christ's person as mediator from the graces of his person as God and man." Neither could any man have run into such an imagination who had competently understood the things which he
- file: EPUB/ch035.xhtml; text: 280. "As for example," saith he, "Christ is called a husband, the church his spouse; and now all the invitations of the gospel are Christ's wooing and making love to his spouse; — and what other men call believing the go
- file: EPUB/ch043.xhtml; text: 10. 846. "Hast thou, O son, fallen under the enemies' hand in my stead? Am I saved by thy wounds? Do I live by thy death?" And the word תָּחַת , used by David, does signify, when applied unto persons, either a succession

## Overlong Heading Candidates

- file: EPUB/ch024.xhtml; tag: h4; text: The foundation of our communion with the Holy ghost (John 16:1-7) opened at large — Παράκλητος , a Comforter; who he is — The Holy Ghost; his own will in his coming to us; sent also by Christ — The Spirit sent as a sanctifier and as a co...
- file: EPUB/ch025.xhtml; tag: h4; text: The foundation of our communion with the Holy ghost (John 16:1-7) opened at large — Παράκλητος , a Comforter; who he is — The Holy Ghost; his own will in his coming to us; sent also by Christ — The Spirit sent as a sanctifier and as a co...
- file: EPUB/ch027.xhtml; tag: h4; text: Of the things wherein we have communion with the Holy Ghost — He brings to remembrance the things spoken by Christ, John 14:26 — The manner how he does it — The Spirit glorifies Christ in the hearts of believers, John 16:14, sheds abroad...

## Short Fragments

- file: EPUB/ch002.xhtml; text: TO THE READER.
- file: EPUB/ch003.xhtml; text: OF
- file: EPUB/ch016.xhtml; text: Hebrews 1:3; of which before.
- file: EPUB/ch016.xhtml; text: Wherefore, —
- file: EPUB/ch018.xhtml; text: Afflictions.
- file: EPUB/ch019.xhtml; text: Hereof, then, are two parts: —
- file: EPUB/ch019.xhtml; text: To his wrath are men obnoxious,
- file: EPUB/ch020.xhtml; text: Of which in the ensuing chapters.
- file: EPUB/ch021.xhtml; text: Therefore, —
- file: EPUB/ch021.xhtml; text: [2ndly.] Peace.

## Enumerator Sequence Candidates

- file: EPUB/ch014.xhtml; marker: (2.); family: paren_decimal; context: (2.) The next thing that comes under consideration is, the way whereby we hold communion with the Lord Christ, in respect of that personal grace whereof we have spoken. Now, this the S

## Repeated Windows

- phrase: bare our sins in his own body on the tree; count: 7
- phrase: is with the father and with his son jesus christ; count: 6
- phrase: pleased the father that in him should all fullness dwell; count: 6
- phrase: the father that in him should all fullness dwell colossians; count: 6
- phrase: there are diversities of operations but it is the same; count: 5
- phrase: are diversities of operations but it is the same god; count: 5
- phrase: our fellowship is with the father and with his son; count: 5
- phrase: fellowship is with the father and with his son jesus; count: 5
- phrase: lord jesus christ and the love of god and the; count: 5
- phrase: it pleased the father that in him should all fullness; count: 5

## Missing Word Samples

- word: ft; pdf: 26; epub: 0
- word: kai; pdf: 19; epub: 0
- word: tou; pdf: 17; epub: 0
- word: th; pdf: 24; epub: 8
- word: pa; pdf: 12; epub: 0
- word: pneu; pdf: 9; epub: 0
- word: ajnti; pdf: 9; epub: 0
- word: ta; pdf: 8; epub: 0
- word: ejn; pdf: 8; epub: 0
- word: ou; pdf: 8; epub: 0

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
