# Text Integrity Audit: Volume 2

- Status: **WARN**
- Warnings: 11
- PDF pages: 555
- EPUB text files: 50
- EPUB paragraphs/headings: 2080

## Coverage

- PDF content tokens: 187098
- EPUB content tokens: 186880
- Approximate PDF-to-EPUB coverage ratio: 0.9949
- Pages checked: 550
- Weak page matches: 3
- Dense source windows checked: 25354
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 2
- Top-of-page body windows checked: 542
- Top-of-page windows skipped as unstable: 29
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 505
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 3

## Paragraphs

- Body paragraphs checked: 1742
- Possible faulty paragraph splits: 13
- Structural starts excluded from split warnings: 243
- Short fragments: 22
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 478
- EPUB enumerator markers: 482
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 450
- EPUB Greek words: 449
- Greek word coverage ratio: 0.9954
- PDF Hebrew words: 88
- EPUB Hebrew words: 89
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 25
- Missing Greek clauses: 0
- Hebrew clauses checked: 11
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 2606
- EPUB Latin words: 2629
- EPUB Tagged Latin words: 585
- Latin word coverage ratio: 0.995
- Latin word tagging ratio: 0.2225
- Latin clauses checked: 60
- Missing Latin clauses: 0
- Tagged Latin runs checked: 169
- Translated Latin runs: 43
- Latin translation ratio: 0.2544

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: contents of vol of communion with god the father son and holy ghost prefatory
- page: 4; sample: his suitableness to endear these considerations improved chapter of the way and manner whereby
- page: 5; sample: influence into our acceptation with god chapter the nature of purchased grace referred to
- page: 6; sample: of the holy ghost how the spirit of adoption and of supplication chapter the
- page: 8; sample: take the doctrine of distinct communion with the divine persons to be new fangled
- page: 9; sample: said by lewis stucley in his preface to theophilus polwhele's book of quenching the
- page: 10; sample: of communion with god the father son and holy ghost each person distinctly in
- page: 12; sample: christ is exhibited under three divisions his personal grace iii vi and under this
- page: 19; sample: are differences of administrations but the same lord the same lord jesus verse and
- page: 21; sample: is to receive the lord christ as the son the son given unto us

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.5; sample: contents of vol of communion with god the father son and holy ghost prefatory note by the editor preface note to the reader by burgess part chapter that
- page: 6; hit_ratio: 0.5; sample: of the powers of the world to come unction by the spirit isaiah the various teachings of the holy ghost how the spirit of adoption and of supplication

## Missing Top-Of-Page Body Windows

