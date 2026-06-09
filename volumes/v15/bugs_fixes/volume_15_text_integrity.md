# Text Integrity Audit: Volume 15

- Status: **WARN**
- Warnings: 13
- PDF pages: 683
- EPUB text files: 107
- EPUB paragraphs/headings: 2276

## Coverage

- PDF content tokens: 221576
- EPUB content tokens: 218388
- Approximate PDF-to-EPUB coverage ratio: 0.9783
- Pages checked: 675
- Weak page matches: 27
- Dense source windows checked: 28786
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 659
- Top-of-page windows skipped as unstable: 20
- Missing top-of-page body windows: 23
- Bottom-of-page body windows checked: 615
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 28

## Paragraphs

- Body paragraphs checked: 1842
- Possible faulty paragraph splits: 4
- Structural starts excluded from split warnings: 218
- Short fragments: 21
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 0
- Overlong heading candidates: 7
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 402
- EPUB enumerator markers: 410
- Missing enumerator marker forms: 3
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 872
- EPUB Greek words: 871
- Greek word coverage ratio: 0.9893
- PDF Hebrew words: 2
- EPUB Hebrew words: 2
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 39
- Missing Greek clauses: 1
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3300
- EPUB Latin words: 3310
- EPUB Tagged Latin words: 0
- Latin word coverage ratio: 0.9821
- Latin word tagging ratio: 0.0
- Latin clauses checked: 66
- Missing Latin clauses: 2
- Tagged Latin runs checked: 0
- Translated Latin runs: 0
- Latin translation ratio: 1.0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `missing_latin_clauses`: Some dense Latin passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 3; sample: righteousness and legal ceremonies contended for together the reason of it chapter the disciples
- page: 4; sample: worship prohibitions of additions produced considered applied chapter of the authority needful for the
- page: 5; sample: ignorance readiness to take offense remedies hereof pride false teachers chapter grounds and reasons
- page: 7; sample: discourse concerning liturgies and their imposition prefatory note it deserves attention that this pamphlet
- page: 10; sample: from the authority of the law maker the latter he utterly rejected as introduced
- page: 52; sample: may keep the commandments of the lord your god which command you chapter what
- page: 75; sample: with the occasions and reasons of the present differences and divisions about things sacred
- page: 90; sample: and power do make compliance with themselves in all their impositions and self interested
- page: 102; sample: in our hearts and made natural unto us by that one and self same
- page: 103; sample: profess and yet notwithstanding all this such cross entangled wheels are there in the

## Missing Top-Of-Page Body Windows

- page: 471; sample: all the reasonings, exceptions, and pleas in and of that book, to render them useless unto the end designed, which is to reinforce a charge of
- page: 472; sample: things under the rule of those who are set over them by virtue of civil constitutions foreign unto them, not submitted willingly unto by them,
- page: 473; sample: Nonconformists from the charge of schism. And I desire the reader to take notice that we delight not in these contentions, that we desire nothing but
- page: 474; sample: of divine worship, it will be necessary for men to oblige themselves unto total, constant communion, with a renunciation and condemnation of all
- page: 475; sample: I will spare the reader as much as is possible in the repetition of things formerly spoken, and the transcription of his words or my own, without
- page: 476; sample: Without any long deductions, artificial insinuations, or diverting reasonings, without wresting the text or context, these things are plain and
- page: 477; sample: 2. That because the apostles made such a rule (which we know not what it is, or what is become of it), the guides of the church (and that in such a
- page: 478; sample: minded,' to pursue your main end; but if any be 'otherwise minded. Did any think they ought not to mind chiefly their great end? — that is
- page: 479; sample: (2.) That in some things there were different apprehensions and practices amongst them, which hindered not their agreement in what they had
- page: 480; sample: 3. There were others who, acquiescing in the liberty of the Gentiles declared by the apostles,

## Missing Bottom-Of-Page Body Windows

- page: 224; sample: the good way, and walk therein, and ye find rest for your souls" — Jeremiah 6:16.
- page: 273; sample: (3.) He gives hereon that excellent rule: 'H diafwni>a th~v nhstei>av th<n oJmo>noian th~v pi>stewv suni>sthsin — "The difference of fastings" (and
- page: 361; sample: as the apostle speaks, hJli>kon ajgw~na e]cw, Colossians 2:1) "was night
- page: 364; sample: oJsi>wv prosene>gkontav ta< dw~ra th~v ejpiskoph~v ajpobalwmen maka>rioi de< proodoiporh>santev presbu>teroi
- page: 470; sample: answered beforehand in the preceding discourse, so as that the principles and demonstrations of them contained therein may easily be applied unto
- page: 471; sample: provide for their own continuation, to admit or exclude members, or to reform at any time what is amiss among them; — churches which are in all
- page: 472; sample: These things being premised, I shall proceed to examine what the reverend Doctor hath farther offered against our former vindication of the
- page: 473; sample: edification by joint communion as unlawful and evil. And it will be hard to prove that, on a concession of the lawfulness of communion in some acts
- page: 474; sample: application of these words of the apostle in my "Vindication of the Nonconformists."
- page: 475; sample: whereby an appearance is made of various arguings, and the proof of sundry things which belong not unto the case in hand.

