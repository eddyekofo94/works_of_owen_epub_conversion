# Text Integrity & Anomaly Audit Report: Volume 1

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 243045
* **Total Suspected Anomalies Found:** 48

Add corrections to `text_replacements` inside `volumes/v1/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 13 items
* **Punctuation Spacing Blemishes:** 3 items
* **OCR & Bracket Residues:** 0 items
* **Mixed-Case Capitalization Errors:** 0 items
* **Unresolved Citation References:** 0 items
* **Structural Nesting Sequence Jumps:** 6 items
* **Invalid Bible References:** 26 items
* **List Formatting Inconsistencies:** 0 items

---

## Hyphenation Anomalies

### 1. `Bar-jona`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Chapter 1 - Peter's Confession*
* **Contexts:**
  * ... swered and said unto him, Blessed art thou, Simon **Bar-jona**: for flesh and blood has not revealed it unto the ...
  * ... swered and said unto him, Blessed art thou, Simon **Bar-jona**: for flesh and blood has not revealed it unto the ...

### 2. `pole-star`
* **Description:** Splittable word (rejoins to valid word 'polestar')
* **Chapter:** *Chapter 15 - Conformity Unto Christ*
* **Contexts:**
  * ... ity of all sorts of sufferings. This has been the **pole-star** of the church in all its storms; the guide, the c ...

### 3. `over-valuation`
* **Description:** Splittable word (rejoins to valid word 'overvaluation')
* **Chapter:** *Preface (Meditations and Discourses on the Glory of Christ)*
* **Contexts:**
  * ... es do arise. For they all grow on this root of an **over-valuation** of temporal things. And unless we can arrive unto ...

### 4. `day-star`
* **Description:** Splittable word (rejoins to valid word 'daystar')
* **Chapter:** *Chapter 2 - the Glory of the Person of Christ*
* **Contexts:**
  * ... t dawn, the "shadows did not flee away," nor the "**day-star** shine" in the hearts of men. But when the "Sun of ...

### 5. `merchant-man`
* **Description:** Splittable word (rejoins to valid word 'merchantman')
* **Chapter:** *Chapter 3 - the Glory of Christ in the Mysterious Constitution of His Person.*
* **Contexts:**
  * ... "wise unto salvation." We should herein be as the **merchant-man** that seeks for pearls; he seeks for all sorts of ...

### 6. `Spiritual-mindedness`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Chapter 3 - the Glory of Christ in the Mysterious Constitution of His Person.*
* **Contexts:**
  * ... which are required whereunto. See the treatise on **Spiritual-mindedness** It is to be feared that there are some who profes ...

### 7. `days-man`
* **Description:** Splittable word (rejoins to valid word 'daysman')
* **Chapter:** *Chapter 4 - the Glory of Christ in His Susception of the Office of a Mediator*
* **Contexts:**
  * ... 1 Samuel 2:25. There is not [[BLOCKQUOTE]] "any **days-man** betwixt us, that might lay his hand upon us both, ...

### 8. `re-collected`
* **Description:** Splittable word (rejoins to valid word 'recollected')
* **Chapter:** *Chapter 11 - the Glory of Christ in the Recapitulation of All Things in Him.*
* **Contexts:**
  * ... inctly and variously towards the two parts of the **re-collected** family of angels and men, according as their diff ...

### 9. `re-collection`
* **Description:** Splittable word (rejoins to valid word 'recollection')
* **Chapter:** *Chapter 11 - the Glory of Christ in the Recapitulation of All Things in Him.*
* **Contexts:**
  * ... , was made known unto them. Herein namely, in the **re-collection** of all things in Christ — divine wisdom has made ...

### 10. `hundred-fold`
* **Description:** Splittable word (rejoins to valid word 'hundredfold')
* **Chapter:** *Chapter 13 - the Second Difference Between Our Beholding the Glory of Christ by Faith in This World and by Sight in Heaven*
* **Contexts:**
  * ... nal life in the world to come, we shall receive a **hundred-fold** recompense for all that we can lose or suffer for ...

### 11. `two-fold`
* **Description:** Splittable word (rejoins to valid word 'twofold')
* **Chapter:** *Chapter 11 - of the Offices of Christ; And, First, of His Kingly.*
* **Contexts:**
  * ... oes the kingly office of Christ consist? A. In a **two-fold** power; first, his power of ruling in and over his ...

### 12. `re-stipulation`
* **Description:** Splittable word (rejoins to valid word 'restipulation')
* **Chapter:** *Chapter 12 - of Christ's Priestly Office.*
* **Contexts:**
  * ... nd in him mercy, pardon, grace, and glory, with a **re-stipulation** of faith from them unto this promise, and new obe ...

### 13. `TWO-FOLD`
* **Description:** Splittable word (rejoins to valid word 'TWOFOLD')
* **Chapter:** *Chapter 14 - of the Two-fold Estate of Christ.*
* **Contexts:**
  * [[SUMMARY]] OF THE **TWO-FOLD** ESTATE OF CHRIST. Q. 1. In what estate or condit ...
  * ... tion does Christ exercise these offices? A. In a **two-fold** estate; first, of humiliation or abasement; se ...

---

## Punctuation Spacing Blemishes

### 1. `first .`
* **Description:** Spaced period (space before period)
* **Chapter:** *General Preface.*
* **Contexts:**
  * ... tion in the numerals — I, 1, (1), [1], first, and **first .** It would have been an advantage if we could have ...

### 2. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Chapter 16 - an Humble Inquiry Into, and Prospect Of, the Infinite Wisdom of God*
* **Contexts:**
  * ... o obnoxious unto the curse by its sin and apostasy**,,** that it was not reparable to the glory of God; an ...

### 3. `2 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Lesser Catechism*
* **Contexts:**
  * ... repentance also, and holiness. — Chapter 20. Q. **2 .** What is repentance? A. A forsaking of all sin, w ...