- page: 3; sample: CONTENTS OF VOL. 2. OF COMMUNION WITH GOD THE FATHER,

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 540; sample: and rp,Ko. This last word we render "satisfaction," Numbers 35:32,33,
- page: 547; sample: woman being freed, affirmed afterward, that she considered none in the company, but him who said, wJv th~v yuch~v a[n pri>aito w[ste mh> me

## Possible Paragraph Splits

- file: EPUB/ch001.xhtml; previous: CHRISTIAN READER,; next: IT is now six years past since I was brought under an engagement of promise for the publishing of some meditations on the subject which thou wilt find handled in the ensuing treati
- file: EPUB/ch002.xhtml; previous: To The Reader; next: ALPHONSUS, king of Spain, is said to have found food and physic in reading Livy; and Ferdinand, king of Sicily, in reading Quintus Curtius Rufus : but thou hast here nobler enterta
- file: EPUB/ch002.xhtml; previous: Reader, I am Thy servant in Christ Jesus; next: Daniel Burgess
- file: EPUB/ch005.xhtml; previous: der three divisions: — his _personal grace,_ III. — VI.; and under this branch are two long digressions, designed to unfold the glory and loveliness of Christ; _— purchased grace_,; next: VII.
- file: EPUB/ch008.xhtml; previous: And you have distinct mention of the love of the Splint, Romans 15:30. The apostle also peculiarly directs his supplication to him in that solemn benediction, 2 Corinthians 13:14,; next: And such benedictions are originally supplications. He is likewise entitled unto all instituted worship, from the appointment of the administration of baptism in his name, Matthew
- file: EPUB/ch010.xhtml; previous: art, then, in this, upon a most sure bottom. If thou believest and receives the Father as love, he will infallibly be so to thee, though others may fall under his severity. But, —; next: Obj. 3. "I cannot find my heart making returns of love unto God. Could I find my soul set upon him, I could then believe his soul delighted in me."
- file: EPUB/ch021.xhtml; previous: (2ndly.) The Son has ordained and appointed it as mediator. John 15:16, "'I have ordained you, that ye should bring forth fruit' of obedience, and that it should remain." And, —; next: (3rdly.) The holy Ghost appoints and ordains believers to works of obedience and holiness, and to work holiness in others. So, in particular, Acts 13:2, he appoints and designs men
- file: EPUB/ch021.xhtml; previous: ur walking in the light of faith does glory arise to the Father. The fruits of his love, of his grace, of his kindness, are seen upon us; and God is glorified in our behalf. And, —; next: [2ndly.] The Son is gloried thereby. It is the will of God that as all men honor the Father, so should they honor the Son, John 5:23. And how is this done? By believing in him, Joh
- file: EPUB/ch023.xhtml; previous: (1st.) Unto a present place, name, and room, in the house of God, and all the privileges and administrations thereof; next: (2ndly.) To a future fullness of the great inheritance of glory, — of a kingdom purchased for that whole family whereof they are by Jesus Christ: —
- file: EPUB/ch026.xhtml; previous: nce on him. He distributes as he will; — who should not be content with his portion? what claim can any lay to that which he distributeth as he will? which is farther manifested, —; next: [3rdly.] By his being said to give when and what he bestows. They "spake with other tongues, as the Spirit gave them utterance," Acts 2:4. He gave them to them; that is, freely: wh

## Inline Structural Marker Candidates

- file: EPUB/ch005.xhtml; text: Part I. — The fact of communion with God is asserted, CHAP. I Passages in Scripture are quoted to show that special mention is made of communion with all the persons of the Trinity, II. Communion with the FATHER is described, III. and pr...

## Short Fragments

- file: EPUB/ch001.xhtml; text: CHRISTIAN READER,
- file: EPUB/ch002.xhtml; text: To The Reader
- file: EPUB/ch002.xhtml; text: Daniel Burgess
- file: EPUB/ch005.xhtml; text: VII.
- file: EPUB/ch008.xhtml; text: — of which place afterward.
- file: EPUB/ch018.xhtml; text: Afflictions.
- file: EPUB/ch019.xhtml; text: Hereof, then, are two parts: —
- file: EPUB/ch020.xhtml; text: Of which in the ensuing chapters.
- file: EPUB/ch032.xhtml; text: END.
- file: EPUB/ch035.xhtml; text: Particularly, —

## Enumerator Sequence Candidates

- file: EPUB/ch014.xhtml; marker: (2.); family: paren_decimal; context: ion, Hosea 3:3; Song of Solomon 1:15 — On the part of Christ — On the part of the saints. (2.) The next thing that comes under consideration is, the way whereby we hold communion with the Lord Christ, in respect of that personal grace wh...

## Repeated Windows

- phrase: is with the father and with his son jesus christ; count: 7
- phrase: bare our sins in his own body on the tree; count: 7
- phrase: our fellowship is with the father and with his son; count: 6
- phrase: fellowship is with the father and with his son jesus; count: 6
- phrase: pleased the father that in him should all fullness dwell; count: 6
- phrase: the father that in him should all fullness dwell colossians; count: 6
- phrase: it pleased the father that in him should all fullness; count: 5
- phrase: to be propitiation through faith in his blood to declare; count: 5
- phrase: be propitiation through faith in his blood to declare his; count: 5
- phrase: propitiation through faith in his blood to declare his righteousness; count: 5

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 3; epub: 12
- word: historical; pdf: 0; epub: 8
- word: greek; pdf: 5; epub: 12
- word: modern; pdf: 5; epub: 12
- word: footnotes; pdf: 0; epub: 7
- word: hebrew; pdf: 6; epub: 12
- word: edition; pdf: 5; epub: 11

## Untagged Latin Word Samples

- word: jesus; epub: 360; tagged: 6
- word: nor; epub: 271; tagged: 8
- word: mediator; epub: 164; tagged: 3
- word: yea; epub: 91; tagged: 2
- word: distinct; epub: 78; tagged: 0
- word: whereas; epub: 58; tagged: 0
- word: whereunto; epub: 52; tagged: 0
- word: poor; epub: 51; tagged: 1
- word: adam; epub: 51; tagged: 1
- word: sum; epub: 42; tagged: 1

## Untranslated Latin Samples

- phrase: Quintus Curtius ‡ Rufus
- phrase: permista deliciis auxilia
- phrase: pauci sacras Scripturas
- phrase: nomina rerum, plurimi nomina magistrorum sequuntur
- phrase: paucissimae lectionis mancipia
- phrase: contra antidotum
- phrase: VII., VIII
- phrase: doloris socii
- phrase: is "communitas homini cum Deo
- phrase: Believe you in God; believe also in me.

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
