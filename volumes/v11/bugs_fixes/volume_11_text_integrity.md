# Text Integrity Audit: Volume 11

- Status: **WARN**
- Warnings: 11
- PDF pages: 815
- EPUB text files: 31
- EPUB paragraphs/headings: 2521

## Coverage

- PDF content tokens: 303980
- EPUB content tokens: 297636
- Approximate PDF-to-EPUB coverage ratio: 0.9768
- Pages checked: 809
- Weak page matches: 1
- Dense source windows checked: 37106
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 2
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 791
- Top-of-page windows skipped as unstable: 12
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 791
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 3

## Paragraphs

- Body paragraphs checked: 2149
- Possible faulty paragraph splits: 40
- Structural starts excluded from split warnings: 295
- Short fragments: 30
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 7
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 2
- Roman heading candidates: 2
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 263
- EPUB enumerator markers: 264
- Missing enumerator marker forms: 3
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 2084
- EPUB Greek words: 2079
- Greek word coverage ratio: 0.997
- PDF Hebrew words: 0
- EPUB Hebrew words: 0
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 117
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 4459
- EPUB Latin words: 4467
- EPUB Tagged Latin words: 3269
- Latin word coverage ratio: 0.9955
- Latin word tagging ratio: 0.7318
- Latin clauses checked: 404
- Missing Latin clauses: 0
- Tagged Latin runs checked: 796
- Translated Latin runs: 249
- Latin translation ratio: 0.3128

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `missing_enumerator_markers`: Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: explained and confirmed prefatory note by the editor the dedication the epistle dedicatory preface
- page: 4; sample: of them evinced in sundry instances of vocation justification and sanctification isaiah 27-31 opened
- page: 5; sample: samuel farther considered and its unsuitableness to illustrate romans 28-31 proved interpretation of scripture
- page: 6; sample: chapter argument from the covenant of grace an entrance into the consideration of the
- page: 7; sample: who intended in that promise not judas the accomplishment of the premise the testimony
- page: 8; sample: and fountain of all goodness to his people in his own good pleasure the
- page: 9; sample: the death of christ and the necessity of faith and obedience reconciled sundry considerations
- page: 10; sample: effects ascribed in the scripture to his so doing as union with christ union
- page: 11; sample: the argument and of the first part of this treatise chapter the improvement of
- page: 12; sample: promises more particularly and more largely insisted on chapter arguments against the doctrine considered

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 172; sample: good thoughts and actings whatsoever. ( Romans 7:8-24; 2 Corinthians 3:5.)
- page: 268; sample: pleasure? ( John 1:16; 1 Corinthians 12:13; Ephesians 1:23, 2:20- 22, 4:15, 16; Galatians 2:20; Colossians 1:17-19, 2:19.) What is it,

## Possible Paragraph Splits

