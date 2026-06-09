# Text Integrity & Anomaly Audit Report: Volume 5

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 228811
* **Total Suspected Anomalies Found:** 42

Add corrections to `text_replacements` inside `volumes/v5/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 10 items
* **Punctuation Spacing Blemishes:** 4 items
* **OCR & Bracket Residues:** 1 items
* **Mixed-Case Capitalization Errors:** 0 items
* **Unresolved Citation References:** 2 items
* **Structural Nesting Sequence Jumps:** 4 items
* **Invalid Bible References:** 6 items
* **List Formatting Inconsistencies:** 0 items
* **Unmatched Quotation Marks:** 15 items

---

## Hyphenation Anomalies

### 1. `wire-draw`
* **Description:** Splittable word (rejoins to valid word 'wiredraw')
* **Chapter:** *To the Reader (The Doctrine of Justification by Faith)*
* **Contexts:**
  * ... iness to cavil at expressions, to wrest my words, **wire-draw** inferences and conclusions from them not expressl ...

### 2. `dikaio-oo`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 4 - of Justification*
* **Contexts:**
  * ... y no man was ever yet so fond as to pretend that "**dikaio-oo**" did signify to pardon sin, yet is it the only wo ...

### 3. `non-imputation`
* **Description:** Splittable word (rejoins to valid word 'nonimputation')
* **Chapter:** *Chapter 4 - of Justification*
* **Contexts:**
  * ... nishment due unto sin;" for it comprises both the **non-imputation** of sin and the imputation of righteousness, with ...

### 4. `sub-distinguished`
* **Description:** Splittable word (rejoins to valid word 'subdistinguished')
* **Chapter:** *Chapter 5 - the Continuation of Justification*
* **Contexts:**
  * ... t that either of these should, on any account, be **sub-distinguished** into a first and second of the same kind, — that ...

### 5. `non-imputation`
* **Description:** Splittable word (rejoins to valid word 'nonimputation')
* **Chapter:** *Chapter 7 - Imputation, & the Nature of It*
* **Contexts:**
  * ... ation, or, that our justification consists in the **non-imputation** of sin, and the imputation of righteousness. But ...
  * ... tation, in both branches of it, — negative in the **non-imputation** of sin, and positive in the imputation of righteo ...

### 6. `non-solvent`
* **Description:** Splittable word (rejoins to valid word 'nonsolvent')
* **Chapter:** *Chapter 8 - Imputation of the Sins of the Church Unto Christ*
* **Contexts:**
  * ... noxius", — liable to payments for others that are **non-solvent**. 2. God can, therefore, have no surety properly, ...

### 7. `blood-guiltiness`
* **Description:** Splittable word (rejoins to valid word 'bloodguiltiness')
* **Chapter:** *Chapter 8 - Imputation of the Sins of the Church Unto Christ*
* **Contexts:**
  * ... ver me" מִדָּמִים, "from blood"; which we render "**blood-guiltiness**," Psalm 51:14. And this was because, by the const ...

### 8. `non-imputation`
* **Description:** Splittable word (rejoins to valid word 'nonimputation')
* **Chapter:** *Chapter 8 - Imputation of the Sins of the Church Unto Christ*
* **Contexts:**
  * ... tever be imputed unto them. And where that is, no **non-imputation** of sin, as unto punishment, can free the person i ...
  * ... y he escaped present punishment, yet did not that **non-imputation** free him formally from being a sinner. Wherefore ...

### 9. `non-imputation`
* **Description:** Splittable word (rejoins to valid word 'nonimputation')
* **Chapter:** *Chapter 18 - the Nature of Justification*
* **Contexts:**
  * ... , in that the imputation of righteousness and the **non-imputation** of sin (both which the apostle mentions distinctl ...

### 10. `co-interest`
* **Description:** Splittable word (rejoins to valid word 'cointerest')
* **Chapter:** *Chapter 18 - the Nature of Justification*
* **Contexts:**
  * ... heir merit, as inconsistent with grace, but their **co-interest** on our part with, or subsequent interest unto fai ...

---

## Punctuation Spacing Blemishes

### 1. `Answer .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 3 - the Use of Faith in Justification*
* **Contexts:**
  * ... d what belongs thereunto, or is derived from it. **Answer .** This exception derives from that common objection ...

### 2. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 4 - of Justification*
* **Contexts:**
  * ... merely to be freed from the punishment of sin." **Ans .** 1. All these reasons prove not that it is the sam ...

### 3. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 12 - the Imputation of the Obedience of Christ*
* **Contexts:**
  * ... in the ensuing discourse, or answered elsewhere. **Ans .** This cause is of more importance, and more eviden ...

### 4. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 18 - the Nature of Justification*
* **Contexts:**
  * **..**. non sumus justi effecti per sanctam vitam Christi**..**Item, Christus mortuus est ut justitiam illam Dei **..**.

---

## OCR & Bracket Residues

