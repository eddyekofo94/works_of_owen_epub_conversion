# Text Integrity Audit: Volume 13

- Status: **WARN**
- Warnings: 13
- PDF pages: 749
- EPUB text files: 83
- EPUB paragraphs/headings: 2219

## Coverage

- PDF content tokens: 247367
- EPUB content tokens: 249366
- Approximate PDF-to-EPUB coverage ratio: 0.9989
- Pages checked: 725
- Weak page matches: 4
- Dense source windows checked: 33515
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 720
- Top-of-page windows skipped as unstable: 8
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 679
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 1782
- Possible faulty paragraph splits: 1
- Structural starts excluded from split warnings: 117
- Short fragments: 35
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Syllabus-anchor candidates: 8
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 3
- Roman heading candidates: 4
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 15
- PDF enumerator markers: 80
- EPUB enumerator markers: 80
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1038
- EPUB Greek words: 1030
- Greek word coverage ratio: 0.9744
- PDF Hebrew words: 12
- EPUB Hebrew words: 12
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 59
- Missing Greek clauses: 1
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 2127
- EPUB Latin words: 2054
- EPUB Tagged Latin words: 1423
- Latin word coverage ratio: 0.9553
- Latin word tagging ratio: 0.6928
- Latin clauses checked: 197
- Missing Latin clauses: 11
- Tagged Latin runs checked: 374
- Translated Latin runs: 155
- Latin translation ratio: 0.4144

## Modern References & Translations

- Manifest found: yes
- Unresolved modern references: 2
- Untranslated substantial foreign passages: 2
- Unenriched legacy footnotes: 4

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `syllabus_anchor_candidates`: Some introduced scholastic syllabus runs appear unflattened or need triage
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `unresolved_modern_references`: Modern notes manifest contains unresolved main-body reference candidates.
- `untranslated_substantial_foreign_passages`: Modern notes manifest contains substantial foreign passages without a high-confidence translation popup.
- `unenriched_legacy_footnotes`: Modern notes manifest contains existing source footnotes needing editorial enrichment.

## Missing Dense Source Windows

- page: 31; sample: the law of nature being pre supposed we find them farther speaking often one
- page: 46; sample: or no may better serve to illustrate plutarch's discourse of socrates demon than any
- page: 50; sample: and jesuits pretending falsely by their impostures to the power of miracle working though
- page: 58; sample: they may interest themselves in holy soul concerning affairs both in respect of their
- page: 68; sample: is an ignorant congregation of which thanks to our prelates pluralists non residents homilies
- page: 76; sample: eshcol cluster of the fruit of canaan rules of walking in fellowship with reference
- page: 77; sample: election appointment acceptation submission galatians acts thessalonians acts corinthians which do not gire them
- page: 87; sample: commandment and is peculiarly the law of christ john thessalonians john the state and
- page: 95; sample: daily while it is called to day lest any of you be hardened through
- page: 99; sample: the command with the threatenings attending its non performance the great glory of the

## Possible Paragraph Splits

- file: EPUB/ch048.xhtml; previous: ld be restrained. It is far from my purpose to return him any answer in the like manner to these things; to do it " — opus est mangone perito Qui Smithfieldensi polleat eloquio." †; next: Yet some instances of prodigious excesses in this kind will, in our process, be reflected on; and it may be the repetition of them may make an appearance, unto some less considerat

## Syllabus Anchor Candidates

