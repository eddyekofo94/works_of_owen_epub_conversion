# Bug Regression Report: Volume 6

- Status: **PASS**
- EPUB audit: `volume_6_audit.json`
- Text integrity audit: `volume_6_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 15 | 205 | OK |
| Inline structural marker candidates | 3 | 3 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 1 | 1 | OK |
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
| Repeated phrase hits | 1 | 7 | OK |
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
| Lowercase page fragments | 31 | 35 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: CHRISTIAN READER,; next: I SHALL in a few words acquaint thee with the reasons that obtained my consent to the publishing of the ensuing discourse. The consideration of the present state and condition of t
- file: EPUB/ch003.xhtml; previous: s is the sum of the account I shall give) may in anything be useful to the least of the saints, it will be looked on as a return of the weak prayers wherewith it is attended by its; next: unworthy author
- file: EPUB/ch003.xhtml; previous: unworthy author; next: John Owen
- file: EPUB/ch019.xhtml; previous: CHRISTIAN READER,; next: If thou art in any measure awake in these days wherein we live, and hast taken notice of the manifold, great, and various temptations wherewith all sorts of persons that know the L
- file: EPUB/ch022.xhtml; previous: ty of such indispensable necessity to them who intend to walk with God in any peace, or with any faithfulness, — are to be considered and removed. And they are these that follow: —; next: Obj. 1. "Why should we so fear and labor to avoid temptation? James 1:2, we are commanded to 'count it all joy when we fall into divers temptations.' Now, certainly I need not soli

### Inline structural marker candidates

- file: EPUB/ch025.xhtml; text: Such was the state of the church or Sardis, (3.) A season of great spiritual enjoyments is often, by the malice of Satan and the weakness of our hearts, turned into a season of danger as to this business of temptation.
- file: EPUB/ch076.xhtml; text: Indeed, if we should go upon our own heads, without his warranty and authority, to ask any thing at his hand, we might well expect to meet with disappointment; for what should encourage us unto any such boldness? but now
- file: EPUB/ch082.xhtml; text: Gospel pardon is a thing of another nature; it hath its spring in the gracious heart of the Father, is made out by a sovereign act of his will, rendered consistent with the glory of his justice and holiness by the blood 

### Repeated word windows

- phrase: there is forgiveness with thee that thou mayest be feared
- phrase: the lust of the flesh the lust of the eyes
- phrase: from the lord and my judgment is passed over from
- phrase: the lord and my judgment is passed over from my
- phrase: lord and my judgment is passed over from my god

### Missing front CONTENTS pages

- page: 6; sample: chapter the doctrine grounds of it our savior's direction in this case his promise of preservation issues of men entering into temptation of ungrounded professors of the choicest

### Repeated phrase hits

- file: combined_text; text: institution of religious worship an evidence of forgiveness

### Lowercase page fragments

- file: EPUB/ch003.xhtml; text: unworthy author
- file: EPUB/ch004.xhtml; text: and reduce the whole to an improvement of the great evangelical truth and mystery
- file: EPUB/ch006.xhtml; text: and of our repentance our mortification is no small portion. How doth he do it? H
- file: EPUB/ch037.xhtml; text: a similitude most lively, expressing the lustings of the law of sin, restlessly a
- file: EPUB/ch044.xhtml; text: and with the prophet, Hosea 14:9,