---

## OCR & Bracket Residues

No anomalies found in this category.

## Mixed-Case Capitalization Errors

No anomalies found in this category.

## Unresolved Citation References

No anomalies found in this category.

## Structural Nesting Sequence Jumps

### 1. `13.`
* **Description:** List sequence starts at 13 instead of 1
* **Chapter:** *Preface*
* **Contexts:**
  * ... icabo te, non me super te:" De Verbis Dom., Serm. **13.** — "Upon this rock which thou hast confessed — upo ...

### 2. `4. ... 7.`
* **Description:** List sequence jump (skipped from 4 to 7)
* **Chapter:** *Chapter 10 - the Principle of the Assignation of Divine Honor Unto the Person of Christ*
* **Contexts:**

### 3. `III.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Chapter 15 - Conformity Unto Christ*
* **Contexts:**
  * ... ONFORMITY UNTO CHRIST, AND FOLLOWING HIS EXAMPLE **III.** The third thing proposed to declare the use of th ...

### 4. `III.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Preface (Meditations and Discourses on the Glory of Christ)*
* **Contexts:**
  * ... e is the head, we are participant in this glory. **III.** It is he in whom our nature has been carried succ ...

### 5. `10.`
* **Description:** List sequence starts at 10 instead of 1
* **Chapter:** *The Lesser Catechism*
* **Contexts:**
  * ... son, to be a mediator between God and man. — Chap **10.** Q. What is he unto us? A. A King, a Priest, and ...

### 6. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *The Lesser Catechism*
* **Contexts:**

---

## Invalid Bible References

### 1. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 3 - the Person of Christ the Most Ineffable Effect of Divine Wisdom*
* **Contexts:**
  * ... hat wherein he will be admired unto eternity. See **Philippians 17**:6 2:6-9. In Isaiah (chap. 6) there is a represen ...

### 2. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 4 - to Person of Christ the Foundation of All*
* **Contexts:**
  * ... one of us," as the apostle declares it at large, **Philippians 17**:6 2:6-8. It is the nature of sincere goodness — e ...