## Possible Paragraph Splits

- file: EPUB/ch016.xhtml; previous: o are yet "without Christ, being aliens from the commonwealth of Israel, and strangers from the covenants of promise, having no hope, and without God in the world," Ephesians 2:12,; next: — such, we mean, as are either negatively or privatively infidels or unbelievers, who have yet never heard the sound of the gospel, or do continue to refuse and reject it where it
- file: EPUB/ch022.xhtml; previous: To The Reader; next: I THOUGHT to have wholly omitted the consideration of that part of the discourse of Dr Stillingfleet, in his preface, which concerneth the furtherance and promotion of the designs
- file: EPUB/ch038.xhtml; previous: e those of which Justice Hobart speaks: and therefore it is plain he spake of all the churches which were under the care of the apostles, which he calls 'voluntary congregations.'"; next: Ans. 1. Whereas this argument seems to be cast into the form of a syllogism, I could easily manifest how asyllogistical it is, did I delight to contend with him or any else. But, —
- file: EPUB/ch059.xhtml; previous: lessness, have miscarried in not observing exactly his will and appointment in and about his worship. This was the case of Nadab and Abihu, the sons of Aaron, Leviticus 10:1, 2; of; next: Korah, Dathan, and Abiram, Numbers 16:1-40; of the sons of Eli, — a sin not to be "expiated with sacrifice nor offering for ever," 1 Samuel 2:27-34, 3:14; of Uzza in putting the ar

## Inline Structural Marker Candidates

- file: EPUB/ch034.xhtml; text: It might be easily demonstrated what great numbers [there are] amongst us, — [1.] Who have imbibed atheistical opinions, and either vent them or speak presumptuously, according unto their influence and tendency every day; [2.] Who are pr...

## Suspicious Large-Number Starts

- file: EPUB/ch007.xhtml; text: 30. again, cap. 39:
- file: EPUB/ch029.xhtml; text: 42. Montanus fell into his dotage on the same account; so did Novatianus at Rome, Euseb., lib. 6 cap. 43, and Arius at Alexandria. Hence is that censure of them by Lactantius, lib. 4 cap. 30:
- file: EPUB/ch034.xhtml; text: 12. If the reader would have an account of the lives and manners of the first churches in their members, he may find it in Clem. Epist. ad Cor. pp. 2-4; Justin Mart. Apol. 2; Tertullian in his Algol. and lib. 2 ad Uxor.
- file: EPUB/ch038.xhtml; text: 15. So in the excellent epistle of the churches of Vienne and Lyons unto the churches of Asia and Phrygia, concerning the persecutions that befell them, as they declare themselves to have been particular churches only, s

## Overlong Heading Candidates

- file: EPUB/ch049.xhtml; tag: h3; text: MAY NOT SUCH AN ESTATE OF FAITH AND PERFECTION IN OBEDIENCE BE ATTAINED IN THIS LIFE, AS WHEREIN BELIEVERS MAY BE FREED FROM ALL OBLIGATION UNTO THE OBSERVATION OF GOSPEL INSTITUTIONS?
- file: EPUB/ch056.xhtml; tag: h3; text: WHAT IS PRINCIPALLY TO BE ATTENDED UNTO BY US IN THE MANNER OF THE CELEBRATION OF THE WORSHIP OF GOD, AND OBSERVATION OF THE INSTITUTIONS AND ORDINANCES OF THE GOSPEL?
- file: EPUB/ch059.xhtml; tag: h3; text: WHENCE MAY IT APPEAR THAT THE RIGHT AND DUE OBSERVATION OF INSTITUTED WORSHIP IS OF GREAT IMPORTANCE UNTO THE GLORY OF GOD, AND OF HIGH CONCERNMENT UNTO THE SOULS OF MEN?
- file: EPUB/ch065.xhtml; tag: h3; text: SEEING THE CHURCH IS A SOCIETY OR SPIRITUAL INCORPORATION OF PERSONS UNDER RULE, GOVERNMENT, OR DISCIPLINE, DECLARE WHO OR WHAT ARE THE RULERS, GOVERNORS, OR OFFICERS THEREIN UNDER JESUS CHRIST?
- file: EPUB/ch066.xhtml; tag: h3; text: SEEING THE CHURCH IS A SOCIETY OR SPIRITUAL INCORPORATION OF PERSONS UNDER RULE, GOVERNMENT, OR DISCIPLINE, DECLARE WHO OR WHAT ARE THE RULERS, GOVERNORS, OR OFFICERS THEREIN UNDER JESUS CHRIST?
- file: EPUB/ch071.xhtml; tag: h3; text: MAY A PERSON BE CALLED TO, OR BE EMPLOYED IN, A PART ONLY OF THE OFFICE OR WORK OF THE MINISTRY; OR MAY HE HOLD THE RELATION AND EXERCISE THE DUTY OF AN ELDER OR MINISTER UNTO MORE CHURCHES THAN ONE AT THE SAME TIME?
- file: EPUB/ch082.xhtml; tag: h3; text: MAY NOT THE CHURCH, IN THE SOLEMN WORSHIP OF GOD, AND CELEBRATION OF THE ORDINANCES OF THE GOSPEL, MAKE USE OF AND CONTENT ITSELF IN THE USE OF FORMS OF PRAYER IN AN UNKNOWN TONGUE COMPOSED BY OTHERS, AND PRESCRIBED UNTO THEM?

