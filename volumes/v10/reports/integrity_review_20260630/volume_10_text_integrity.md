# Text Integrity Audit: Volume 10

- Status: **WARN**
- Warnings: 13
- PDF pages: 828
- EPUB text files: 105
- EPUB paragraphs/headings: 3299

## Coverage

- PDF content tokens: 265658
- EPUB content tokens: 263203
- Approximate PDF-to-EPUB coverage ratio: 0.9881
- Pages checked: 817
- Weak page matches: 11
- Dense source windows checked: 35099
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 4
- Top-of-page body windows checked: 776
- Top-of-page windows skipped as unstable: 7
- Missing top-of-page body windows: 5
- Bottom-of-page body windows checked: 704
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 4

## Paragraphs

- Body paragraphs checked: 2696
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 190
- Short fragments: 33
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 5
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 185
- EPUB enumerator markers: 196
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 838
- EPUB Greek words: 845
- Greek word coverage ratio: 0.9951
- PDF Hebrew words: 18
- EPUB Hebrew words: 18
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 41
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 1960
- EPUB Latin words: 1929
- EPUB Tagged Latin words: 868
- Latin word coverage ratio: 0.9755
- Latin word tagging ratio: 0.45
- Latin clauses checked: 98
- Missing Latin clauses: 2
- Tagged Latin runs checked: 270
- Translated Latin runs: 110
- Latin translation ratio: 0.4074

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: contents of θεομαχια αττεξουσιαστικη display of arminianism prefatory note by the editor epistle dedicatory
- page: 4; sample: salus electorum sanguis jesu or the death of death in the death of christ
- page: 5; sample: book arguments against the universality of redemption the two first from the nature of
- page: 6; sample: the removal of other remaining objections some few testimonies of the ancients an appendix
- page: 7; sample: formerly taught about the death of christ upon the principles now delivered dissertation on
- page: 8; sample: of the argument the same concluded the third argument this divine attribute demonstrated in
- page: 9; sample: natural and positive right positive right what description also of natural right concessions of
- page: 10; sample: conclusion of the answer to twisse's principal arguments the defense of sibrandus lubbertus against
- page: 11; sample: delay of punishment and its various dispensations the conclusion of this dissertation the uses
- page: 12; sample: θεομαχια αυτεξουσιαστικη display of arminianism being discovery of the old pelagian idol free-will with

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.0; sample: contents of θεομαχια αττεξουσιαστικη display of arminianism prefatory note by the editor epistle dedicatory to the christian reader θεμοχιας αυτεξουσιαστικης specimen of the two main ends aimed at
- page: 4; hit_ratio: 0.25; sample: salus electorum sanguis jesu or the death of death in the death of christ prefatory note by the editor epistle dedicatory two attestations touching the ensuing treatise to
- page: 5; hit_ratio: 0.25; sample: book arguments against the universality of redemption the two first from the nature of the new covenant and the dispensation thereof containing three other arguments containing two other
- page: 6; hit_ratio: 0.5; sample: the removal of other remaining objections some few testimonies of the ancients an appendix in reply to mr joshua sprigge of the death of christ prefatory note by

## Missing Top-Of-Page Body Windows

- page: 6; sample: 7. — The removal of other remaining objections, Some few Testimonies of the Ancients,
- page: 63; sample: "Unite my heart to fear thy or to one part of the
- page: 91; sample: "What hast thou that thou didst The sum of their doctrine is: God
- page: 136; sample: "Thou hast wrought all our works "Faith and conversion cannot be
- page: 649; sample: TO HIS ILLUSTRIOUS HIGHNESS LORD OLIVER CROMWELL, OF ENGLAND,

## Missing Bottom-Of-Page Body Windows

- page: 39; sample: standeth for ever, the thoughts of certain time," Episcop.
- page: 90; sample: determineth of them," Corr. pleasing to God," Rem. Apol.
- page: 112; sample: he him; male and female created he not so vehement and inordinate
- page: 142; sample: on the Gentiles through Jesus only way of salvation be the

## Possible Paragraph Splits

