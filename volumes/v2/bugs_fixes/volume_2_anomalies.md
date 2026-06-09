# Text Integrity & Anomaly Audit Report: Volume 2

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 221564
* **Total Suspected Anomalies Found:** 56

Add corrections to `text_replacements` inside `volumes/v2/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 21 items
* **Punctuation Spacing Blemishes:** 10 items
* **OCR & Bracket Residues:** 0 items
* **Mixed-Case Capitalization Errors:** 0 items
* **Unresolved Citation References:** 2 items
* **Structural Nesting Sequence Jumps:** 5 items
* **Invalid Bible References:** 18 items
* **List Formatting Inconsistencies:** 0 items

---

## Hyphenation Anomalies

### 1. `re-assume`
* **Description:** Splittable word (rejoins to valid word 'reassume')
* **Chapter:** *Preface*
* **Contexts:**
  * ... bringing me under the engagements mentioned), to **re-assume** the consideration of what I had first fixed on, I ...

### 2. `banqueting-houses`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 1 - Of the fellowship which the saints have with Jesus Christ the Son of God — That th...*
* **Contexts:**
  * ... But thus Christ makes all his assemblies to love **banqueting-houses**; and there he gives his saints entertainment. (2 ...

### 3. `head-stone`
* **Description:** Splittable word (rejoins to valid word 'headstone')
* **Chapter:** *Chapter 2 - What it is wherein we have peculiar fellowship with the Lord Christ — This is in g...*
* **Contexts:**
  * ... revealed in or exhibited by the gospel. He is the **head-stone** in the building of the temple of God, to whom "Gr ...

### 4. `days-man`
* **Description:** Splittable word (rejoins to valid word 'daysman')
* **Chapter:** *Chapter 2 - What it is wherein we have peculiar fellowship with the Lord Christ — This is in g...*
* **Contexts:**
  * ... of our nature, Hebrews 2:14, 16, and so becomes a **days-man**, or umpire between both. By this means he fills u ...

### 5. `days-man`
* **Description:** Splittable word (rejoins to valid word 'daysman')
* **Chapter:** *Digression 1.*
* **Contexts:**
  * ... o come. (3.) Thus is he fitted for a mediator, a **days-man**, an umpire between God and us, — being one with h ...

### 6. `hand-writing`
* **Description:** Splittable word (rejoins to valid word 'handwriting')
* **Chapter:** *Digression 2.*
* **Contexts:**
  * ... or iniquity, Daniel 9:24; and he blotteth out the **hand-writing** of ordinances, Colossians 2:14, redeeming us from ...

### 7. `Day-spring`
* **Description:** Splittable word (rejoins to valid word 'Dayspring')
* **Chapter:** *Chapter 4 - Of communion with Christ in a conjugal relation in respect of consequential affect...*
* **Contexts:**
  * ... that comes into the world," John 1:9. He is the "**Day-spring**," the "Day-star," and the "Sun;" so that it is im ...

### 8. `Day-star`
* **Description:** Splittable word (rejoins to valid word 'Daystar')
* **Chapter:** *Chapter 4 - Of communion with Christ in a conjugal relation in respect of consequential affect...*
* **Contexts:**
  * ... he world," John 1:9. He is the "Day-spring," the "**Day-star**," and the "Sun;" so that it is impossible any lig ...

### 9. `Hephzi-bah`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Chapter 4 - Of communion with Christ in a conjugal relation in respect of consequential affect...*
* **Contexts:**
  * ... in them." Christ says of his church that she is "**Hephzi-bah**," Isaiah 62, "My delight in her." Here says David ...
  * ... My delight in her." Here says David of the same, "**Hephzi-bah**, — "My delight in them." As Christ delights in hi ...

### 10. `well-head`
* **Description:** Splittable word (rejoins to valid word 'wellhead')
* **Chapter:** *Chapter 5 - Other consequential affections: — 1 On the part of Christ — He values his saints —...*
* **Contexts:**
  * ... lvation before God, for the fountain, spring, and **well-head** of all their supplies, they will not now receive ...

### 11. `law-making`
* **Description:** Splittable word (rejoins to valid word 'lawmaking')
* **Chapter:** *Chapter 5 - Other consequential affections: — 1 On the part of Christ — He values his saints —...*
* **Contexts:**
  * ... t be deposed from the sole privilege and power of **law-making** in his church; that the true husband might be thr ...

### 12. `non-imputation`
* **Description:** Splittable word (rejoins to valid word 'nonimputation')
* **Chapter:** *Chapter 6 - Of communion with Christ in purchased grace — considered in respect of its rise an...*
* **Contexts:**
  * ... istinct mention made of reconciliation, through a **non-imputation** of sin, as Psalm 32:1, Luke 1:77, Romans 3:25, 2 ...
  * ... hteousness of Christ only is imputed to us in the **non-imputation** of sin, and that on the condition of our faith an ...

### 13. `hand-writing`
* **Description:** Splittable word (rejoins to valid word 'handwriting')
* **Chapter:** *Chapter 10 - Of communion with Christ in privileges — Of adoption; the nature of it, the conseq...*
* **Contexts:**
  * ... r, Acts 15:10; wherefore Christ "blotted out this **hand-writing** of ordinances that was against them, which was co ...

### 14. `son-like`
* **Description:** Splittable word (rejoins to valid word 'sonlike')
* **Chapter:** *Chapter 10 - Of communion with Christ in privileges — Of adoption; the nature of it, the conseq...*
* **Contexts:**
  * ... mans 6:18; 1 Peter 2:16. Now, this amplitude, or **son-like** freedom of the Spirit in obedience, consists in s ...
  * ... more ability; and this is a great share of their **son-like** freedom in obedience. It gives them joy in it. 1 ...

### 15. `co-heirs`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 10 - Of communion with Christ in privileges — Of adoption; the nature of it, the conseq...*
* **Contexts:**
  * ... God: fellowship in title and right; we are heirs, **co-heirs** with Christ: fellowship in likeness and conformit ...

### 16. `un-son`
* **Description:** Splittable word (rejoins to valid word 'unson')
* **Chapter:** *Chapter 5 - Some observations and inferences from discourses foregoing concerning the Spirit —...*
* **Contexts:**
  * ... make men quake and tremble; casting them into an **un-son**-like frame of spirit, driving them up and down wi ...

### 17. `well-spring`
* **Description:** Splittable word (rejoins to valid word 'wellspring')
* **Chapter:** *A Vindication*
* **Contexts:**
  * ... f the only begotten Son of God, whose life is the **well-spring** and cause of ours. It is too cold an interpretati ...

### 18. `co-partners`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *A Vindication*
* **Contexts:**
  * ... , may understand it; or, however, that he and his **co-partners** in design may know that I neither am nor ever wil ...
  * ... its end, I will defend it against him and all his **co-partners**, whilst the Scripture may be allowed to be the ru ...

### 19. `maran-atha`
* **Description:** Splittable word (rejoins to valid word 'maranatha')
* **Chapter:** *A Vindication*
* **Contexts:**
  * ... ess say, He that does not so, let him be anathema **maran-atha**. Secondly, We do not imagine, but believe from th ...

### 20. `days-man`
* **Description:** Splittable word (rejoins to valid word 'daysman')
* **Chapter:** *A Vindication*
* **Contexts:**
  * ... us, by partaking of our nature: and so becomes a **days-man** or umpire between both. Now, though this be a gre ...
  * ... of our nature, Hebrews 2:14, 16: and so becomes a **days-man** or umpire between both." See what it is to be adv ...

### 21. `tri-unity`
* **Description:** Splittable word (rejoins to valid word 'triunity')
* **Chapter:** *Of the Person of Christ*
* **Contexts:**
  * ... e is a second person, the Son of God, in the holy **tri-unity** of the Godhead, we have proved before. That this ...

---

## Punctuation Spacing Blemishes

### 1. `Burgess .`
* **Description:** Spaced period (space before period)
* **Chapter:** *To the Reader.*
* **Contexts:**
  * ... Reader, I am Thy servant in Christ Jesus, Daniel **Burgess .**

### 2. `II .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Analysis.*
* **Contexts:**
  * ... d practical inferences deduced from it, IV. Part **II .** — The reality of communion with CHRIST is proved, ...

