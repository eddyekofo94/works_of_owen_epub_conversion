# Bug Regression Report: Volume h7

- Status: **WARN**
- EPUB audit: `volume_h7_audit.json`
- Text integrity audit: `volume_h7_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 40 | 61 | OK |
| Inline structural marker candidates | 40 | 1 | REGRESSION |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 2 | 0 | REGRESSION |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 1 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 0 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 0 | 0 | OK |
| Overlong headings containing body prose | 0 | 0 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 0 | OK |
| Fragmented Hebrew span-run files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |
| Scripture blockquote false positives | 0 | 0 | OK |
| Orphan scripture brackets | 0 | 0 | OK |
| Glued ordinal anchors | 0 | 0 | OK |
| Structural bold leaks | 0 | 0 | OK |
| Repeated structural markers | 0 | 0 | OK |
| Scholastic bold leaks | 0 | 0 | OK |
| Inline scholastic labels | 0 | 0 | OK |
| Trailing scholastic labels | 0 | 0 | OK |
| DIGRESSION headings not h3 | 0 | 0 | OK |
| Cross-chapter continuation before heading | 0 | 0 | OK |
| Overlong NAV entries | 0 | 0 | OK |
| Duplicate NAV labels | 0 | 0 | OK |
| Spaced caps OCR | 0 | 0 | OK |
| Lowercase page fragments | 0 | 0 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## New Warning Codes

- Text integrity: reference_continuation_splits

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch002.xhtml; previous: In these ways, and by these means, "faith is the substance of things hoped for;" and,—; next: Obs. I. No faith will carry us through the difficulties of our profession, from oppositions within and without, giving us constancy and perseverance therein unto the end, but that 
- file: EPUB/ch002.xhtml; previous: hat it makes a life on things invisible. It is not only conversant about them, but mixeth itself with them, making them the spiritual nourishment of the soul, 2 Cor. 4:16-18. And,—; next: Obs. III. The glory of our religion is, that it depends on, and is resolved into invisible things. They are far more excellent and glorious than any thing that sense can behold or 
- file: EPUB/ch002.xhtml; previous: sion under trouble and persecution; with a discovery of the nature and end of the ensuing instances, with their suitableness unto his purpose. And we may observe in general, that,—; next: Obs. V. It is faith alone that takes believers out of this world whilst they are in it, that exalts them above it whilst they are under its rage; that enables them to live upon thi
- file: EPUB/ch003.xhtml; previous: ony is assigned to faith alone; as for other reasons, so because all those other things were fruits of their faith, whose acceptance with God depended thereon. And we may observe,—; next: Obs. III. It is faith alone which from the beginning of the world (or from the giving of the first promise) was the means and way of obtaining acceptance with God.—There hath been 
- file: EPUB/ch004.xhtml; previous: ne; and some assigned such a beginning unto it, as it had been better it never had any. Nothing but an assent unto divine revelation can give us a clear understanding hereof. And,—; next: Obs. II. Then doth faith put forth its power in our minds in a due manner, when it gives us clear and distinct apprehensions of the things we do believe. Faith that gives not under

### Inline structural marker candidates

- file: EPUB/ch006.xhtml; text: Of this Enoch it is affirmed, 1. That he was "translated;" 2. The end of that translation is declared, "that he should not see death;" 3. The consequent of it, "he was not found;" 4. The efficient cause of that translati
- file: EPUB/ch006.xhtml; text: In the field of conjectures used on this occasion, I judge it probable, (1.) That his rapture was visible, in the sight of many that feared God, who were to be witnesses of it unto the world, that it might be his ordinan
- file: EPUB/ch008.xhtml; text: There is in the words, 1. The person spoken of or instanced in; which is Noah.
- file: EPUB/ch008.xhtml; text: Δι ʼ ἧς . (2.) Lastly, There is a double consequent of this faith of Noah and his obedience therein; [1.] With respect unto the world, "he condemned it;" [2.] With respect unto himself, he "became heir of the righteousne
- file: EPUB/ch011.xhtml; text: There is in the words, 1. A supposition that these pilgrims had originally a country of their own whereunto they did belong.

### Repeated word windows

- phrase: run with patience the race that is set before us
- phrase: seed all the nations of the earth should be blessed
- phrase: made mention of the departing of the children of israel
- phrase: the two states of the law and the gospel with
- phrase: every weight and the sin that doth so easily beset

### Reference continuation splits

- file: EPUB/ch034.xhtml; previous: All this he "patiently endured," as the sense of the word was declared on the foregoing verse.; next: 4.
- file: EPUB/ch036.xhtml; previous: All this he "patiently endured," as the sense of the word was declared on the foregoing verse.; next: 4.
