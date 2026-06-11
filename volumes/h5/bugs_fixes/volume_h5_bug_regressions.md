# Bug Regression Report: Volume h5

- Status: **WARN**
- EPUB audit: `volume_h5_audit.json`
- Text integrity audit: `volume_h5_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 40 | 61 | OK |
| Inline structural marker candidates | 32 | 1 | REGRESSION |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 0 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 1 | 0 | REGRESSION |
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
| Lowercase page fragments | 0 | 0 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch002.xhtml; previous:  all. Neither was a due consideration hereof ever more necessary than it is in the days wherein we live. And other things may be added of the like nature unto this purpose. Again,—; next: Obs. II. Some important doctrines of truth may, in the preaching of the gospel, be omitted for a season, but none must ever be forgotten or neglected.—So deals the apostle in this 
- file: EPUB/ch002.xhtml; previous: , with the utmost endeavours of our whole souls. 'We have abode long enough by the shore; let us now hoist our sails and launch forth into the deep.' And we may hence learn, that,—; next: Obs. III. It is a necessary duty of the dispensers of the gospel to excite their hearers, by all pressing considerations, to make a progress in the knowledge of the truth. Thus dea
- file: EPUB/ch002.xhtml; previous: g he had, the principal subject of his epistles is constantly the increase of light and knowledge in the churches, which he knew to be so necessary for them. We may therefore add,—; next: Obs. IV. The case of that people is deplorable and dangerous whose teachers are not able to carry them on in the knowledge of the mysteries of the gospel. The key of knowledge may 
- file: EPUB/ch003.xhtml; previous: From what hath been discoursed, we may inquire after our own interest in this great and necessary duty; to assist us wherein I shall yet add some further directions; as,—; next: Repentance is twofold: first, Initial; secondly, Continued in our whole course; and our inquiry is to be after our interest in both of them. The former is that whose general nature
- file: EPUB/ch003.xhtml; previous: Now there are several ways whereby men miss their duty with respect unto this first principle, and thereby ruin their souls eternally:—; next: 1 Some utterly despise it. Such are the presumptuous sinners mentioned, Deut. 29:19, 20. As they disregard the curse of the law, so they do also the promise of the gospel, as unto 

### Inline structural marker candidates

- file: EPUB/ch004.xhtml; text: Obs. III. There is a goodness and excellency in this heavenly gift, which may be tasted or experienced in some measure by such as never receive them, in their life, power, and efficacy. They may taste,—(1.) Of the word i
- file: EPUB/ch004.xhtml; text: 1. Its communication or application unto the earth,—it falls upon it; 2. An especial adjunct thereof in its frequency,—it falls often on it; 3. By that reception which the earth is naturally fitted and suited to give unt
- file: EPUB/ch004.xhtml; text: Μεταλαμβάνει εὐλογίας ἀπὸ τοῦ Θεοῦ . The earth must be tilled, from its nature and the law of its creation, And therefore Adam was to have tilled and wrought the ground in the garden even before the fall, Gen. 2:15. And 
- file: EPUB/ch004.xhtml; text: They are, therefore, no otherwise meet for God but in and through Christ, according to the infinite condescension which he is pleased to exercise in the covenant of grace. Therein doth the Lord Christ, 1. Make our person
- file: EPUB/ch005.xhtml; text: Obs. III. There is a goodness and excellency in this heavenly gift, which may be tasted or experienced in some measure by such as never receive them, in their life, power, and efficacy. They may taste,—(1.) Of the word i

### Repeated word windows

- phrase: made an high priest for ever after the order of
- phrase: an high priest for ever after the order of melchisedec
- phrase: because they were not suffered to continue by reason of
- phrase: they were not suffered to continue by reason of death
- phrase: of the word unto the souls and consciences of men

### Missing enumerator markers

- marker: (1st)
