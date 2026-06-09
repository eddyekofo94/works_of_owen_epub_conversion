# Bug Regression Report: Volume 11

- Status: **WARN**
- EPUB audit: `volume_11_audit.json`
- Text integrity audit: `volume_11_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 14 | 150 | OK |
| Inline structural marker candidates | 8 | 8 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 2 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 3 | 5 | OK |
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
| Repeated phrase hits | 0 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 0 | 1 | OK |
| Overlong headings containing body prose | 1 | 1 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 0 | OK |
| Fragmented Hebrew span-run files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |
| Scripture blockquote false positives | 0 | 0 | OK |
| Orphan scripture brackets | 0 | 0 | OK |
| Glued ordinal anchors | 0 | 0 | OK |
| Structural bold leaks | 0 | 2 | OK |
| Repeated structural markers | 0 | 0 | OK |
| Scholastic bold leaks | 0 | 0 | OK |
| Inline scholastic labels | 0 | 0 | OK |
| Trailing scholastic labels | 0 | 0 | OK |
| DIGRESSION headings not h3 | 0 | 0 | OK |
| Cross-chapter continuation before heading | 0 | 0 | OK |
| Overlong NAV entries | 0 | 0 | OK |
| Duplicate NAV labels | 0 | 0 | OK |
| Spaced caps OCR | 0 | 0 | OK |
| Lowercase page fragments | 8 | 1 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch005.xhtml; previous: ak to deal so harshly with some of them with whom he hath to do. And it is still feared that "Parata tollit cornua; Qualis Lycambae spretus infido gener, Aut acer hostis Bupalo." 3; next: It might, indeed, be the more excusable if evident provocation were always ready at hand to be charged with the blame of this procedure, if he said only,
- file: EPUB/ch005.xhtml; previous: st of a crooked and perverse generation, knowing that it is but yet a little while, and he that shall come will come, and will not tarry. Yea, come, Lord Jesus, come. So prays your; next: unworthy fellow-laborer and brother in our dear Lord Jesus
- file: EPUB/ch005.xhtml; previous: unworthy fellow-laborer and brother in our dear Lord Jesus; next: John Owen
- file: EPUB/ch006.xhtml; previous: o make the matter more clear, cap. 13, he disputes, that " Auxilium sine quo nullus perseverat, et per quod quilibet perseverat, est Spiritus Sanctus, divina bonitas et voluntas. "; next: Every cause of bringing sinful man to God is called by them "auxilium.' In these three, "Spiritus Sanctus, divina bonitas, et voluntas," he compriseth the chief causes of persevera
- file: EPUB/ch008.xhtml; previous:  of many in these days — The great offense given and taken thereby, with the provision made for its removal — The nature of that offense and temptation thence arising considered _—; next: Answer to some arguings of Mr. G., chap. 9, from thence against the truth proposed — The use of trials and shakings — Grounds of believers' assurance that they are so — The same fa

### Inline structural marker candidates

- file: EPUB/ch010.xhtml; text: All these things, to the falling of a hair or the withering of a [blade of] grass, hath he determined from of old. Now, this divine fore-appointment of all things the Scripture assigns sometimes to the knowledge and unde
- file: EPUB/ch010.xhtml; text: I shall only add that, — 1. When Mr. Goodwin shall make good that order and series of decrees here by him mentioned from the Scripture, or with solid reason from the nature of the things themselves, suitably to the prope
- file: EPUB/ch012.xhtml; text: Gospel promises, then, are, — 1. The free and gracious dispensations, and, 2. discoveries of God's good-will and love, to, 3. sinners, 4. through Christ, 5. in a covenant of grace; 6. wherein, upon his truth and faithful
- file: EPUB/ch013.xhtml; text: The former argument confirmed by an induction of particular instances — [Joshua 1:5] opened — The concernment of all believers in that promise proved by the apostle, Hebrews 42:5. — The general interest of all believers 
- file: EPUB/ch022.xhtml; text: As to the matter in hand, this is evident by the light of this single consideration, that in such an ecclesiastical body of Christ there are always, or may be, — and Christ himself, in the rules and laws that he hath giv

### Repeated word windows

- phrase: both to will and to do of his good pleasure
- phrase: law in their inward parts and write it in their
- phrase: in their inward parts and write it in their hearts
- phrase: all things work together for good to them that love
- phrase: he wrought in christ when he raised him from the

### Missing enumerator markers

- marker: (1.)
- marker: (2.)
- marker: (3.)

### Low Greek word coverage

- {'word': 'ὅπερ', 'pdf': 3, 'epub': 1}

### Missing Greek clauses

- page: 68; sample: κυριος ανευ του πατρος ουδεν ποιει ου δυναμαι γαρ φησι ποιειν εμαυτου

### Overlong headings containing body prose

- file: EPUB/ch004.xhtml; text: HIS HIGHNESS OLIVER, LORD-PROTECTOR OF THE COMMONWEALTH OF ENGLAND, SCOTLAND, AND IRELAND, WITH THE DOMINIONS THEREOF. SIR, THE wise man tells us that "no man knoweth love or

### Lowercase page fragments

- file: EPUB/ch005.xhtml; text: unworthy fellow-laborer and brother in our dear Lord Jesus
- file: EPUB/ch006.xhtml; text: cant et fructum afferant, et fructus eorum maneat, quis audeat dicere 'Forsitan n
- file: EPUB/ch010.xhtml; text: it is said of him,
- file: EPUB/ch012.xhtml; text: and in [1 John 4:10] "Herein is love, not that we loved God, but that he loved us
- file: EPUB/ch015.xhtml; text: and verse 22, "Let them be one, even as we, are one." And that ye may not think t
