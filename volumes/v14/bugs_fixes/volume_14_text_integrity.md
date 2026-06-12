# Text Integrity Audit: Volume 14

- Status: **WARN**
- Warnings: 9
- PDF pages: 661
- EPUB text files: 70
- EPUB paragraphs/headings: 1709

## Coverage

- PDF content tokens: 230479
- EPUB content tokens: 231220
- Approximate PDF-to-EPUB coverage ratio: 0.9989
- Pages checked: 653
- Weak page matches: 3
- Dense source windows checked: 31142
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 3
- Top-of-page body windows checked: 619
- Top-of-page windows skipped as unstable: 0
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 605
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 2

## Paragraphs

- Body paragraphs checked: 1377
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 147
- Short fragments: 15
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 4
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 3
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 130
- EPUB enumerator markers: 140
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1246
- EPUB Greek words: 1246
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 51
- EPUB Hebrew words: 51
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 64
- Missing Greek clauses: 0
- Hebrew clauses checked: 2
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 4240
- EPUB Latin words: 4282
- EPUB Tagged Latin words: 2541
- Latin word coverage ratio: 0.9967
- Latin word tagging ratio: 0.5934
- Latin clauses checked: 312
- Missing Latin clauses: 2
- Tagged Latin runs checked: 694
- Translated Latin runs: 338
- Latin translation ratio: 0.487

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 4; sample: note by the editor to the reader chap an answer to the preface or
- page: 5; sample: proposals from protestant principles tending unto moderation and unity farther vindication of the second
- page: 10; sample: to the reader reader the treatise entitled fiat lux which thou wilt find examined
- page: 14; sample: them being not in those days in rerum natura way of handling religion he
- page: 31; sample: are not now in rerum natura knowing what will ensue to their disadvantage on
- page: 36; sample: close and safe all the long-billed birds that he hoped to lime twig by
- page: 39; sample: we say plainly that she fell by she fell by apostasy from many of
- page: 40; sample: ask of this or that age or of the first of the first certainly
- page: 49; sample: sense but hic nigrae succus loliginis haec est aerugo mera hor sat suppose they
- page: 58; sample: chapter motive matter and method of our author's book what remains of our author's

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.25; sample: contents of animadversions on treatise entitled fiat lux prefatory note by the editor to the reader preface chap our author's preface and his method heathen pleas general principles
- page: 5; hit_ratio: 0.0; sample: proposals from protestant principles tending unto moderation and unity farther vindication of the second chapter of the animadversions the remaining principles of fiat lux considered judicious readers schoolmen
- page: 6; hit_ratio: 0.25; sample: communion heroes of the ass's head whose worship was objected to jews and christians the church of rome no safe guide prefatory note by the editor preface some

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 5; sample: the pretenses for image-worship examined and disproved 22. — Of Latin service

## Inline Structural Marker Candidates

- file: EPUB/ch030.xhtml; text: And I know that, concerning all your dispute and arguings in these pages, you may say what Lucian doth about his "true story:" Γράφω τοίνυν περὶ ῶν μήτ εῖδον , μήτ ἔπαθον , μήτε παρ ἄλλων ἐπυθόμην ? — "You write about the things which yo...
- file: EPUB/ch033.xhtml; text: Do you think it so easy for you, " Cornicum oculos, configere," as Cicero tells us an attorney, one Cn. Flavius, thought to do, in going beyond all that the great lawyers had done before him, Orat. pro Muraena , 11. We cannot yet be pers...
- file: EPUB/ch041.xhtml; text: Some few observations upon this discourse of yours will farther manifest the absurdity of that consequence which you feign not to have been taken notice of in the "Animadversions;" for which you had no cause, but that you might easily di...
- file: EPUB/ch044.xhtml; text: Our Savior gave them equal commission to teach all nations; told them that as his Father had sent him so he sent them; that he had chosen them twelve, but that one of them was a devil, — never that one of them should be pope. Their insti...

## Suspicious Large-Number Starts