### 3. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Chapter 2 - That the saints have this communion distinctly with the Father, Son, and Spirit — ...*
* **Contexts:**
  * ... xpressly conjoin, and yet as expressly distinguish**,,** the Father and the Son in directing his supplicat ...

### 4. `Objection .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 3 - Of the peculiar and distinct communion which the saints have with the Father — Obs...*
* **Contexts:**
  * ... ce, yet he gathers us with everlasting kindness. **Objection .** But you will say, "This comes nigh to that blasph ...

### 5. `Answer .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 3 - Of the peculiar and distinct communion which the saints have with the Father — Obs...*
* **Contexts:**
  * ... m more, or to walk with him unto well-pleasing?" **Answer .** There are few truths of Christ which, from some o ...

### 6. `Objection .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 6 - Of communion with Christ in purchased grace — considered in respect of its rise an...*
* **Contexts:**
  * ... obedience of Christ, as the other by his death. **Objection .** "But if this be so, then are we as righteous as C ...

### 7. `Objection .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8 - How the saints hold communion with Christ as to their acceptation with God — What ...*
* **Contexts:**
  * ... we receive love, life, righteousness, and peace. **Objection .** But it may be said, "Surely this course of proced ...

### 8. `Answer .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8 - How the saints hold communion with Christ as to their acceptation with God — What ...*
* **Contexts:**
  * ... e always giving sins, and taking righteousness?" **Answer .** There is not any thing that Jesus Christ is more ...

