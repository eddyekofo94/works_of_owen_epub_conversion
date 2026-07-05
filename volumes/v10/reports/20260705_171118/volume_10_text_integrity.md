# Text Integrity Audit: Volume 10

- Status: **WARN**
- Warnings: 4
- PDF pages: 828
- EPUB text files: 104
- EPUB paragraphs/headings: 3368

## Coverage

- PDF content tokens: 262672
- EPUB content tokens: 263334
- Approximate PDF-to-EPUB coverage ratio: 0.9994
- Pages checked: 807
- Weak page matches: 2
- Dense source windows checked: 35198
- Missing dense source-window pages: 3
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 776
- Top-of-page windows skipped as unstable: 7
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 704
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 2745
- Possible faulty paragraph splits: 1
- Structural starts excluded from split warnings: 191
- Short fragments: 35
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Syllabus-anchor candidates: 25
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 2
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 185
- EPUB enumerator markers: 186
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 822
- EPUB Greek words: 845
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 18
- EPUB Hebrew words: 18
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 40
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 1417
- EPUB Latin words: 1418
- EPUB Tagged Latin words: 834
- Latin word coverage ratio: 0.9958
- Latin word tagging ratio: 0.5882
- Latin clauses checked: 95
- Missing Latin clauses: 0
- Tagged Latin runs checked: 255
- Translated Latin runs: 99
- Latin translation ratio: 0.3882

## Modern References & Translations

- Manifest found: yes
- Unresolved modern references: 0
- Untranslated substantial foreign passages: 0
- Unenriched legacy footnotes: 69

## Warnings

- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `syllabus_anchor_candidates`: Some introduced scholastic syllabus runs appear unflattened or need triage
- `unenriched_legacy_footnotes`: Modern notes manifest contains existing source footnotes needing editorial enrichment.

## Missing Dense Source Windows

- page: 107; sample: flesh john idem by nature the children of wrath even as others ephesians by
- page: 319; sample: to be taken and destroyed sheep and goats matthew john passim those on whom
- page: 320; sample: in thee and that my name might be declared throughout all the earth chap

## Possible Paragraph Splits

- file: EPUB/ch021.xhtml; previous: Chapter 6. The means used by the fore-recounted agents in this work: —; next: I.

## Inline Structural Marker Candidates

- file: EPUB/ch020.xhtml; text: In 1650, Mr. Home, minister at Lynn in Norfolk, a man, according to Palmer (Nonconf. Mem., 3. pp. 6, 7), "of exemplary and primitive piety," and author of several works, published a reply to Owen's work, under the title, "The Open Door f...

## Syllabus Anchor Candidates

