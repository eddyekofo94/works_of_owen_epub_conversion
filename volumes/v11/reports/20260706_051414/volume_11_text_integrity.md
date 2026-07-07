# Text Integrity Audit: Volume 11

- Status: **WARN**
- Warnings: 4
- PDF pages: 815
- EPUB text files: 30
- EPUB paragraphs/headings: 2448

## Coverage

- PDF content tokens: 296711
- EPUB content tokens: 297903
- Approximate PDF-to-EPUB coverage ratio: 0.9988
- Pages checked: 794
- Weak page matches: 1
- Dense source windows checked: 32387
- Missing dense source-window pages: 21
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 791
- Top-of-page windows skipped as unstable: 12
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 791
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 1

## Paragraphs

- Body paragraphs checked: 2086
- Possible faulty paragraph splits: 5
- Structural starts excluded from split warnings: 251
- Short fragments: 29
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Syllabus-anchor candidates: 3
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 2
- Roman heading candidates: 2
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 0
- PDF enumerator markers: 254
- EPUB enumerator markers: 254
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 2078
- EPUB Greek words: 2079
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 0
- EPUB Hebrew words: 0
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 117
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3856
- EPUB Latin words: 3860
- EPUB Tagged Latin words: 3014
- Latin word coverage ratio: 0.9984
- Latin word tagging ratio: 0.7808
- Latin clauses checked: 383
- Missing Latin clauses: 0
- Tagged Latin runs checked: 772
- Translated Latin runs: 245
- Latin translation ratio: 0.3174

## Modern References & Translations

- Manifest found: yes
- Unresolved modern references: 0
- Untranslated substantial foreign passages: 0
- Unenriched legacy footnotes: 9

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `syllabus_anchor_candidates`: Some introduced scholastic syllabus runs appear unflattened or need triage
- `unenriched_legacy_footnotes`: Modern notes manifest contains existing source footnotes needing editorial enrichment.

## Missing Dense Source Windows

- page: 127; sample: hereunto was that of the pelagians and semi pelagians which austin opposed in sundry
- page: 128; sample: much of ancient candid truth in opposition to the pelagians and semi pelagians preserved
- page: 129; sample: it its principles and causes its relation to the good will of the father
- page: 131; sample: note by the editor see page f7 to remove from the preceding preface the
- page: 135; sample: of judging professors to be true believers matthew considered what is the rule of
- page: 136; sample: unchangeableness and faithfulness of god jude corinthians isaiah jeremiah 31-34 isaiah hebrews 10-12 corinthians
- page: 137; sample: was known upon the earth revelation jude matthew thessalonians peter 20-22 timothy john hebrews
- page: 139; sample: gracious promises wherein their refreshments and reserves under such temptations do lie romans corinthians
- page: 140; sample: do give the least hint to such an assertion romans psalm isaiah 7-10 peter
- page: 141; sample: corinthians ephesians romans john the temptation arising from the apostasy of hypocrites is neither

## Missing Top-Of-Page Body Windows

- page: 792; sample: "Thirdly, It is no punishment at all to hypocrites to be under no possibility of being 'renewed again by repentance:' nay, in case they

## Missing Bottom-Of-Page Body Windows

- page: 791; sample: that this pretended "pregnant reason" is as barren as the former to the proving of the assertion laid down to be proved by it. He adds, —

## Possible Paragraph Splits

- file: EPUB/ch005.xhtml; previous: k to deal so harshly with some of them with whom he hath to do. And it is still feared that "Parata tollit cornua; Qualis Lycambae spretus infido gener, Aut acer hostis Bupalo ." 3; next: It might, indeed, be the more excusable if evident provocation were always ready at hand to be charged with the blame of this procedure, if he said only,
- file: EPUB/ch006.xhtml; previous: To the same purpose, with application to a particular person, doth that great and holy doctor discourse, De Doctrin. Christiana, lib. 3 cap. 33. ◇; next: Saith he,
- file: EPUB/ch006.xhtml; previous: "Nulla," saith he, "quidem nobis incumbit necessitas, ut in tanta exemplarium et editionum varietate et inconstantia, nihil uspiam Ignatio interpolatum ant adsutum affirmemus ." †; next: And, indeed, the foisted passages in many places are so evident, yea shameful, that no man who is not resolved to say any thing, without care of proof or truth, can once appear in
- file: EPUB/ch006.xhtml; previous: make the matter more clear, cap. 13, he disputes, that " Auxilium sine quo nullus perseverat, et per quod quilibet perseverat, est Spiritus Sanctus, divina bonitas et voluntas ." †; next: Every cause of bringing sinful man to God is called by them "auxilium.' In these three, " Spiritus Sanctus, divina bonitas, et voluntas ," he compriseth the chief causes of perseve
- file: EPUB/ch009.xhtml; previous: cally insinuates into their understandings and affections, for their establishment, is an exurgency § of that description of himself which he gives, verse 28: from his eternity , —; next: He is "the everlasting God;" from his power, — He is "the Creator of the ends of the earth;" from his unchangeableness, — "He fainteth not," he waxeth not weary, and therefore ther

## Inline Structural Marker Candidates

- file: EPUB/ch024.xhtml; text: and defile themselves daily with the pollutions of the world. This consequence, according to the principles and known tenets of our adversaries, is legitimate and true, inasmuch as they hold 'That true believers may fall so foul and so f...

## Syllabus Anchor Candidates

