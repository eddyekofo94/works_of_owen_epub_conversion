# Bug Regression Report: Volume 6

- Status: **WARN**
- EPUB audit: `volume_6_audit.json`
- Text integrity audit: `volume_6_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 193 | 61 | REGRESSION |
| Inline structural marker candidates | 4 | 1 | REGRESSION |
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
| Lowercase page fragments | 27 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch004.xhtml; previous: tribute to the carrying on of the work of mortification in believers may receive order and perspicuity, I shall lay the foundation of it in those words of the apostle, Romans 8:13,; next: The apostle having made a recapitulation of his doctrine of justification by faith, and the blessed estate and condition of them who are made by grace partakers thereof, verses 1-3
- file: EPUB/ch005.xhtml; previous: when they are still, so ought our contrivances against it to be vigorous at all times and in all conditions, even where there is least suspicion. Sin doth not only abide in us, but; next: If sin be subtle, watchful, strong, and always at work in the business of killing our souls, and we be slothful, negligent, foolish, in proceeding to the ruin thereof, can we expec
- file: EPUB/ch005.xhtml; previous: one, if not continually mortified, it will bring forth great, cursed, scandalous, soul-destroying sins. The apostle tells us what the works and fruits of it are, Galatians 5:19-21,; next: You know what it did in David and sundry others. Sin aims always at the utmost; every time it rises up to tempt or entice, might it have its own course, it would go out to the utmo
- file: EPUB/ch007.xhtml; previous: THE last principle I shall insist on (omitting, first, the necessity of mortification unto life, and, secondly, the certainty of life upon mortification) is, —; next: Strength and comfort, and power and peace, in our walking with God, are the things of our desires. Were any of us asked seriously, what it is that troubles us, we must refer it to 
- file: EPUB/ch010.xhtml; previous:  refining will do them no good. The prophet gives us the sad issue of wicked men's utmost attempts for mortification, by what means soever that God affords them: Jeremiah 6:29, 30,; next: And what is the reason hereof? Verse 28, They were "brass and iron" when they were put into the furnace. Men may refine brass and iron long enough before they will be good silver.

### Inline structural marker candidates

- file: EPUB/ch021.xhtml; text: Before I descend to other particulars, having now entered hereon, I shall show in general, — 1st. How or by what means commonly any temptation attains its hour;
- file: EPUB/ch049.xhtml; text: The Nature Of The Forgiveness Of Sin Is Declared; The Truth And Reality Of It Asserted; And The Case Of A Soul Distressed With The Guilt Of Sin, And Relieved By A Discovery Of Forgiveness With God, Is At Large Discoursed
- file: EPUB/ch060.xhtml; text: In the supposition there is, — 1. The name of God, that is fixed on as suited unto it; and, 2. The thing itself supposed.
- file: EPUB/ch061.xhtml; text: In the supposition there is, — 1. The name of God, that is fixed on as suited unto it; and, 2. The thing itself supposed.

### Repeated word windows

- phrase: there is forgiveness with thee that thou mayest be feared
- phrase: the lord hath forsaken me and my lord hath forgotten
- phrase: lord hath forsaken me and my lord hath forgotten me
- phrase: the lust of the flesh the lust of the eyes
- phrase: from the lord and my judgment is passed over from

### Repeated phrase hits

- file: combined_text; text: institution of religious worship an evidence of forgiveness

### Lowercase page fragments

- file: EPUB/ch053.xhtml; text: every way and means of thy appearance, of the manifestation of thyself, and comin
- file: EPUB/ch056.xhtml; text: chiefly to respect that which he himself, in this address unto God, did principal
- file: EPUB/ch062.xhtml; text: stand?," When the Holy Ghost would set out the certainty and dreadfulness of the
- file: EPUB/ch064.xhtml; text: prepares the soul for the receiving of mercy in a sense of pardon, the great thin
- file: EPUB/ch069.xhtml; text: government of the world, his holiness and righteousness, to take care that every
