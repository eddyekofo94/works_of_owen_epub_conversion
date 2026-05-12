# Bug Regression Report: Volume 2

- Status: **PASS**
- EPUB audit: `volume_2_audit.json`
- Text integrity audit: `volume_2_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 61 | 61 | OK |
| Inline structural marker candidates | 0 | 1 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Repeated phrase hits | 1 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: OF; next: "Tell me, O thou whom my soul loveth, where they feedest.' — Song of Solomon l:7.
- file: EPUB/ch004.xhtml; previous: art I. - The fact of communion with God is asserted, CHAP. I Passages in Scripture are quoted to show that special mention is made of communion with all the persons of the Trinity,; next: Communion with the FATHER is described,
- file: EPUB/ch004.xhtml; previous: Communion with the FATHER is described,; next: and practical inferences deduced from it, IV.
- file: EPUB/ch005.xhtml; previous: art I. - The fact of communion with God is asserted, CHAP. I Passages in Scripture are quoted to show that special mention is made of communion with all the persons of the Trinity,; next: Communion with the FATHER is described,
- file: EPUB/ch005.xhtml; previous: Communion with the FATHER is described,; next: and practical inferences deduced from it, IV.

### Repeated word windows

- phrase: bare our sins in his own body on the tree
- phrase: is with the father and with his son jesus christ
- phrase: pleased the father that in him should all fullness dwell
- phrase: the father that in him should all fullness dwell colossians
- phrase: there are diversities of operations but it is the same

### Repeated phrase hits

- file: combined_text; text: part 3 of communion with the holy ghost