- action: likely_false_positive; file: EPUB/ch006.xhtml; anchor_index: 374; item_range: p375-p378; marker_family: arabic; item_count: 4; announced_count: None; anchor: their divinity. So that notwithstanding all their corruptions, these ensuing principles passed currently amongst the most eminent of them as to the doctrine under consideration, which continue in credit with many of their sophistical suc...; items: [{'marker': '1.', 'text': 'That perseverance is a grace of God, bestowed according to predestination, or election, on men; that is, that God gives it to believers that are predestinated and elected.'}, {'marker': '2.', 'text': 'That on w...; whitelist_key: EPUB/ch006.xhtml#p374-syllabus-but-yet-as-there-was-none-of-those-but-one-way-or
- action: likely_false_positive; file: EPUB/ch006.xhtml; anchor_index: 376; item_range: p377-p378; marker_family: arabic; item_count: 2; announced_count: None; anchor: 2. That on whomsoever the grace of perseverance is bestowed, they do persevere to the end; and it is impossible in some sense that they should otherwise do.; items: [{'marker': '3.', 'text': 'That none who are not predestinate, what grace soever they may be made partakers of in this world, shall constantly continue to the end.'}, {'marker': '4.', 'text': 'That no believer can by his own strength or ...; whitelist_key: EPUB/ch006.xhtml#p376-syllabus-2-that-on-whomsoever-the-grace-of-perseverance-is-bestowed-they-do
- action: likely_false_positive; file: EPUB/ch008.xhtml; anchor_index: 492; item_range: p493-p494; marker_family: arabic; item_count: 2; announced_count: 2; anchor: rit, and to be made naked of the habit of grace or new nature bestowed on them. That, and that only, whereunto this effect is ascribed is sin. Now, there are two ways whereby sin may be supposed to produce such effects in reference to th...; items: [{'marker': '1.', 'text': 'Efficiently , by a reaction in the same subject, as frequent acts of vice will debilitate and overthrow an acquired habit whereunto it is opposite.'}, {'marker': '2.', 'text': 'Meritoriously , by provoking the ...; whitelist_key: EPUB/ch008.xhtml#p492-syllabus-as-to-what-is-on-the-other-side-affirmed-that-believers-may

## Suspicious Large-Number Starts

- file: EPUB/ch006.xhtml; text: 24. It seems, moreover, that those bishops and deacons in those days, as was observed, were appointed to the office by and with the consent of the people, or whole body of the church; no loss do these words import, Συνευ
- file: EPUB/ch006.xhtml; text: 30. Paulus tandem et Silas Syriam et Cilieiam peragrantes, ver. 41, cap. 16:4, δόγματα κεκριμένα ὑπὸ τῶν ἀποστόλων , singulis elvitatibus observanda tradiderunt, ut quae ad hanc Antiochiae metropolin, ut totidem subordin

## Roman Heading Candidates

- file: EPUB/ch015.xhtml; text: I. 1. The indwelling of the Spirit is the great and solemn promise of the covenant of grace; the manner of it we shall afterward evince: [Ezekiel 36:27] Ezekiel 36:27, "I will put my Spirit within you, and cause you to w
- file: EPUB/ch015.xhtml; text: II. 1. The first signal issue and effect which is ascribed to this indwelling of the Spirit is union; not a personal union with himself, which is impossible.

## Short Fragments

- file: EPUB/ch001.xhtml; text: OR, THE
- file: EPUB/ch001.xhtml; text: BY
- file: EPUB/ch001.xhtml; text: John Owen
- file: EPUB/ch001.xhtml; text: ANNO DOM: 1654.
- file: EPUB/ch004.xhtml; text: TO
- file: EPUB/ch004.xhtml; text: John Owen
- file: EPUB/ch004.xhtml; text: ######
- file: EPUB/ch005.xhtml; text: John Owen
- file: EPUB/ch006.xhtml; text: Saith he,
- file: EPUB/ch006.xhtml; text: Well, what then?

## Enumerator Sequence Candidates

- file: EPUB/ch017.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) There are promises of what good and great things God will farther do unto and for them who obey him; as, that he will keep them and preserve them that they shall not be lost, that

## Missing Word Samples

- word: sod; pdf: 3; epub: 0
- word: semi; pdf: 3; epub: 0

## Excess Word Samples

- word: psalms; pdf: 1; epub: 56
- word: historical; pdf: 2; epub: 10
- word: digital; pdf: 0; epub: 8
- word: theological; pdf: 2; epub: 9
- word: footnotes; pdf: 0; epub: 7
- word: modern; pdf: 4; epub: 10

## Missing Latin Word Samples

- word: semi; pdf: 3; epub: 0

## Untagged Latin Word Samples

- word: perpetrate; epub: 10; tagged: 0
- word: salmasius; epub: 9; tagged: 0
- word: vedelius; epub: 8; tagged: 0
- word: co-operate; epub: 8; tagged: 0
- word: alexandria; epub: 9; tagged: 3
- word: estimate; epub: 6; tagged: 0
- word: synodalia; epub: 6; tagged: 0
- word: iota; epub: 5; tagged: 0
- word: smyrna; epub: 5; tagged: 0
- word: cilicia; epub: 6; tagged: 1

## Untranslated Latin Samples

- phrase: catena patrum
- phrase: Sancti Sanciti
- phrase: Sancta sanctis
- phrase: actum agere
- phrase: velut amnis
- phrase: super notas aluere ripas
- phrase: profundo Pindarus
- phrase: monstrum horrendum
- phrase: sanguine laxo Membra
- phrase: cornua; Qualis Lycambae spretus infido

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
