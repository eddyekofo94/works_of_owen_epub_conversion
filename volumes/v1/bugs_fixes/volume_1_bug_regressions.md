# Bug Regression Report: Volume 1

- Status: **PASS**
- EPUB audit: `volume_1_audit.json`
- Text integrity audit: `volume_1_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 101 | 125 | OK |
| Inline structural marker candidates | 1 | 6 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| Low-density chapter failures | 0 | 0 | OK |
| Malformed transition budget failures | 0 | 0 | OK |
| Fragmented sentence runs | 0 | 0 | OK |
| Low Greek word coverage | 0 | 0 | OK |
| Low Hebrew word coverage | 1 | 0 | OK |
| Missing Greek clauses | 0 | 0 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 5 | 8 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 1 | 3 | OK |
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
| Lowercase page fragments | 7 | 38 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch004.xhtml; previous: on, the Only-begotten, the First-begotten, the Door, the Way, the Arrow, Wisdom, and sundry other things." And Ennodius has, as it were, turned this passage of Jerome into verse: —; next: Chap. IV. That he was the foundation of all the holy counsels of God, with respect unto the vocation, sanctification, justification, and eternal salvation of the church, is, in the
- file: EPUB/ch009.xhtml; previous: nswer hereunto God tells him, that he cannot see his face and live; none can have either bodily sight or direct mental intuition of the Divine Being. But this I will do, saith God,; next: This is all that God would grant, viz, such external representations of himself, in the proclamation of his name, and created appearances of his glory, as we have of a man whose ba
- file: EPUB/ch009.xhtml; previous: he being of God, his infinite wisdom, power, and goodness — viz., in the impressions and characters of them on the things that were made — in their own representations of him, they; next: Wherefore this common presumption — that there was no way to attain a due sense of the Divine Being but by some representation of it — though true in itself, yet, by the craft of S
- file: EPUB/ch009.xhtml; previous: This was the testimony which the apostles gave concerning him, when he dwelt among them in the days of his flesh. They saw; next: The divine glory was manifest in him, and in him they saw the glory of the Father. So the same apostle witnesses again, who recorded this testimony:
- file: EPUB/ch010.xhtml; previous:  wisdom and knowledge of God — in his counsels concerning the vocation, sanctification, and salvation, of the church — concerning which the apostle falls into that holy admiration,; next: And they are called "treasures" on a twofold account, both mentioned together by the Psalmist. "How precious are thy thoughts unto me, O Lord; how great is the sum of them!" They a

### Inline structural marker candidates

- file: EPUB/ch031.xhtml; text: In the susception of this office we may behold the glory of Christ, — I. In his condescension; II. In his love.

### Repeated word windows

- phrase: the glory of god in the face of jesus christ
- phrase: between our beholding the glory of christ by faith in
- phrase: our beholding the glory of christ by faith in this
- phrase: beholding the glory of christ by faith in this world
- phrase: the glory of christ by faith in this world and

### Repeated phrase hits

- file: combined_text; text: chapter 14 motives unto the love of christ
- file: combined_text; text: meditations and discourses on the glory of christ
- file: combined_text; text: chapter 8 of the state of corrupted nature
- file: combined_text; text: chapter 10 of the person of jesus christ
- file: combined_text; text: chapter 14 of the two-fold estate of christ

### Chapter headings rendered as paragraphs

- file: EPUB/ch003.xhtml; text: Chapter 1

### Lowercase page fragments

- file: EPUB/ch004.xhtml; text: factores autem sermonum ejus facti, communionem habeamus cum ipso".
- file: EPUB/ch008.xhtml; text: as he also proclaims the same delight in him, from heaven, in the days of his fle
- file: EPUB/ch016.xhtml; text: and verse 23, "My Father will love him, and we will come unto him, and make our a
- file: EPUB/ch022.xhtml; text: and in sundry other places. The assumption, the taking of our human nature to be
- file: EPUB/ch030.xhtml; text: against him he lifted up himself; — which was the beginning of his transgression.
