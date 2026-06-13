# Text Integrity Audit: Volume 4

- Status: **WARN**
- Warnings: 5
- PDF pages: 650
- EPUB text files: 70
- EPUB paragraphs/headings: 2124

## Coverage

- PDF content tokens: 219413
- EPUB content tokens: 220142
- Approximate PDF-to-EPUB coverage ratio: 0.9987
- Pages checked: 641
- Weak page matches: 6
- Dense source windows checked: 28430
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 4
- Missing front CONTENTS pages: 4
- Top-of-page body windows checked: 622
- Top-of-page windows skipped as unstable: 14
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 605
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 4

## Paragraphs

- Body paragraphs checked: 1786
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 298
- Short fragments: 18
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 2
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 416
- EPUB enumerator markers: 426
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 713
- EPUB Greek words: 712
- Greek word coverage ratio: 0.9957
- PDF Hebrew words: 99
- EPUB Hebrew words: 99
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 38
- Missing Greek clauses: 0
- Hebrew clauses checked: 7
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 1455
- EPUB Latin words: 1478
- EPUB Tagged Latin words: 844
- Latin word coverage ratio: 0.9945
- Latin word tagging ratio: 0.571
- Latin clauses checked: 114
- Missing Latin clauses: 0
- Tagged Latin runs checked: 214
- Translated Latin runs: 117
- Latin translation ratio: 0.5467

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB

## Missing Dense Source Windows

- page: 3; sample: contents πηευματολογια or discourse concerning the holy spirit continued book vi part the reason
- page: 4; sample: question stated the principal sufficient cause of the understanding which believers have in the
- page: 5; sample: book vii discourse of the work of the holy spirit in prayer prefatory note
- page: 6; sample: given as comforter or the object of his acting in this office inhabitation of
- page: 8; sample: be the word of god with the causes and nature of that faith wherewith
- page: 17; sample: and power this they do undeniably and infallibly psalm romans 19-21 yet it is
- page: 19; sample: own counsels as it is expressed psalm and although this fell not out without
- page: 20; sample: of curse unto the contrary malachi 4-6 so the writings of the new testament
- page: 21; sample: is the only repository of all divine supernatural revelation psalm isaiah timothy the pretenses
- page: 22; sample: in the ministry of the word see matthew corinthians 18-20 ephesians 11-15 timothy the

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.25; sample: contents πηευματολογια or discourse concerning the holy spirit continued book vi part the reason of faith prefatory note by the editor preface the subject stated preliminary remarks what
- page: 4; hit_ratio: 0.5; sample: question stated the principal sufficient cause of the understanding which believers have in the mind and will of god as revealed in the scriptures the spirit of god
- page: 5; hit_ratio: 0.25; sample: book vii discourse of the work of the holy spirit in prayer prefatory note by the editor preface to the reader the use of prayer and the work
- page: 6; hit_ratio: 0.5; sample: unto whom the holy spirit is promised and given as comforter or the object of his acting in this office inhabitation of the spirit the first thing promised

## Missing Top-Of-Page Body Windows

- page: 35; sample: wisdom before all the world, Deuteronomy 4:6-8. Now, we shall not need to consider what were the first attempts of other nations in

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 44; sample: testimony may rationally be supposed to be so far influenced by self- interest as to be of little validity.
- page: 158; sample: them according as might be expected from unjust invaders of other men's rights and malae fidei possesoribus. So when the Philistines contended for
- page: 219; sample: understanding, and I shall keep thy law," Psalm 119:34. So the apostle speaks to Timothy,

## Inline Structural Marker Candidates

- file: EPUB/ch010.xhtml; text: Now, there are greater and more evident impressions of divine excellencies left on the written word, from the infinite wisdom of the Author of it, than any that are communicated unto the works of God, of what sort soever. Hence David, co...
- file: EPUB/ch043.xhtml; text: In regard to his effects on believers, it is first proved that his effectual consolations are the privilege of believers exclusively, III. And some of his operations in them as such, and of the benefits which they in consequence enjoy, a...

## Roman Heading Candidates

- file: EPUB/ch042.xhtml; text: II. and XI. The discourse on Spiritual Gifts, though comparatively short, is the second part of the main.body of the whole work on the Spirit; and, from various allusions to it in other works of the author, he seems to t

## Short Fragments

- file: EPUB/ch004.xhtml; text: May 11, 1677.
- file: EPUB/ch009.xhtml; text: Some of them we must mention: —
- file: EPUB/ch009.xhtml; text: Isaiah 8:19,20,
- file: EPUB/ch015.xhtml; text: I.
- file: EPUB/ch028.xhtml; text: I.
- file: EPUB/ch028.xhtml; text: II.
- file: EPUB/ch028.xhtml; text: VII.
- file: EPUB/ch034.xhtml; text: I answer, —
- file: EPUB/ch036.xhtml; text: I say, therefore, —
- file: EPUB/ch043.xhtml; text: I.

## Enumerator Sequence Candidates

- file: EPUB/ch020.xhtml; marker: (2.); family: paren_decimal; context: (2.) Moreover, the effect of this work of the Holy Spirit on the minds of men doth evidence of what nature it is, And this, also, is variously expressed; as, —

## Repeated Windows

- phrase: we believe the scripture to be the word of god; count: 21
- phrase: to believe the scripture to be the word of god; count: 16
- phrase: believe the scripture to be the word of god with; count: 9
- phrase: the mind and will of god as revealed in the; count: 9
- phrase: to be the word of god with faith divine and; count: 7
- phrase: mind and will of god as revealed in the scripture; count: 7
- phrase: be the word of god with faith divine and supernatural; count: 6
- phrase: believe the scripture to be the word of god in; count: 6
- phrase: of the mind and will of god as revealed in; count: 6
- phrase: of the holy spirit in the illumination of our minds; count: 5

## Missing Word Samples

- word: self; pdf: 7; epub: 3
- word: 14-17; pdf: 4; epub: 0
- word: editor; pdf: 4; epub: 1
- word: 16-18; pdf: 3; epub: 1

## Excess Word Samples

- word: chapter; pdf: 48; epub: 91
- word: psalms; pdf: 7; epub: 30
- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 1; epub: 10
- word: historical; pdf: 4; epub: 12
- word: greek; pdf: 8; epub: 15
- word: modern; pdf: 4; epub: 11
- word: footnotes; pdf: 0; epub: 7
- word: edition; pdf: 3; epub: 9

## Untagged Latin Word Samples

- word: advocate; epub: 31; tagged: 0
- word: abba; epub: 31; tagged: 1
- word: communicate; epub: 18; tagged: 0
- word: iii; epub: 16; tagged: 1
- word: adhere; epub: 15; tagged: 0
- word: obstinate; epub: 15; tagged: 0
- word: forego; epub: 14; tagged: 0
- word: vii; epub: 12; tagged: 1
- word: subordinate; epub: 11; tagged: 0
- word: nowhere; epub: 11; tagged: 0

## Untranslated Latin Samples

- phrase: de facto
- phrase: Pietate et religione atque
- phrase: una sapientia
- phrase: deorum hnmortalium
- phrase: omnia regi
- phrase: orator?] Orat. de
- phrase: De Civitate Dei
- phrase: hoc fixum, quos Spiritus sanctus intus
- phrase: acquiescere in Scriptura, et
- phrase: demonstrationi et rationibus subjici eam fas

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
