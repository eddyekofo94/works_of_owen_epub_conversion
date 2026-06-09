# Bug Regression Report: Volume 15

- Status: **WARN**
- EPUB audit: `volume_15_audit.json`
- Text integrity audit: `volume_15_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 4 | 98 | OK |
| Inline structural marker candidates | 1 | 3 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 3 | 3 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 1 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 1 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 0 | 0 | OK |
| Overlong headings containing body prose | 2 | 0 | REGRESSION |
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
| Lowercase page fragments | 11 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch016.xhtml; previous: o are yet "without Christ, being aliens from the commonwealth of Israel, and strangers from the covenants of promise, having no hope, and without God in the world," Ephesians 2:12,; next: — such, we mean, as are either negatively or privatively infidels or unbelievers, who have yet never heard the sound of the gospel, or do continue to refuse and reject it where it 
- file: EPUB/ch022.xhtml; previous: To The Reader; next: I THOUGHT to have wholly omitted the consideration of that part of the discourse of Dr Stillingfleet, in his preface, which concerneth the furtherance and promotion of the designs 
- file: EPUB/ch038.xhtml; previous: e those of which Justice Hobart speaks: and therefore it is plain he spake of all the churches which were under the care of the apostles, which he calls 'voluntary congregations.'"; next: Ans. 1. Whereas this argument seems to be cast into the form of a syllogism, I could easily manifest how asyllogistical it is, did I delight to contend with him or any else. But, —
- file: EPUB/ch059.xhtml; previous: lessness, have miscarried in not observing exactly his will and appointment in and about his worship. This was the case of Nadab and Abihu, the sons of Aaron, Leviticus 10:1, 2; of; next: Korah, Dathan, and Abiram, Numbers 16:1-40; of the sons of Eli, — a sin not to be "expiated with sacrifice nor offering for ever," 1 Samuel 2:27-34, 3:14; of Uzza in putting the ar

### Inline structural marker candidates

- file: EPUB/ch034.xhtml; text: It might be easily demonstrated what great numbers [there are] amongst us, — [1.] Who have imbibed atheistical opinions, and either vent them or speak presumptuously, according unto their influence and tendency every day

### Repeated word windows

- phrase: the unity of the spirit in the bond of peace
- phrase: the whole body fitly joined together and compacted by that
- phrase: whole body fitly joined together and compacted by that which
- phrase: body fitly joined together and compacted by that which every
- phrase: fitly joined together and compacted by that which every joint

### Missing enumerator markers

- marker: (1.)
- marker: (2.)
- marker: (4.)

### Missing Greek clauses

- page: 482; sample: οσοι τω κανονι τουτω στοιχησουσιν

### Repeated phrase hits

- file: combined_text; text: chapter 7 no other church-state of divine institution

### Overlong headings containing body prose

- file: EPUB/ch071.xhtml; text: MAY A PERSON BE CALLED TO, OR BE EMPLOYED IN, A PART ONLY OF THE OFFICE OR WORK OF THE MINISTRY; OR MAY HE HOLD THE RELATION AND EXERCISE THE DUTY OF AN ELDER OR MINISTER UNTO MORE
- file: EPUB/ch082.xhtml; text: MAY NOT THE CHURCH, IN THE SOLEMN WORSHIP OF GOD, AND CELEBRATION OF THE ORDINANCES OF THE GOSPEL, MAKE USE OF AND CONTENT ITSELF IN THE USE OF FORMS OF PRAYER IN AN UNKNOWN TONGUE

### Lowercase page fragments

- file: EPUB/ch015.xhtml; text: for until this be done, men are to be esteemed but as "raging waves of the sea, f
- file: EPUB/ch018.xhtml; text: because, as temporal commodities, so suits did increase. This judgment, though it
- file: EPUB/ch023.xhtml; text: saith Hilary. Suppose that men retain a form of godliness in the profession of th
- file: EPUB/ch037.xhtml; text: unto whom of all sorts it is commanded that they should examine and try antichris
- file: EPUB/ch048.xhtml; text: and that because "there arose not a prophet afterwards in Israel like unto Moses,
