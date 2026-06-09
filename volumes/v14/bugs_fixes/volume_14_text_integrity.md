# Text Integrity Audit: Volume 14

- Status: **WARN**
- Warnings: 14
- PDF pages: 661
- EPUB text files: 70
- EPUB paragraphs/headings: 1646

## Coverage

- PDF content tokens: 230477
- EPUB content tokens: 227537
- Approximate PDF-to-EPUB coverage ratio: 0.9845
- Pages checked: 653
- Weak page matches: 15
- Dense source windows checked: 31012
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 3
- Top-of-page body windows checked: 619
- Top-of-page windows skipped as unstable: 13
- Missing top-of-page body windows: 9
- Bottom-of-page body windows checked: 605
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 17

## Paragraphs

- Body paragraphs checked: 1315
- Possible faulty paragraph splits: 4
- Structural starts excluded from split warnings: 126
- Short fragments: 13
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 6
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 5
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 130
- EPUB enumerator markers: 129
- Missing enumerator marker forms: 7
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1246
- EPUB Greek words: 1250
- Greek word coverage ratio: 0.9917
- PDF Hebrew words: 51
- EPUB Hebrew words: 51
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 64
- Missing Greek clauses: 2
- Hebrew clauses checked: 2
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 5634
- EPUB Latin words: 5625
- EPUB Tagged Latin words: 0
- Latin word coverage ratio: 0.9883
- Latin word tagging ratio: 0.0
- Latin clauses checked: 318
- Missing Latin clauses: 1
- Tagged Latin runs checked: 0
- Translated Latin runs: 0
- Latin translation ratio: 1.0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 4; sample: note by the editor to the reader chap an answer to the preface or
- page: 5; sample: proposals from protestant principles tending unto moderation and unity farther vindication of the second
- page: 7; sample: animadversions on treatise entitled fiat lux or guide in differences of religion between papist
- page: 10; sample: to the reader reader the treatise entitled fiat lux which thou wilt find examined
- page: 36; sample: close and safe all the long-billed birds that he hoped to lime twig by
- page: 39; sample: we say plainly that she fell by she fell by apostasy from many of
- page: 40; sample: ask of this or that age or of the first of the first certainly
- page: 49; sample: sense but hic nigrae succus loliginis haec est aerugo mera hor sat suppose they
- page: 58; sample: chapter motive matter and method of our author's book what remains of our author's
- page: 83; sample: impossible to be kept if christ be not our law maker and director of

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.25; sample: contents of animadversions on treatise entitled fiat lux prefatory note by the editor to the reader preface chap our author's preface and his method heathen pleas general principles
- page: 5; hit_ratio: 0.0; sample: proposals from protestant principles tending unto moderation and unity farther vindication of the second chapter of the animadversions the remaining principles of fiat lux considered judicious readers schoolmen
- page: 6; hit_ratio: 0.25; sample: communion heroes of the ass's head whose worship was objected to jews and christians the church of rome no safe guide prefatory note by the editor preface some

## Missing Top-Of-Page Body Windows

