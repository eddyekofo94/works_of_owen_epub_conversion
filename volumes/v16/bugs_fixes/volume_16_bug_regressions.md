# Bug Regression Report: Volume 16

- Status: **PASS**
- EPUB audit: `volume_16_audit.json`
- Text integrity audit: `volume_16_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 33 | 61 | OK |
| Inline structural marker candidates | 10 | 10 | OK |
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
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 55 | OK |
| Untagged Hebrew characters | 0 | 26 | OK |
| Hebrew integrity failures | 0 | 26 | OK |
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
| Lowercase page fragments | 5 | 5 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch003.xhtml; previous: d his fullness, and, by union with him, Christ mystical, Ephesians 2:2 2:23; and this is that πανήγυρις (the only word most fully expressing the catholic church used in Scripture),; next: that is, in the Lamb's book of life; and they shall all appear one day gathered together to their Head, in the perfection and fullness of the New Jerusalem state, where they will m
- file: EPUB/ch003.xhtml; previous: nd the court which is without the temple, namely, the generality of visible professors, and the external part of worship, which hath been so long trod down by Gentilism. Wherefore,; next: Men, it may be, have thought they have got, or at least saved, by not troubling themselves with the care, charge, and trouble of gathering churches and walking in gospel order; but
- file: EPUB/ch008.xhtml; previous: d the same spirit, the same mind herein, ought, according to their measure, to be in all that have the pastoral office committed unto them. So the apostle expresseth it in himself,; next: And unless this compassion and goodness do run through the discharge of their whole office, men cannot be said to be evangelical shepherds, nor the sheep said in any sense to be th
- file: EPUB/ch025.xhtml; previous: 3. It is contrary to the rule delivered, Malachi 1:13, 14,; next: We are obliged, by all divine laws, natural, moral, and positive, to serve God always with our best. The obligations hereunto are inseparable from all just conceptions of the divin
- file: EPUB/ch029.xhtml; previous: marry who is maliciously and obstinately deserted, alarming that the Christian religion doth not prejudice the natural right and privilege of men in such cases: 1 Corinthians 7:15,; next: If a person obstinately depart, on pretense of religion or otherwise, and will no more cohabit with a husband or wife, it is known that, by the law of nature and the usage of all n

### Inline structural marker candidates

- file: EPUB/ch004.xhtml; text: The neglect of this duty brings inconceivable prejudice unto churches, and if continued in will prove their ruin; for they are not to be preserved, propagated, and continued, at the easy rate of a constant supply by the 
- file: EPUB/ch006.xhtml; text: Unto the attaining of this wisdom are required, — 1. Fervent prayer for it, James 1:5. 2. Diligent study of the Scripture, to find out and understand the rules given by Christ unto this purpose, Ezra 7:10; 2 Timothy 2:1,
- file: EPUB/ch012.xhtml; text: Nor was this a temporary institution, for that season, and so the officers appointed extraordinary, but it was to abide in the church throughout a!! generations; for, — 1. The work itself, as a distinct work of ministry 
- file: EPUB/ch013.xhtml; text: The whole of what we plead for is here exemplified; as, — [1.] The cause of excommunication, which is a scandalous sin unrepented of. [2.] The preparation for its execution, which is the church's sense of the sin and sca
- file: EPUB/ch014.xhtml; text: There is nothing, therefore, in Scripture example or the light of natural reason, with the principles of all societies in union or communion, that will lead us any farther than this, that such synods are to be composed a

### Repeated word windows

- phrase: the various readings of ben asher and ben naphtali of
- phrase: various readings of ben asher and ben naphtali of the
- phrase: of ben asher and ben naphtali of the eastern and
- phrase: ben asher and ben naphtali of the eastern and western
- phrase: asher and ben naphtali of the eastern and western jews

### Repeated phrase hits

- file: combined_text; text: of the formal cause of a particular church
- file: combined_text; text: of marrying after divorce in case of adultery
- file: combined_text; text: reflections on a slanderous libel against dr owen
- file: combined_text; text: the prebends of christ church college in oxford
- file: combined_text; text: sermon 6 the obligation to increase in godliness

### Lowercase page fragments

- file: EPUB/ch003.xhtml; text: that is, in the Lamb's book of life; and they shall all appear one day gathered t
- file: EPUB/ch032.xhtml; text: words and scope show. But he was not in his age an example of every age by his ba
- file: EPUB/ch033.xhtml; text: them in his own person, is a mere cavil; for all that are born to God by baptism
- file: EPUB/ch064.xhtml; text: that is, whatsoever is required to lead a godly life is given unto believers by t
- file: EPUB/ch065.xhtml; text: how long shall they! be in this state and condition? "And he answered, Until the
