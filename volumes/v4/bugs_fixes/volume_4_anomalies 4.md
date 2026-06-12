# Text Integrity & Anomaly Audit Report: Volume 4

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 261905
* **Total Suspected Anomalies Found:** 109

Add corrections to `text_replacements` inside `volumes/v4/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 16 items
* **Punctuation Spacing Blemishes:** 51 items
* **OCR & Bracket Residues:** 0 items
* **Mixed-Case Capitalization Errors:** 0 items
* **Unresolved Citation References:** 8 items
* **Structural Nesting Sequence Jumps:** 27 items
* **Invalid Bible References:** 7 items
* **List Formatting Inconsistencies:** 0 items

---

## Hyphenation Anomalies

### 1. `day-star`
* **Description:** Splittable word (rejoins to valid word 'daystar')
* **Chapter:** *Chapter 3 - Convincing Arguments for Divine Revelation*
* **Contexts:**
  * ... neth in a dark place, until the day dawn, and the **day-star** arise in your hearts: knowing this first, that no ...

### 2. `com-prebends`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 4 - Moral Certainty*
* **Contexts:**
  * ... t oftentimes shines in darkness, but the darkness **com-prebends** it not. But this neither is nor can be the formal ...

### 3. `day-star`
* **Description:** Splittable word (rejoins to valid word 'daystar')
* **Chapter:** *Chapter 5 - Divine Revelation Itself the Only Foundation*
* **Contexts:**
  * ... neth in a dark place, until the day dawn, and the **day-star** arise in your hearts: knowing this first, that no ...

### 4. `hac-tenus`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Appendix.*
* **Contexts:**
  * ... ecipue quidem propter nullum argumentum, quod vel **hac-tenus** fecimus vel ratione similiter excogitari possit, ...

### 5. `pre-required`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Preface*
* **Contexts:**
  * ... d of God," with that faith which is our duty, and **pre-required** unto all other acceptable obedience. But although ...

### 6. `pre-imbibed`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 5 - Causes of the ignorance of the mind of God revealed in the Scripture, and of error...*
* **Contexts:**
  * ... gness to hear him. But if men will not forego all **pre-imbibed** opinions, prejudices, and conceptions of mind, ho ...

### 7. `Prayer-books`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Preface*
* **Contexts:**
  * ... that the Christians received their Tephilloth, or **Prayer-books**, from Armillus, — that is, Antichrist. It is tru ...

### 8. `limi-rations`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 4 - the Nature of Prayer*
* **Contexts:**
  * ... ed the supply of it, in such a way and under such **limi-rations** as may make it good and useful unto us; and there ...

### 9. `evil-doer`
* **Description:** Splittable word (rejoins to valid word 'evildoer')
* **Chapter:** *Chapter 1 - The Holy Ghost the comforter of the church by way of office — How he is the church...*
* **Contexts:**
  * ... advocate. Christ was looked on by the world as an **evil-doer**; accused to be a glutton, a wine-bibber, a sediti ...

### 10. `wine-bibber`
* **Description:** Splittable word (rejoins to valid word 'winebibber')
* **Chapter:** *Chapter 1 - The Holy Ghost the comforter of the church by way of office — How he is the church...*
* **Contexts:**
  * ... world as an evil-doer; accused to be a glutton, a **wine-bibber**, a seditious person, a seducer, a blasphemer, a m ...

### 11. `eye-salve`
* **Description:** Splittable word (rejoins to valid word 'eyesalve')
* **Chapter:** *Chapter 5 - Particular Actings of the Holy Spirit As A Comforter*
* **Contexts:**
  * ... ed the [[BLOCKQUOTE]] "anointing of our eyes with **eye-salve** that we may see," Revelation 3:18. So doth it an ...

### 12. `safe-keeping`
* **Description:** Splittable word (rejoins to valid word 'safekeeping')
* **Chapter:** *Chapter 6 - the Spirit a Seal, and How.*
* **Contexts:**
  * ... es, that are said to be sealed. 2. It is for the **safe-keeping** or preservation of that which a seal is set upon. ...

### 13. `co-heirs`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 7 - the Spirit an Earnest, and How.*
* **Contexts:**
  * ... he giving of his Spirit unto us, God making of us **co-heirs** with Christ, we have the greatest and most assure ...
  * ... t of the Spirit" given unto us, whereby we become **co-heirs** with Christ, whose Spirit we are made partakers o ...
  * ... n of the same Spirit from him and by him makes us **co-heirs** with him; and so he is an earnest given us of God ...

### 14. `over-earnestly`
* **Description:** Splittable word (rejoins to valid word 'overearnestly')
* **Chapter:** *Chapter 3 - of Gifts and Offices Extraordinary*
* **Contexts:**
  * ... orm some parts of it, so it may be very few would **over-earnestly** press after a participation of their office; for ...

### 15. `ma-nagery`
* **Description:** Splittable word (rejoins to valid word 'managery')
* **Chapter:** *Chapter 3 - of Gifts and Offices Extraordinary*
* **Contexts:**
  * ... only their power and authority, in a new kind of **ma-nagery**, many would willingly possess themselves of. (2. ...

### 16. `child-like`
* **Description:** Splittable word (rejoins to valid word 'childlike')
* **Chapter:** *Chapter 6 - of Ordinary Gifts of the Spirit*
* **Contexts:**
  * ... [2.] The means hereof is our deliverance out of a **child-like** state, accompanied with, — 1st. Weakness; 2dly.. ...

---

## Punctuation Spacing Blemishes

### 1. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Preface*
* **Contexts:**
  * ... out them, — not for want of a due assent unto them**,,** but of a right understanding what is the true and ...

### 2. `sense ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter I - the Subject Stated - Preliminary Remarks.*
* **Contexts:**
  * ... y, that it was an evidence unto faith, and not to **sense ;** as is that also which we have now by the Scriptur ...

