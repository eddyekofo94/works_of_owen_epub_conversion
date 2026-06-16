# Bug Regression Report: Volume 9

- Status: **PASS**
- EPUB audit: `volume_9_audit.json`
- Text integrity audit: `volume_9_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 38 | 61 | OK |
| Inline structural marker candidates | 1 | 1 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 4 | 4 | OK |
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
| Chapter headings rendered as paragraphs | 1 | 1 | OK |
| Overlong headings containing body prose | 5 | 5 | OK |
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
| Lowercase page fragments | 2 | 2 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: s transferred to the apostate Church of Rome in the New, and all applied unto it, in the Book of the Revelation; and that upon this great analogy, which I shall now briefly show: —; next: Why doth God call the apostate state of the church, under the New Testament, "Babylon, Babylon the Mystery?" For these three reasons: — First. As old Babylon was the rise and sprin
- file: EPUB/ch003.xhtml; previous: What I shall speak to is this: —; next: When a land is filled with sin against the Lord, let men's hopes and expectations be what they will, they are in danger of utter destruction, and cannot be saved but by the actings
- file: EPUB/ch003.xhtml; previous: e I take this — yea, and I take it in the best of my hopes — to be that wherein we are concerned, pray take these two things along with you, before I go to show it in particular: —; next: The first is, that, in this state, if God gives time and space, there is encouragement enough left to make our applications to him for the removal of impending judgments. Methinks 
- file: EPUB/ch003.xhtml; previous:  another hand; — the case of this nation is such, that without repentance evidenced, and universal reformation sincerely endeavored, England cannot be saved, — will not be saved; —; next: God will forsake it, — destruction from the Lord will overtake us.
- file: EPUB/ch006.xhtml; previous: The words may yield us these two observations: —; next: Observation 1. All staggering at the promises of God is through unbelief.

### Inline structural marker candidates

- file: EPUB/ch003.xhtml; text: I shall speak yet a little more particularly. You may consider in the words, 1. That which is mentioned in the last place; — the state of the people at this time: "Their land was filled with sin against the Holy One of I

### Repeated word windows

- phrase: discourse discourse discourse discourse discourse discourse discourse discourse discourse discourse
- phrase: loved us and washed us from our sins in his
- phrase: us and washed us from our sins in his own
- phrase: and washed us from our sins in his own blood
- phrase: is so filled with sin against the holy one of

### Missing front CONTENTS pages

- page: 3; sample: contents of vol part sermon published prefatory note by the editor seasonable words for english protestants part sermons published prefatory note by the editor the strength of faith
- page: 4; sample: discourse seeing the act of closing with christ is secret and hidden and the special times and seasons of our conversion unto god are unknown unto most what
- page: 5; sample: the excellency of christ the use and advantage of faith in time of public calamity the use of faith under reproaches and persecutions the use of faith if
- page: 6; sample: also he took the cup when he had supped saying this cup is the new testament in my blood this do ye as oft as ye drink it

### Chapter headings rendered as paragraphs

- file: EPUB/ch059.xhtml; text: Chapter 4

### Overlong headings containing body prose

- file: EPUB/ch002.xhtml; text: "To the Reader — Upon the desire of some interested in the publication of this sermon, I have perused it, and do communicate these my thoughts concerning it. "There appear unto me
- file: EPUB/ch044.xhtml; text: DISCOURSE 7. 44 Question. When our own faith is weakened as to the hearing of our prayers — when we ourselves are hindered within ourselves from believing the answer of our pray
- file: EPUB/ch053.xhtml; text: "To The Reader, — The following Discourses were preached by that truly venerable divine in the last century, Dr John Owen: and, in order to be fully satisfied they are genuine, Mrs
- file: EPUB/ch060.xhtml; text: SERMON 7. 61 "My heart is inditing a good matter: I speak of the things which I have made touching the King; my tongue is the pen of a ready writer. Thou art fairer than the chi
- file: EPUB/ch089.xhtml; text: DISCOURSE 19. 86 "I am crucified with Christ: nevertheless I live; yet not I, but Christ liveth in me: and the life which I now live in the flesh I live by the faith of the Son

### Lowercase page fragments

- file: EPUB/ch002.xhtml; text: the Lord; ' — nay, now, that it is neither day nor night, as the prophet speaks;
- file: EPUB/ch067.xhtml; text: of Stoke Newington
