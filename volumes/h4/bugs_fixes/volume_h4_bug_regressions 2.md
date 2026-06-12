# Bug Regression Report: Volume h4

- Status: **WARN**
- EPUB audit: `volume_h4_audit.json`
- Text integrity audit: `volume_h4_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 40 | 61 | OK |
| Inline structural marker candidates | 16 | 1 | REGRESSION |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 1 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 1 | 0 | REGRESSION |
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

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch001.xhtml; previous: men of one age: Eccles. 1:4, "One generation passeth away, and another generation cometh,"—that is, the men of one age. See Deut. 32:7. So is γενεή , as in Homer's Iliad, vi. 146:—; next: Οἵη περ θύλλων γενεὴ , τοιήδε καὶ ἀνδρῶν .
- file: EPUB/ch001.xhtml; previous: oice of God, if you will choose so to do, take heed of that which would certainly be a hinderance thereof.' Thus dealeth the apostle with the Hebrews; and herein teacheth us that,—; next: Obs. V. The formal reason of all our obedience consists in its relation to the voice or authority of God.
- file: EPUB/ch001.xhtml; previous: whereon they invited unto a feast all the priests that ministered. But most frequently they so express a present opportunity or season. So the Greeks use σήμερον , as in Anacreon,—; next: Σήμερον μέλει μοι · τὸ δὲ αὔριον τίς οἷδε ;—
- file: EPUB/ch001.xhtml; previous: Σήμερον μέλει μοι · τὸ δὲ αὔριον τίς οἷδε ;—; next: "My care is for to-day" (the present season); "who knows to-morrow" (or the time to come)?
- file: EPUB/ch001.xhtml; previous:  fall out). "Sufficient unto the day" (the present time and season) "is the evil thereof." To the same purpose do they use "hodie" in the Latin tongue, as in these common sayings,—; next: " Sera nimis vita est crastina , viv' hodie:"

### Inline structural marker candidates

- file: EPUB/ch002.xhtml; text: 1. What from the nature of the things themselves, which are suited unto the various states, conditions, and apprehensions of the minds of men; 2. What from the manner of their expression, on which a character of divine w
- file: EPUB/ch003.xhtml; text: 1. What from the nature of the things themselves, which are suited unto the various states, conditions, and apprehensions of the minds of men; 2. What from the manner of their expression, on which a character of divine w
- file: EPUB/ch005.xhtml; text: 1. That those that preach it are sent of God; 2. That what is preached be according to the analogy of faith; 3. That it be drawn from the written word; 4. That it be delivered in the name and authority of God.
- file: EPUB/ch010.xhtml; text: 1. That those that preach it are sent of God; 2. That what is preached be according to the analogy of faith; 3. That it be drawn from the written word; 4. That it be delivered in the name and authority of God.
- file: EPUB/ch014.xhtml; text: To complete our profession, yea, to constitute our ὁμολογία , there is required that we make a solemn declaration of our subjection unto the gospel in these things. And this is made two ways. (1.) By works. (2.) By words

### Repeated word windows

- phrase: if ye will hear his voice harden not your hearts
- phrase: it is said to-day if ye will hear his voice
- phrase: any of you should seem to come short of it
- phrase: although the works were finished from the foundation of the
- phrase: the works were finished from the foundation of the world

### Missing Hebrew clauses

- page: 2; sample: כְּקֹלוֹ קוֹל יְהוֹהָ