### 3. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Chapter I - the Subject Stated - Preliminary Remarks.*
* **Contexts:**
  * ... ged that the Bible is, as a sufficient and perfect**,,** so the only treasury of divine revelations; and w ...

### 4. `1 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 3 - Convincing Arguments for Divine Revelation*
* **Contexts:**
  * ... t be deceived. Two things are replied hereunto: — **1 .** "That where the things believed are divine and su ...

### 5. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 3 - Convincing Arguments for Divine Revelation*
* **Contexts:**
  * **..**. ism, are forced to retreat unto for shelter. 2dly**..** Their style or manner of writing deserves a pecul **..**.

### 6. `afflatus ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 4 - Moral Certainty*
* **Contexts:**
  * ... elation, consisted in an immediate inspiration or **afflatus ,** or in visions and voices from heaven, with a powe ...

### 7. `same ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 4 - Moral Certainty*
* **Contexts:**
  * ... ct of faith, or reason whereon we believe, is the **same ,** and common unto all that do believe; for our inqu ...

### 8. `disappear .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 6 - the Nature of Divine Revelations*
* **Contexts:**
  * ... fancied unto themselves in the dark to vanish and **disappear .** Digitus Dei!—this is none other but the power of ...

### 9. `inspired ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 7 - Inferences From the Whole*
* **Contexts:**
  * ... by writings that were not divinely and infallibly **inspired ;** and so might the doctrine of Christ have been, bu ...

### 10. `grace .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 7 - Inferences From the Whole*
* **Contexts:**
  * ... h we have no power to answer but by virtue of his **grace .** 4. Where the proposal of the Scripture is made i ...

### 11. `enthusiasm ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 1 - Usurpation of the church of Rome with reference unto the interpretation of the Scr...*
* **Contexts:**
  * ... s not resolved into, any immediate inspiration or **enthusiasm ;** it doth not depend upon nor is resolved into the ...

### 12. `him ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 3 - Other testimonies pleaded in confirmation of the same truth — John 16:13 opened — ...*
* **Contexts:**
  * ... sed is, our abiding in Christ: "Ye shall abide in **him ;**" which the apostle expresseth, [1 John 2:24] by " ...

