# Bug Regression Report: Volume 13

- Status: **WARN**
- EPUB audit: `volume_13_audit.json`
- Text integrity audit: `volume_13_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 92 | 95 | OK |
| Inline structural marker candidates | 8 | 8 | OK |
| Repeated word windows | 25 | 25 | OK |
| Missing front CONTENTS pages | 0 | 2 | OK |
| Reference continuation splits | 0 | 0 | OK |
| Citation continuation splits | 0 | 0 | OK |
| Adjacent duplicate paragraphs | 0 | 0 | OK |
| Missing enumerator markers | 0 | 6 | OK |
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
| Repeated phrase hits | 3 | 7 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 1 | 2 | OK |
| Overlong headings containing body prose | 2 | 2 | OK |
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
| Lowercase page fragments | 10 | 0 | REGRESSION |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch006.xhtml; previous: uty: concerning each of which we have both the precept and the practice, God's command and their performance. The one in that injunction given unto the priest, Deuteronomy 31:11-13; next: All which we find punctually performed on both sides, Nehemiah 8:1-8. Ezra the priest, standing on a pulpit of wood, read the law and gave the meaning of it; and the "ears of all t
- file: EPUB/ch006.xhtml; previous: ning of it; and the "ears of all the people were attentive to the book of the law." Which course continued until there was an end put to the observances of that law; as Acts 15:21,; next: On which ground, not receding from their ancient observations, the people assembled to hear our Savior teaching with authority, Luke 21:38; and St Paul divers times took advantage 
- file: EPUB/ch006.xhtml; previous: ary assemblies to preach the gospel unto them. For the other, which concerns their own searching into the law and studying of the word, we have a strict command, Deuteronomy 6:6-9,; next: Which strict charge is again repeated, chapter 11:18, summarily comprehending all ways whereby they might become exercised in the law.
- file: EPUB/ch006.xhtml; previous: s belonged to that kind of public teaching which was necessary under that administration of the covenant. But instead of many, I will name one not liable to exception: Malachi 2:7,; next: — where both a recital of his own duty, that he should be full of knowledge to instruct; the intimation to the people, that they should seek unto him, or give heed to his teaching;
- file: EPUB/ch006.xhtml; previous: 6:2,3, than him because he did. There are, indeed, many sharp reproofs in the Old Testament of those who undertook to be God's messengers without his warrant; as Jeremiah 22:21,22,; next: — to which, and the like places, it may satisfactorily be answered, that howsoever, by the way of analogy, they may be drawn into rule for these times of the gospel, yet they were 

### Inline structural marker candidates

- file: EPUB/ch009.xhtml; text: Now, three ways may a man receive, and be assured that he hath received, this divine mission, or know that he is called of God to the preaching of the word; I mean not that persuasion of divine concurrence which is neces
- file: EPUB/ch016.xhtml; text: Explication III. The greatness of the work (for which who is sufficient? 2 Corinthians 2:16); — the strength of the opposition which lies against it, 1 Corinthians 16:9; Revelation 12:12; 2 Timothy 4:3-5; — the concernme
- file: EPUB/ch016.xhtml; text: Let motives hereunto be, — 1. God's command. 2. Our own preservation from sin and protection from punishment, that with others we be not infected and plagued. 3. Christ's delight in the purity of his ordinances.
- file: EPUB/ch016.xhtml; text: Now, to a right performance of this duty, and in the discharge of it, are required, — 1. A due valuation, strong desire, and high esteem of the church's prosperity, in every member of it, Psalm 122:6. 2. Bowels of compas
- file: EPUB/ch016.xhtml; text: Motives to this duty are: — 1. The love of God unto us, 1 John 3: 16. 2. The glory of the gospel, exceedingly exalted thereby, Titus 3:8,14; Matthew 5:7.

### Repeated word windows

- phrase: the grounds and reasons on which protestant dissenters desire their
- phrase: ii word of advice to the citizens of london this
- phrase: word of advice to the citizens of london this tract
- phrase: of advice to the citizens of london this tract only
- phrase: advice to the citizens of london this tract only appeared

### Repeated phrase hits

- file: combined_text; text: eshcol a cluster of the fruit of canaan
- file: combined_text; text: a review of the true nature of schism
- file: combined_text; text: chapter 3 a review of the charger's preface

### Chapter headings rendered as paragraphs

- file: EPUB/ch020.xhtml; text: Chapter 11

### Overlong headings containing body prose

- file: EPUB/ch049.xhtml; text: [Inconsistent expressions of Parker in regard to the power of the magistrate and the rights of conscience — The design of his discourse to prove the magistrate's authority to gover
- file: EPUB/ch050.xhtml; text: [Alleged power of the magistrate over the conscience in matters of morality refuted — Distinction between moral virtue and grace — Meaning of the terms — Four propositions of Parke

### Lowercase page fragments

- file: EPUB/ch003.xhtml; text: obliged servant in Jesus Christ, our common Master
- file: EPUB/ch004.xhtml; text: will be mounting. In the matter concerning which I propose my weak essay, some wo
- file: EPUB/ch007.xhtml; text: and again,
- file: EPUB/ch009.xhtml; text: and Jeremiah 20:9, "His word was in mine heart as a burning fire shut up in my bo
- file: EPUB/ch011.xhtml; text: to which add that of the apostle,