- file: EPUB/ch001.xhtml; previous: BY; next: John Owen
- file: EPUB/ch001.xhtml; previous: John Owen; next: SERVANT OF JESUS CHRIST IN THE WORKE OF THE GOSPELL
- file: EPUB/ch001.xhtml; previous: SERVANT OF JESUS CHRIST IN THE WORKE OF THE GOSPELL; next: OXFORD, PRINTED BY LEON. LICHFIELD PRINTER TO THE UNIVERSITY, FOR TIM. ROBINSON.
- file: EPUB/ch005.xhtml; previous: k to deal so harshly with some of them with whom he hath to do. And it is still feared that "Parata tollit cornua; Qualis Lycambae spretus infido gener, Aut acer hostis Bupalo ." 3; next: It might, indeed, be the more excusable if evident provocation were always ready at hand to be charged with the blame of this procedure, if he said only,
- file: EPUB/ch005.xhtml; previous: st of a crooked and perverse generation, knowing that it is but yet a little while, and he that shall come will come, and will not tarry. Yea, come, Lord Jesus, come. So prays your; next: unworthy fellow-laborer and brother in our dear Lord Jesus
- file: EPUB/ch005.xhtml; previous: unworthy fellow-laborer and brother in our dear Lord Jesus; next: John Owen
- file: EPUB/ch006.xhtml; previous: ople, making it become new Rome, so that the bishop of the church there was to enjoy equal privileges with him whose lot was fallen in the old imperial city. Rut our doctor adds, —; next: Sect. 5, " Illud ex Judaeorum exemplari transcripsisse apostoli videntur; cum Mosaica id lege cautum esset, ut judices et ministri in qualibet civitate ordinarentur , [Deuteronomy
- file: EPUB/ch006.xhtml; previous: To the same purpose, and with the same confident persuasion, he speaks, Epist. ad Ephesians, [cap. 9]: —; next: Ρύσεται ὑμᾶς Ιησοῦς Χριστὸς , ὁ ζεμελιώσας ὑμᾶς ἐπὶ τὴν πέτραν , ὠς λίθους ἐκλεκτοὺς εὐαρμολογουμένους εἰς οἰκοδομὴν ζείας Πατρὸς , ἀναφερομένους εἰς τὰ ὕψη διὰ Χριστοῦ , τοῦ ὑπὲρ
- file: EPUB/ch006.xhtml; previous: nt with all that are baptized, yet he is never mixed with any that are not worthy; that is, he dwells not with any that obtain not salvation," Basil, Lib. de Spir. Sanc. cap. 16; —; next: Νῦν μὲν γὰρ εἰ καὶ μὴ ἀνακέκραται τοῖς ἀναξίοις ? ἀλλὰ οῦν παρεῖναι δοκεῖ πῶς τοῖς ἅπαξ ἐσφραγισμένοις . By that seeming presence of the Holy Ghost with hypocrites that are baptize
- file: EPUB/ch006.xhtml; previous: of Prosper, De Ingrat., I shall transcribe the 10th chapter, to present to the reader the substance and pith of that treatise, as also the state of the controversy in those days: —; next: — "Quam sans tides sit vestra patescat, Gratia qua Christi populus sumus, hoc cohibetur Limite vobiscum, et formam hanc adscribitis illi: Ut cunctos vocet ilia quidem, invitetque;

## Inline Structural Marker Candidates

- file: EPUB/ch003.xhtml; text: Five leading arguments are adduced in proof of the perseverance of the saints: — It is argued, 1. From the divine nature as immutable; under which head the following passages are considered, [Malachi 3:6] [James 1:16] -18; [Romans 11:29]...
- file: EPUB/ch013.xhtml; text: The latter I at present only intend. Saith he, 1. "I know them;" 2. "I give them eternal life;" 3. "They shall never perish;" 4. "No man shall pluck them out of my hand;" 5. "My Father is omnipotent, and hath a sovereignty over all, and ...
- file: EPUB/ch015.xhtml; text: Their quickening is everywhere ascribed to the Spirit that is given unto them; there is not a quickening, a life-giving power, in a quality, a created thing. In the state of nature, besides gracious dispensations and habits in the soul i...
- file: EPUB/ch019.xhtml; text: Sect. 12, "If the principles of the doctrine we speak of dissolve the efficiency of the said threatenings towards the end for the accomplishment whereof they are given, then they render them unsavory, useless, and vain; but the principle...
- file: EPUB/ch022.xhtml; text: As to the matter in hand, this is evident by the light of this single consideration, that in such an ecclesiastical body of Christ there are always, or may be, — and Christ himself, in the rules and laws that he hath given for the govern...
- file: EPUB/ch022.xhtml; text: That they should be saved by Christ, and yet not washed in his blood, not sanctified by his Spirit (which to be is to be regenerate), is another new notion of the new gospel The countenance which Mr. Goodwin would beg to his doctrine fro...
- file: EPUB/ch022.xhtml; text: The proposition is ready at hand in the words, "He that is born of God doth not, cannot commit sin." The reason of the proposition confirming the truth thereof is twofold: — 1. Because he is born of God; 2. Because His seed, whereof he i...

## Suspicious Large-Number Starts

- file: EPUB/ch006.xhtml; text: 24. It seems, moreover, that those bishops and deacons in those days, as was observed, were appointed to the office by and with the consent of the people, or whole body of the church; no loss do these words import, Συνευ
- file: EPUB/ch006.xhtml; text: 30. Paulus tandem et Silas Syriam et Cilieiam peragrantes, ver. 41, cap. 16:4, δόγματα κεκριμένα ὑπὸ τῶν ἀποστόλων , singulis elvitatibus observanda tradiderunt, ut quae ad hanc Antiochiae metropolin, ut totidem subordin

## Roman Heading Candidates

- file: EPUB/ch007.xhtml; text: M. Pacho secured possession of another copy in 1847, which afterwards came under the examination of Mr. Cureton.
- file: EPUB/ch015.xhtml; text: II. 1. The first signal issue and effect which is ascribed to this indwelling of the Spirit is union; not a personal union with himself, which is impossible.

