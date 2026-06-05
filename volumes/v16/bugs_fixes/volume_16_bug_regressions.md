# Bug Regression Report: Volume 16

- Status: **PASS**
- EPUB audit: `volume_16_audit.json`
- Text integrity audit: `volume_16_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 2 | 35 | OK |
| Inline structural marker candidates | 8 | 12 | OK |
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
| Missing Greek clauses | 0 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 1 | 1 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 6 | 7 | OK |
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
| Lowercase page fragments | 0 | 1 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch032.xhtml; previous: plum ipsis quoque fiens; deinde et usque ad mortem pervenit, ut sit primogenitus ex mortuis , ipse primatum tenens in omnibus, princeps vitae, prior omnium, et praecedens omnes." †; next: Lib. 1: cap. 18: Οσοι γάρ εἰσι ταύτης τῆς γνώμης μυσταγωγοὶ , τοσαῦται καὶ ἀπολυτρώσεις . Οτι μὲν εἰς ἐξάρνησιν τοῦ βαπτισ́ματος τῆς εἰς Θεὸν ἀναγεννήσεως , καὶ πάσης τῆς πίστεως ἀ
- file: EPUB/ch058.xhtml; previous: cam veritatem, ut interim fatear illos non admodum peritos fuisse linguae Hebraicae id vel quod inviti cogimur fateri , alioquin in plurimis locis non tam fcede lapsi fuissent ." †; next: If, moreover, the ability be granted, what security have we of their principles and honesty? Cardinal Ximenes, in his preface to the edition of the Complutensian Bibles, tells us (

### Inline structural marker candidates

- file: EPUB/ch004.xhtml; text: The neglect of this duty brings inconceivable prejudice unto churches, and if continued in will prove their ruin; for they are not to be preserved, propagated, and continued, at the easy rate of a constant supply by the 
- file: EPUB/ch006.xhtml; text: Unto the attaining of this wisdom are required, — 1. Fervent prayer for it, James 1:5. 2. Diligent study of the Scripture, to find out and understand the rules given by Christ unto this purpose, Ezra 7:10; 2 Timothy 2:1,
- file: EPUB/ch013.xhtml; text: The whole of what we plead for is here exemplified; as, — [1.] The cause of excommunication, which is a scandalous sin unrepented of. [2.] The preparation for its execution, which is the church's sense of the sin and sca
- file: EPUB/ch027.xhtml; text: (2.) Admit of none unto this sacrament by virtue of their communion with any other church, or any churches not of their own constitution; nor, (3.) Will administer it unto any hut those whom they claim to be their own, a
- file: EPUB/ch029.xhtml; text: Secondly, If the innocent party upon a divorce be not set at liberty, then, 1. He is deprived of his right by the sin of another; which is against the law of nature; — and so every wicked woman hath it in her power to de

### Repeated word windows

- phrase: the various readings of ben asher and ben naphtali of
- phrase: various readings of ben asher and ben naphtali of the
- phrase: of ben asher and ben naphtali of the eastern and
- phrase: ben asher and ben naphtali of the eastern and western
- phrase: asher and ben naphtali of the eastern and western jews

### Flat ANALYSIS chapters

- file: EPUB/ch042.xhtml

### Repeated phrase hits

- file: combined_text; text: of the formal cause of a particular church
- file: combined_text; text: of marrying after divorce in case of adultery
- file: combined_text; text: reflections on a slanderous libel against dr owen
- file: combined_text; text: the prebends of christ church college in oxford
- file: combined_text; text: sermon 6 the obligation to increase in godliness