### 13. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 3 - Other testimonies pleaded in confirmation of the same truth — John 16:13 opened — ...*
* **Contexts:**
  * **..**. , the other from the special design proposed. 1st**..** The general end proposed is, our abiding in Chris **..**.
  * **..**. o requireth a limitation or exposition; for, — 1st**..** It is only the things as before declared that res **..**.
  * **..**. farther ministerial teaching in the church. 2dly**..** It is spoken of the things themselves absolutely, **..**.

### 14. `ndly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 4 - The especial work of the Holy Spirit in the illumination of our minds unto the und...*
* **Contexts:**
  * ... seeing all were so, and were always to be so. [2 **ndly .**] It brings in a neglect of the Scripture, and a l ...

### 15. `thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 4 - The especial work of the Holy Spirit in the illumination of our minds unto the und...*
* **Contexts:**
  * ... tions of them that pretend unto it; and would, [4 **thly .**] thereon be a principle, first of confusion, then ...
  * ... then of infidelity, and so lead unto atheism. [5 **thly .**] The prophets themselves had not the knowledge an ...

### 16. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 4 - The especial work of the Holy Spirit in the illumination of our minds unto the und...*
* **Contexts:**
  * ... this is required of us; but the apostle adds, — **2dly .** That there must, moreover, be a divine light shin ...

### 17. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 4 - The especial work of the Holy Spirit in the illumination of our minds unto the und...*
* **Contexts:**
  * **..**. iven unto us, for so alone do we come by it. 2dly**..** It is given us. That a real and effectual communi **..**.

### 18. `2 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 5 - Causes of the ignorance of the mind of God revealed in the Scripture, and of error...*
* **Contexts:**
  * ... umination, I have elsewhere at large discoursed. **2 .** Corrupt affections prevalent in the minds of men ...

### 19. `flesh ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 6 - The work of the Holy Spirit in the composing and disposal of the Scripture as a me...*
* **Contexts:**
  * ... Word, which was God, and was with God," was "made **flesh ;**" that "God was manifest in the flesh;" that "the ...

### 20. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 6 - The work of the Holy Spirit in the composing and disposal of the Scripture as a me...*
* **Contexts:**
  * ... t confirmed elsewhere, is a dangerous curiosity. **3dly .** As to sundry prophecies of future revolutions in ...

### 21. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 6 - The work of the Holy Spirit in the composing and disposal of the Scripture as a me...*
* **Contexts:**
  * **..**. as had so much obscurity attending of them: — 1st**..** As for types, allegories, mystical stories, and o **..**.
  * **..**. erved "better things for us," [Hebrews 11:40] 2dly**..** Whatever seems yet to be continued under any obsc **..**.

### 22. `2 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 7 - Means to be used for the right understanding of the mind of God in the Scripture —...*
* **Contexts:**
  * ... Spirit in the diligent performance of this duty. **2 .** Readiness to receive impressions from divine trut ...

### 23. `3 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 7 - Means to be used for the right understanding of the mind of God in the Scripture —...*
* **Contexts:**
  * ... n hearts, we lose our principal advantage by it. **3 .** Practical obedience in the course of our walking ...

### 24. `4 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 7 - Means to be used for the right understanding of the mind of God in the Scripture —...*
* **Contexts:**
  * ... can descend into it from the fountain of truth. **4 .** A constant design for growth and a progress in kn ...

### 25. `corrupted .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... sition that the ordinal text hath been changed or **corrupted .** And the boldness of some herein is grown intolera ...

### 26. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * **..**. things to be rested on or much trusted unto. 2dly**..** That the exercise of this skill in and about the **..**.
  * **..**. ith respect unto the end aimed at. Wherefore, 3dly**..** The blessing of God on our endeavors, succeeding **..**.
  * **..**. we expect herein from the Holy Spirit. And, 4thly**..** Sundry other things are required of us, if we hop **..**.

