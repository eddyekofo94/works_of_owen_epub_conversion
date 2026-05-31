# Text Integrity Audit: Volume 10

- Status: **WARN**
- Warnings: 11
- PDF pages: 828
- EPUB text files: 104
- EPUB paragraphs/headings: 3215

## Coverage

- PDF content tokens: 270237
- EPUB content tokens: 269340
- Approximate PDF-to-EPUB coverage ratio: 0.9947
- Pages checked: 817
- Weak page matches: 15
- Dense source windows checked: 955
- Missing dense source-window pages: 808
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 1
- Top-of-page body windows checked: 782
- Top-of-page windows skipped as unstable: 19
- Missing top-of-page body windows: 4
- Bottom-of-page body windows checked: 709
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 9

## Paragraphs

- Body paragraphs checked: 2550
- Possible faulty paragraph splits: 158
- Structural starts excluded from split warnings: 173
- Short fragments: 25
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 7
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 8
- Roman heading candidates: 1
- Overlong heading candidates: 46
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 185
- EPUB enumerator markers: 195
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 838
- EPUB Greek words: 849
- Greek word coverage ratio: 0.9975
- PDF Hebrew words: 18
- EPUB Hebrew words: 18
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 41
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

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
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 3; sample: contents of θεομαχια αττεξουσιαστικη display of arminianism prefatory note by the editor epistle dedicatory
- page: 4; sample: the ensuing treatise to the reader book in general of the end of the
- page: 5; sample: book arguments against the universality of redemption the two first from the nature of
- page: 6; sample: actual believing in relation thereunto digression concerning the immediate effect of the death of
- page: 7; sample: public epistle dedicatory the preface to the reader part the introduction the design of
- page: 8; sample: first part of the dissertation part objections of the adversaries answered the racovian catechism
- page: 10; sample: 10 instance of this learned opponent refuted the considerations of rewarding and punishing different
- page: 11; sample: 11 courts from the divine appointment the manner of it what this learned author
- page: 12; sample: 12 θεομαχια αυτεξουσιαστικη display of arminianism being discovery of the old pelagian idol free-will
- page: 13; sample: 13 prefatory note the relation of man to his creator has engaged the attention

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.5; sample: contents of θεομαχια αττεξουσιαστικη display of arminianism prefatory note by the editor epistle dedicatory to the christian reader θεμοχιας αυτεξουσιαστικης specimen of the two main ends aimed at

## Missing Top-Of-Page Body Windows

- page: 63; sample: "Unite my heart to fear thy or to one part of the
- page: 91; sample: "What hast thou that thou didst The sum of their doctrine is: God
- page: 136; sample: "Thou hast wrought all our works "Faith and conversion cannot be
- page: 649; sample: TO HIS ILLUSTRIOUS HIGHNESS LORD OLIVER CROMWELL, OF ENGLAND,

## Missing Bottom-Of-Page Body Windows

- page: 12; sample: Qe>v w+ Ake>si>lai kli>maka kai< mo>nov ajna>bhqi eijv to<n oujrano>n. — Constant., apud Socrat., lib. 1. cap. 10.
- page: 39; sample: standeth for ever, the thoughts of certain time," Episcop.
- page: 62; sample: Psalm 119:36. man to this or that particular,
- page: 90; sample: determineth of them," Corr. pleasing to God," Rem. Apol.
- page: 112; sample: he him; male and female created he not so vehement and inordinate
- page: 142; sample: on the Gentiles through Jesus only way of salvation be the
- page: 195; sample: due," — which gave occasion to the altar which Paul saw bearing the superscription of Agnw>stw| Qew~|, "To the unknown God," — so Socrates
- page: 543; sample: a]nqrwpov yilo<v ajlla< uiJo<v Qeou~ menogenh<v oJ uJperapoqnh>skwn—kai< eij po>te dia< pisteu>ontev eijv
- page: 644; sample: God judge the world?" — OXFORD: THOMAS ROBINSON. 1653.

## Possible Paragraph Splits

