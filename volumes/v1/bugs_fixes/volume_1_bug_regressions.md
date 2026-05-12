# Bug Regression Report: Volume 1

- Status: **WARN**
- EPUB audit: `volume_1_audit.json`
- Text integrity audit: `volume_1_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 13 | 13 | OK |
| Inline structural marker candidates | 1 | 1 | OK |
| Repeated word windows | 25 | 25 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Repeated phrase hits | 7 | 6 | REGRESSION |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |

## New Warning Codes

- EPUB: orphan_endnotes

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch011.xhtml; previous: But —; next: There was yet more required thereunto, or to render his offices effectual unto their proper ends. Not one of them could have been so, had he been no more than a man — had he had no
- file: EPUB/ch011.xhtml; previous: And he discharged this office four ways: —; next: (1st,) By personal appearances in the likeness of human nature, in the shape of a man, as an indication of his future incarnation; and under those appearances instructing the churc
- file: EPUB/ch011.xhtml; previous: ls was subordinate unto him; and whatever instruction was thereby given unto the church in the mind and will of God, it was immediately from him, as the great prophet of the church; next: (3rdly,) By sending his Holy Spirit to inspire, act, and guide the prophets, by whom God would reveal himself. God spoke unto them by the "mouth of his holy prophets, which have be
- file: EPUB/ch013.xhtml; previous: nce, or a readiness thereunto. Hence is that expression, "He bowed down his head and worshipped," [ Genesis 24:26;] see [also] Psalm 95:6. And these external signs are of two sorts; next: (1st,) Such as are natural and occasional;
- file: EPUB/ch013.xhtml; previous: ofession of the gospel, are another season rendering this peculiar invocation of Christ both comely and necessary. Two things will befall the minds of believers in such a season; —; next: [1st,] that their thoughts will be neatly exercised about him, and conversant with him. They cannot but continually think and meditate on him for whom they suffer. None ever suffer

### Inline structural marker candidates

- file: EPUB/ch019.xhtml; text: Whatever men may fancy to the contrary, it is the design of the apostle, in sundry places of his writings, to prove that they did so, especially Romans 1; 1 Corinthians 1. Wherefore, it was an infinite condescension of d

### Repeated word windows

- phrase: the glory of god in the face of jesus christ
- phrase: between our beholding the glory of christ by faith in
- phrase: our beholding the glory of christ by faith in this
- phrase: beholding the glory of christ by faith in this world
- phrase: the glory of christ by faith in this world and

### Repeated phrase hits

- file: combined_text; text: chapter 14 motives unto the love of christ
- file: combined_text; text: meditations and discourses on the glory of christ
- file: combined_text; text: the greater catechism chapter 1 of the scripture
- file: combined_text; text: chapter 8 of the state of corrupted nature
- file: combined_text; text: chapter 14 of the two-fold estate of christ