### 27. `God ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Preface*
* **Contexts:**
  * ... to enable them to pray according unto the will of **God ;** there is no assistance promised to enable any to ...

### 28. `1 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Preface*
* **Contexts:**
  * ... ur duty herein; and they are these that follow: — **1 .** It it the duty of every man to pray for himself. ...

### 29. `4 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Preface*
* **Contexts:**
  * ... readful among the heathen," Malachi 1:8, 13, 14. **4 .** In our reasonable service, the best wherewith we ...

### 30. `5 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Preface*
* **Contexts:**
  * ... y are free from the force of this consideration. **5 .** There is no man but, in the use of the aids which ...

### 31. `6 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Preface*
* **Contexts:**
  * ... d what he is not able for he is not called unto. **6 .** We are expressly commanded to pray, but are nowhe ...

### 32. `7 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Preface*
* **Contexts:**
  * ... o the light of nature and Scripture institution. **7 .** There is assistance promised unto believers to en ...

### 33. `8 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Preface*
* **Contexts:**
  * ... they may do so in the reading of them afterward. **8 .** Whatever forms of prayer were given out unto the ...

### 34. `ceremonies .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Preface*
* **Contexts:**
  * ... ning the observance of them with sundry arbitrary **ceremonies .** And this also in the end, as is confessed among a ...

### 35. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 2 - Zechariah 12:10 Opened and Vindicated.*
* **Contexts:**
  * ... the day of Pentecost, [Acts 2:15] Acts 2:1521." **Ans .** 1. I have elsewhere already, in general, obviated ...

### 36. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 6 - the Due Manner of Prayer*
* **Contexts:**
  * ... y be so esteemed, are of another consideration." **Ans .** 1. It may be that some think so; and also, it may ...

### 37. `which ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 8 - Duty of Prayer by Virtue of a Spiritual Gift Explained*
* **Contexts:**
  * ... d in the mind into that sense and those sentences **which ,**nay be expressed; and the mind can conceive no mor ...

### 38. `1 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8 - Duty of Prayer by Virtue of a Spiritual Gift Explained*
* **Contexts:**
  * ... the truth asserted by the ensuing observations. **1 .** Every man is to pray or call upon God, according ...

### 39. `6 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8 - Duty of Prayer by Virtue of a Spiritual Gift Explained*
* **Contexts:**
  * ... be planted, it will neither thrive nor flourish. **6 .** Spiritual gifts are of two sorts: — (1.) Such as ...

### 40. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8 - Duty of Prayer by Virtue of a Spiritual Gift Explained*
* **Contexts:**
  * ... estly otherwise, and contrary to all experience. **Ans .** [1.] For the first of these inferences, I grant i ...

### 41. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 8 - Duty of Prayer by Virtue of a Spiritual Gift Explained*
* **Contexts:**
  * **..**. m him to express themselves in vocal prayer. 2dly**..** It is required hereunto that such persons be foun **..**.
  * **..**. nd helps quickly grow into disuse with them. 3dly**..** The ability which we ascribe unto all who have th **..**.

### 42. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 9 - Duties Inferred From the Preceding Discourse.*
* **Contexts:**
  * ... e to deal about between God and their own souls. **2dly .** Unto Scripture light . This is that which lively ...

### 43. `light .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 9 - Duties Inferred From the Preceding Discourse.*
* **Contexts:**
  * ... n God and their own souls. 2dly . Unto Scripture **light .** This is that which lively expresseth the spiritua ...

### 44. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 9 - Duties Inferred From the Preceding Discourse.*
* **Contexts:**
  * ... gs intended, the use of the words profiteth not. **3dly .** Unto an observation of their ways and walking, wi ...

### 45. `4thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 9 - Duties Inferred From the Preceding Discourse.*
* **Contexts:**
  * ... re to be used herein I may not here insist upon. **4thly .** Unto the account which they receive from themselv ...