- action: likely_false_positive; file: EPUB/ch016.xhtml; anchor_index: 438; item_range: p439-p442; marker_family: arabic; item_count: 4; announced_count: None; anchor: ercy, patience, forbearance, long-suffering, and free grace towards us, sparing, pardoning, pitying, bearing with us, in innumerable daily, hourly failings and provocations; especially all this being proposed for our imitation in our mea...; items: [{'marker': '2.', 'text': 'The goodness, unwearied and unchangeable love of the Lord Jesus Christ putting in every day for us, not ceasing to plead in our behalf, notwithstanding our continual backsliding, 1 John 2:1, 2.'}, {'marker': '3...; whitelist_key: EPUB/ch016.xhtml#p438-syllabus-1-god-s-infinite-mercy-patience-forbearance-long-suffering-and-free-grace
- action: likely_false_positive; file: EPUB/ch016.xhtml; anchor_index: 448; item_range: p449-p453; marker_family: arabic; item_count: 5; announced_count: None; anchor: Now, to a right performance of this duty, and in the discharge of it, are required, —; items: [{'marker': '1.', 'text': "A due valuation, strong desire, and high esteem of the church's prosperity, in every member of it, Psalm 122:6."}, {'marker': '2.', 'text': 'Bowels of compassion as a fruit of love; to be sensible of, and intim...; whitelist_key: EPUB/ch016.xhtml#p448-syllabus-now-to-a-right-performance-of-this-duty-and-in-the-discharge
- action: likely_false_positive; file: EPUB/ch021.xhtml; anchor_index: 648; item_range: p649-p650; marker_family: arabic; item_count: 2; announced_count: None; anchor: 1. The several considerations of the church wherein and with which union is to be preserved.; items: [{'marker': '2.', 'text': 'What that union is, and wherein it doth consist, which, according to the mind of Christ, we are to keep and observe with the church, under the several notions of it respectively.'}, {'marker': '3.', 'text': 'An...; whitelist_key: EPUB/ch021.xhtml#p648-syllabus-1-the-several-considerations-of-the-church-wherein-and-with-which-union
- action: likely_false_positive; file: EPUB/ch022.xhtml; anchor_index: 654; item_range: p655-p657; marker_family: arabic; item_count: 3; announced_count: 3; anchor: TO begin with the first thing proposed: The church of Christ living in this world, as to our present concernment, is taken in Scripture three ways: —; items: [{'marker': '1.', 'text': 'For the mystical body of Christ, his elect, redeemed, justified, and sanctified ones throughout the world; commonly called the church catholic militant.'}, {'marker': '2.', 'text': 'For the universality of men ...; whitelist_key: EPUB/ch022.xhtml#p654-syllabus-to-begin-with-the-first-thing-proposed-the-church-of-christ-living
- action: likely_false_positive; file: EPUB/ch026.xhtml; anchor_index: 964; item_range: p965-p967; marker_family: unknown; item_count: 3; announced_count: None; anchor: nciples which, in this discourse, I have not been occasioned to draw forth at all or to improve. Many things of great weight and importance must come under debate and consideration before a clear account can be given of the case stated i...; items: [{'marker': '(1.)', 'text': 'The true nature of an instituted church under the gospel, as to the matter, form, and all other necessary constitutive causes, is to be investigated and found out.'}, {'marker': '(2.)', 'text': 'The nature an...; whitelist_key: EPUB/ch026.xhtml#p964-syllabus-2-were-i-fully-to-handle-the-things-pointed-to-in-this
- action: likely_false_positive; file: EPUB/ch036.xhtml; anchor_index: 1109; item_range: p1110-p1111; marker_family: arabic; item_count: 2; announced_count: None; anchor: don me for producing and insisting on these things, seeing I do it with this profession, that I can fix on nothing else so much to the purpose in hand; and yet how little these are so cannot but be evident, upon a slight view, to the mea...; items: [{'marker': '1.', 'text': 'He tells us that "there may be a breach of union with respect to the catholic church upon other considerations;" not that there may be a breach of the union of the catholic church.'}, {'marker': '2.', 'text': '...; whitelist_key: EPUB/ch036.xhtml#p1109-syllabus-the-reader-must-pardon-me-for-producing-and-insisting-on-these-things
- action: likely_false_positive; file: EPUB/ch045.xhtml; anchor_index: 1341; item_range: p1342-p1344; marker_family: arabic; item_count: 3; announced_count: None; anchor: In the meantime, let them pass at their own proper rate and value, which the stamp of civil authority hath put upon them. What is farther discoursed by the author on this subject, proceeding no farther but why may it not be so and so, we...; items: [{'marker': '3.', 'text': 'Pages 23, 24, there is a distribution of all dissenters into two parties: —'}, {'marker': '(1.)', 'text': 'Such as say, "That although they are in a state of separation from our church, yet this separation is n...; whitelist_key: EPUB/ch045.xhtml#p1341-syllabus-as-it-should-seem-an-opinion-opposite-unto-this-notion-of-national
- action: likely_false_positive; file: EPUB/ch045.xhtml; anchor_index: 1355; item_range: p1356-p1357; marker_family: arabic; item_count: 2; announced_count: None; anchor: e things wherein they who agree in the foundation are differently minded or otherwise than one another. But, 3. This was a standing rule for agreement and uniformity in practice in church order and worship, which the apostles had given a...; items: [{'marker': '4.', 'text': 'That this rule they did not give only as apostles, but as governors of the church, as appears from Acts 15:5 15.'}, {'marker': '5.', 'text': 'Wherefore, what the apostles so did, that any church hath power to d...; whitelist_key: EPUB/ch045.xhtml#p1355-syllabus-2-that-the-rule-here-intended-is-not-the-rule-of-charity

## Suspicious Large-Number Starts

- file: EPUB/ch022.xhtml; text: 10. I no way doubt of the perpetual existence of innumerable believers in every age, and such as made the profession that is absolutely necessary to salvation, one way or other, though I question a regular association of
- file: EPUB/ch022.xhtml; text: 22. In what sense this church is visible was before declared. Men elected, redeemed, justified, as such, are not visible, for that which makes them so is not; but this hinders not but they may be so upon the other consid
- file: EPUB/ch023.xhtml; text: 29. There being, then, in the world a great multitude, which no man can number, of all nations, kindreds, people, and language, professing the doctrine of the gospel, not tied to mountains or hills, John 4:21, 23, but wo

## Roman Heading Candidates

- file: EPUB/ch057.xhtml; text: II. From the law of nations. For, —
- file: EPUB/ch057.xhtml; text: V. From the promises of gospel times. For, —
- file: EPUB/ch057.xhtml; text: VI. From the equity of gospel rules For, —
- file: EPUB/ch059.xhtml; text: IV. The payment of tithes, —

## Short Fragments

- file: EPUB/ch002.xhtml; text: M AY 11, 1644.
- file: EPUB/ch002.xhtml; text: JOSEPH CARYL.
- file: EPUB/ch003.xhtml; text: John Owen
- file: EPUB/ch007.xhtml; text: and again,
- file: EPUB/ch007.xhtml; text: Whence I conclude, —
- file: EPUB/ch011.xhtml; text: to which add that of the apostle,
- file: EPUB/ch011.xhtml; text: Whence.it appears, that, —
- file: EPUB/ch012.xhtml; text: Τῷ Θεῷ ἀριστομεγίστῳ δόζα .
- file: EPUB/ch015.xhtml; text: To The Reader
- file: EPUB/ch016.xhtml; text: 2 Thessalonians 3:1,2,

## Enumerator Sequence Candidates

- file: EPUB/ch023.xhtml; marker: (2.); family: paren_decimal; context: (2.) That doing so, in the course of our lives we manifest and declare a principle that is utterly inconsistent with the belief of those truths which outwardly we profess; or, —
- file: EPUB/ch042.xhtml; marker: [16]; family: bracket_decimal; context: Nor did I, as is pretended, plead for their presbyterian way in the year [16]46; all the ministers almost in the county of Essex know the contrary, one especially, being a man of great ability and moderation of spirit, and for his knowle...

## Repeated Windows

- phrase: not fear the lord god hath spoken who can but; count: 3
- phrase: fear the lord god hath spoken who can but prophesy; count: 3
- phrase: remember them which have the rule over you who have; count: 3
- phrase: them which have the rule over you who have spoken; count: 3
- phrase: which have the rule over you who have spoken unto; count: 3
- phrase: have the rule over you who have spoken unto you; count: 3
- phrase: the rule over you who have spoken unto you the; count: 3
- phrase: rule over you who have spoken unto you the word; count: 3
- phrase: over you who have spoken unto you the word of; count: 3
- phrase: you who have spoken unto you the word of god; count: 3

## Missing Word Samples

- word: self; pdf: 13; epub: 6
- word: fellow; pdf: 3; epub: 0
- word: re; pdf: 3; epub: 1

## Excess Word Samples

- word: prefatory; pdf: 14; epub: 30
- word: editor; pdf: 0; epub: 12
- word: volume; pdf: 5; epub: 13
- word: digital; pdf: 0; epub: 8
- word: historical; pdf: 0; epub: 8
- word: theological; pdf: 0; epub: 7
- word: footnotes; pdf: 0; epub: 7
- word: modern; pdf: 5; epub: 11

## Missing Greek Clauses

- page: 263; word_count: 5; sample: δουλον κυριου ου δει μαχεσθαι

## Untagged Latin Word Samples

- word: populi; epub: 8; tagged: 0
- word: apollos; epub: 7; tagged: 0
- word: regulate; epub: 7; tagged: 0
- word: metropolis; epub: 6; tagged: 0
- word: cenchrea; epub: 6; tagged: 0
- word: judea; epub: 6; tagged: 0
- word: aen; epub: 6; tagged: 0
- word: prelate; epub: 5; tagged: 0
- word: rigor; epub: 5; tagged: 0
- word: demonstrandum; epub: 5; tagged: 0

## Missing Latin Clauses

- page: 389; word_count: 6; sample: christianorum merito sane illicita si illicitis
- page: 389; word_count: 4; sample: merito damnanda si quis
- page: 389; word_count: 5; sample: ea queritur eo titulo quo
- page: 389; word_count: 5; sample: factionibus querela est in cujus
- page: 389; word_count: 13; sample: aliquando convenimus hoc sumus congregati quod et dispersi hoc universi quod et
- page: 389; word_count: 4; sample: quum probi cum boni
- page: 389; word_count: 11; sample: cum pii cum casti congregantur non est factio dicenda sed curia
- page: 437; word_count: 11; sample: non partum studiis agimur sed sumsimus arma consiliis inimica tuis discordia
- page: 682; word_count: 8; sample: religione eapita quae plurimum habere videntur obscuritatis tantis
- page: 682; word_count: 5; sample: quam ubi cogitur assensus hugo

## Untranslated Latin Samples

- phrase: Medio tutissimus
- phrase: Sixtus Senensis
- phrase: in causa facili
- phrase: bonum oritur ex integris
- phrase: ecclesia: puto propterea quia
- phrase: contra ecclesiam
- phrase: facturos esse particulas; et
- phrase: Christo non tantam
- phrase: ecclesia magnas
- phrase: non qua itur, sed qua eundum est

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