### 3. `Philippians 29`
* **Description:** Invalid Bible reference (chapter 29 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 7 - Power and Efficacy Communicated Unto the Office of Christ*
* **Contexts:**
  * ... the sea, with all things in them and under them, (**Philippians 29**:10 2:10,) with the dead bodies of men, which he s ...

### 4. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 9 - Honor Due to the Person of Christ*
* **Contexts:**
  * ... nd "thought it not robbery to be equal with God," **Philippians 17**:6 2:6, 7. He can no more really and essentially, ...

### 5. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 9 - Honor Due to the Person of Christ*
* **Contexts:**
  * ... which the apostle unto this purpose insists upon, **Philippians 14**:5 2:5-8. Now the great design of all believers is ...

### 6. `Jude 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 1 for Jude)
* **Chapter:** *Chapter 10 - the Principle of the Assignation of Divine Honor Unto the Person of Christ*
* **Contexts:**
  * ... to accompany the accomplishment of this promise, **Jude 14**; and Noah was a preacher of the righteousness to ...

### 7. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 14 - Motives Unto the Love of Christ*
* **Contexts:**
  * ... all other things to engage our love unto him. See **Philippians 14**:5 2:5-11, with chap. 3:8-11. Motives unto the lo ...

### 8. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 15 - Conformity Unto Christ*
* **Contexts:**
  * ... the same mind be in us that was in Christ Jesus," **Philippians 17**:6 2:6; and that we "walk in love, as he also love ...

### 9. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 15 - Conformity Unto Christ*
* **Contexts:**
  * ... m, as they are all of them summarily represented, **Philippians 14**:5 2:5-8, by reason of the glory of his person and ...

### 10. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 18 - the Nature of the Person of Christ*
* **Contexts:**
  * ... angels, but he took on him the seed of Abraham;" **Philippians 17**:6 2:6, 7, [[BLOCKQUOTE]] "Being in the form of ...
  * ... him the form of a servant, and became obedient," **Philippians 17**:6 2:6-8. That by his being "in the form of God," ...

### 11. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 20 - the Exercise of the Mediatory Office of Christ in Heaven*
* **Contexts:**
  * ... to undergo things difficult, hard, and terrible, **Philippians 17**:6 2:6-8. Such were the things which our Lord Jesu ...

### 12. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 3 - the Glory of Christ in the Mysterious Constitution of His Person.*
* **Contexts:**
  * ... 10; Isaiah 6:1-4, 9:6; Zechariah 3:8; John 1:1-3; **Philippians 17**:6 2:6-8; Hebrews 1:1-3, 2:14-16; Revelation 1:17, ...

### 13. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 4 - the Glory of Christ in His Susception of the Office of a Mediator*
* **Contexts:**
  * ... nd discharge of it. So the apostle expresseth it, **Philippians 14**:5 2:5-8, [[BLOCKQUOTE]] "Let this mind be in you ...
  * ... he Son of God, as it is described by the apostle, **Philippians 14**:5 2:5-8. And this is that wherein in an especial ...
  * ... in it is to be resolved; as the apostle declares, **Philippians 14**:5 2:5-8. And no man does deny himself in a due ma ...

### 14. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 4 - the Glory of Christ in His Susception of the Office of a Mediator*
* **Contexts:**
  * ... and thought it not robbery to be equal with God," **Philippians 17**:6 2:6; — that is, being really and essentially G ...

### 15. `Philippians 20`
* **Description:** Invalid Bible reference (chapter 20 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 4 - the Glory of Christ in His Susception of the Office of a Mediator*
* **Contexts:**
  * ... of a servant, and was found in fashion as a man, **Philippians 20**:7 2:7. This is his condescension. It is not said ...
  * ... bled himself, and made himself of no reputation," **Philippians 20**:7 2:7, 8. He veiled the glory of his divine natur ...

### 16. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 7 - the Glory of Christ in His Exaltation After the Accomplishment of the Work*
* **Contexts:**
  * ... e is frequently expressed elsewhere, Romans 14:9; **Philippians 14**:5 2:5-9. So much as we know of Christ, his suffer ...

### 17. `2 Kings 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 22 for Kings)
* **Chapter:** *Chapter 9 - the Glory of Christ in His Intimate Conjunction With the Church*
* **Contexts:**
  * ... pecially those committed in the days of Manasseh, **2 Kings 23**:26, 27; as afterward, in the final destruction of ...

### 18. `Jude 6`
* **Description:** Invalid Bible reference (chapter 6 exceeds max 1 for Jude)
* **Chapter:** *Chapter 4 - of the Works of God; And, First, of Those That Are Internal and Immanent.*
* **Contexts:**
  * ... whom other things were ordained. 1 Timothy 5:21; **Jude 6**. Q. 4. What are the decrees of God concerning me ...

### 19. `Philippians 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 9 - of the Incarnation of Christ.*
* **Contexts:**
  * ... of the cross. Isaiah 50:6; John 1:14; Luke 1:35; **Philippians 23**:8 2:8; 1 Timothy 3:16.

### 20. `Philippians 29`
* **Description:** Invalid Bible reference (chapter 29 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 10 - of the Person of Jesus Christ.*
* **Contexts:**
  * ... in John 1:23; Isaiah 45:22, 23, in Romans 14:11, **Philippians 29**:10 2:10, 11; Malachi 3:1, in Matthew 11:10. Seco ...

### 21. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 10 - of the Person of Jesus Christ.*
* **Contexts:**
  * ... pressly, John 1:1, 20:28; Acts 20:28; Romans 9:5; **Philippians 17**:6 2:6; Hebrews 1:8; 1 Timothy 3:16; secondly, of ...

### 22. `Philippians 26`
* **Description:** Invalid Bible reference (chapter 26 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 11 - of the Offices of Christ; And, First, of His Kingly.*
* **Contexts:**
  * ... Acts 2:36, 10:42; 1 Corinthians 11:3, 15:27, 28; **Philippians 26**:9 2:9; Hebrews 3:2, 6, 2:7-9. Q. 3. Wherein does ...

### 23. `Philippians 20`
* **Description:** Invalid Bible reference (chapter 20 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 12 - of Christ's Priestly Office.*
* **Contexts:**
  * ... ebrews 10:5-10. Psalm 2:7, 8; Isaiah 53:8, 10-12; **Philippians 20**:7 2:7, 9; Hebrews 12:2; John 17:2, 4. Q. 2. Wher ...

### 24. `Philippians 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 14 - of the Two-fold Estate of Christ.*
* **Contexts:**
  * ... or abasement; secondly, of exaltation or glory. **Philippians 23**:8 2:8-10. Q. 2. Wherein consisteth the state of ...

### 25. `Philippians 26`
* **Description:** Invalid Bible reference (chapter 26 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 14 - of the Two-fold Estate of Christ.*
* **Contexts:**
  * ... r. Matthew 28:18; Romans 1:4, 6:4; Ephesians 4:9; **Philippians 26**:9 2:9, 10; 1 Timothy 3:16.

### 26. `Philippians 5`
* **Description:** Invalid Bible reference (chapter 5 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 25 - of the Communion of Saints,*
* **Contexts:**
  * ... 12:5; 1 Corinthians 12:27,28; Ephesians 4:11-13; **Philippians 5**:2 2:2; Colossians 3:15; 1 Peter 3:8.

---

## List Formatting Inconsistencies

No anomalies found in this category.