- file: EPUB/ch031.xhtml; text: 27. In the explication of your distinction of "congruity" and "condignity," how woefully are you divided! as also in the application of it. There is no end of your altercations about it, the terms of it being horrid, unc
- file: EPUB/ch033.xhtml; text: 30. And he hath done well to record them, that they might be preserved " in perpetuam rei memoriam ," that we might learn what your great father exercised himself about, —
- file: EPUB/ch033.xhtml; text: 11. And that of Basil condemned Engenius as one " a fide devium et pertinacem haereticum," sess. 34; — "an erroneous person and obstinate heretic." Other instances of the like nature might be called over, manifesting tha

## Short Fragments

- file: EPUB/ch003.xhtml; text: READER,
- file: EPUB/ch003.xhtml; text: Farewell.
- file: EPUB/ch027.xhtml; text: Decemb. 9, 1663.
- file: EPUB/ch029.xhtml; text: To The Reader.
- file: EPUB/ch029.xhtml; text: CHRISTIAN READER,
- file: EPUB/ch030.xhtml; text: Hesiod. Εργ . καὶ ἡμ .
- file: EPUB/ch030.xhtml; text: And, —
- file: EPUB/ch035.xhtml; text: Hor. ad. Pis . 150.
- file: EPUB/ch036.xhtml; text: And, —
- file: EPUB/ch037.xhtml; text: Well said he of old, —

## Enumerator Sequence Candidates

- file: EPUB/ch033.xhtml; marker: (7.); family: paren_decimal; context: (7.) " Quod illi soli licet, pro temporis necessitate, novas leges condere;" — "That he alone, as necessity requires, can make new laws." Let him proceed.
- file: EPUB/ch033.xhtml; marker: (11.); family: paren_decimal; context: (11.) " Quod unicum est nomen in mundo, — papae scilicet ;" — "That there is only one name in the world, — into wit, that of the pope;" no other name, it seems, given under heaven. Once

## Repeated Windows

- phrase: chapter farther vindication of the second chapter of the animadversions; count: 3
- phrase: that whence and from whom we first received our religion; count: 3
- phrase: whence and from whom we first received our religion there; count: 3
- phrase: and from whom we first received our religion there and; count: 3
- phrase: from whom we first received our religion there and with; count: 3
- phrase: whom we first received our religion there and with them; count: 3
- phrase: we first received our religion there and with them we; count: 3
- phrase: that the roman profession of religion and practice in the; count: 3
- phrase: the roman profession of religion and practice in the worship; count: 3
- phrase: roman profession of religion and practice in the worship of; count: 3

## Missing Word Samples

- word: pre; pdf: 5; epub: 2
- word: eminence; pdf: 5; epub: 2

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 5; epub: 14
- word: historical; pdf: 1; epub: 9
- word: modern; pdf: 2; epub: 9
- word: footnotes; pdf: 0; epub: 7

## Untagged Latin Word Samples

- word: celsus; epub: 44; tagged: 0
- word: prelate; epub: 26; tagged: 0
- word: dissent; epub: 24; tagged: 0
- word: emperor; epub: 23; tagged: 0
- word: pleas; epub: 22; tagged: 0
- word: ago; epub: 21; tagged: 0
- word: adhere; epub: 20; tagged: 0
- word: anno; epub: 22; tagged: 5
- word: credo; epub: 15; tagged: 0
- word: eleutherius; epub: 15; tagged: 0

## Missing Latin Clauses

- page: 259; word_count: 24; sample: deos suos venerabantur vel pannum rubrum in hastam elevatum quod narratur de
- page: 520; word_count: 5; sample: in rerum natura is as

## Untranslated Latin Samples

- phrase: ultima Papae
- phrase: mihi ostentatam, tantam, tam bonam, tam optatam, tam insperatam
- phrase: Oculis male lippus inunctis
- phrase: in amicorum vitiis tam cernis acutum, Quam
- phrase: ancillam cum filio suo
- phrase: loca nullius ante Trita solo
- phrase: Hor, ad Pis
- phrase: Ephesus, Smyrna, Laodicea, Alexandria
- phrase: Erugo mera," [Hor
- phrase: Petrus, tibi dabo

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