### 9. `Obj .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8 - How the saints hold communion with Christ as to their acceptation with God — What ...*
* **Contexts:**
  * ... engaging themselves to this communion with him. **Obj .** Yea, hut you will say, "If this be so, what need ...

### 10. `1 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Doctrine of the Holy Trinity Explained and Vindicated*
* **Contexts:**
  * ... se of. The sum of what they say in general is, — **1 .** "How can these things be? How can three be one, a ...

---

## OCR & Bracket Residues

No anomalies found in this category.

## Mixed-Case Capitalization Errors

No anomalies found in this category.

## Unresolved Citation References

### 1. `lib. iii`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *An Appendix*
* **Contexts:**
  * ... d purchase my liberty with his own life," [Cyrop. **lib. iii**.] And these things are added on the occasion of t ...

### 2. `lib. x`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *An Appendix*
* **Contexts:**
  * ... caedemque ac cruorem, coelestum, inferorum iras," **lib. x**. 28; — "That he carried away before him, from tho ...

---

## Structural Nesting Sequence Jumps

### 1. `I. ... III.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Analysis.*
* **Contexts:**

### 2. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Digression 2.*
* **Contexts:**
  * [[DIGRESSION]] DIGRESSION **2.** [[SUMMARY]] All solid wisdom laid up in Christ — ...
  * ... dom and prudence, for the management of affairs; **2.** Ability of learning and literature; — but God rej ...
  * ... knowledge of God, his nature and his properties. **2.** The knowledge of ourselves in reference to the wi ...

### 3. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Chapter 5 - Other consequential affections: — 1 On the part of Christ — He values his saints —...*
* **Contexts:**
  * ... nces of that valuation: — (1.) His incarnation; (**2.**) Exinanition, 2 Corinthians 8:9; Philippians 17:6 ...
  * ... . His valuation of them in comparison of others. **2.** Believers' estimation of Christ: — (1.) They val ...
  * ... y value him above all other things and persons; (**2.**) Above their own lives; (3.) All spiritual excel ...