## Short Fragments

- file: EPUB/ch022.xhtml; text: To The Reader
- file: EPUB/ch028.xhtml; text: Cels., lib. 8.
- file: EPUB/ch032.xhtml; text: Yet, —
- file: EPUB/ch037.xhtml; text: I say, therefore, —
- file: EPUB/ch037.xhtml; text: Or, —
- file: EPUB/ch038.xhtml; text: I answer, —
- file: EPUB/ch040.xhtml; text: OWEN ON COMMUNION WITH GOD.
- file: EPUB/ch043.xhtml; text: Answer — That we:
- file: EPUB/ch044.xhtml; text: Answer — That we:
- file: EPUB/ch057.xhtml; text: Answer —

## Missing Enumerator Markers

- marker: (1.); pdf: 89; epub: 87; examples: [{'location': 'pdf:p237', 'context': 'ledge to be the foundation of all that we plead for in point of church reformation; as, — (1.) That the reasons and arguings of the Doctor in this matter, — the necessity of his cause compelling him ...
- marker: (2.); pdf: 89; epub: 87; examples: [{'location': 'pdf:p237', 'context': 'de eminent by his defense of the protestant religion against those of the church of Rome. (2.) But it may be pleaded, that although the churches following the first ages did insensibly degenerate fro...
- marker: (4.); pdf: 32; epub: 31; examples: [{'location': 'pdf:p262', 'context': '262 from the use of the ceremonies, and full compliance with episcopal jurisdiction. (4.) Hereon those who were for the establishment, having secured their interests therein and obtained power, began...

## Repeated Windows

- phrase: the unity of the spirit in the bond of peace; count: 6
- phrase: the whole body fitly joined together and compacted by that; count: 6
- phrase: whole body fitly joined together and compacted by that which; count: 6
- phrase: body fitly joined together and compacted by that which every; count: 6
- phrase: fitly joined together and compacted by that which every joint; count: 6
- phrase: joined together and compacted by that which every joint supplieth; count: 6
- phrase: together and compacted by that which every joint supplieth according; count: 6
- phrase: and compacted by that which every joint supplieth according to; count: 6
- phrase: compacted by that which every joint supplieth according to the; count: 6
- phrase: by that which every joint supplieth according to the effectual; count: 6

## Missing Word Samples

- word: apostle's; pdf: 9; epub: 1
- word: jewish; pdf: 11; epub: 5
- word: pre; pdf: 6; epub: 0
- word: intends; pdf: 7; epub: 3
- word: verses; pdf: 6; epub: 2
- word: attainments; pdf: 6; epub: 2
- word: self; pdf: 5; epub: 1
- word: eminence; pdf: 4; epub: 0
- word: forborne; pdf: 5; epub: 2
- word: analogy; pdf: 5; epub: 2

## Excess Word Samples

- word: churchstate; pdf: 0; epub: 19
- word: digital; pdf: 0; epub: 10
- word: greek; pdf: 6; epub: 15
- word: modern; pdf: 0; epub: 9
- word: churchcommunion; pdf: 0; epub: 9
- word: theological; pdf: 0; epub: 7
- word: hebrew; pdf: 0; epub: 7
- word: edition; pdf: 5; epub: 11
- word: footnotes; pdf: 0; epub: 6

## Missing Greek Clauses

- page: 482; word_count: 5; sample: οσοι τω κανονι τουτω στοιχησουσιν

## Untagged Latin Word Samples

- word: nor; epub: 601; tagged: 0
- word: jesus; epub: 296; tagged: 0
- word: church-state; epub: 217; tagged: 0
- word: whereas; epub: 127; tagged: 0
- word: thereunto; epub: 120; tagged: 0
- word: yea; epub: 99; tagged: 0
- word: whereunto; epub: 85; tagged: 0
- word: endeavor; epub: 57; tagged: 0
- word: distinct; epub: 56; tagged: 0
- word: hereunto; epub: 51; tagged: 0

## Missing Latin Clauses

- page: 330; word_count: 4; sample: lucius dioscorus aelurus sergius
- page: 470; word_count: 4; sample: si pergama dextra etc

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
