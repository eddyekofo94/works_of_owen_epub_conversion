# Text Integrity Audit: Volume 7

- Status: **WARN**
- Warnings: 12
- PDF pages: 683
- EPUB text files: 63
- EPUB paragraphs/headings: 2333

## Coverage

- PDF content tokens: 230677
- EPUB content tokens: 230772
- Approximate PDF-to-EPUB coverage ratio: 0.9971
- Pages checked: 679
- Weak page matches: 3
- Dense source windows checked: 32118
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 5
- Missing front CONTENTS pages: 2
- Top-of-page body windows checked: 667
- Top-of-page windows skipped as unstable: 16
- Missing top-of-page body windows: 3
- Bottom-of-page body windows checked: 632
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 2

## Paragraphs

- Body paragraphs checked: 1972
- Possible faulty paragraph splits: 9
- Structural starts excluded from split warnings: 241
- Short fragments: 18
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 5
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 3
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 381
- EPUB enumerator markers: 399
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 325
- EPUB Greek words: 325
- Greek word coverage ratio: 0.9969
- PDF Hebrew words: 26
- EPUB Hebrew words: 26
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 18
- Missing Greek clauses: 0
- Hebrew clauses checked: 3
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 2349
- EPUB Latin words: 2382
- EPUB Tagged Latin words: 40
- Latin word coverage ratio: 0.9962
- Latin word tagging ratio: 0.0168
- Latin clauses checked: 20
- Missing Latin clauses: 0
- Tagged Latin runs checked: 9
- Translated Latin runs: 5
- Latin translation ratio: 0.5556

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: contents of nature and causes of apostasy from the gospel prefatory note by the
- page: 4; sample: of apostasy from the truth and decays in the practice of evangelical holiness directions
- page: 5; sample: and what they are to be accompanied withal etc what of god or in
- page: 6; sample: growth in our spiritual affections as unto this assimilation decays in spiritual affections with
- page: 24; sample: the nature and causes of apostasy from the gospel chapter the nature of apostasy
- page: 31; sample: were differenced from them as that they had such things as did accompany salvation
- page: 37; sample: holy ghost in miraculous operations so expressly chap elsewhere δωρεα so far as can
- page: 39; sample: on the earth but he gave the gospel church state by that spirit which
- page: 45; sample: respect unto its blessed effects psalm acts james on this account the psalmist assures
- page: 59; sample: description of himself nahum god is jealous and the lord revengeth the lord revengeth

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.25; sample: contents of nature and causes of apostasy from the gospel prefatory note by the editor the nature of apostasy from the gospel declared in an exposition of hebrews
- page: 7; hit_ratio: 0.25; sample: law doth not destroy the dominion of sin and how grace dethrones sin and gives dominion over it the practical observations drawn from end application made of the

## Missing Top-Of-Page Body Windows

- page: 3; sample: CONTENTS OF . NATURE AND CAUSES OF APOSTASY FROM THE GOSPEL.
- page: 24; sample: THE NATURE AND CAUSES OF APOSTASY FROM THE GOSPEL.
- page: 183; sample: 12:39-41, and that of the apostles, Acts 28:25-27, and is expounded,

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 617; sample: ejpiqumi>av, Romans 13:14, — a continual working and provision to

## Possible Paragraph Splits

- file: EPUB/ch004.xhtml; previous: 3. To those who pretend to perfection in this life. The causes of this kind of apostasy are mentioned,; next: VIII.
- file: EPUB/ch004.xhtml; previous: Apostasy from purity of worship is exhibited, in the neglect of what God has appointed, and by additions which he has not appointed, in the ordinances of the gospel,; next: XI.
- file: EPUB/ch005.xhtml; previous: To The Reader; next: SOME brief account of the occasion and design of the ensuing discourse I judge due unto the reader, that, upon a prospect of them, he may either proceed in its perusal or desist, a
- file: EPUB/ch015.xhtml; previous: observe, that upon the destruction of Babylon, it is said that "in her was found the blood of prophets, and of saints, and of all that were slain upon the earth," Revelation 18:24,; next: — that is, for the gospel and the profession thereof. Whoever, therefore, offereth violence unto the life of any on the account of their profession of the gospel and religion of Ch
- file: EPUB/ch023.xhtml; previous: the fullness of wisdom in spiritual things; 3. their value as perfective of our present condition; and, 4. as constituting in the future enjoyment of them our eternal blessedness,; next: XIX.
- file: EPUB/ch030.xhtml; previous: em solid relief but the consideration and faith of things invisible and eternal. So the apostle declares this state of things, 2 Corinthians 4:16-18 (the words before insisted on),; next: He lays all sorts of afflictions in one scale, and, on the consideration of them, declares them to be "light" and "but for a moment." Then he lays glory in the other scale, and fin
- file: EPUB/ch037.xhtml; previous: him by our affections, it is despised by him; he owns us not. As "if a man would give all the substance of his house for love, it would utterly be contemned," Song of Solomon 8:7,; next: — it is not to be bought or purchased with riches; so if a man would give to God an the substance of his house without love, it would in like manner be despised. And however, on th
- file: EPUB/ch050.xhtml; previous: ls in the affections, when there is a neglect of the means by which it is mortified, when a reservation is made in favor of any known sin, and when hardness of heart is manifested,; next: III.
- file: EPUB/ch054.xhtml; previous: (4thly.) They will receive in the warnings which are given them by the word preached, especially if their particular case be touched on or laid open; next: (5thly.) They will have no quiet, rest, or self-approbation, until they come thoroughly off unto a healing and recovery, such as that described, Hosea 14:1-4. Thus it may be with s