- page: 621; sample: many of the professors of it, from the very first beginning of the Reformation, and which are continued unto this day.
- page: 622; sample: have accompanied or followed it; which, until they are removed, the weakness of the protestant interest, through mutual divisions, will remain
- page: 623; sample: conformity in canonical obedience, ceremonies, rites, and modes of worship, hath no other end but the sustentation and preservation thereof,
- page: 624; sample: both: which things are effectual engines to expel all peace and union among Protestants.
- page: 625; sample: preserve the protestant religion amongst us, to keep uniformity in the profession of it, and agreement amongst its professors, it is answered, —
- page: 626; sample: Nor is it morally possible that ever Popery should return into this or any other nation, but under the conduct of such a church constitution; without
- page: 627; sample: unto the interest of Popery, as it may be; it is possible some individual persons may be found that, for the sake of truth, will expose their lives to
- page: 628; sample: the days of Queen Elizabeth and King James, before the inroad of novel opinions among us, to be subscribed by all enjoying a public ministry.
- page: 629; sample: which themselves, by diligent prayer, sedulous preaching of the word, and an exemplary conversation, ought to labor for in the hearts of men.

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 5; sample: the pretenses for image-worship examined and disproved 22. — Of Latin service
- page: 274; sample: th~v ne>av JRw>mhv aJgiwta>tw| zro>nw|, eujlo>gwv kri>nantev th<n basilei>a| kai< sugklh>tw| timhqei~san po>lin, kai< tw~n i]swn ajpolau>ousan
- page: 389; sample: to oppose the truth which they maintain. And yet I know well enough what Aristotle hath taught us concerning to< lauza>nein to< ejn ajrch~, kai<
- page: 454; sample: au[th hJ uJpotagh>, kai< oujc j aJplw~v ei+pe piqe>sqw, ajll j uJpotasse>sqw
- page: 514; sample: jIsodunamou~si aiJ ti>miai eijko.nev tw~ euaggeli>w| — "Honorable images are equivalent to the gospel."
- page: 517; sample: ajpo>stolov ei]rhken, o[ti ta< shmei~a toi~v ajpi>stoiv ouj toi~v pisteu>ousi
- page: 541; sample: [Ewv me>n ejsti sumpepedhme>na ta< du>w xu>la tou~ staurou~ proskunw~ to<n tu>pon dia< Cristo<n to<n ejn aujtw~| staurwqe>nta,
- page: 620; sample: 3. The only weakness in it, as the interest of the nation (before it was infested with novel opinions), was the differences that have been amongst
- page: 621; sample: established. Yet experience manifests that, partly from its constitution, partly from the inclinations of them by whom it is managed, other evils

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: READER,; next: THE treatise entitled "Fiat Lux," which thou wilt find examined in the ensuing discourse, was lent unto me, not long since, by an honorable person, with a request to return an answ
- file: EPUB/ch029.xhtml; previous: CHRISTIAN READER,; next: ALTHOUGH our Lord Jesus Christ hath laid blessed and stable foundations of unity, peace, and agreement in judgment and affection amongst all his disciples, and given forth command
- file: EPUB/ch045.xhtml; previous: r thou be an apostle, or an evangelist, or a prophet, or whatever thou be; for subjection overthrows not piety. And he saith not simply, 'Let him obey,' but, 'Let him be subject.'"; next: The very same instances are given by Theodoret, Oecumenius, and Theophylact. Bernard, Epist. 42, ad Archiepisc. Senonena, meets with your exception, which in his days began to be b
- file: EPUB/ch050.xhtml; previous: τεύουσι — "But if any should say, 'Why do our images work no miracles?' to them we answer, 'Because,' as the apostle saith, 'signs are for unbelievers, not for them that believe.'"; next: And yet the misadventure of it is, that the most of the miracles which they report and build their faith upon were wrought as by, so amongst, their chiefest believers. And what wer

## Inline Structural Marker Candidates

- file: EPUB/ch030.xhtml; text: And I know that, concerning all your dispute and arguings in these pages, you may say what Lucian doth about his "true story:" Γράφω τοίνυν περὶ ῶν μήτ εῖδον , μήτ ἔπαθον , μήτε παρ ἄλλων ἐπυθόμην ? — "You write about the things which yo...
- file: EPUB/ch033.xhtml; text: Do you think it so easy for you, "Cornicum oculos, configere," as Cicero tells us an attorney, one Cn. Flavius, thought to do, in going beyond all that the great lawyers had done before him, Orat. pro Muraena, 11. We cannot yet be persua...
- file: EPUB/ch038.xhtml; text: The present face of Christianity makes the worm a wearisome wilderness; nor should I think any thing a more necessary duty than it would be for persons of piety and ability to apologize for the religion of Jesus Christ, and to show how u...
- file: EPUB/ch041.xhtml; text: Some few observations upon this discourse of yours will farther manifest the absurdity of that consequence which you feign not to have been taken notice of in the "Animadversions;" for which you had no cause, but that you might easily di...
- file: EPUB/ch044.xhtml; text: Our Savior gave them equal commission to teach all nations; told them that as his Father had sent him so he sent them; that he had chosen them twelve, but that one of them was a devil, — never that one of them should be pope. Their insti...
- file: EPUB/ch059.xhtml; text: (2.) the oppression of Nonconformists in order that its claims and dignity might be upheld; and (3.) the spirit it fostered of subserviency to royal aggrandizement, in order to secure a share in the preferment which is under the patronag...

## Suspicious Large-Number Starts

- file: EPUB/ch030.xhtml; text: 15. 20 In their steps you set out in this your first reason, wherein there is not one word of truth. I had formerly told you that I Aid not think you could yourself believe some of the things that you affirmed, at which
- file: EPUB/ch031.xhtml; text: 41. "A supernatural work," saith he, "proceeding from grace, in itself, and in its own nature, hath a proportion unto and condignity of the reward, and is of sufficient value to be worth the same." And you seem to be of
- file: EPUB/ch031.xhtml; text: 27. In the explication of your distinction of "congruity" and "condignity," how woefully are you divided! as also in the application of it. There is no end of your altercations about it, the terms of it being horrid, unc
- file: EPUB/ch033.xhtml; text: 30. And he hath done well to record them, that they might be preserved "in perpetuam rei memoriam," that we might learn what your great father exercised himself about, —
- file: EPUB/ch033.xhtml; text: 11. And that of Basil condemned Engenius as one "a fide devium et pertinacem haereticum," sess. 34; — "an erroneous person and obstinate heretic." Other instances of the like nature might be called over, manifesting that

## Short Fragments

- file: EPUB/ch003.xhtml; text: READER,
- file: EPUB/ch003.xhtml; text: Farewell.
- file: EPUB/ch029.xhtml; text: To The Reader.
- file: EPUB/ch029.xhtml; text: CHRISTIAN READER,
- file: EPUB/ch030.xhtml; text: Hesiod. Εργ . καὶ ἡμ .
- file: EPUB/ch032.xhtml; text: which of old she professed!
- file: EPUB/ch035.xhtml; text: Hor. ad. Pis. 150.
- file: EPUB/ch036.xhtml; text: And, —
- file: EPUB/ch040.xhtml; text: I wish we had agreed beforehand,
- file: EPUB/ch045.xhtml; text: God, Christ, Minister, People.

## Missing Enumerator Markers

- marker: (1.); pdf: 29; epub: 27; examples: [{'location': 'pdf:p40', 'context': 'all by heresy, I add, that she is thus fallen also from what she was. But then he asks, — (1.) "By what general council was she ever condemned?" (2.) "Which of the fathers ever wrote against her? By w...
- marker: (2.); pdf: 32; epub: 30; examples: [{'location': 'pdf:p40', 'context': 'what she was. But then he asks, — (1.) "By what general council was she ever condemned?" (2.) "Which of the fathers ever wrote against her? By what authority was she otherwise reproved?" But this is a...
- marker: (3.); pdf: 22; epub: 20; examples: [{'location': 'pdf:p276', 'context': 'ope Gregory I. taught them that he who assumed that title was a forerunner of antichrist. (3.) "Quod ille solus possit deponere episcopos, vel reconciliare;" — "That he alone can depose bishops, or r...
- marker: (4.); pdf: 10; epub: 9; examples: [{'location': 'pdf:p308', 'context': 'mneth as heretical, as you are bound to believe what it pro-poseth for Catholic doctrine. (4.) I desire to know when a man who lives here in England begins to be obliged to believe the determinations...
- marker: (5.); pdf: 4; epub: 3; examples: [{'location': 'pdf:p502', 'context': 'ests; so that the context ex-dudes your sense. The same is the interpretation of Erasmus. (5.) Your vulgar Latin [the Vulgate] reads the words, "administrantibus Domino," as they were "ministering un...
- marker: [3.]; pdf: 2; epub: 1; examples: [{'location': 'pdf:p598', 'context': 'e unto that resignation of themselves unto the church of Rome which it requireth of them. [3.] They have a guide promised unto them, to give them an understanding of the rule in the discharge of this...
- marker: [4.]; pdf: 1; epub: 0; examples: [{'location': 'pdf:p628', 'context': 'of the land, or all parochial churches; the care whereof is incumbent on the magistrates. [4.] Let the church be protected in the exercise of its spiritual power by spiritual means only, — as preachi...

## Enumerator Sequence Candidates

- file: EPUB/ch033.xhtml; marker: (7.); family: paren_decimal; context: (7.) "Quod illi soli licet, pro temporis necessitate, novas leges condere;" — "That he alone, as necessity requires, can make new laws." Let him proceed.
- file: EPUB/ch033.xhtml; marker: (11.); family: paren_decimal; context: (11.) "Quod unicum est nomen in mundo, — papae scilicet;" — "That there is only one name in the world, — into wit, that of the pope;" no other name, it seems, given under heaven. Once m

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

- word: national; pdf: 18; epub: 7
- word: authoritative; pdf: 17; epub: 8
- word: constitution; pdf: 17; epub: 8
- word: liberties; pdf: 13; epub: 5
- word: courts; pdf: 8; epub: 3
- word: unnecessary; pdf: 6; epub: 2
- word: magistrates; pdf: 5; epub: 1
- word: estates; pdf: 5; epub: 2
- word: pre; pdf: 5; epub: 2
- word: eminence; pdf: 5; epub: 2

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: modern; pdf: 2; epub: 11
- word: footnotes; pdf: 0; epub: 6

## Missing Greek Clauses

- page: 209; word_count: 47; sample: αρχομενοι μεν ολιγοι τε ησαν και εν εφρονουν ες πληθος δε σπαρεντες
- page: 235; word_count: 8; sample: εχθρος γαρ μοι κεινος ομως αιδαο πυλησιν ος

## Untagged Latin Word Samples

- word: nor; epub: 471; tagged: 0
- word: et; epub: 122; tagged: 0
- word: jesus; epub: 111; tagged: 0
- word: yea; epub: 84; tagged: 0
- word: non; epub: 66; tagged: 0
- word: whereas; epub: 65; tagged: 0
- word: whereunto; epub: 52; tagged: 0
- word: est; epub: 51; tagged: 0
- word: endeavor; epub: 48; tagged: 0
- word: de; epub: 45; tagged: 0

## Missing Latin Clauses

- page: 259; word_count: 24; sample: deos suos venerabantur vel pannum rubrum in hastam elevatum quod narratur de

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