## Short Fragments

- file: EPUB/ch001.xhtml; text: OR, THE
- file: EPUB/ch001.xhtml; text: BY
- file: EPUB/ch001.xhtml; text: John Owen
- file: EPUB/ch001.xhtml; text: ANNO DOM: 1654.
- file: EPUB/ch004.xhtml; text: TO
- file: EPUB/ch005.xhtml; text: John Owen
- file: EPUB/ch006.xhtml; text: Saith he,
- file: EPUB/ch006.xhtml; text: Well, what then?
- file: EPUB/ch006.xhtml; text: Doubtless; for, —
- file: EPUB/ch006.xhtml; text: And cap. 12,

## Missing Enumerator Markers

- marker: (1.); pdf: 63; epub: 62; examples: [{'location': 'pdf:p10', 'context': 'Union with Christ by the indwelling of the same Spirit in him and us — This proved from, (1.) Scriptural declarations of it — 2 Peter 1:4, how we are made partakers of the divine nature — Union expres...
- marker: (2.); pdf: 65; epub: 62; examples: [{'location': 'pdf:p10', 'context': 'disciples, John 17:2l — The union of the persons in the Trinity with themselves — (2.) Scriptural illustrations for the manifestation of union — The union of head and members, what it is, and wherein ...
- marker: (3.); pdf: 24; epub: 23; examples: [{'location': 'pdf:p11', 'context': 'g it on work, faith — (2.) In the manner of doing it, eyeing both precepts and promises — (3.) The end aimed at in it, the glory of God as a rewarder, Hebrews 11:6; Romans 4:4 — The principle in us wh...

## Enumerator Sequence Candidates

- file: EPUB/ch017.xhtml; marker: (2dly.); family: paren_ordinal; context: (2dly.) There are promises of what good and great things God will farther do unto and for them who obey him; as, that he will keep them and preserve them that they shall not be lost, that

## Repeated Windows

- phrase: both to will and to do of his good pleasure; count: 9
- phrase: law in their inward parts and write it in their; count: 5
- phrase: in their inward parts and write it in their hearts; count: 5
- phrase: all things work together for good to them that love; count: 4
- phrase: he wrought in christ when he raised him from the; count: 4
- phrase: wrought in christ when he raised him from the dead; count: 4
- phrase: will put my law in their inward parts and write; count: 4
- phrase: put my law in their inward parts and write it; count: 4
- phrase: my law in their inward parts and write it in; count: 4
- phrase: in them both to will and to do of his; count: 4

## Missing Word Samples

- word: 19-22; pdf: 9; epub: 3
- word: 3-5; pdf: 7; epub: 3
- word: 31-34; pdf: 7; epub: 3
- word: 27-29; pdf: 6; epub: 2
- word: g's; pdf: 4; epub: 0
- word: 27-31; pdf: 5; epub: 2
- word: 17-20; pdf: 5; epub: 2
- word: 28-30; pdf: 5; epub: 2
- word: 16-18; pdf: 4; epub: 1
- word: 2-4; pdf: 3; epub: 0

## Excess Word Samples

- word: psalms; pdf: 1; epub: 56
- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 2; epub: 11
- word: historical; pdf: 2; epub: 10
- word: modern; pdf: 4; epub: 11
- word: footnotes; pdf: 0; epub: 7
- word: hebrew; pdf: 2; epub: 8

## Missing Latin Word Samples

- word: semi; pdf: 3; epub: 0

## Untagged Latin Word Samples

- word: ergo; epub: 25; tagged: 5
- word: perpetrate; epub: 10; tagged: 0
- word: salmasius; epub: 9; tagged: 0
- word: ingenerate; epub: 9; tagged: 0
- word: nowhere; epub: 9; tagged: 0
- word: vedelius; epub: 8; tagged: 0
- word: relate; epub: 8; tagged: 0
- word: predestinate; epub: 8; tagged: 0
- word: co-operate; epub: 8; tagged: 0
- word: alas; epub: 8; tagged: 0

## Untranslated Latin Samples

- phrase: Imputatio Fidei
- phrase: Vindiciae Evangelicae
- phrase: catena patrum
- phrase: Sancti Sanciti," etc.; Thomas
- phrase: Sancta sanctis
- phrase: actum agere
- phrase: velut amnis
- phrase: super notas aluere ripas
- phrase: profundo Pindarus
- phrase: monstrum horrendum

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