## Inline Structural Marker Candidates

- file: EPUB/ch021.xhtml; text: An inquiry follows into the objects of spiritual thoughts; which are, — 1. The dispensations of Providence; 2. Special trials and temptations; and 3. Heavenly and eternal realities. In regard to the latter, —
- file: EPUB/ch022.xhtml; text: An inquiry follows into the objects of spiritual thoughts; which are, — 1. The dispensations of Providence; 2. Special trials and temptations; and 3. Heavenly and eternal realities. In regard to the latter, —
- file: EPUB/ch033.xhtml; text: It is the spiritual mind alone that can reconcile those things which are prescribed to us as our duty towards God. "To delight and rejoice in him always, to triumph in the remembrance of him, to draw nigh unto him with boldness and confi...
- file: EPUB/ch050.xhtml; text: The reason of the assurance that sin shall have no more dominion over believers is, that they are "not under the law, but under grace;" because, — whereas, 1. the law gives no strength against sin, 2. confers no spiritual liberty, and, 3...
- file: EPUB/ch057.xhtml; text: I shall name some of them: — 1. Such a soul can have no solid peace, because it hath not satisfaction what state it doth belong unto. 2. It cannot receive refreshment by gospel consolations in any condition, for its just fears of the dom...

## Roman Heading Candidates

- file: EPUB/ch047.xhtml; text: I. 1. That spiritual life whereof we are made partakers in this world is threefold, or there are three gospel privileges or graces so expressed: —
- file: EPUB/ch050.xhtml; text: I. As to the nature of this dominion, —
- file: EPUB/ch050.xhtml; text: II. As to the evidence of this dominion, —

## Short Fragments

- file: EPUB/ch004.xhtml; text: I.
- file: EPUB/ch004.xhtml; text: II.
- file: EPUB/ch004.xhtml; text: VIII.
- file: EPUB/ch004.xhtml; text: III.
- file: EPUB/ch004.xhtml; text: XI.
- file: EPUB/ch005.xhtml; text: To The Reader
- file: EPUB/ch006.xhtml; text: And, —
- file: EPUB/ch006.xhtml; text: Ans.
- file: EPUB/ch014.xhtml; text: Verse 20,
- file: EPUB/ch018.xhtml; text: I answer, —

## Enumerator Sequence Candidates

- file: EPUB/ch031.xhtml; marker: (2.); family: paren_decimal; context: (2.) WE have treated in general before of the proper objects of our spiritual thoughts as unto our present duty. That which we were last engaged in is an especial instance in heavenly
- file: EPUB/ch031.xhtml; marker: [3.]; family: bracket_decimal; context: [3.] Again; meditate and think of the glory of heaven so as to compare it with the opposite state of death and eternal misery. Few men care to think much of hell, and the everlasting t

## Repeated Windows

- phrase: the good word of god and the powers of the; count: 4
- phrase: good word of god and the powers of the world; count: 4
- phrase: word of god and the powers of the world to; count: 4
- phrase: of god and the powers of the world to come; count: 4
- phrase: the knowledge of his glory in the face of jesus; count: 4
- phrase: knowledge of his glory in the face of jesus christ; count: 4
- phrase: they received not the love of the truth that they; count: 3
- phrase: received not the love of the truth that they might; count: 3
- phrase: not the love of the truth that they might be; count: 3
- phrase: the love of the truth that they might be saved; count: 3

## Missing Word Samples

- word: london; pdf: 3; epub: 0
- word: editor; pdf: 3; epub: 1

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: modern; pdf: 1; epub: 10
- word: greek; pdf: 3; epub: 11
- word: hebrew; pdf: 1; epub: 8
- word: edition; pdf: 4; epub: 10
- word: footnotes; pdf: 0; epub: 6

## Untagged Latin Word Samples

- word: nor; epub: 395; tagged: 0
- word: yea; epub: 184; tagged: 0
- word: jesus; epub: 159; tagged: 0
- word: thereunto; epub: 95; tagged: 0
- word: endeavor; epub: 89; tagged: 0
- word: whereas; epub: 84; tagged: 0
- word: hereunto; epub: 60; tagged: 0
- word: sincere; epub: 52; tagged: 0
- word: whereunto; epub: 41; tagged: 0
- word: immediate; epub: 37; tagged: 0

## Untranslated Latin Samples

- phrase: But ye are not in the flesh, but in the Spirit.
- phrase: the word of Christ might dwell in them richly in all wisdom,
- phrase: God is love; and he that dwelleth in love dwelleth in God, and God in him,
- phrase: having no joy in its prevalency, but grief, being planted in this respect

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
