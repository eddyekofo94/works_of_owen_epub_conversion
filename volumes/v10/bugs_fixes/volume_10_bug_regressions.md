# Bug Regression Report: Volume 10

- Status: **PASS**
- EPUB audit: `volume_10_audit.json`
- Text integrity audit: `volume_10_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 158 | 158 | OK |
| Inline structural marker candidates | 7 | 8 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 1 | 1 | OK |
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
| Flat ANALYSIS chapters | 0 | 0 | OK |
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
| Chapter headings rendered as paragraphs | 1 | 1 | OK |
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
| Lowercase page fragments | 18 | 18 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch002.xhtml; previous: ered, by the Committee of the House of Commons in Parliament for the Regulating of Printing and Publishing of Books, That this book, entitled "A Display of Arminianism," be printed; next: JOHN WHITE
- file: EPUB/ch006.xhtml; previous: to particular contingent events, Isaiah 48:14. Yea, it is an ordinary thing with the Lord to confirm the certainty of those things that are yet for to come from his own decree; as,; next: Isaiah 14:24,25; — "It is certain the Assyrian shall be broken, because the Lord hath purposed it;" which were a weak kind of reasoning, if his purpose might be altered. Nay "He is
- file: EPUB/ch007.xhtml; previous: omination? Even actions in themselves sinful are not; though not as sinful, yet in some other regard, as punishments of others. "Behold," saith Nathan to David, in the name of God,; next: So, also, when wicked robbers had nefariously spoiled Job of all his substance, the holy man concludeth, "The LORD gave, and the LORD hath taken away," Job 1:21. Now, if the workin
- file: EPUB/ch008.xhtml; previous: His powerful overruling of all events, both necessary, free, and contingent, and disposing of them to certain ends for the manifestation of his glory. So Joseph tells his brethren,; next: Fourthly, His determining and restraining second causes to such and such effects:
- file: EPUB/ch009.xhtml; previous: his revealed will to walk in his statutes, and keep his laws; upon this he also promiseth that he will so effect all things, that of some this shall be performed: Ezekiel 36:26,27,; next: So that the self-same obedience of the people of God is here the object of his will, taken in either acceptation. And yet the precept of God is not here, as some learned men suppos

### Inline structural marker candidates

- file: EPUB/ch020.xhtml; text: In 1650, Mr. Home, minister at Lynn in Norfolk, a man, according to Palmer (Nonconf. Mem., 3. pp. 6, 7), "of exemplary and primitive piety," and author of several works, published a reply to Owen's work, under the title,
- file: EPUB/ch021.xhtml; text: Arg. 6. From Scripture assertions and consequences. Answers to the proofs of this sixth argument: — 1. From 1 John 4:14; John 1:4, 7; 1 Timothy 2:4. 2. From some texts before vindicated. 3. From Psalm 19:4; Romans 10:18;
- file: EPUB/ch031.xhtml; text: Now, what is it to obey the grace of God? Is it not to believe? Therefore, it seems that Christ intercedeth for them that they may believe, upon condition that they do believe. Others, more cautiously, assert the good us
- file: EPUB/ch046.xhtml; text: Let now any one tell me what the reprobates, in this life, lie under more? And do not all the elect, until their actual reconciliation, in and by Christ, lie under the very same? for, — (1.) Are not their prayers an abom
- file: EPUB/ch057.xhtml; text: Now, fourthly, after all this, and not before, it lies upon a believer to assure his soul, according as he finds the fruit of the death of Christ in him and towards him, of the goodwill and eternal love of God to him in 

### Repeated word windows

- phrase: that we might be made the righteousness of god in
- phrase: we might be made the righteousness of god in him
- phrase: made him to be sin for us who knew no
- phrase: him to be sin for us who knew no sin
- phrase: hath set forth to be propitiation through faith in his

### Missing front CONTENTS pages

- page: 3; sample: contents of θεομαχια αττεξουσιαστικη display of arminianism prefatory note by the editor epistle dedicatory to the christian reader θεμοχιας αυτεξουσιαστικης specimen of the two main ends aimed at

### Repeated phrase hits

- file: combined_text; text: chapter 8 objections against the former proposal answered
- file: combined_text; text: chapter 1 arguments against the universality of redemption
- file: combined_text; text: an entrance to the answer unto particular arguments
- file: combined_text; text: chapter 4 answer to the second general argument
- file: combined_text; text: chapter 5 the last argument from scripture answered

### Chapter headings rendered as paragraphs

- file: EPUB/ch021.xhtml; text: Chapter 1

### Lowercase page fragments

- file: EPUB/ch010.xhtml; text: which is in Christ Jesus," Romans 8:29,30,39. "He hath chosen us in him before th
- file: EPUB/ch014.xhtml; text: and is no way repugnant to the holy Scripture, declaring our duty to be all this
- file: EPUB/ch021.xhtml; text: of the whole work is prefixed to it. We have not felt at liberty to adopt the num
- file: EPUB/ch024.xhtml; text: which last words express also the very aim and end of Christ in giving himself fo
- file: EPUB/ch026.xhtml; text: with that redoubled voice which afterward came from the excellent glory, "This is