- file: EPUB/ch002.xhtml; previous: ered, by the Committee of the House of Commons in Parliament for the Regulating of Printing and Publishing of Books, That this book, entitled "A Display of Arminianism," be printed; next: JOHN WHITE
- file: EPUB/ch006.xhtml; previous: n the Arminian doctrine concerning God's decrees, I will in brief present to your view the opposition that is in this matter betwixt the word of God and the patrons of free-will: —; next: S.S. Lib. Arbit. "He hath chosen us in him before the foundation of the world," Ephesians 1:4.
- file: EPUB/ch007.xhtml; previous: nd of consolation. Now, to present in one view how opposite the opinions of the worshippers of the great goddess contingency are to this sacred truth, take this short antithesis: —; next: S.S. Lib. Arbit. "Known unto God are all his works from the beginning of the world," Acts 15:18.
- file: EPUB/ch008.xhtml; previous: oreknowledge of such things to be fallible and easily to be deceived; so that there is no reconciliation possible to be hoped for betwixt these following and the like assertions: —; next: S.S. Lib. Arbit. "In him we live, and move, and have our being," Acts 17:28.
- file: EPUB/ch009.xhtml; previous: 3. And these few instances will manifest the Arminian opposition to the word of God in this particular: —; next: S.S. Lib. Arbit. "Our God is in the heavens: he hath done whatsoever he hath pleased," Psalm 115:3.
- file: EPUB/ch010.xhtml; previous: it, with sundry other false assertions and heretical positions of the Arminians about this fundamental article of our religion, concluding this chapter with the following scheme: —; next: S.S. Lib. Arbit. "Whom he did foreknow, he also did predestinate to be conformed to the image of his Son, that he might be the first-born among many brethren. Moreover whom he did
- file: EPUB/ch011.xhtml; previous: ondemned, cursed, and exploded. Now, amongst those many motives they had to proceed so severely against this heresy, one especially inculcated deserves our consideration, namely, —; next: That it overthrew the necessity of Christ's coming into the world to redeem mankind. It is sin only that makes a Savior necessary; and shall Christians tolerate such an error as, b
- file: EPUB/ch011.xhtml; previous: our church, agreeable to the Scripture, affirming the desert of original sin to be God's wrath and damnation. To both which how opposite is the Arminian doctrine may thus appear: —; next: S.S. Lib. Arbit. "By the offense of one judgment came upon all men to condemnation," Romans 5:18.
- file: EPUB/ch012.xhtml; previous: ve it; and I am certain it will be long enough. But this, I say, belongs not to this place; only, let us see how, from the word of God, we may overthrow the former odious heresy: —; next: God in the beginning "created man in his own image," Genesis 1:27, — that is, "upright," Ecclesiastes 7:29, endued with a nature composed to obedience and holiness. That habitual g
- file: EPUB/ch013.xhtml; previous: s in Christianity; for my part, in these following contradictory assertions I will choose rather to adhere to the authority of the word of God than of Arminius and his sectaries: —; next: S.S. Lib. Arbit. "He made him to be sin for us, who knew no sin; that we might be made the righteousness of God in him," 2 Corinthians 5:21. "He loved the church, and gave himself

## Inline Structural Marker Candidates

- file: EPUB/ch020.xhtml; text: In 1650, Mr. Home, minister at Lynn in Norfolk, a man, according to Palmer (Nonconf. Mem., 3. pp. 6, 7), "of exemplary and primitive piety," and author of several works, published a reply to Owen's work, under the title, "The Open Door f...

## Suspicious Large-Number Starts

- file: EPUB/ch013.xhtml; text: 36. To abide argueth a continued, uninterrupted act.
- file: EPUB/ch014.xhtml; text: 96. All which assertions, how contrary they are to the express word of God, I shall now demonstrate.
- file: EPUB/ch058.xhtml; text: 13. [A.D. 350]: —
- file: EPUB/ch084.xhtml; text: 117. And again, Aristotle says, "It is a very strong proof, if all shall agree in what we shall say." And in that observation another author concurs: "The things that are commonly agreed on are worthy of credit." And her
- file: EPUB/ch085.xhtml; text: 389 It remains, then, that we should now consider, in the third place, what testimony God has given, and is still giving, to this essential attribute of his in the works of providence. This Paul takes notice of, Romans 1

## Roman Heading Candidates

- file: EPUB/ch058.xhtml; text: V. CYRIL of Jerusalem, Cataches.

## Short Fragments

- file: EPUB/ch002.xhtml; text: JOHN WHITE
- file: EPUB/ch004.xhtml; text: TO THE CHRISTIAN READER.
- file: EPUB/ch018.xhtml; text: Τῷ Θεῷ ἀριστομεγίστῳ δόξα .
- file: EPUB/ch021.xhtml; text: 1 . Of the work;
- file: EPUB/ch022.xhtml; text: TO THE READER.
- file: EPUB/ch022.xhtml; text: READER,
- file: EPUB/ch027.xhtml; text: Whence he saith,
- file: EPUB/ch030.xhtml; text: VI.
- file: EPUB/ch048.xhtml; text: Arg. 15.
- file: EPUB/ch053.xhtml; text: Where, —

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

## Missing Word Samples

- word: editor; pdf: 4; epub: 1
- word: dedicatory; pdf: 3; epub: 0

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 11; epub: 20
- word: modern; pdf: 5; epub: 12
- word: chapters; pdf: 5; epub: 12
- word: historical; pdf: 3; epub: 10
- word: footnotes; pdf: 0; epub: 7
- word: hebrew; pdf: 3; epub: 9
- word: edition; pdf: 2; epub: 8

## Untagged Latin Word Samples

- word: grotius; epub: 55; tagged: 0
- word: socinus; epub: 38; tagged: 2
- word: arminius; epub: 37; tagged: 1
- word: creditor; epub: 37; tagged: 2
- word: ipso; epub: 29; tagged: 1
- word: corvinus; epub: 28; tagged: 1
- word: debtor; epub: 22; tagged: 0
- word: lubbertus; epub: 23; tagged: 2
- word: solutio; epub: 23; tagged: 2
- word: thomas; epub: 22; tagged: 2

## Missing Latin Clauses

- page: 4; word_count: 5; sample: salus electorum sanguis jesu or
- page: 170; word_count: 5; sample: salus electorum sanguis jesu or

## Untranslated Latin Samples

- phrase: Elenchus Controversiarum
- phrase: Socinus, "quae
- phrase: Junius, ‡ Arminius
- phrase: Martii, anno Domini
- phrase: in quibus possimus
- phrase: AEneas Sylvius
- phrase: in forma pauperis
- phrase: postquam Christiana
- phrase: gradibus itur in coelum
- phrase: cornicula risum, furtivis nudata coloribus

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
