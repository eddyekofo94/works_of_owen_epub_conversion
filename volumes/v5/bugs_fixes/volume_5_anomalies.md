# Text Integrity & Anomaly Audit Report: Volume 5

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 228810
* **Total Suspected Anomalies Found:** 10

Add corrections to `text_replacements` inside `volumes/v5/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 0 items
* **Punctuation Spacing Blemishes:** 0 items
* **OCR & Bracket Residues:** 8 items
* **Mixed-Case Capitalization Errors:** 0 items
* **Unresolved Citation References:** 0 items
* **Structural Nesting Sequence Jumps:** 0 items
* **Invalid Bible References:** 1 items
* **List Formatting Inconsistencies:** 0 items
* **Unmatched Quotation Marks:** 1 items

---

## Hyphenation Anomalies

No anomalies found in this category.

## Punctuation Spacing Blemishes

No anomalies found in this category.

## OCR & Bracket Residues

### 1. `s detailed`
* **Description:** Split word anomaly (isolated letter 's')
* **Chapter:** *Prefatory Note (The Doctrine of Justification by Faith)*
* **Contexts:**
  * ... e is impossible, useless, and pernicious, receive **s detailed** confutation, 12; thirdly, from the difference bet ...

### 2. `s ex`
* **Description:** Split word anomaly (isolated letter 's')
* **Chapter:** *General Considerations,*
* **Contexts:**
  * ... sequium meum cum omnibus quae tu egisti, et pssus **s ex** tam perfecta charitate et obedientia. Et cum divi ...
  * ... of God by the gospel, "from faith to faith," it i**s ex**pressly contradictory to his whole discourse, chap ...
  * ... h believeth in Jesus. Where is boasting then? It i**s ex**cluded. By what law? Of works? Nay; but by the law ...

### 3. `be1ieveth`
* **Description:** Spliced alphanumeric word (contains inline numbers)
* **Chapter:** *Chapter 1 - Justifying Faith*
* **Contexts:**
  * ... ieve on him whom he has sent;" verse 47, "He that **be1ieveth** on me has everlasting life;" chapter "He that bel ...

### 4. `s proposed`
* **Description:** Split word anomaly (isolated letter 's')
* **Chapter:** *Chapter 1 - Justifying Faith*
* **Contexts:**
  * ... Wherefore, our first inquiry is concerning what wa**s proposed** in the second place, — namely, What is on our par ...
  * ... aith is in general an assent unto the truth that i**s proposed** unto us upon divine testimony. And hereby, as it ...
  * ... ce and mercy of God, through the blood of Christ, **s proposed** in the promises of the gospel; — that is, they di ...

### 5. `s declared`
* **Description:** Split word anomaly (isolated letter 's')
* **Chapter:** *Chapter 8 - Imputation of the Sins of the Church Unto Christ*
* **Contexts:**
  * ... what I intend to prove in the present discourse i**s declared** fully therein. Thus, therefore, he speaks: "How, ...
  * ... as a vine and its branches, John 15:1,2. And it i**s declared** by the relation that was between Adam and his pos ...
  * ... s it wholly into the immutability of his counsel, **s declared** by his promise and oath, chapter 6:18,19: so that ...

### 6. `name)y`
* **Description:** OCR residue containing stray closing bracket/paren
* **Chapter:** *Chapter 18 - the Nature of Justification*
* **Contexts:**
  * ... reignty and freedom of the grace of God herein, — **name)y**, that we are justified freely by his grace, — and ...

### 7. `p)ace`
* **Description:** OCR residue containing stray closing bracket/paren
* **Chapter:** *Chapter 18 - the Nature of Justification*
* **Contexts:**
  * ... t., cap. 4. And the words of Chrysostom upon this **p)ace**, unto the same purpose, have been cited before at ...

### 8. `s to`
* **Description:** Split word anomaly (isolated letter 's')
* **Chapter:** *Evidences of the Faith of Godìs Elect*
* **Contexts:**
  * ... efficacy which they have on the souls of believer **s to** assure them of this truth. In this record, so sol ...
  * ... ners may be saved, or what they shall do themselve**s to** be saved: "What shall we do? to be saved?" "What ...
  * ... powerfully efficacious unto its end. As such it i**s to** be received, or it is rejected. It is not enough ...

---

## Mixed-Case Capitalization Errors

No anomalies found in this category.

## Unresolved Citation References

No anomalies found in this category.

## Structural Nesting Sequence Jumps

No anomalies found in this category.

## Invalid Bible References

### 1. `John 22`
* **Description:** Invalid Bible reference (chapter 22 exceeds max 21 for John)
* **Chapter:** *General Considerations,*
* **Contexts:**
  * ... elieve that Jesus is the Christ, the Son of God," **John 22**:30,31. Unto this end every thing is recorded by ...

---

## List Formatting Inconsistencies

No anomalies found in this category.

## Unmatched Quotation Marks

### 1. `Isaiah 13:6, 7; — "When the day of judgment or of death shall come, all hands will be dissolved" (that is, faint or fall...`
* **Description:** Paragraph has unmatched double quotes (count: 7)
* **Chapter:** *General Considerations,*
* **Contexts:**
  * **Isaiah 13:6, 7; — "When the day of judgment or of death shall come, all hands will be dissolved" (that is, faint or fall...**

---

