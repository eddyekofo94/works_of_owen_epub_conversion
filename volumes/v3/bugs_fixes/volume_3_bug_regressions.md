# Bug Regression Report: Volume 3

- Status: **PASS**
- EPUB audit: `volume_3_audit.json`
- Text integrity audit: `volume_3_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 161 | 176 | OK |
| Inline structural marker candidates | 14 | 14 | OK |
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
| Missing Greek clauses | 1 | 1 | OK |
| Missing Hebrew clauses | 5 | 5 | OK |
| Residual AGES source artifacts | 0 | 0 | OK |
| Flat ANALYSIS chapters | 0 | 0 | OK |
| Missing configured fonts | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 0 | 0 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 3 | 4 | OK |
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
| Lowercase page fragments | 16 | 20 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch006.xhtml; previous: anions, saying, "These men are the servants of the most high God," Acts 16:17. So also did the man who abode in the tombs, possessed with an unclean spirit, who cried out unto him,; next: And other testimonies to the like purpose among the heathen, and from their oracles, might be produced.
- file: EPUB/ch006.xhtml; previous: great importance, he repeats it frequently unto them, and inculcates it upon them. Consider somewhat of what he says to this purpose in his last discourse with them: John 14:16-18,; next: whom the world cannot receive, because it seeth him not, neither knoweth him: but ye know him; for he dwelleth with you, and shall be in you. I will not leave you comfortless: I wi
- file: EPUB/ch006.xhtml; previous: John 20:17, to wean her from any carnal consideration of him, so he instructs them all now to look after and trust unto the promise of the Holy Ghost. Hence is that of our apostle,; next: for although it was a great privilege to have known Christ in this world after the flesh, yet it was much greater to enjoy him in the dispensation of the Spirit. And this was spoke
- file: EPUB/ch006.xhtml; previous: nstructed in what concerns him; for there is somewhat that doth so, which is accompanied with irrecoverable and eternal ruin; and so is nothing else in the world. So Mark 3:28, 29,; next: Or, "Whosoever speaketh against the Holy Ghost, it shall not be forgiven him, neither in this world, neither in the world to come," Matthew 12:32.
- file: EPUB/ch006.xhtml; previous:  pleaded in its justification, it is to be rejected, as they also are by whom it is declared. This rule the apostle Paul confirms by the highest instance imaginable: Galatians 1:8,; next: And the apostle shows that, for our advantage in this trial we are to make of spirits, it is good to have a clear conviction of, and a constant adherence unto, some fundamental pri

### Inline structural marker candidates

- file: EPUB/ch003.xhtml; text: The FIRST BOOK of the treatise is devoted to considerations of a general and preliminary nature. The promise of spiritual gifts contained in Scripture is examined; and occasion is hence taken to illustrate the importance
- file: EPUB/ch006.xhtml; text: THE apostle Paul, in the 12th chapter of his First Epistle to the Corinthians, directs their exercise of spiritual gifts, concerning which, amongst other things and emergencies, they had made inquiry of him. This the fas
- file: EPUB/ch006.xhtml; text: Treating, therefore, περὶ τῶν πνευματικῶν , [7] of these spiritual things or gifts in the church, he first declares their author, from whom they come, and by whom they are wrought and bestowed. Him he calls the "Spirit,"
- file: EPUB/ch007.xhtml; text: This is one signification of the word רוּחַ , [34] or this is one thing denoted by it in the Scripture. So, among many other places, expressly Amos 4:13, "For, lo," יוֹצֵר הָרִים וּבֹרֵא רוּחַ [35] , he that formeth the 
- file: EPUB/ch007.xhtml; text: The substance of his discourse is, that treating of Christ (who indeed is neither mentioned nor intended in the text), he speaks of "confirming the thunder" (which nowhere here appears), by which the sound of the Scriptu

### Repeated word windows

- phrase: both to will and to do of his good pleasure
- phrase: the name of the father and of the son and
- phrase: in us both to will and to do of his
- phrase: us both to will and to do of his good
- phrase: name of the father and of the son and of

### Missing Greek clauses

- page: 34; sample: ζηλουτε δε τα χαρισματα τα κρειττνα

### Missing Hebrew clauses

- page: 70; sample: רוּחַ נְדוֹלָה וְחָזָק
- page: 74; sample: רוּחַ בְּנֵי הָאָדָם
- page: 80; sample: רוּחַ־רָעָה מֵאֵת יְהוָֹה
- page: 109; sample: שַׁדַּי תְחַיֵנִי רוּחַ־אֵל עָצָתְנִי וְנִשְׁמַת
- page: 130; sample: רֹאצ עַפְרוֹת חֵבֵל

### Repeated phrase hits

- file: combined_text; text: chapter 2 general dispensation of the holy spirit
- file: combined_text; text: chapter 2 works of the holy spirit preparatory
- file: combined_text; text: chapter 3 believers the only object of sanctification

### Lowercase page fragments

- file: EPUB/ch006.xhtml; text: whom the world cannot receive, because it seeth him not, neither knoweth him: but
- file: EPUB/ch007.xhtml; text: declares the mistake of the LXX. and the occasion of it: —
- file: EPUB/ch008.xhtml; text: and a fire thence kindled was always kept burning on the altar. And in like manne
- file: EPUB/ch010.xhtml; text: for it is evidently of the gifts of the Spirit, enabling men for rule and governm
- file: EPUB/ch013.xhtml; text: and they who were instructed in the doctrine of John the Baptist only, knew not "