### 1. `cap. l`
* **Description:** Stray lowercase 'l' following citation abbreviation 'cap' (likely typo for '1' or 'i')
* **Chapter:** *Chapter 19 - Objections Against the Doctrine of Justification*
* **Contexts:**
  * ... rine of the Reformed churches, De Servat. par. 4, **cap. l**; and he made it the foundation whereon, and the r ...

---

## Mixed-Case Capitalization Errors

No anomalies found in this category.

## Unresolved Citation References

### 1. `Epist. 2, 29`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 4 - of Justification*
* **Contexts:**
  * ... r author) but by him. And he uses it expressly, 1 **Epist. 2, 29**, and chap. 3, 7, where these words, Ο ποιῶν δικαι ...

### 2. `lib. 4`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 8 - Imputation of the Sins of the Church Unto Christ*
* **Contexts:**
  * ... gissent, alienae culpae rei trucidarentur", B.P., **lib. 4** 22; — should be guilty of the fault of another ( ...

---

## Structural Nesting Sequence Jumps

### 1. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Chapter 3 - the Use of Faith in Justification*
* **Contexts:**
  * ... ξ ἀκοῆς πίστεως are directly opposed, Galatians 3:**2.** But when it is said that a man is not justified ἐ ...
  * ... — itself being the formal object of its assent. **2.** We cannot so receive Christ in the promise, as in ...
  * ... their faith in their justification before God. (**2.**) The Scripture plainly declares that faith as jus ...

### 2. `5. ... 7.`
* **Description:** List sequence jump (skipped from 5 to 7)
* **Chapter:** *Chapter 11 - the Nature of the Obedience That God Requires*
* **Contexts:**

### 3. `3. ... 5.`
* **Description:** List sequence jump (skipped from 3 to 5)
* **Chapter:** *Chapter 12 - the Imputation of the Obedience of Christ*
* **Contexts:**

### 4. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 20 - Doctrine of the Apostle James Concerning Faith*
* **Contexts:**

---

## Invalid Bible References

### 1. `John 22`
* **Description:** Invalid Bible reference (chapter 22 exceeds max 21 for John)
* **Chapter:** *General Considerations,*
* **Contexts:**
  * ... elieve that Jesus is the Christ, the Son of God," **John 22**:30, 31. Unto this end every thing is recorded by ...

