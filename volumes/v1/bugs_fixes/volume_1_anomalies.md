# Text Integrity & Anomaly Audit Report: Volume 1

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 243048
* **Total Suspected Anomalies Found:** 45

Add corrections to `text_replacements` inside `volumes/v1/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 13 items
* **Punctuation Spacing Blemishes:** 25 items
* **OCR & Bracket Residues:** 2 items
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

### 1. `first  .`
* **Description:** Spaced period (space before period)
* **Chapter:** *General Preface.*
* **Contexts:**
  * ... ion in the numerals — I, 1, (1), [1], first, and first . It would have been an advantage if we could have ...

### 2. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 7 - Power and Efficacy Communicated Unto the Office of Christ*
* **Contexts:**
  * ... benefit and comfort of divine light or truth — **1st ,** The fullness of its revelation; 2ndly , The infa ...
  * ... rance in the faith of it, or obedience unto it. **1st ,** Full it must be, to free us from all attempt of f ...

### 3. `2ndly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 7 - Power and Efficacy Communicated Unto the Office of Christ*
* **Contexts:**
  * ... truth — 1st , The fullness of its revelation; **2ndly ,** The infallibility of it; and, 3rdly , The author ...
  * ... either does nor can know, because not revealed. **2ndly ,** And it must be infallible also. For this divine t ...

### 4. `3rdly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 7 - Power and Efficacy Communicated Unto the Office of Christ*
* **Contexts:**
  * ... velation; 2ndly , The infallibility of it; and, **3rdly ,** The authority from whence it does proceed. If ei ...
  * ... with him as to instruction in the mind of God. **3rdly ,** It was requisite unto the office of this great pr ...

### 5. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 9 - Honor Due to the Person of Christ*
* **Contexts:**
  * ... ather, and jointly with him. And he is proposed, **1st ,** As having fulfilled the work of his mediation in ...
  * ... ration is described to consist in three things. **1st ,** Solemn prostration: "And the four living creature ...

### 6. `2ndly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 9 - Honor Due to the Person of Christ*
* **Contexts:**
  * ... his incarnation and oblation — as a Lamb slain. **2ndly ,** In his glorious exaltation — "in the midst of the ...
  * ... ever." So also is it described, chap. 4:10, 11. **2ndly ,** In the ascription of all divine honor and glory, ...
  * ... ercised unto this worship of him here on earth. **2ndly ,** Invocation is the second general branch of divine ...

### 7. `3rdly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 9 - Honor Due to the Person of Christ*
* **Contexts:**
  * ... glory, as is at large expressed, chap. 5:11-13. **3rdly ,** In the way of expressing the design of their soul ...

### 8. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 9 - Honor Due to the Person of Christ*
* **Contexts:**
  * ... ed in the duty of invocation or prayer unto him? **Ans .** 1. There is no precedent nor example of any suc ...

### 9. `2ndly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 10 - the Principle of the Assignation of Divine Honor Unto the Person of Christ*
* **Contexts:**
  * ... ve them all unto us, or that prayer is in vain. **2ndly ,** Again, that we are baptized into the name of Jesu ...
  * ... aith of them who believe not his divine person. **2ndly ,** There is no derogation from the honor and glory o ...

### 10. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 10 - the Principle of the Assignation of Divine Honor Unto the Person of Christ*
* **Contexts:**
  * ... he formal reason and only ground of divine faith **1st ,** That the Lord Christ is not the absolute and ulti ...

### 11. `3rdly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 10 - the Principle of the Assignation of Divine Honor Unto the Person of Christ*
* **Contexts:**
  * ... h the Son, he therein honoreth the Father also. **3rdly ,** Hence it appears what is that especial acting of ...

### 12. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 15 - Conformity Unto Christ*
* **Contexts:**
  * ... these things belongs unto these three heads: — **1st ,** A declaration that all these things are wrought i ...

### 13. `2ndly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 15 - Conformity Unto Christ*
* **Contexts:**
  * ... to give repentance and the forgiveness of sins. **2ndly ,** A declaration of the way and manner how believers ...

### 14. `3rdly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 15 - Conformity Unto Christ*
* **Contexts:**
  * ... ecome the fullness of him who fills all in all. **3rdly ,** A conviction that a real interest in, and partici ...

### 15. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Chapter 16 - an Humble Inquiry Into, and Prospect Of, the Infinite Wisdom of God*
* **Contexts:**
  * ... o obnoxious unto the curse by its sin and apostasy**,,** that it was not reparable to the glory of God; an ...

### 16. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 18 - the Nature of the Person of Christ*
* **Contexts:**
  * ... e seems to be an agreement between them. For, — **1st ,** The soul and body are so united as to constitute ...

### 17. `2ndly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 18 - the Nature of the Person of Christ*
* **Contexts:**
  * ... same perfect, complete nature after this union. **2ndly ,** The union of the soul and body doth constitute th ...

### 18. `3rdly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 18 - the Nature of the Person of Christ*
* **Contexts:**
  * ... tself to be its own, into personal subsistence. **3rdly ,** Soul and body are united by an external efficient ...

### 19. `4thly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 18 - the Nature of the Person of Christ*
* **Contexts:**
  * ... wards the human which we have before described. **4thly ,** Neither soul nor body have any personal subsisten ...

### 20. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 20 - the Exercise of the Mediatory Office of Christ in Heaven*
* **Contexts:**
  * ... son and thing in its proper place and exercise. **1st ,** Heaven itself is a temple, a sanctuary, made so b ...
  * ... t shall be far better, Philippians 1:23. For, — **1st ,** although service here below shall cease, and be g ...
  * ... e earth, and that, among others, in two things. **1st ,** For the encouragement of their faith. God could, ...

### 21. `2ndly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 20 - the Exercise of the Mediatory Office of Christ in Heaven*
* **Contexts:**
  * ... f Christ in the tabernacle of his human nature. **2ndly ,** God is on the throne of grace, gloriously exalted ...
  * ... ice itself, it is an inconceivable advancement. **2ndly ,** The enjoyment of Christ in and by the ordinances ...
  * ... th himself unto our faith, Revelation 1:17, 18. **2ndly ,** That our faith may be guided and directed in all ...

### 22. `3rdly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 20 - the Exercise of the Mediatory Office of Christ in Heaven*
* **Contexts:**
  * ... mmunications of grace and mercy through Christ. **3rdly ,** The Lord Christ, in his human nature, is before t ...
  * ... d himself, and will manifest himself in Christ. **3rdly ,** The person of Christ, and therein his human natur ...

### 23. `4thly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 20 - the Exercise of the Mediatory Office of Christ in Heaven*
* **Contexts:**
  * ... atory office and power in behalf of the church. **4thly ,** All the holy angels, in the various orders and de ...

### 24. `5thly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 20 - the Exercise of the Mediatory Office of Christ in Heaven*
* **Contexts:**
  * ... tration, are about the throne continually. So — **5thly ,** Are the spirits of just men made perfect, in the ...

### 25. `2 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Lesser Catechism*
* **Contexts:**
  * ... repentance also, and holiness. — Chapter 20. Q. **2 .** What is repentance? A. A forsaking of all sin, ...

---

## OCR & Bracket Residues

### 1. `fulfil1ing`
* **Description:** Spliced alphanumeric word (contains inline numbers)
* **Chapter:** *Chapter 8 - Representations of the Glory of Christ Under the Old Testament.*
* **Contexts:**
  * ... erity of the curse wherewith it was attended; his **fulfil1ing** of it was life, by the pardon and righteousness w ...

### 2. `sou1s`
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