- file: EPUB/ch002.xhtml; previous: ered, by the Committee of the House of Commons in Parliament for the Regulating of Printing and Publishing of Books, That this book, entitled "A Display of Arminianism," be printed; next: JOHN WHITE
- file: EPUB/ch006.xhtml; previous: to particular contingent events, Isaiah 48:14. Yea, it is an ordinary thing with the Lord to confirm the certainty of those things that are yet for to come from his own decree; as,; next: Isaiah 14:24,25; — "It is certain the Assyrian shall be broken, because the Lord hath purposed it;" which were a weak kind of reasoning, if his purpose might be altered. Nay "He is
- file: EPUB/ch007.xhtml; previous: omination? Even actions in themselves sinful are not; though not as sinful, yet in some other regard, as punishments of others. "Behold," saith Nathan to David, in the name of God,; next: So, also, when wicked robbers had nefariously spoiled Job of all his substance, the holy man concludeth, "The LORD gave, and the LORD hath taken away," Job 1:21. Now, if the workin
- file: EPUB/ch008.xhtml; previous: His powerful overruling of all events, both necessary, free, and contingent, and disposing of them to certain ends for the manifestation of his glory. So Joseph tells his brethren,; next: Fourthly, His determining and restraining second causes to such and such effects:
- file: EPUB/ch009.xhtml; previous: his revealed will to walk in his statutes, and keep his laws; upon this he also promiseth that he will so effect all things, that of some this shall be performed: Ezekiel 36:26,27,; next: So that the self-same obedience of the people of God is here the object of his will, taken in either acceptation. And yet the precept of God is not here, as some learned men suppos
- file: EPUB/ch010.xhtml; previous: uld be saved," chapter 2:47. From both which places it is evident that God bestoweth faith only on them whom he hath pre-ordained to eternal life; but most clearly, Romans 8:29,30,; next: St Austin interpreted this place by adding in every link of the chain, "Only those." However, the words directly import a precedency of predestination before the bestowing of other
- file: EPUB/ch010.xhtml; previous: them he also called: and whom he called, them he also justified: and whom he justified, them he also glorified." So that "nothing shall be able to separate us from the love of God,; next: which is in Christ Jesus," Romans 8:29,30,39. "He hath chosen us in him before the foundation of the world, that we should be holy," Ephesians 1:4.
- file: EPUB/ch011.xhtml; previous: hought so by the wisdom of God himself; but our sin even compelled that good and wise Creator to hate and curse the work of his own hands. "Cursed is the ground," saith he to Adam,; next: Hence was that heavy burden of "vanity," that "bondage of corruption," under which to this day "the whole creation groaneth and travaileth in pain" until it be delivered, Romans 8:
- file: EPUB/ch014.xhtml; previous: are dead," Ephesians 2:1,2, begetting us anew, John 1:13, making us in all things such as he would have us to be, is contained in that promise of the new covenant, Jeremiah 32:40,; next: and is no way repugnant to the holy Scripture, declaring our duty to be all this that the Lord would have us. And now, let all men judge whether, against so many and clear testimon
- file: EPUB/ch022.xhtml; previous: ess than the least of all the saints of God, and unworthy the name which yet he is bold to subscribe himself by, — Your honor's most obliged servant in the service of Jesus Christ,; next: THERE are two rotten pillars on which the fabric of late Arminianism (an egg of the old Pelagianism, which we had well hoped had been long since chilled, but is sit upon and broode

## Inline Structural Marker Candidates

- file: EPUB/ch020.xhtml; text: In 1650, Mr. Home, minister at Lynn in Norfolk, a man, according to Palmer (Nonconf. Mem., 3. pp. 6, 7), "of exemplary and primitive piety," and author of several works, published a reply to Owen's work, under the title, "The Open Door f...
- file: EPUB/ch021.xhtml; text: Arg. 6. From Scripture assertions and consequences. Answers to the proofs of this sixth argument: — 1. From 1 John 4:14; John 1:4, 7; 1 Timothy 2:4. 2. From some texts before vindicated. 3. From Psalm 19:4; Romans 10:18; Acts 14:17, etc....
- file: EPUB/ch031.xhtml; text: Now, what is it to obey the grace of God? Is it not to believe? Therefore, it seems that Christ intercedeth for them that they may believe, upon condition that they do believe. Others, more cautiously, assert the good using of the means ...
- file: EPUB/ch046.xhtml; text: Let now any one tell me what the reprobates, in this life, lie under more? And do not all the elect, until their actual reconciliation, in and by Christ, lie under the very same? for, — (1.) Are not their prayers an abomination to the Lo...
- file: EPUB/ch057.xhtml; text: Now, fourthly, after all this, and not before, it lies upon a believer to assure his soul, according as he finds the fruit of the death of Christ in him and towards him, of the goodwill and eternal love of God to him in sending his Son t...
- file: EPUB/ch064.xhtml; text: Wherefore, to clear the whole, I shall, — 1. Give you in the passages opposed; and, 2. Vindicate them from mutual opposition, with what is besides charged on them.
- file: EPUB/ch073.xhtml; text: To evince the main assertion, I shall, — 1. Show the nature and quality of this right; 2. The bottom or foundation of it; and, 3. Prove the thesis. 1. By right I understand jus in general. Now, "Jus est quod justum est," Aug. in Psalm cx...

## Suspicious Large-Number Starts

