# Bug Regression Report: Volume 1

- Status: **PASS**
- EPUB audit: `volume_1_audit.json`
- Text integrity audit: `volume_1_text_integrity.json`

## Regression Budget

| Check | Observed | Budget | Status |
|-------|----------|--------|--------|
| Possible faulty paragraph splits | 125 | 125 | OK |
| Inline structural marker candidates | 0 | 1 | OK |
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
| Missing Greek clauses | 14 | 16 | OK |
| Missing Hebrew clauses | 0 | 0 | OK |
| EPUB packaging errors | 0 | 0 | OK |
| Untagged Greek characters | 8 | 55 | OK |
| Untagged Hebrew characters | 0 | 0 | OK |
| Hebrew integrity failures | 0 | 0 | OK |
| Repeated phrase hits | 6 | 8 | OK |
| Possible Beta Code residue files | 0 | 2 | OK |
| Escaped language-tag files | 0 | 0 | OK |
| Literal footnote marker files | 0 | 0 | OK |
| Empty bracket noise files | 0 | 0 | OK |
| Unprocessed AGES verse markers | 0 | 0 | OK |
| Page reference split files | 0 | 0 | OK |
| Chapter headings rendered as paragraphs | 1 | 3 | OK |
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
| Lowercase page fragments | 8 | 38 | OK |
| Noteref leading spaces | 0 | 0 | OK |
| Greek span legacy accents | 0 | 0 | OK |
| Long quote joined to prose | 0 | 0 | OK |
| I WILL/I AM mangles | 0 | 0 | OK |

## Triage Samples

### Possible faulty paragraph splits

- file: EPUB/ch004.xhtml; previous: on, the Only-begotten, the First-begotten, the Door, the Way, the Arrow, Wisdom, and sundry other things." And Ennodius has, as it were, turned this passage of Jerome into verse: —; next: Chap. IV. That he was the foundation of all the holy counsels of God, with respect unto the vocation, sanctification, justification, and eternal salvation of the church, is, in the
- file: EPUB/ch007.xhtml; previous:  abilities are weak and contemptible, in the eye of that wisdom which is of this world, than in those of the highest natural sagacity, enjoying the best improvements of reason. For; next: However they may be poor, and, as another apostle speaketh, "foolish, weak, base, and despised;" ( 1 Corinthians 1:27, 28;) yet that faith which enables them to assent unto and emb
- file: EPUB/ch009.xhtml; previous: nswer hereunto God tells him, that he cannot see his face and live; none can have either bodily sight or direct mental intuition of the Divine Being. But this I WILL do, saith God,; next: This is all that God would grant, viz, such external representations of himself, in the proclamation of his name, and created appearances of his glory, as we have of a man whose ba
- file: EPUB/ch009.xhtml; previous: he being of God, his infinite wisdom, power, and goodness — viz., in the impressions and characters of them on the things that were made — in their own representations of him, they; next: Wherefore this common presumption — that there was no way to attain a due sense of the Divine Being but by some representation of it — though true in itself, yet, by the craft of S
- file: EPUB/ch009.xhtml; previous: This was the testimony which the apostles gave concerning him, when he dwelt among them in the days of his flesh. They saw; next: The divine glory was manifest in him, and in him they saw the glory of the Father. So the same apostle witnesses again, who recorded this testimony:

### Repeated word windows

- phrase: the glory of god in the face of jesus christ
- phrase: between our beholding the glory of christ by faith in
- phrase: our beholding the glory of christ by faith in this
- phrase: beholding the glory of christ by faith in this world
- phrase: the glory of christ by faith in this world and

### Missing Greek clauses

- page: 26; sample: ουτος εστιν ηε προς τον πατερα αγουσα ηοσος ηε πετρα ηε κλεις
- page: 32; sample: υποστατις φυσις μιαν φυσιν οτι κατ αληθειαν εστι μια φυσις του λογου
- page: 37; sample: ενωσιν φυσικην ενωσιν κατα συνθεσιν
- page: 37; sample: υιος θεου υιος ανθρωπου γινεται ουτω δε φωτος ηλιου μια και
- page: 42; sample: παιδαγωγος θεος εν ανθρωπου σχηματι αχραντος πατρικω θεληματι διακονος λογος θεος

### Untagged Greek characters

- file: EPUB/ch004.xhtml; text: , κ.τ.λ. (cap. 6)
- file: EPUB/ch005.xhtml; text: , κ.τ.λ." — "Thou art a rock, and on thee will I build." At least the gender had not been altered, but he would have said, "
- file: EPUB/ch019.xhtml; text: .τ. λ., 2 Corinthians 3:18. We behold his glory "in a glass," which implants the image of it on our minds. And hereby the mind is transformed into the same image, made like unto Christ so represented unto us — which is t

### Repeated phrase hits

- file: combined_text; text: chapter 14 motives unto the love of christ
- file: combined_text; text: meditations and discourses on the glory of christ
- file: combined_text; text: meditations and discourses concerning the glory of christ
- file: combined_text; text: chapter 8 of the state of corrupted nature
- file: combined_text; text: chapter 10 of the person of jesus christ

### Chapter headings rendered as paragraphs

- file: EPUB/ch003.xhtml; text: Chapter 1

### Lowercase page fragments

- file: EPUB/ch004.xhtml; text: f
- file: EPUB/ch011.xhtml; text: m
- file: EPUB/ch016.xhtml; text: a
- file: EPUB/ch021.xhtml; text: a
- file: EPUB/ch022.xhtml; text: a
