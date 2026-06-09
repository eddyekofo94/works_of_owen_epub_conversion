# Text Integrity & Anomaly Audit Report: Volume 16

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 258379
* **Total Suspected Anomalies Found:** 10

Add corrections to `text_replacements` inside `volumes/v16/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 0 items
* **Punctuation Spacing Blemishes:** 0 items
* **OCR & Bracket Residues:** 0 items
* **Mixed-Case Capitalization Errors:** 0 items
* **Unresolved Citation References:** 1 items
* **Structural Nesting Sequence Jumps:** 6 items
* **Invalid Bible References:** 3 items
* **List Formatting Inconsistencies:** 0 items

---

## Hyphenation Anomalies

No anomalies found in this category.

## Punctuation Spacing Blemishes

No anomalies found in this category.

## OCR & Bracket Residues

No anomalies found in this category.

## Mixed-Case Capitalization Errors

No anomalies found in this category.

## Unresolved Citation References

### 1. `lib. 3 cap. 2`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 1 - the Subject-matter of the Church.*
* **Contexts:**
  * ... titution of a church in its members," De Ecclesia **lib. 3 cap. 2**. 4. They must be such as do make an open profess ...
  * ... ith none in this matter. Bellarmine, De Ecclesia **lib. 3 cap. 2**, gives an account out of Augustine, and that trul ...

---

## Structural Nesting Sequence Jumps

### 1. `4.`
* **Description:** List sequence starts at 4 instead of 1
* **Chapter:** *Sermon 4 - Spiritual Strength; - Its Reality, Decay, & Renovati*
* **Contexts:**
  * SERMON **4.** SPIRITUAL STRENGTH; — ITS REALITY, DECAY, AND ...

### 2. `8.`
* **Description:** List sequence starts at 8 instead of 1
* **Chapter:** *Sermon 8 - the Mutual Care of Believers Over One Another.*
* **Contexts:**
  * SERMON **8.** THE MUTUAL CARE OF BELIEVERS OVER ONE ANOTHER ...
  * ... RS OVER ONE ANOTHER. PREACHED SEPTEMBER 6, 167**8.** "But speaking the truth in love, may grow up i ...

### 3. `10.`
* **Description:** List sequence starts at 10 instead of 1
* **Chapter:** *Sermon 10 - the Death of the Righteous.*
* **Contexts:**
  * SERMON **10.** THE DEATH OF THE RIGHTEOUS. PREACHED JULY 1, ...

### 4. `11.`
* **Description:** List sequence starts at 11 instead of 1
* **Chapter:** *Sermon 11 - the Humiliation and Condescension of Christ.*
* **Contexts:**
  * SERMON **11.** THE HUMILIATION AND CONDESCENSION OF CHRIST. ...

### 5. `12.`
* **Description:** List sequence starts at 12 instead of 1
* **Chapter:** *Sermon 12 - Enoch's Walk With God.*
* **Contexts:**
  * SERMON **12.** ENOCH'S WALK WITH GOD. [THE DATE OF THIS SERM ...

### 6. `13.`
* **Description:** List sequence starts at 13 instead of 1
* **Chapter:** *Sermon 13 - a Fast Sermon: - Christian Duty Under the Hidings O*
* **Contexts:**
  * SERMON **13.** A FAST SERMON: — CHRISTIAN DUTY UNDER THE HID ...

---

## Invalid Bible References

### 1. `Philippians 5`
* **Description:** Invalid Bible reference (chapter 5 exceeds max 4 for Philippians)
* **Chapter:** *A Vindication of Two Passages in Irenaeus Against the Exception*
* **Contexts:**
  * ... f, — 'Took upon him the form of a servant,' etc., **Philippians 5** 7, 8. "By all which reasons," saith Mr Tombs, "I ...

### 2. `2 Kings 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 22 for Kings)
* **Chapter:** *Sermon 6 - the Obligation to Increase in Godliness,*
* **Contexts:**
  * ... t;" — sometimes it is called a walking after God: **2 Kings 23**:3, "The king made a covenant to walk after the LO ...

### 3. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 11 - the Humiliation and Condescension of Christ.*
* **Contexts:**
  * ... and thought it not robbery to be equal with God," **Philippians 17**:6 2:6. He was "in the form of God." God hath no i ...

---

## List Formatting Inconsistencies

No anomalies found in this category.