- file: EPUB/ch011.xhtml; text: 119 "Infants are simply in that estate in which Adam was before his fall," saith Venator. 120 "Neither is it at all considerable whether they be the children of believem or of heathens and infidels; for infants, as infan
- file: EPUB/ch011.xhtml; text: 134 "Whether ever any one were damned for original sin, and adjudged to everlasting torments, is deservedly doubted of. Yea, we doubt not to affirm that never any was so damned," saith Corvinus. And that this is not his
- file: EPUB/ch013.xhtml; text: 36. To abide argueth a continued, uninterrupted act.
- file: EPUB/ch014.xhtml; text: 169 " Can any one," say they, "wisely and seriously prescribe the performance of a condition to another, under the promise of a reward and threatening of punishment, who will effect it in him to whom it is prescribed? Th
- file: EPUB/ch014.xhtml; text: 96. All which assertions, how contrary they are to the express word of God, I shall now demonstrate.
- file: EPUB/ch016.xhtml; text: 202 "Herein," saith Arminius, "consisteth the liberty of the will, that all things required to enable it to will any thing being accomplished, it still remains indifferent to will or not." And all of them at the synod: 2
- file: EPUB/ch016.xhtml; text: 206 "In such a one wherein he may be suffered to sin, or to do well, at his pleasure," as the same author intimates. It seems, then, as to sin, so nothing is required for him to be able to do good but God's permission?
- file: EPUB/ch084.xhtml; text: 117. And again, Aristotle says, "It is a very strong proof, if all shall agree in what we shall say." And in that observation another author concurs: "The things that are commonly agreed on are worthy of credit." And her

## Roman Heading Candidates

- file: EPUB/ch021.xhtml; text: II. His oblation not a mean good in itself, but only as conducing to its end, and inseparable from his intercession; as, —

## Overlong Heading Candidates

- file: EPUB/ch024.xhtml; tag: h4; text: II. The effect, also, and actual product of the work itself, or what is accomplished and fulfilled by the death, blood-shedding, or oblation of Jesus Christ, is no less clearly manifested, but is as fully, and very often more distinctly,...
- file: EPUB/ch024.xhtml; tag: h4; text: III. Thus full, clear, and evident are the expressions in the Scripture concerning the ends and effects of the death of Christ, that a man would think every one might run and read.
- file: EPUB/ch025.xhtml; tag: h4; text: I. The end of anything is that which the agent intendeth to accomplish in and by the operation which is proper unto its nature, and which it applieth itself unto, — that which any one aimeth at, and designeth in himself to attain, as a t...
- file: EPUB/ch025.xhtml; tag: h4; text: III. The former consideration, by reason of the defect and perverseness of some agents (for otherwise these things are coincident), holds out a twofold end of things, — first, of the work, and, secondly, of the workman; of the act and th...
- file: EPUB/ch025.xhtml; tag: h4; text: V. Moreover, the means are of two sorts: — First, Such as have a true goodness in themselves without reference to any farther kind; though not so considered as we use them for means.
- file: EPUB/ch025.xhtml; tag: h4; text: VI. These things being thus proposed in general, our next task must be to accommodate them to the present business in hand; which we shall do in order, by laying down the agent working, the means wrought and the end effected, in the grea...
- file: EPUB/ch026.xhtml; tag: h4; text: I. The agent in, and chief author of, this great work of our redemption is the whole blessed Trinity; for all the works which outwardly are of the Deity are undivided and belong equally to each person, their distinct manner of subsistenc...
- file: EPUB/ch026.xhtml; tag: h4; text: II. Two peculiar acts there are in this work of our redemption by the blood of Jesus, which may be and are properly assigned to the person of the FATHER: — First, The sending, of his Son into the world for this employment.
- file: EPUB/ch030.xhtml; tag: h4; text: I. Our first reason is taken from that perpetual union which the Scripture maketh of both these, almost always joining them together, and so manifesting those things to be most inseparable which are looked upon as the distinct fruits and...
- file: EPUB/ch030.xhtml; tag: h4; text: II. To offer and to intercede, to sacrifice and to pray, are both acts of the same sacerdotal office, and both required in him who is a priest; so that if he omit either of these, he cannot be a faithful priest for them: if either he doe...

## Short Fragments

- file: EPUB/ch002.xhtml; text: JOHN WHITE
- file: EPUB/ch027.xhtml; text: Whence he saith,
- file: EPUB/ch030.xhtml; text: VI.
- file: EPUB/ch035.xhtml; text: Such are Hebrews 9:12, 14,
- file: EPUB/ch048.xhtml; text: Arg. 15.
- file: EPUB/ch053.xhtml; text: Where, —
- file: EPUB/ch057.xhtml; text: Scriptural Redemption.
- file: EPUB/ch059.xhtml; text: COGGESHALL, APRIL 25, 1648.
- file: EPUB/ch062.xhtml; text: J.O. May 15th, [1650.]
- file: EPUB/ch064.xhtml; text: Thus far he.

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

- word: proo; pdf: 0; epub: 18
- word: digital; pdf: 0; epub: 8
- word: psalms; pdf: 0; epub: 6

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