### 2. `Philippians 26`
* **Description:** Invalid Bible reference (chapter 26 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 12 - the Imputation of the Obedience of Christ*
* **Contexts:**
  * ... ajestical exaltation, as the Scripture witnesses, **Philippians 26**:9 2:9; Luke 24:26; Romans 14:9; yet absolutely hi ...

### 3. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 12 - the Imputation of the Obedience of Christ*
* **Contexts:**
  * ... , as it is asserted by the apostle, Hebrews 2:14; **Philippians 14**:5 2:5-8. Some of the ancient schoolmen disputed, ...

### 4. `Philippians 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 12 - the Imputation of the Obedience of Christ*
* **Contexts:**
  * ... pect unto his antecedent obedience and suffering, **Philippians 23**:8 2:8,9. The actual possession of this glory was, ...
  * ... bedient unto death, even the death of the cross," **Philippians 23**:8 2:8. But yet there is herein no color of probab ...

### 5. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 12 - the Imputation of the Obedience of Christ*
* **Contexts:**
  * ... pecial dispensation and condescension, expressed, **Philippians 17**:6 2:6-8, — the obedience he yielded thereon was f ...

### 6. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 18 - the Nature of Justification*
* **Contexts:**
  * ... this purpose, 2 Corinthians 8:9; Galatians 2:20; **Philippians 17**:6 2:6,7; Revelation 1:5, 6. And those also are mo ...

---

## List Formatting Inconsistencies

No anomalies found in this category.

## Unmatched Quotation Marks

### 1. `1. The first inquiry in this matter, in a way of duty, is after the proper relief of the conscience of a sinner pressed ...`
* **Description:** Paragraph has unmatched double quotes (count: 19)
* **Chapter:** *General Considerations,*
* **Contexts:**
  * **1. The first inquiry in this matter, in a way of duty, is after the proper relief of the conscience of a sinner pressed ...**

### 2. `[[BLOCKQUOTE]] "Credisne te non posse salvari nisi per mortem Christi? Respondet infirmus, 'Etiam". Tum dicit illi, Age ...`
* **Description:** Paragraph has unmatched double quotes (count: 3)
* **Chapter:** *General Considerations,*
* **Contexts:**
  * **[[BLOCKQUOTE]] "Credisne te non posse salvari nisi per mortem Christi? Respondet infirmus, 'Etiam". Tum dicit illi, Age ...**

### 3. `Isaiah 13:6, 7; — "When the day of judgment or of death shall come, all hands will be dissolved" (that is, faint or fall...`
* **Description:** Paragraph has unmatched double quotes (count: 7)
* **Chapter:** *General Considerations,*
* **Contexts:**
  * **Isaiah 13:6, 7; — "When the day of judgment or of death shall come, all hands will be dissolved" (that is, faint or fall...**

### 4. `The excellent words of Justin Martyr deserve the first place: Αὑτὸς τὸν ἴδιον υἱὸν ἀπέδοτο λύτρον ὑπέρ ἡμῶν, τὸν ἅγιον ὑ...`
* **Description:** Paragraph has unmatched double quotes (count: 19)
* **Chapter:** *General Considerations,*
* **Contexts:**
  * **The excellent words of Justin Martyr deserve the first place: Αὑτὸς τὸν ἴδιον υἱὸν ἀπέδοτο λύτρον ὑπέρ ἡμῶν, τὸν ἅγιον ὑ...**

### 5. `A full comprehension of it no creature can in this world arise unto. Only, in the contemplation of faith, we may arrive ...`
* **Description:** Paragraph has unmatched double quotes (count: 3)
* **Chapter:** *General Considerations,*
* **Contexts:**
  * **A full comprehension of it no creature can in this world arise unto. Only, in the contemplation of faith, we may arrive ...**

### 6. `But the true and genuine signification of these words is to be determined from those in the original languages of the Sc...`
* **Description:** Paragraph has unmatched double quotes (count: 5)
* **Chapter:** *Chapter 4 - of Justification*
* **Contexts:**
  * **But the true and genuine signification of these words is to be determined from those in the original languages of the Sc...**

### 7. `3. "Ex injuria; or,`
* **Description:** Paragraph has unmatched double quotes (count: 1)
* **Chapter:** *Chapter 7 - Imputation, & the Nature of It*
* **Contexts:**
  * **3. "Ex injuria; or,**

### 8. `(1.) "Injuriarum," of wrongs: Εἰ δέ τι ἡδίκησέ σε? — If he has dealt unjustly with thee, or by thee, if he has so wronge...`
* **Description:** Paragraph has unmatched double quotes (count: 3)
* **Chapter:** *Chapter 7 - Imputation, & the Nature of It*
* **Contexts:**
  * **(1.) "Injuriarum," of wrongs: Εἰ δέ τι ἡδίκησέ σε? — If he has dealt unjustly with thee, or by thee, if he has so wronge...**

### 9. `In this state the apostle interposes himself by a voluntary sponsion, to undertake for Onesimus: "I Paul have written it...`
* **Description:** Paragraph has unmatched double quotes (count: 9)
* **Chapter:** *Chapter 7 - Imputation, & the Nature of It*
* **Contexts:**
  * **In this state the apostle interposes himself by a voluntary sponsion, to undertake for Onesimus: "I Paul have written it...**

### 10. `(1.) The Lord Christ, our mediator and surety, was, in his human nature, made ὑπὸ νόμον, — "under the law," Galatians 4:...`
* **Description:** Paragraph has unmatched double quotes (count: 9)
* **Chapter:** *Chapter 12 - the Imputation of the Obedience of Christ*
* **Contexts:**
  * **(1.) The Lord Christ, our mediator and surety, was, in his human nature, made ὑπὸ νόμον, — "under the law," Galatians 4:...**

### 11. `We shall take our fourth argument from the express exclusion of all works, of what sort soever, from our justification b...`
* **Description:** Paragraph has unmatched double quotes (count: 11)
* **Chapter:** *Chapter 14 - the Exclusion of All Sorts of Works*
* **Contexts:**
  * **We shall take our fourth argument from the express exclusion of all works, of what sort soever, from our justification b...**

### 12. `(3.) Works of the law originally included no merit, as that which "ariseth from the proportion of one thing unto another...`
* **Description:** Paragraph has unmatched double quotes (count: 1)
* **Chapter:** *Chapter 14 - the Exclusion of All Sorts of Works*
* **Contexts:**
  * **(3.) Works of the law originally included no merit, as that which "ariseth from the proportion of one thing unto another...**

### 13. `[[BLOCKQUOTE]] "Si obedientia vitae Christi nobis ad justitiam imputaretur, non fuit opus Christum pro nobis mori; mori ...`
* **Description:** Paragraph has unmatched double quotes (count: 1)
* **Chapter:** *Chapter 18 - the Nature of Justification*
* **Contexts:**
  * **[[BLOCKQUOTE]] "Si obedientia vitae Christi nobis ad justitiam imputaretur, non fuit opus Christum pro nobis mori; mori ...**

### 14. `injustus", 1 Peter 3:18. " Quod si ergo justi effecti sumus per vitam illius, causa nulla relicta fuit cur pro nobis mor...`
* **Description:** Paragraph has unmatched double quotes (count: 5)
* **Chapter:** *Chapter 18 - the Nature of Justification*
* **Contexts:**
  * **injustus", 1 Peter 3:18. " Quod si ergo justi effecti sumus per vitam illius, causa nulla relicta fuit cur pro nobis mor...**

### 15. `This treatise, entitled Gospel Grounds and Evidences of the Faith of God's Elect," was given to the world in 1695. The r...`
* **Description:** Paragraph has unmatched double quotes (count: 7)
* **Chapter:** *Prefatory Note (Evidences of the Faith of God's Elect)*
* **Contexts:**
  * **This treatise, entitled Gospel Grounds and Evidences of the Faith of God's Elect," was given to the world in 1695. The r...**

---

