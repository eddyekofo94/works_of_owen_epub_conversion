# Bug Regression Report: Volume 16

- Status: **PASS**
- EPUB audit: `volume_16_audit.json`
- Text integrity audit: `volume_16_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 33 | 35 | OK |
| Inline structural marker candidates | 6 | 12 | OK |
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

- file: EPUB/ch002.xhtml; previous: th, while teaching, is the duty of the pastor; and on this point Owen was no more chargeable with inconsistency as an Independent than other eminent men of the same denomination, —; next: Thomas Hooker, Cotton Mather, and Timothy Dwight, — who contend for the office of the ruling elder. Some Presbyterians would homologate implicitly the exposition which our author g
- file: EPUB/ch003.xhtml; previous: But the different consideration lies in these things, —; next: That the mystical church doth never fail, neither is diminished by any shocks of temptation or suffering that, in their visible profession, any of them undergo; whereas visible chu
- file: EPUB/ch004.xhtml; previous:  the gospel and the profession of it, giving no representation of the holiness of Christ or his doctrine; (4.) If such churches do not, can not, will not reform themselves: then, —; next: It is the duty of every man who takes care of his own present edification and the future salvation of his soul peaceably to withdraw from the communion of such churches, and to joi
- file: EPUB/ch007.xhtml; previous: , magistrate, or ruler, by suffrage or common consent of those concerned. And this was usually done with making bare the hand and arm with lifting up, as Aristophanes witnesseth: —; next: — Ομως δὲ χειροτονητέον Εξωμισάσαις τὸν ἕτερον βραχίονα . — Ecclesiastes 266.
- file: EPUB/ch007.xhtml; previous: hose who in their conjunction into it by their own consent are every way equal, there can but three things be required unto the actual constitution of rule and office among them: —; next: And the first is, That there be some among them that are fitted and qualified for the discharge of such an office in a peculiar manner above others. This is previous unto all gover

### Inline structural marker candidates

- file: EPUB/ch004.xhtml; text: Hence it appears that there are none excluded from an entrance into the church-state but such as are either, — (1.) Grossly ignorant; or, (2.) Persecutors or reproachers of those that are good, or of the ways of God wher
- file: EPUB/ch004.xhtml; text: The neglect of this duty brings inconceivable prejudice unto churches, and if continued in will prove their ruin; for they are not to be preserved, propagated, and continued, at the easy rate of a constant supply by the 
- file: EPUB/ch006.xhtml; text: Unto the attaining of this wisdom are required, — 1. Fervent prayer for it, James 1:5. 2. Diligent study of the Scripture, to find out and understand the rules given by Christ unto this purpose, Ezra 7:10; 2 Timothy 2:1,
- file: EPUB/ch013.xhtml; text: The whole of what we plead for is here exemplified; as, — [1.] The cause of excommunication, which is a scandalous sin unrepented of. [2.] The preparation for its execution, which is the church's sense of the sin and sca
- file: EPUB/ch058.xhtml; text: The industry of learned men of old, and of late Jews and Christians, has been well exercised in the interpretation and reconciliation of them: by one or other a fair and probable account is given of them all. Where we ca

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
