# Bug Regression Report: Volume 11

- Status: **WARN**
- EPUB audit: `volume_11_audit.json`
- Text integrity audit: `volume_11_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 40 | 150 | OK |
| Inline structural marker candidates | 7 | 8 | OK |
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
| Chapter headings rendered as paragraphs | 0 | 1 | OK |
| Overlong headings containing body prose | 0 | 1 | OK |
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
| Lowercase page fragments | 9 | 1 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch001.xhtml; previous: BY; next: John Owen
- file: EPUB/ch001.xhtml; previous: John Owen; next: SERVANT OF JESUS CHRIST IN THE WORKE OF THE GOSPELL
- file: EPUB/ch001.xhtml; previous: SERVANT OF JESUS CHRIST IN THE WORKE OF THE GOSPELL; next: OXFORD, PRINTED BY LEON. LICHFIELD PRINTER TO THE UNIVERSITY, FOR TIM. ROBINSON.
- file: EPUB/ch005.xhtml; previous: k to deal so harshly with some of them with whom he hath to do. And it is still feared that "Parata tollit cornua; Qualis Lycambae spretus infido gener, Aut acer hostis Bupalo ." 3; next: It might, indeed, be the more excusable if evident provocation were always ready at hand to be charged with the blame of this procedure, if he said only,
- file: EPUB/ch005.xhtml; previous: st of a crooked and perverse generation, knowing that it is but yet a little while, and he that shall come will come, and will not tarry. Yea, come, Lord Jesus, come. So prays your; next: unworthy fellow-laborer and brother in our dear Lord Jesus

### Inline structural marker candidates

- file: EPUB/ch003.xhtml; text: Five leading arguments are adduced in proof of the perseverance of the saints: — It is argued, 1. From the divine nature as immutable; under which head the following passages are considered, [Malachi 3:6] [James 1:16] -1
- file: EPUB/ch013.xhtml; text: The latter I at present only intend. Saith he, 1. "I know them;" 2. "I give them eternal life;" 3. "They shall never perish;" 4. "No man shall pluck them out of my hand;" 5. "My Father is omnipotent, and hath a sovereign
- file: EPUB/ch015.xhtml; text: Their quickening is everywhere ascribed to the Spirit that is given unto them; there is not a quickening, a life-giving power, in a quality, a created thing. In the state of nature, besides gracious dispensations and hab
- file: EPUB/ch019.xhtml; text: Sect. 12, "If the principles of the doctrine we speak of dissolve the efficiency of the said threatenings towards the end for the accomplishment whereof they are given, then they render them unsavory, useless, and vain; 
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

### Lowercase page fragments

- file: EPUB/ch005.xhtml; text: unworthy fellow-laborer and brother in our dear Lord Jesus
- file: EPUB/ch006.xhtml; text: for his terming him a grammarian; yet, indeed, of him (such was the hard entertai
- file: EPUB/ch008.xhtml; text: the spiritual peace and salvation of their souls, as naturally men are to forbear
- file: EPUB/ch010.xhtml; text: it is said of him,
- file: EPUB/ch012.xhtml; text: and in [1 John 4:10] "Herein is love, not that we loved God, but that he loved us