### 46. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 9 - Duties Inferred From the Preceding Discourse.*
* **Contexts:**
  * **..**. ble neglect of his grace and bounty therein. 2dly**..** The increase will be added unto, by virtue of God **..**.
  * **..**. hat is spoken unless a man lift up his voice; 2dly**..** When the vehemency of affections will bear no res **..**.
  * **..**. to attend unto a fourfold direction therein: — 1st**..** Unto their own experience. If such persons are be **..**.

### 47. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 11 - Prescribed Forms of Prayer Examined.*
* **Contexts:**
  * ... a great advantage, at least unto many, in prayer. **Ans .** Whether they are approved or disapproved of God, ...

### 48. `old .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 1 - Spiritual Gifts, Their Names and Signification.*
* **Contexts:**
  * ... the new testament differenced from that under the **old .** There is, indeed, a great difference between thei ...

### 49. `4 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 4 - Extraordinary Spiritual Gifts*
* **Contexts:**
  * ... the apostles and evangelists all the world over. **4 .** The use of this gift in the church at that time a ...

### 50. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 6 - of Ordinary Gifts of the Spirit*
* **Contexts:**
  * ... that design, "They lie in wait to accomplish it;" **3dly .** The means they use to compass their end, which ar ...

### 51. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 6 - of Ordinary Gifts of the Spirit*
* **Contexts:**
  * **..**. sign of their authors, which is "to deceive;" 2dly**..** Their diligence in that design, "They lie in wait **..**.
  * **..**. ike state, accompanied with, — 1st. Weakness; 2dly**..** Instability; and, 3dly. Wilfulness. And sad is th **..**.

---

## OCR & Bracket Residues

No anomalies found in this category.

## Mixed-Case Capitalization Errors

No anomalies found in this category.

## Unresolved Citation References

### 1. `lib. 2`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 3 - Convincing Arguments for Divine Revelation*
* **Contexts:**
  * ... ropitious and succourable unto them," Antiq. Rom. **lib. 2**. The consideration hereof made them so obstinate ...

### 2. `lib. 6 cap. 3`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Appendix.*
* **Contexts:**
  * ... ns divinitus adjuvetur," De Grat. et Lib. Arbit., **lib. 6 cap. 3**; — "The arguments which render the articles of o ...

### 3. `lib. 2 cap. 8, di`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Appendix.*
* **Contexts:**
  * ... e divinely assisted. Melchior Canns, Lee. Theol., **lib. 2 cap. 8, di**sputes expressly to this purpose: [[BLOCKQUOTE]] ...

### 4. `lib. 2`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 3 - Other testimonies pleaded in confirmation of the same truth — John 16:13 opened — ...*
* **Contexts:**
  * ... pirit, and the Holy One to be the Spirit himself, **lib. 2** de Spir. Sanc. But the other interpretation is mo ...

### 5. `lib. 24 cap. 30`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 2 - Zechariah 12:10 Opened and Vindicated.*
* **Contexts:**
  * ... t such covered branches. So Livy, De Bel. Punic., **lib. 24 cap. 30**, "Ramos oleae, ac velamenta alia supplicantium po ...

### 6. `lib. 10 cap. 23`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 2 - Zechariah 12:10 Opened and Vindicated.*
* **Contexts:**
  * ... to their gods, supplicia and supplications, Liv., **lib. 10 cap. 23**, "Eo anno prodigia multa fuerunt: quorum averrunc ...

### 7. `lib. 4 chap. 3`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 5 - the Work of the Holy Spirit*
* **Contexts:**
  * ... sibi Deum. " To the same purpose speaks Damascen, **lib. 4 chap. 3**; and Austin in sundry places, collected by Beda, ...

### 8. `Epist. 1`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 2 - General Adjuncts or Properties of the Office of a Comforter*
* **Contexts:**
  * ... the "God of love and peace," 2 Corinthians 13:112 **Epist. 1**3:11. And the communication of the whole love of G ...

---

## Structural Nesting Sequence Jumps

### 1. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *The Works of John Owen Vol. 4*
* **Contexts:**

