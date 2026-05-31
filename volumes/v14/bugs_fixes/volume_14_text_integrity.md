# Text Integrity Audit: Volume 14

- Status: **WARN**
- Warnings: 10
- PDF pages: 661
- EPUB text files: 69
- EPUB paragraphs/headings: 1726

## Coverage

- PDF content tokens: 231840
- EPUB content tokens: 232164
- Approximate PDF-to-EPUB coverage ratio: 0.9969
- Pages checked: 656
- Weak page matches: 3
- Dense source windows checked: 769
- Missing dense source-window pages: 636
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 621
- Top-of-page windows skipped as unstable: 13
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 607
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 7

## Paragraphs

- Body paragraphs checked: 1388
- Possible faulty paragraph splits: 75
- Structural starts excluded from split warnings: 164
- Short fragments: 14
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 3
- Overlong heading candidates: 21
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 130
- EPUB enumerator markers: 130
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1249
- EPUB Greek words: 1250
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 51
- EPUB Hebrew words: 51
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 64
- Missing Greek clauses: 0
- Hebrew clauses checked: 2
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 7; sample: animadversions on treatise entitled fiat lux or guide in differences of religion between papist
- page: 10; sample: 10 to the reader reader the treatise entitled fiat lux which thou wilt find
- page: 11; sample: 11 flourish withal are not vox ultima papae discovery of the inconsistency of his
- page: 12; sample: 12 preface considering the condition of affairs in these nations in reference to the
- page: 13; sample: 13 discontented individuals which hath been their constant employment but also come with their
- page: 14; sample: 14 advantage in his conjectures at the way and manner wherein he would proceed
- page: 15; sample: 15 no certainty or establishment for their faith in scripture but must for it
- page: 16; sample: 16 in my dealing with him shall not make it my business to defend
- page: 17; sample: 17 religion as some of them seem to be they come not within the
- page: 18; sample: 18 know none that can vie with the romanists in laying foundations of and

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 274; sample: th~v ne>av JRw>mhv aJgiwta>tw| zro>nw|, eujlo>gwv kri>nantev th<n basilei>a| kai< sugklh>tw| timhqei~san po>lin, kai< tw~n i]swn ajpolau>ousan
- page: 389; sample: to oppose the truth which they maintain. And yet I know well enough what Aristotle hath taught us concerning to< lauza>nein to< ejn ajrch~, kai<
- page: 454; sample: au[th hJ uJpotagh>, kai< oujc j aJplw~v ei+pe piqe>sqw, ajll j uJpotasse>sqw
- page: 514; sample: jIsodunamou~si aiJ ti>miai eijko.nev tw~ euaggeli>w| — "Honorable images are equivalent to the gospel."
- page: 517; sample: ajpo>stolov ei]rhken, o[ti ta< shmei~a toi~v ajpi>stoiv ouj toi~v pisteu>ousi
- page: 541; sample: [Ewv me>n ejsti sumpepedhme>na ta< du>w xu>la tou~ staurou~ proskunw~ to<n tu>pon dia< Cristo<n to<n ejn aujtw~| staurwqe>nta,

## Possible Paragraph Splits

- file: EPUB/ch001.xhtml; previous: EDITED BY; next: WILLIAM H. GOOLD
- file: EPUB/ch001.xhtml; previous: WILLIAM H. GOOLD; next: ANIMADVERSIONS ON A TREATISE ENTITLED "FIAT LUX."
- file: EPUB/ch001.xhtml; previous: PREFATORY NOTE BY THE EDITOR; next: Preface Chap. 1. — Our author's preface, and his method
- file: EPUB/ch001.xhtml; previous: 7. —; next: Use of reason
- file: EPUB/ch005.xhtml; previous: orld, began in Ireland, amongst his good Roman Catholics, who were blessed from Rome into rebellion and murder, somewhat before any drop of blood was shed in England or Scotland, —; next: Let them that are innocent throw stones at others: Roman Catholics are unfit to be employed in that work. But it was never judged either a safe or honest way to judge of any religi
- file: EPUB/ch006.xhtml; previous: works done in Christ, by his special grace, out of obedience to his command, with a promise of everlasting reward and intrinsic acceptability thence accruing." Thus we see still, —; next: Use of disputing has cast him, at the very entrance of his discourse, upon, as he supposeth, a particular controversy between Protestants and Roman Catholics, quite besides his des
- file: EPUB/ch007.xhtml; previous: f constitutive principles of that union and agreement which remains amongst them. But, whatever their evils be, it is pretended that they have a remedy at hand for them all. But, —; next: This I know, that a returnal unto Rome will not do it, unless, when we come thither, we can learn to behave ourselves better than those do who are there already; and there is indee
- file: EPUB/ch009.xhtml; previous: most of the great contests in the world about perishing things proceed from the unmortified lusts of men. The Scripture abounds in testimonies given hereunto: St. James expressly,; next: Men's lusts put them on endless irregularities, in unbounded desires, and foolish, sinful enterprises, for their satisfaction. Neither is Satan, the old enemy of the welfare of man
- file: EPUB/ch009.xhtml; previous: ns, doubtless promote them, and make men precipitate above their natural tempers in their productions; but the principal cause of all our evils is still to be looked for at home, —; next: Sect. 3 p. 34. In the next section of this chapter, whereunto he prefixes "Nullity of Title," he pursues the persuasive unto peace, moderation, charity, and quietness in our severa
- file: EPUB/ch011.xhtml; previous: would not denounce an anathema against such a defense of any religion whatever. But you will say, the same person defends also the Scripture, just as he in the poet did Pelilius: —; next: A defense worse and more bitter than a downright accusation. I am not now to observe what prejudice this excuse brings to the cause of our author with all intelligent persons, havi

## Inline Structural Marker Candidates

- file: EPUB/ch031.xhtml; text: And I know that, concerning all your dispute and arguings in these pages, you may say what Lucian doth about his "true story:" Γράφω τοίνυν περὶ ῶν μήτ εῖδον , μήτ ἔπαθον , μήτε παρ ἄλλων ἐπυθόμην ? — "You write about the things which yo...

## Suspicious Large-Number Starts

- file: EPUB/ch031.xhtml; text: 15. 20 In their steps you set out in this your first reason, wherein there is not one word of truth. I had formerly told you that I Aid not think you could yourself believe some of the things that you affirmed, at which
- file: EPUB/ch032.xhtml; text: 27. In the explication of your distinction of "congruity" and "condignity," how woefully are you divided! as also in the application of it. There is no end of your altercations about it, the terms of it being horrid, unc
- file: EPUB/ch034.xhtml; text: 30. And he hath done well to record them, that they might be preserved "in perpetuam rei memoriam," that we might learn what your great father exercised himself about, —
- file: EPUB/ch034.xhtml; text: 11. And that of Basil condemned Engenius as one "a fide devium et pertinacem haereticum," sess. 34; — "an erroneous person and obstinate heretic." Other instances of the like nature might be called over, manifesting that

## Roman Heading Candidates

- file: EPUB/ch063.xhtml; text: II. Then follows an account of the way in which Protestantism had arisen; of the costly sacrifices made in order that it might be established, its martyrs exceeding in number those who had fallen under the Pagan persecut
- file: EPUB/ch063.xhtml; text: III. The political weakness of Protestantism, frown its manifold divisions, is exhibited, and the importance is urged of establishing a great Protestant interest throughout Europe.
- file: EPUB/ch063.xhtml; text: IV. Then follows a discussion of the probable way in which the Papacy may regain predominance; — either by defection, or force, or reconciliation. The author dwells chiefly on the danger to be apprehended frown the last

## Overlong Heading Candidates

- file: EPUB/ch007.xhtml; tag: h4; text: IX. "That the pope is a good man, one that seeks nothing but our good, that never did us harm, and hath the care and inspection of us committed unto him by Christ."
- file: EPUB/ch007.xhtml; tag: h4; text: III. That which is the main pillar, bearing the weight of all this fine fabric, is the principle we mentioned in the third place, — namely, "That the Roman profession of religion and practice in the worship of God are every way the same ...
- file: EPUB/ch007.xhtml; tag: h4; text: IV. It is frequently pleaded by our author (nor is there any thing which he more triumphs in), "That all things, as to religion, were quiet and in peace, all men in union and agreement amongst themselves in the worship of God, before the...
- file: EPUB/ch007.xhtml; tag: h4; text: V. "That the first reformers were most of them sorry, contemptible persons, whose errors were propagated by indirect means, and entertained for sinister ends," is in several places of this book alleged, and consequences, pretended thence...
- file: EPUB/ch007.xhtml; tag: h4; text: VI. "That our departure from Rome hath been the cause of all our evils, and particularly of all those divisions which are at this day found amongst Protestants, and which have been since the Reformation," is a supposition that not only i...
- file: EPUB/ch007.xhtml; tag: h4; text: VII. "That we have no remedy of our evils, no means of ending our differences, but by a returnal to the Roman see." Whether there be any way to end differences among ourselves, as far and as soon as there is any need they should be ended...
- file: EPUB/ch007.xhtml; tag: h4; text: IX. We are come at length unto the pope, of whom we are told that "he is a good man, one that seeks nothing but our good, that never did us harm, but has the care and inspection of us committed unto him by Christ." For my part I am glad ...
- file: EPUB/ch007.xhtml; tag: h4; text: X. The last principle which I have observed diffusing its influences throughout the whole discourse is, that "the devotion of Catholics far transcends that of Protestants; their preaching also" (which I forgot to mention before) "is far ...
- file: EPUB/ch034.xhtml; tag: h4; text: II. So infallible was he during his life, so infallible was he thought to be when he was dead, — whilst he lived he taught heresy, and when he was dead he was condemned for a heretic; and with him the principle which is the hinge of your...
- file: EPUB/ch037.xhtml; tag: h4; text: I. Protestants lay down this as the ἡ ἀρχὴ τῆς ὑποστάσεως καὶ ὁμολογίας , — as "the very beginning and first principle of their confidence and confession," — that all Scripture is given by inspiration of God, as the Holy Ghost teacheth t...

## Short Fragments

- file: EPUB/ch001.xhtml; text: EDITED BY
- file: EPUB/ch001.xhtml; text: WILLIAM H. GOOLD
- file: EPUB/ch001.xhtml; text: Use of reason
- file: EPUB/ch004.xhtml; text: Farewell.
- file: EPUB/ch028.xhtml; text: Decemb. 9, 1663.
- file: EPUB/ch030.xhtml; text: CHRISTIAN READER,
- file: EPUB/ch031.xhtml; text: Hesiod. Εργ . καὶ ἡμ .
- file: EPUB/ch036.xhtml; text: Hor. ad. Pis. 150.
- file: EPUB/ch037.xhtml; text: And, —
- file: EPUB/ch041.xhtml; text: I wish we had agreed beforehand,

## Enumerator Sequence Candidates

- file: EPUB/ch034.xhtml; marker: (7.); family: paren_decimal; context: (7.) "Quod illi soli licet, pro temporis necessitate, novas leges condere;" — "That he alone, as necessity requires, can make new laws." Let him proceed.
- file: EPUB/ch034.xhtml; marker: (11.); family: paren_decimal; context: (11.) "Quod unicum est nomen in mundo, — papae scilicet;" — "That there is only one name in the world, — into wit, that of the pope;" no other name, it seems, given under heaven. Once m

## Repeated Windows

- phrase: fiat lux prefatory note by the editor to the reader; count: 4
- phrase: vindication of the first chapter of the animadversions the method; count: 3
- phrase: of the first chapter of the animadversions the method of; count: 3
- phrase: the first chapter of the animadversions the method of fiat; count: 3
- phrase: defense of the second chapter of the animadversions principles of; count: 3
- phrase: of the second chapter of the animadversions principles of fiat; count: 3
- phrase: the second chapter of the animadversions principles of fiat lux; count: 3
- phrase: second chapter of the animadversions principles of fiat lux re-examined; count: 3
- phrase: chapter of the animadversions principles of fiat lux re-examined of; count: 3
- phrase: of the animadversions principles of fiat lux re-examined of our; count: 3

## Missing Word Samples

- word: pre; pdf: 5; epub: 2
- word: eminence; pdf: 5; epub: 2

## Excess Word Samples

- word: editor; pdf: 5; epub: 11
- word: digital; pdf: 0; epub: 6

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
