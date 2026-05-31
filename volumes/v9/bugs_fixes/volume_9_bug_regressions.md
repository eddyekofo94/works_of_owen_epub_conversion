# Bug Regression Report: Volume 9

- Status: **WARN**
- EPUB audit: `volume_9_audit.json`
- Text integrity audit: `volume_9_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 186 | 61 | REGRESSION |
| Inline structural marker candidates | 5 | 1 | REGRESSION |
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
| Chapter headings rendered as paragraphs | 1 | 0 | REGRESSION |
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
| Lowercase page fragments | 1 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch002.xhtml; previous: celebrated and much-respected preacher in London, — a kind of Latimer among the Nonconformists of his time. He died in 1713, and his funeral sermon was preached by Matthew Henry: —; next: the Lord; ' — nay, now, that it is neither day nor night, as the prophet speaks; — now, that city. and country are crying, 'Watchman, what of the night? ?' — now, that the three fr
- file: EPUB/ch003.xhtml; previous: This was not now the case of Israel and Judah. It proved afterward to be their case, as the apostle describes it, 1 Thessalonians 2:15, 16,; next: How come? They have filled their measure, reached to their bounds; — "wrath is come upon them to the uttermost." I hope, I pray, that this is not, that this may not be, the state o
- file: EPUB/ch003.xhtml; previous:  but let all mankind do what they will, he will not pass it by without some severe, desolating judgment. Such was their case even at this time; — you may see in 2 Chronicles 36:16,; next: It was impossible that the judgment of God should be turned away from them. In this state God saith, "Pray not for this people; my heart shall not be toward them," (until he had br
- file: EPUB/ch003.xhtml; previous:  are absolutely resolved upon sovereign grace and mercy: and without relief from thence, I shall only say, as to the proof of the proposition, what the prophet saith, Isaiah 34:16,; next: To omit all the considerations and all the proof I intended, that sovereign grace and mercy must be our relief, if ever we be relieved, I proceed unto the second thing; which is, —
- file: EPUB/ch006.xhtml; previous: e first place. Eternal life is promised by God, who cannot lie, Titus 1:2; that is, who is so faithful, as that it is utterly impossible he should deceive any. So Hebrews 6:17, 18,; next: The design of God is, that we may receive encouragement in our flying for refuge to the hope set before us, — that is, in believing. What doth he propose to this end? Why, his own 

### Inline structural marker candidates

- file: EPUB/ch011.xhtml; text: Now, surely, if God hath this delight in us in our walking before him, is it not expected that our delight should be in him in our obedience? It suits not my present business to go over the testimonies of Scripture, wher
- file: EPUB/ch021.xhtml; text: The latter containeth, — 1. A doctrinal observation for the use of the church, from the whole, verse 7. 2. The reasons and confirmation of the doctrine so laid down, taken from the power and righteousness of God in the a
- file: EPUB/ch021.xhtml; text: They shall have no better issue, because, — (1.) The Lord will take away their stout hearts, whereby they are supported; (2.) He will take away their strong hands, whereby they are confirmed: and when hearts and hands ar
- file: EPUB/ch024.xhtml; text: His estate is doubly expressed: — 1. From the place where he was, — " From the end of the earth;" and, 2. From the condition he was in, — " His heart was overwhelmed." And in the course he steered there are two things al
- file: EPUB/ch029.xhtml; text: There is a twofold hardening from God's fear: — 1. There is a total hardening; and, 2. A partial hardening: — 1. There is a total hardening, like that mentioned, Isaiah 6:10,

### Repeated word windows

- phrase: as often as ye eat this bread and drink this
- phrase: often as ye eat this bread and drink this cup
- phrase: loved us and washed us from our sins in his
- phrase: us and washed us from our sins in his own
- phrase: and washed us from our sins in his own blood

### Chapter headings rendered as paragraphs

- file: EPUB/ch059.xhtml; text: Chapter 4

### Overlong headings containing body prose

- file: EPUB/ch002.xhtml; text: "To the Reader — Upon the desire of some interested in the publication of this sermon, I have perused it, and do communicate these my thoughts concerning it. "There appear unto me
- file: EPUB/ch053.xhtml; text: "To The Reader, — The following Discourses were preached by that truly venerable divine in the last century, Dr John Owen: and, in order to be fully satisfied they are genuine, Mrs

### Lowercase page fragments

- file: EPUB/ch002.xhtml; text: the Lord; ' — nay, now, that it is neither day nor night, as the prophet speaks;