### 2. `11.`
* **Description:** List sequence starts at 11 instead of 1
* **Chapter:** *Chapter 1 - Usurpation of the church of Rome with reference unto the interpretation of the Scr...*
* **Contexts:**
  * ... do it in and by the written word, [1 Peter 1:10] **11.** II. That as to the right understanding of the mi ...

### 3. `3. ... 27.`
* **Description:** List sequence jump (skipped from 3 to 27)
* **Chapter:** *Chapter 2 - The general assertion confirmed with testimonies of the Scripture — Psalm 119:18 o...*
* **Contexts:**

### 4. `5. ... 40.`
* **Description:** List sequence jump (skipped from 5 to 40)
* **Chapter:** *Chapter 2 - The general assertion confirmed with testimonies of the Scripture — Psalm 119:18 o...*
* **Contexts:**

### 5. `2. ... 18.`
* **Description:** List sequence jump (skipped from 2 to 18)
* **Chapter:** *Chapter 4 - The especial work of the Holy Spirit in the illumination of our minds unto the und...*
* **Contexts:**

### 6. `3. ... 16.`
* **Description:** List sequence jump (skipped from 3 to 16)
* **Chapter:** *Chapter 6 - The work of the Holy Spirit in the composing and disposal of the Scripture as a me...*
* **Contexts:**

### 7. `II. ... VII.`
* **Description:** List sequence jump (skipped from 2 to 7)
* **Chapter:** *Analysis.*
* **Contexts:**

### 8. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Preface*
* **Contexts:**
  * ... e prayed unto, and that it is our duty so to do. **2.** It it the duty of some, by virtue of natural rela ...
  * ... ient to enervate all pleas for their imposition. **2.** There is a promise in the Scripture, there are ma ...

### 9. `1. ... 10.`
* **Description:** List sequence jump (skipped from 1 to 10)
* **Chapter:** *Chapter 6 - the Due Manner of Prayer*
* **Contexts:**

### 10. `10. ... 17.`
* **Description:** List sequence jump (skipped from 10 to 17)
* **Chapter:** *Chapter 6 - the Due Manner of Prayer*
* **Contexts:**

### 11. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Chapter 8 - Duty of Prayer by Virtue of a Spiritual Gift Explained*
* **Contexts:**
  * ... s instead thereof, which they do not understand? **2.** All the examples we have in the Scripture of the ...
  * ... secret guilt which it doth variously contract. (**2.**) Constant, diligent reading of the Scriptures is ...
  * ... joined unto any other gifts or graces whatever. (**2.**) Such as were adjuncts of, or annexed unto, any o ...

### 12. `II.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Prefatory Note*
* **Contexts:**
  * ... and on the Perseverance of the Saints. See vols. **II.** and XI. The discourse on Spiritual Gifts, though ...

### 13. `II. ... XI.`
* **Description:** List sequence jump (skipped from 2 to 11)
* **Chapter:** *Prefatory Note*
* **Contexts:**

### 14. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Chapter 1 - The Holy Ghost the comforter of the church by way of office — How he is the church...*
* **Contexts:**

### 15. `4. ... 9.`
* **Description:** List sequence jump (skipped from 4 to 9)
* **Chapter:** *Chapter 5 - Particular Actings of the Holy Spirit As A Comforter*
* **Contexts:**

### 16. `1. ... 18.`
* **Description:** List sequence jump (skipped from 1 to 18)
* **Chapter:** *Chapter 5 - Particular Actings of the Holy Spirit As A Comforter*
* **Contexts:**

### 17. `3. ... 28.`
* **Description:** List sequence jump (skipped from 3 to 28)
* **Chapter:** *The Application of the Foregoing Discourse.*
* **Contexts:**

### 18. `4. ... 10.`
* **Description:** List sequence jump (skipped from 4 to 10)
* **Chapter:** *Chapter 2 - Differences Between Spiritual Gifts and Saving Grace.*
* **Contexts:**

