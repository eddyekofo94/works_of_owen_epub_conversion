# Text Integrity & Anomaly Audit Report: Volume 1

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 243045
* **Total Suspected Anomalies Found:** 26

Add corrections to `text_replacements` inside `volumes/v1/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 13 items
* **Punctuation Spacing Blemishes:** 4 items
* **OCR & Bracket Residues:** 4 items
* **Mixed-Case Capitalization Errors:** 0 items
* **Unresolved Citation References:** 0 items
* **Structural Nesting Sequence Jumps:** 5 items

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
  * ... tion does Christ exercise these offices? A. In a **two-fold** estate; first, of humiliation or abasement; ...

---

## Punctuation Spacing Blemishes

### 1. `first .`
* **Description:** Spaced period (space before period)
* **Chapter:** *General Preface.*
* **Contexts:**
  * ... tion in the numerals — I, 1, (1), [1], first, and **first .** It would have been an advantage if we could have ...

### 2. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 9 - Honor Due to the Person of Christ*
* **Contexts:**
  * ... ed in the duty of invocation or prayer unto him? **Ans .** 1. There is no precedent nor example of any such ...

### 3. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Chapter 16 - an Humble Inquiry Into, and Prospect Of, the Infinite Wisdom of God*
* **Contexts:**
  * ... o obnoxious unto the curse by its sin and apostasy**,,** that it was not reparable to the glory of God; an ...

### 4. `2 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Lesser Catechism*
* **Contexts:**
  * ... repentance also, and holiness. — Chapter 20. Q. **2 .** What is repentance? A. A forsaking of all sin, w ...

---

## OCR & Bracket Residues

### 1. `h in`
* **Description:** Split word anomaly (isolated letter 'h')
* **Chapter:** *General Preface.*
* **Contexts:**
  * ... itical authors of Great Britain; and there is trut**h in** the assertion, that the philosopher "ploughed wit ...
  * ... with peculiar closeness of application; stripping **h in** of his false dependencies, and exhibiting before ...
  * ... of Dr Wright, a minister of the Established Churc**h in** Stirling. In the list of subscribers to a folio v ...

### 2. `d imaginem`
* **Description:** Split word anomaly (isolated letter 'd')
* **Chapter:** *Preface*
* **Contexts:**
  * ... E]] "Imago, [id est, Verbum Dei, ] ad eum qui est **d imaginem**, [hoc est, hominem, ] venit, et quaerit imago eum ...

### 3. `fulfil1ing`
* **Description:** Spliced alphanumeric word (contains inline numbers)
* **Chapter:** *Chapter 8 - Representations of the Glory of Christ Under the Old Testament.*
* **Contexts:**
  * ... erity of the curse wherewith it was attended; his **fulfil1ing** of it was life, by the pardon and righteousness w ...

### 4. `sou1s`
* **Description:** Spliced alphanumeric word (contains inline numbers)
* **Chapter:** *Chapter 12 - Differences Between Our Beholding the Glory of Christ by Faith in This World and by Sight in Heaven*
* **Contexts:**
  * ... sight. Those are the two spiritual powers of our **sou1s**; — by the one whereof we are made partakers of gr ...

---

## Mixed-Case Capitalization Errors

No anomalies found in this category.

## Unresolved Citation References

No anomalies found in this category.

## Structural Nesting Sequence Jumps

### 1. `3. ... 40.`
* **Description:** List sequence jump (skipped from 3 to 40)
* **Chapter:** *Preface*
* **Contexts:**

### 2. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Chapter 5 - the Person of Christ the Great Representative of God*
* **Contexts:**

### 3. `4. ... 7.`
* **Description:** List sequence jump (skipped from 4 to 7)
* **Chapter:** *Chapter 10 - the Principle of the Assignation of Divine Honor Unto the Person of Christ*
* **Contexts:**

### 4. `1. ... 26.`
* **Description:** List sequence jump (skipped from 1 to 26)
* **Chapter:** *Chapter 9 - the Glory of Christ in His Intimate Conjunction With the Church*
* **Contexts:**

### 5. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *The Lesser Catechism*
* **Contexts:**

---