- action: likely_false_positive; file: EPUB/ch008.xhtml; anchor_index: 172; item_range: p173-p174; marker_family: arabic; item_count: 2; announced_count: 3; anchor: ee, or the counsel of his will," Ephesians 1:11, for whatsoever he doth now it pleased him from the beginning, Psalm 115:3; seeing, also, that known unto God are all his works from eternity; therefore, three things concerning his provide...; items: [{'marker': '1.', 'text': 'His decree or purpose, 57 whereby he hath disposed of all things in order, and appointed them for certain ends, which he hath fore-ordained.'}, {'marker': '2.', 'text': 'His prescience, whereby he certainly for...; whitelist_key: EPUB/ch008.xhtml#p172-syllabus-providence-is-a-word-which-in-its-proper-signification-may-seem-to
- action: likely_false_positive; file: EPUB/ch021.xhtml; anchor_index: 699; item_range: p700-p707; marker_family: arabic; item_count: 8; announced_count: None; anchor: Chapter 3. An unfolding of the remaining texts of Scripture produced for the confirmation of the first general objection or argument for universal redemption.; items: [{'marker': '2.', 'text': '1 John 2:l, 2, largely opened and vindicated.'}, {'marker': '3.', 'text': 'John 6:51 explained.'}, {'marker': '4.', 'text': 'A vindication of other texts produced by Thomas More, viz.: —'}, {'marker': '(1.)', '...; whitelist_key: EPUB/ch021.xhtml#p699-syllabus-chapter-3-an-unfolding-of-the-remaining-texts-of-scripture-produced-for
- action: likely_false_positive; file: EPUB/ch021.xhtml; anchor_index: 708; item_range: p709-p713; marker_family: arabic; item_count: 5; announced_count: None; anchor: Chapter 4. Answer to the second general objection or argument for the universality of redemption.; items: [{'marker': '2.', 'text': 'From the word "all" in several scriptures, viz.: —'}, {'marker': '1.', 'text': '1 Timothy 2:4, 6. 2. 2 Peter 3:9.'}, {'marker': '3.', 'text': 'Hebrews 2:9.'}, {'marker': '4.', 'text': '2 Corinthians 5:14, 15. 5...; whitelist_key: EPUB/ch021.xhtml#p708-syllabus-chapter-4-answer-to-the-second-general-objection-or-argument-for-the
- action: likely_false_positive; file: EPUB/ch021.xhtml; anchor_index: 714; item_range: p715-p719; marker_family: arabic; item_count: 5; announced_count: None; anchor: Chapter 5. The last objection or argument from Scripture answered.; items: [{'marker': '3.', 'text': 'From texts which seem to hold out a perishing of some for whom Christ died, viz.: —'}, {'marker': '1.', 'text': 'Romans 14:15.'}, {'marker': '2.', 'text': '1 Corinthians 8:11.'}, {'marker': '3.', 'text': '2 Pet...; whitelist_key: EPUB/ch021.xhtml#p714-syllabus-chapter-5-the-last-objection-or-argument-from-scripture-answered
- action: likely_false_positive; file: EPUB/ch021.xhtml; anchor_index: 726; item_range: p727-p736; marker_family: arabic; item_count: 10; announced_count: None; anchor: Arg. 6. From Scripture assertions and consequences. Answers to the proofs of this sixth argument: —; items: [{'marker': '1.', 'text': 'From 1 John 4:14; John 1:4, 7; 1 Timothy 2:4.'}, {'marker': '2.', 'text': 'From some texts before vindicated.'}, {'marker': '3.', 'text': 'From Psalm 19:4; Romans 10:18; Acts 14:17, etc.'}, {'marker': '4.', 'te...; whitelist_key: EPUB/ch021.xhtml#p726-syllabus-arg-6-from-scripture-assertions-and-consequences-answers-to-the-proofs-of
- action: likely_false_positive; file: EPUB/ch021.xhtml; anchor_index: 729; item_range: p730-p739; marker_family: arabic; item_count: 10; announced_count: None; anchor: 3. From Psalm 19:4; Romans 10:18; Acts 14:17, etc.; items: [{'marker': '4.', 'text': 'From John 16:7-11, etc.'}, {'marker': '5.', 'text': 'From Ezekiel 18:23, 32, 33:11, etc.'}, {'marker': '6.', 'text': 'From Matthew 28:19, 20; Mark 16:15; Isaiah 45:22, etc.'}, {'marker': '7.', 'text': 'From Act...; whitelist_key: EPUB/ch021.xhtml#p729-syllabus-3-from-psalm-19-4-romans-10-18-acts-14-17-etc
- action: likely_false_positive; file: EPUB/ch021.xhtml; anchor_index: 733; item_range: p734-p743; marker_family: arabic; item_count: 10; announced_count: None; anchor: 7. From Acts 2:38, 39, etc.; items: [{'marker': '8.', 'text': 'From 1 Corinthians 15:21, 22, 45-47; Romans 3:22-25, etc.'}, {'marker': '9.', 'text': 'From Matthew 28:19, 20; 2 Corinthians 5:19, etc.'}, {'marker': '10.', 'text': 'From Matthew 5:44, 48; 1 Timothy 2:1-4, etc....; whitelist_key: EPUB/ch021.xhtml#p733-syllabus-7-from-acts-2-38-39-etc
- action: likely_false_positive; file: EPUB/ch031.xhtml; anchor_index: 1004; item_range: p1005-p1007; marker_family: arabic; item_count: 3; announced_count: None; anchor: cludes nothing but an assertion of the true God and dependence on him, in opposition to all the idols of the Gentiles, and other vain conceits whereby they exalted themselves into the throne of the Most High. But that Christ should be sa...; items: [{'marker': '1.', 'text': 'Those who are never saved from their sins, as he saves his people, Matthew 1:21; —'}, {'marker': '2.', 'text': 'Of those who never hear one word of saving or a Savior; —'}, {'marker': '3.', 'text': 'That he sho...; whitelist_key: EPUB/ch031.xhtml#p1004-syllabus-if-any-shall-conceive-that-these-words-because-we-hope-in-the
- action: likely_false_positive; file: EPUB/ch046.xhtml; anchor_index: 1413; item_range: p1414-p1420; marker_family: unknown; item_count: 7; announced_count: None; anchor: 3. Consider what it is to lie under the effects of God's wrath, according to the declaration of the Scripture, and then see how the elect are delivered therefrom, before their actual calling. Now, this consists in divers things; as, —; items: [{'marker': '(1.)', 'text': 'To be in such a state of alienation from God as that none of their services are acceptable to him: "The prayer of the wicked is an abomination to the LORD," Proverbs 28:9.'}, {'marker': '(2.)', 'text': 'To ha...; whitelist_key: EPUB/ch046.xhtml#p1413-syllabus-3-consider-what-it-is-to-lie-under-the-effects-of-god
- action: likely_false_positive; file: EPUB/ch046.xhtml; anchor_index: 1415; item_range: p1416-p1420; marker_family: unknown; item_count: 5; announced_count: None; anchor: (2.) To have no outward enjoyment sanctified, but to have all things unclean unto them, Titus 1:15.; items: [{'marker': '(3.)', 'text': 'To be under the power of Satan who rules at his pleasure in the children of disobedience, Ephesians 2:2.'}, {'marker': '(4.)', 'text': 'To be in bondage unto death, Hebrews 2:15.'}, {'marker': '(5.)', 'text':...; whitelist_key: EPUB/ch046.xhtml#p1415-syllabus-2-to-have-no-outward-enjoyment-sanctified-but-to-have-all-things

## Suspicious Large-Number Starts

- file: EPUB/ch058.xhtml; text: 13. [A.D. 350]: —
- file: EPUB/ch085.xhtml; text: 389 It remains, then, that we should now consider, in the third place, what testimony God has given, and is still giving, to this essential attribute of his in the works of providence. This Paul takes notice of, Romans 1

## Roman Heading Candidates

- file: EPUB/ch058.xhtml; text: V. CYRIL of Jerusalem, Cataches.

## Short Fragments

- file: EPUB/ch002.xhtml; text: JOHN WHITE
- file: EPUB/ch004.xhtml; text: TO THE CHRISTIAN READER.
- file: EPUB/ch018.xhtml; text: Τῷ Θεῷ ἀριστομεγίστῳ δόξα .
- file: EPUB/ch021.xhtml; text: I.
- file: EPUB/ch021.xhtml; text: II.
- file: EPUB/ch022.xhtml; text: TO THE READER.
- file: EPUB/ch022.xhtml; text: READER,
- file: EPUB/ch027.xhtml; text: Whence he saith,
- file: EPUB/ch030.xhtml; text: VI.
- file: EPUB/ch048.xhtml; text: Arg. 15.

## Repeated Windows

- phrase: that we might be made the righteousness of god in; count: 13
- phrase: we might be made the righteousness of god in him; count: 13
- phrase: made him to be sin for us who knew no; count: 8
- phrase: him to be sin for us who knew no sin; count: 8
- phrase: hath set forth to be propitiation through faith in his; count: 7
- phrase: set forth to be propitiation through faith in his blood; count: 7
- phrase: propitiation through faith in his blood to declare his righteousness; count: 7
- phrase: to be sin for us who knew no sin that; count: 7
- phrase: known unto god are all his works from the beginning; count: 6
- phrase: even so father for so it seemed good in thy; count: 6

## Excess Word Samples

- word: historical; pdf: 2; epub: 10
- word: digital; pdf: 0; epub: 8
- word: chapters; pdf: 5; epub: 12
- word: footnotes; pdf: 0; epub: 7
- word: modern; pdf: 5; epub: 11

## Untagged Latin Word Samples

- word: ejusdem; epub: 17; tagged: 2
- word: tantidem; epub: 12; tagged: 0
- word: scotus; epub: 4; tagged: 0
- word: mediate; epub: 3; tagged: 0
- word: apella; epub: 4; tagged: 1
- word: intermediate; epub: 3; tagged: 0
- word: clamor; epub: 3; tagged: 0
- word: rumor; epub: 3; tagged: 0
- word: expiate; epub: 3; tagged: 0
- word: diatriba; epub: 3; tagged: 0

## Untranslated Latin Samples

- phrase: Elenchus Controversiarum
- phrase: Martii, anno Domini
- phrase: Tantum religio
- phrase: suadere malorum
- phrase: in quibus possimus
- phrase: AEneas Sylvius
- phrase: in forma pauperis
- phrase: postquam Christiana
- phrase: gradibus itur in coelum
- phrase: cornicula risum, furtivis nudata coloribus

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
