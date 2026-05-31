# Bug Regression Report: Volume 11

- Status: **WARN**
- EPUB audit: `volume_11_audit.json`
- Text integrity audit: `volume_11_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 143 | 61 | REGRESSION |
| Inline structural marker candidates | 4 | 1 | REGRESSION |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 4 | 0 | REGRESSION |
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
| Chapter headings rendered as paragraphs | 1 | 0 | REGRESSION |
| Overlong headings containing body prose | 1 | 0 | REGRESSION |
| Missing chapter initialization files | 0 | 0 | OK |
| Fragmented Greek span-run files | 0 | 0 | OK |
| Fragmented Hebrew span-run files | 0 | 0 | OK |
| Noteref links without spacing class | 0 | 0 | OK |
| Scripture blockquote false positives | 0 | 0 | OK |
| Orphan scripture brackets | 0 | 0 | OK |
| Glued ordinal anchors | 0 | 0 | OK |
| Structural bold leaks | 2 | 0 | REGRESSION |
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

- file: EPUB/ch001.xhtml; previous: OR, THE; next: DOCTRINE OF THE
- file: EPUB/ch001.xhtml; previous: DOCTRINE OF THE; next: SAINTS PERSEVERANCE _Explained and Confirmed._ **THE CERTAIN PERMANENCY OF THEIR**
- file: EPUB/ch004.xhtml; previous: TO; next: Your Highness's most humble and most faithful servant, John Owen
- file: EPUB/ch005.xhtml; previous: ll manner of signal improvements that may render it keen or pleasant, according to his intendment or desire. What the Latin lyric said of the Grecian poets may be applied to him: —; next: And he is hereby plainly possessed of not a few advantages. It is true that when the proof of his opinion by argument, and the orderly pursuit of it, is incumbent on him (a course 
- file: EPUB/ch005.xhtml; previous: ak to deal so harshly with some of them with whom he hath to do. And it is still feared that "Parata tollit cornua; Qualis Lycambae spretus infido gener, Aut acer hostis Bupalo." 3; next: It might, indeed, be the more excusable if evident provocation were always ready at hand to be charged with the blame of this procedure, if he said only,

### Inline structural marker candidates

- file: EPUB/ch012.xhtml; text: Gospel promises, then, are, — 1. The free and gracious dispensations, and, 2. discoveries of God's good-will and love, to, 3. sinners, 4. through Christ, 5. in a covenant of grace;
- file: EPUB/ch022.xhtml; text: That they should be saved by Christ, and yet not washed in his blood, not sanctified by his Spirit (which to be is to be regenerate), is another new notion of the new gospel The countenance which Mr. Goodwin would beg to
- file: EPUB/ch022.xhtml; text: The proposition is ready at hand in the words, "He that is born of God doth not, cannot commit sin." The reason of the proposition confirming the truth thereof is twofold: — 1. Because he is born of God; 2. Because His s
- file: EPUB/ch023.xhtml; text: Mr. G.'s seventh argument, about the tendency of the doctrine of the saints' apostasy as to their consolation, proposed, considered — What that doctrine offereth for the consolation of the saints stated — The impossibili

### Repeated word windows

- phrase: both to will and to do of his good pleasure
- phrase: all things work together for good to them that love
- phrase: law in their inward parts and write it in their
- phrase: in their inward parts and write it in their hearts
- phrase: he wrought in christ when he raised him from the

### Missing enumerator markers

- marker: (1)
- marker: (1.)
- marker: (2.)
- marker: (3.)

### Chapter headings rendered as paragraphs

- file: EPUB/contents_2.xhtml; text: CHAPTER 1

### Overlong headings containing body prose

- file: EPUB/ch004.xhtml; text: HIS HIGHNESS OLIVER, LORD-PROTECTOR OF THE COMMONWEALTH OF ENGLAND, SCOTLAND, AND IRELAND, WITH THE DOMINIONS THEREOF. SIR, THE wise man tells us that "no man knoweth love or hatre

### Structural bold leaks

- file: EPUB/ch001.xhtml; text: SAINTS PERSEVERANCE _Explained and Confirmed._ **THE CERTAIN PERMANENCY OF THEIR**
- file: EPUB/ch013.xhtml; text: 1. That from the beginning to verse 14 containeth a most fearful and dreadful commination and threatening of the judgments of the Lord against the whole church

### Lowercase page fragments

- file: EPUB/ch017.xhtml; text: of perseverance in reference to the