### 19. `4. ... 11.`
* **Description:** List sequence jump (skipped from 4 to 11)
* **Chapter:** *Chapter 3 - of Gifts and Offices Extraordinary*
* **Contexts:**

### 20. `3. ... 8.`
* **Description:** List sequence jump (skipped from 3 to 8)
* **Chapter:** *Chapter 3 - of Gifts and Offices Extraordinary*
* **Contexts:**

### 21. `8. ... 11.`
* **Description:** List sequence jump (skipped from 8 to 11)
* **Chapter:** *Chapter 3 - of Gifts and Offices Extraordinary*
* **Contexts:**

### 22. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Chapter 3 - of Gifts and Offices Extraordinary*
* **Contexts:**

### 23. `3. ... 15.`
* **Description:** List sequence jump (skipped from 3 to 15)
* **Chapter:** *Chapter 4 - Extraordinary Spiritual Gifts*
* **Contexts:**

### 24. `3. ... 29.`
* **Description:** List sequence jump (skipped from 3 to 29)
* **Chapter:** *Chapter 4 - Extraordinary Spiritual Gifts*
* **Contexts:**

### 25. `2. ... 17.`
* **Description:** List sequence jump (skipped from 2 to 17)
* **Chapter:** *Chapter 8 - of the Gifts of the Spirit With Respect Unto Doctrine, Worship, & Rule*
* **Contexts:**

### 26. `3. ... 17.`
* **Description:** List sequence jump (skipped from 3 to 17)
* **Chapter:** *Chapter 8 - of the Gifts of the Spirit With Respect Unto Doctrine, Worship, & Rule*
* **Contexts:**

### 27. `2. ... 13.`
* **Description:** List sequence jump (skipped from 2 to 13)
* **Chapter:** *Chapter 8 - of the Gifts of the Spirit With Respect Unto Doctrine, Worship, & Rule*
* **Contexts:**

---

## Invalid Bible References

### 1. `Jude 10`
* **Description:** Invalid Bible reference (chapter 10 exceeds max 1 for Jude)
* **Chapter:** *Chapter 6 - the Nature of Divine Revelations*
* **Contexts:**
  * ... actically complies not with what they guide unto, **Jude 10**. And so doth it assent unto many principles of re ...

### 2. `Jude 22`
* **Description:** Invalid Bible reference (chapter 22 exceeds max 1 for Jude)
* **Chapter:** *Chapter 5 - Causes of the ignorance of the mind of God revealed in the Scripture, and of error...*
* **Contexts:**
  * ... rs save with fear, pulling them out of the fire," **Jude 22**, 23. Some are so given up in their apostasy as th ...

### 3. `Philippians 26`
* **Description:** Invalid Bible reference (chapter 26 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 1 - The Holy Ghost the comforter of the church by way of office — How he is the church...*
* **Contexts:**
  * ... im, and belong unto his dominion, Ephesians 1:21; **Philippians 26**:9 2:9-11. Among them, attended with their ready s ...

### 4. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 1 - The Holy Ghost the comforter of the church by way of office — How he is the church...*
* **Contexts:**
  * ... bedient unto death, even the death of the cross," **Philippians 17**:6 2:6-8. Now, in this respect the Lord Christ an ...

### 5. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 2 - General Adjuncts or Properties of the Office of a Comforter*
* **Contexts:**
  * ... capable of. So is it represented by the apostle, **Philippians 17**:6 2:6-8: for he not only took our nature into per ...

### 6. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 6 - of Ordinary Gifts of the Spirit*
* **Contexts:**
  * ... ory authority, whereof the ministry is an effect, **Philippians 17**:6 2:6-11. And it was appointed by him to be the m ...

### 7. `Philippians 26`
* **Description:** Invalid Bible reference (chapter 26 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 7 - of Spiritual Gifts Enabling the Ministry*
* **Contexts:**
  * ... y which the Father gave him upon his exaltation, [**Philippians 26**:9] Philippians 2:9-11, joined unto "that glory wh ...

---

## List Formatting Inconsistencies

No anomalies found in this category.

