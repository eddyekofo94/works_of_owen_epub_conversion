# Text Integrity Audit: Volume 2

- Status: **WARN**
- Warnings: 1
- PDF pages: 555
- EPUB text files: 50
- EPUB paragraphs/headings: 2213

## Coverage

- PDF content tokens: 184901
- EPUB content tokens: 186958
- Approximate PDF-to-EPUB coverage ratio: 0.9999
- Pages checked: 542
- Weak page matches: 1
- Dense source windows checked: 25228
- Missing dense source-window pages: 37
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 542
- Top-of-page windows skipped as unstable: 20
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 505
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 1859
- Possible faulty paragraph splits: 0
- Structural starts excluded from split warnings: 246
- Short fragments: 22
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 471
- EPUB enumerator markers: 483
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 1

## Greek / Hebrew

- PDF Greek words: 444
- EPUB Greek words: 449
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 88
- EPUB Hebrew words: 89
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 24
- Missing Greek clauses: 0
- Hebrew clauses checked: 11
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 1584
- EPUB Latin words: 1645
- EPUB Tagged Latin words: 468
- Latin word coverage ratio: 0.9987
- Latin word tagging ratio: 0.2845
- Latin clauses checked: 59
- Missing Latin clauses: 0
- Tagged Latin runs checked: 144
- Translated Latin runs: 48
- Latin translation ratio: 0.3333

## Warnings

- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage

## Missing Dense Source Windows

- page: 23; sample: matthew john 19-26 corinthians galatians john 22-24 10-13 hebrews philippians john and distinctly directed
- page: 24; sample: divine worship and honor for ever and ever and therefore stephen in his solemn
- page: 26; sample: teaching of the son is life-giving spirit breathing teaching an effectual influence of light
- page: 53; sample: keepeth not his commandments is liar and the truth is not in him chap
- page: 76; sample: consent unto will be for thee and thou shalt be for me and not
- page: 91; sample: and lo he lives for ever and ever and has the keys of hell
- page: 92; sample: canticles to this very end and purpose cant 10-16 my beloved is white and
- page: 95; sample: so it is land that the lord thy god careth for careth for it
- page: 114; sample: the mystery of godliness timothy and that without controversy we receive grace for grace
- page: 117; sample: will it avail us to hear him proclaim himself the lord the lord god

## Short Fragments

- file: EPUB/ch001.xhtml; text: CHRISTIAN READER,
- file: EPUB/ch002.xhtml; text: To The Reader
- file: EPUB/ch002.xhtml; text: Daniel Burgess
- file: EPUB/ch008.xhtml; text: — of which place afterward.
- file: EPUB/ch018.xhtml; text: Afflictions.
- file: EPUB/ch019.xhtml; text: Hereof, then, are two parts: —
- file: EPUB/ch020.xhtml; text: Of which in the ensuing chapters.
- file: EPUB/ch025.xhtml; text: 5thly . His acting in us;
- file: EPUB/ch032.xhtml; text: END.
- file: EPUB/ch035.xhtml; text: Particularly, —

## Enumerator Sequence Candidates

- file: EPUB/ch014.xhtml; marker: (2.); family: paren_decimal; context: ion, Hosea 3:3; Song of Solomon 1:15 — On the part of Christ — On the part of the saints. (2.) The next thing that comes under consideration is, the way whereby we hold communion with the Lord Christ, in respect of that personal grace wh...

## Repeated Windows

- phrase: is with the father and with his son jesus christ; count: 7
- phrase: bare our sins in his own body on the tree; count: 7
- phrase: our fellowship is with the father and with his son; count: 6
- phrase: fellowship is with the father and with his son jesus; count: 6
- phrase: pleased the father that in him should all fullness dwell; count: 6
- phrase: the father that in him should all fullness dwell colossians; count: 6
- phrase: there are diversities of operations but it is the same; count: 5
- phrase: are diversities of operations but it is the same god; count: 5
- phrase: it pleased the father that in him should all fullness; count: 5
- phrase: to be propitiation through faith in his blood to declare; count: 5

## Missing Word Samples

- word: cant; pdf: 3; epub: 1

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 3; epub: 12
- word: william; pdf: 8; epub: 16
- word: historical; pdf: 0; epub: 8
- word: greek; pdf: 5; epub: 12
- word: modern; pdf: 5; epub: 12
- word: footnotes; pdf: 0; epub: 7
- word: hebrew; pdf: 6; epub: 12
- word: edition; pdf: 5; epub: 11

## Untagged Latin Word Samples

- word: mediator; epub: 164; tagged: 3
- word: adam; epub: 51; tagged: 0
- word: poor; epub: 51; tagged: 1
- word: sum; epub: 42; tagged: 1
- word: elsewhere; epub: 33; tagged: 0
- word: immediate; epub: 33; tagged: 0
- word: savor; epub: 25; tagged: 0
- word: abraham; epub: 25; tagged: 1
- word: mere; epub: 27; tagged: 3
- word: terror; epub: 19; tagged: 0

## Untranslated Latin Samples

- phrase: VII., VIII
- phrase: Trinitatis ad extra
- phrase: super vitas
- phrase: austere, severe
- phrase: admodum prae filiis hominum
- phrase: principium quo
- phrase: principium quod
- phrase: eramus unus
- phrase: massa auri
- phrase: culpa, quae

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
