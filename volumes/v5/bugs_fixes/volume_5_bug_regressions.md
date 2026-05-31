# Bug Regression Report: Volume 5

- Status: **WARN**
- EPUB audit: `volume_5_audit.json`
- Text integrity audit: `volume_5_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 78 | 61 | REGRESSION |
| Inline structural marker candidates | 3 | 1 | REGRESSION |
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
| Low Hebrew word coverage | 0 | 0 | OK |
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 1 | 0 | REGRESSION |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 3 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 1 | 0 | REGRESSION |
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
| Lowercase page fragments | 9 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch004.xhtml; previous:  habit inherent in ourselves, and the acts of it, they wrested the whole doctrine of justification unto a compliance wherewithal. So Pighius himself complained of them, Controv. 2,; next: Secondly, A due consideration of him with whom in this matter we have to do, and that immediately, is necessary unto a right stating of our thoughts about it. The Scripture express
- file: EPUB/ch004.xhtml; previous:  Lord's sake," Daniel 9:17, in whom "all the seed of Israel are justified," Isaiah 45:25. In his sight, before his tribunal, it is that men are justified or condemned. Psalm 143:2,; next: And the whole work of justification, with all that belongs thereunto, is represented after the manner of a juridical proceeding before God's tribunal; as we shall see afterwards. "
- file: EPUB/ch004.xhtml; previous: cation, with all that belongs thereunto, is represented after the manner of a juridical proceeding before God's tribunal; as we shall see afterwards. "Therefore," says the apostle,; next: However any man be justified in the sight of men or angels by his own obedience, or deeds of the law, yet in his sight none can be so.
- file: EPUB/ch004.xhtml; previous: any means to manifest his glory unto sinners, all their prefidences and contrivances do issue in dreadful horror and distress. An account of their temper is given us, Isaiah 33:14,; next: Nor is it thus only with some peculiar sort of sinners. The same will be the thoughts of all guilty persons at some time or other. For those who, through sensuality, security, or s
- file: EPUB/ch004.xhtml; previous:  him in battle array. And we may see what extravagant contrivances convinced sinners will put themselves upon, under any real view of the majesty and holiness of God, Micah 6:6, 7,; next: Neither shall I ever think them meet to be contended withal about the doctrine of justification who take no notice of these things, but rather despise them.

### Inline structural marker candidates

- file: EPUB/ch022.xhtml; text: It may be it will be said: "It is true in the time of their heathenism they did not at all follow after righteousness, but when the truth of the gospel was revealed unto them, then they followed after righteousness, and 
- file: EPUB/ch024.xhtml; text: These things being premised, I shall briefly evidence that there is not the least repugnancy or contradiction between what is declared by these two apostles as unto our justification, with the causes of it. And this I sh
- file: EPUB/ch029.xhtml; text: Faith is not an especial assurance of a man's own justification and salvation by Christ; that it will produce, but not until another step or two in its progress be over: but faith is a satisfactory persuasion that the wa

### Repeated word windows

- phrase: of justification by the imputation of the righteousness of christ
- phrase: doctrine of justification by the imputation of the righteousness of
- phrase: the doctrine of justification by the imputation of the righteousness
- phrase: set forth to be propitiation through faith in his blood
- phrase: freely by his grace through the redemption that is in

### EPUB packaging errors

- {'code': 'noteref_targets_missing', 'message': 'Some noteref targets do not have matching endnote anchors', 'examples': ['EPUB/endnotes.xhtml#fn4']}

### Repeated phrase hits

- file: combined_text; text: chapter 3 the use of faith in justification
- file: combined_text; text: chapter 17 testimonies out of the evangelists considered
- file: combined_text; text: chapter 19 objections against the doctrine of justification

### Chapter headings rendered as paragraphs

- file: EPUB/contents_2.xhtml; text: CHAPTER 1

### Lowercase page fragments

- file: EPUB/ch004.xhtml; text: and the other is that of our Savior, Luke 17:10,
- file: EPUB/ch010.xhtml; text: who yet disclaims any confidence therein as unto his justification before God; fo
- file: EPUB/ch011.xhtml; text: attempts the sense of the word, but confounds it with "reputare:"
- file: EPUB/ch012.xhtml; text: and also Serm. 16 "Caput nostrum Dominus Jesus Christus omnia in se corporis sui
- file: EPUB/ch022.xhtml; text: injustus", 1 Peter 3:18. "Quod si ergo justi effecti sumus per vitam illius, caus