### 4. `II.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Chapter 5 - Other consequential affections: — 1 On the part of Christ — He values his saints —...*
* **Contexts:**
  * ... Christ, bounty; on the part of the saints, duty. **II.** Christ values his saints, values believers (which ...
  * ... eference to this life or that which is to come. I**II.** The third conjugal affection on the part of Chris ...

### 5. `2. ... 10.`
* **Description:** List sequence jump (skipped from 2 to 10)
* **Chapter:** *An Appendix*
* **Contexts:**

---

## Invalid Bible References

### 1. `Philippians 29`
* **Description:** Invalid Bible reference (chapter 29 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 2 - That the saints have this communion distinctly with the Father, Son, and Spirit — ...*
* **Contexts:**
  * ... creation unto his sovereignty. (Romans 14:10, 11; **Philippians 29**:10 2:10.) In this place of the apostle it hath a ...
  * ... 4:6; 1 John 2:22-24, 1 John 5:10-13; Hebrews 1:6; **Philippians 29**:10 2:10; John 5:23.) and distinctly directed unto ...

### 2. `Philippians 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 2 - That the saints have this communion distinctly with the Father, Son, and Spirit — ...*
* **Contexts:**
  * ... on of that fullness to him committed you may see, **Philippians 23**:8 2:8-11. "When thou shalt make his soul an offer ...

### 3. `2 Kings 25`
* **Description:** Invalid Bible reference (chapter 25 exceeds max 22 for Kings)
* **Chapter:** *Chapter 2 - What it is wherein we have peculiar fellowship with the Lord Christ — This is in g...*
* **Contexts:**
  * ... ; Genesis 39:21, 41:37; Acts 7:10; 1 Samuel 2:26; **2 Kings 25**:27, etc. 3. The fruits of the Spirit, sanctifyin ...

### 4. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Digression 1.*
* **Contexts:**
  * ... "he thought it not robbery to be equal with God," **Philippians 17**:6 2:6. In the glory of this majesty he dwells in ...

### 5. `Philippians 26`
* **Description:** Invalid Bible reference (chapter 26 exceeds max 4 for Philippians)
* **Chapter:** *Digression 1.*
* **Contexts:**
  * ... having received a "name above every name," etc., **Philippians 26**:9 2:9. Thus is he glorious in his throne, which i ...

### 6. `John 24`
* **Description:** Invalid Bible reference (chapter 24 exceeds max 21 for John)
* **Chapter:** *Digression 2.*
* **Contexts:**
  * ... ters them from all thoughts of approach unto him, **John 24**:19. What relief have we from thoughts of his imme ...

### 7. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 5 - Other consequential affections: — 1 On the part of Christ — He values his saints —...*
* **Contexts:**
  * ... incarnation; (2.) Exinanition, 2 Corinthians 8:9; **Philippians 17**:6 2:6,7; (3.) Obedience as a servant; (4.) In h ...
  * ... he undertook. This is also more fully expressed, **Philippians 17**:6 2:6,7, [[BLOCKQUOTE]] "Who being in the form o ...

### 8. `Jude 15`
* **Description:** Invalid Bible reference (chapter 15 exceeds max 1 for Jude)
* **Chapter:** *Chapter 5 - Other consequential affections: — 1 On the part of Christ — He values his saints —...*
* **Contexts:**
  * ... s beloved, Matthew 25:41-46; 2 Thessalonians 1:6; **Jude 15**. It is hence evident that Christ abounds in pity ...

### 9. `Philippians 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 6 - Of communion with Christ in purchased grace — considered in respect of its rise an...*
* **Contexts:**
  * ... gs, and it was that which gave life to his death, **Philippians 23**:8 2:8. He was obedient to death: for therein "he ...

### 10. `Philippians 38`
* **Description:** Invalid Bible reference (chapter 38 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 7 - The nature of purchased grace; referred to three heads: —*
* **Contexts:**
  * ... rk in us to will and to do of his good pleasure," **Philippians 38**:13 2:13. And in these three, thus briefly named, ...

### 11. `Philippians 20`
* **Description:** Invalid Bible reference (chapter 20 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 8 - How the saints hold communion with Christ as to their acceptation with God — What ...*
* **Contexts:**
  * ... th God, he is, — [1.] Honored of God his Father. **Philippians 20**:7 2:7-11, [[BLOCKQUOTE]] "He made himself of no ...

### 12. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *A Vindication*
* **Contexts:**
  * ... of the grace of our Lord Jesus Christ, mentioned **Philippians 17**:6 2:6-11. But he will now discover the design of ...
  * ... Isaiah 6:1-4; John 12:41; Isaiah 9:6; John 1:14; **Philippians 17**:6 2:6, etc.), or shall think that the grace or ex ...

### 13. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Preface (A Brief Declaration and Vindication of the Doctrine of the Trinity)*
* **Contexts:**
  * ... shion of a man, he might be obedient unto death," **Philippians 17**:6 2:6-8; whereby his divine glory was veiled for ...

### 14. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *The Doctrine of the Holy Trinity Explained and Vindicated*
* **Contexts:**
  * ... troyed of serpents;" compared with Numbers 21:6. **Philippians 14**:5 2:5,6, "Let this mind be in you, which was also ...

### 15. `Philippians 20`
* **Description:** Invalid Bible reference (chapter 20 exceeds max 4 for Philippians)
* **Chapter:** *The Doctrine of the Holy Trinity Explained and Vindicated*
* **Contexts:**
  * ... with the Father in respect of nature and essence, **Philippians 20**:7 2:7,8. A son, of the same nature with his fathe ...

### 16. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Of the Person of Christ*
* **Contexts:**
  * ... body hast thou prepared me;" as also, Romans 8:3. **Philippians 14**:5 2:5-7, "Let this mind be in you, which was also ...

### 17. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Of the Satisfaction of Christ*
* **Contexts:**
  * ... 2. It was also done by his own voluntary consent, **Philippians 17**:6 2:6-8. 3. He was substituted, and did substitu ...

### 18. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Of the Satisfaction of Christ*
* **Contexts:**
  * ... ing our nature upon him, — expressed by his mind, **Philippians 14**:5 2:5-8, and the readiness of his will, Psalm 40: ...

---

## List Formatting Inconsistencies

No anomalies found in this category.

