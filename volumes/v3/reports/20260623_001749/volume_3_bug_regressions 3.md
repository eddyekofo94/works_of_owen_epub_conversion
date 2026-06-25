# Bug Regression Report: Volume 3

- Status: **PASS**
- EPUB audit: `volume_3_audit.json`
- Text integrity audit: `volume_3_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 14 | 176 | OK |
| Inline structural marker candidates | 0 | 14 | OK |
| Repeated word windows | 0 | 25 | OK |
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
| Missing Greek clauses | 0 | 1 | OK |
| Missing Hebrew clauses | 0 | 5 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 0 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 0 | 4 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 0 | 1 | OK |
| Overlong headings containing body prose | 0 | 0 | OK |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 0 | OK |
| Fragmented Hebrew span-run files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |
| Scripture blockquote false positives | 0 | 0 | OK |
| Orphan scripture brackets | 0 | 0 | OK |
| Glued ordinal anchors | 0 | 0 | OK |
| Structural bold leaks | 0 | 1 | OK |
| Repeated structural markers | 0 | 0 | OK |
| Scholastic bold leaks | 0 | 0 | OK |
| Inline scholastic labels | 0 | 0 | OK |
| Trailing scholastic labels | 0 | 0 | OK |
| DIGRESSION headings not h3 | 0 | 0 | OK |
| Cross-chapter continuation before heading | 0 | 0 | OK |
| Overlong NAV entries | 0 | 0 | OK |
| Duplicate NAV labels | 0 | 0 | OK |
| Spaced caps OCR | 0 | 0 | OK |
| Lowercase page fragments | 0 | 20 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch008.xhtml; previous: , Philippians 3:10, 2 Thessalonians 1:9, and might do it from other places innumerable, although the first of these will not confirm what it is produced to give countenance unto, —; next: Schlichting. de Trinitat. ad Meisner., p. 605 ); but it is from the manner and end of his being conjoined with the Father and the Son, wherein their "name," — that is, their divine
- file: EPUB/ch010.xhtml; previous: he overflowing of those waters, yet guided by the will and wisdom of God: Isaiah 32:15, "Until the Spirit be poured upon us from on high, and the wilderness be a fruitful field," —; next: עָרָה רוּחַ מִ מָרוֹם עַר־יֵעָרֶה עָלֵינוּ , is, indeed, sometimes "to pour out," but more properly and more commonly "to uncover," "to make bare," "to reveal;" — "Until the Spirit
- file: EPUB/ch012.xhtml; previous: 1. By our external senses; 2. By impressions on the fantasy or imagination; 3. By pure acts of the understanding: so God by three ways revealed his will unto the prophets, —; next: 1 . By objects of their senses, as by audible voices; 2. By impressions on the imagination in dreams and visions; 3. By illustration or enlightening of their minds.
- file: EPUB/ch015.xhtml; previous: th the union of his natures in his person was not in the least impeached; but yet for his soul or spirit, he commends that in an especial manner into the hands of God his Father, —; next: Psalm 31:5, Luke 23:46, "Father, into thy hands I commend my spirit," — for the Father had engaged himself in an eternal covenant to take care of him, to preserve and protect him e
- file: EPUB/ch020.xhtml; previous: t day; for "this is the condemnation, that light is come into the world, and men loved darkness rather than light, because their deeds were evil," chapter 3:19. Hence it follows, —; next: That the will and affections being more corrupted than the understanding, — as is evident from their opposition unto and defeating of its manifold convictions, — no man doth actual
