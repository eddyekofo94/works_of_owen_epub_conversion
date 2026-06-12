# Text Integrity & Anomaly Audit Report: Volume 14

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 273824
* **Total Suspected Anomalies Found:** 75

Add corrections to `text_replacements` inside `volumes/v14/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 35 items
* **Punctuation Spacing Blemishes:** 6 items
* **OCR & Bracket Residues:** 0 items
* **Mixed-Case Capitalization Errors:** 1 items
* **Unresolved Citation References:** 6 items
* **Structural Nesting Sequence Jumps:** 26 items
* **Invalid Bible References:** 1 items
* **List Formatting Inconsistencies:** 0 items

---

## Hyphenation Anomalies

### 1. `law-maker`
* **Description:** Splittable word (rejoins to valid word 'lawmaker')
* **Chapter:** *Chapter 5 - Obscurity of God, Etc.*
* **Contexts:**
  * ... know of. He proceeds: — 4. "If Christ be not our **law-maker** and director of doing well, as well as our Redeem ...
  * ... ts or Presbyterians teach that "Christ is not our **law-maker** and director of doing well," etc.? I dare say he ...

### 2. `open-hearted`
* **Description:** Splittable word (rejoins to valid word 'openhearted')
* **Chapter:** *Chapter 7 - Use of Reason.*
* **Contexts:**
  * ... men into a good humor, and, knowing them free and **open-hearted**, he plies them whilst they are warm. We have ind ...

### 3. `a-work`
* **Description:** Splittable word (rejoins to valid word 'awork')
* **Chapter:** *Chapter 9 - Protestant Pleas.*
* **Contexts:**
  * ... efense against the Presbyterians. He that set him **a-work** may pay him his wages. Protestants only tell him ...

### 4. `Ro-manists`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Chapter 13 - Popish Contradictions.*
* **Contexts:**
  * ... that no trouble ever was raised amongst us by the **Ro-manists**, here, at unawares, he informs us that his own gr ...

### 5. `top-gallant`
* **Description:** Splittable word (rejoins to valid word 'topgallant')
* **Chapter:** *Chapter 13 - Popish Contradictions.*
* **Contexts:**
  * ... uiet life; another, that they carry their top and **top-gallant** so high, that they will go to heaven without Chri ...

### 6. `sanc-tiffed`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 17 - Latin Service.*
* **Contexts:**
  * ... t make it common." To what end, I pray, hath God **sanc-tiffed** it? Is it that it may be laid up and be hid from ...

### 7. `Syro-Chaldean`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Chapter 17 - Latin Service.*
* **Contexts:**
  * ... eir people, who began to take in a mixture of the **Syro-Chaldean** language with their own, the Targums were found ...

### 8. `far-fetched`
* **Description:** Splittable word (rejoins to valid word 'farfetched')
* **Chapter:** *Chapter 18 - Communion.*
* **Contexts:**
  * ... it doth seem plainly to do; for, setting aside a **far-fetched** false notion or two about Melchizedek, and the do ...

### 9. `bed-staff`
* **Description:** Splittable word (rejoins to valid word 'bedstaff')
* **Chapter:** *Chapter 18 - Communion.*
* **Contexts:**
  * ... let such things as these down our throats, but a **bed-staff**, to cram them down, or they will choke us in the ...

### 10. `non-necessity`
* **Description:** Splittable word (rejoins to valid word 'nonnecessity')
* **Chapter:** *Chapter 18 - Communion.*
* **Contexts:**
  * ... emises, to erect his triumphant conclusion of the **non-necessity** of participation of the blessed cup by the people ...

### 11. `Peace-making`
* **Description:** Splittable word (rejoins to valid word 'Peacemaking')
* **Chapter:** *Chapter 21 - Pope.*
* **Contexts:**
  * ... e series of men going under that name. Instead of **Peace-making** and reconciliation, they tell us of fierce and cr ...

### 12. `inno-cency`
* **Description:** Splittable word (rejoins to valid word 'innocency')
* **Chapter:** *Chapter 21 - Pope.*
* **Contexts:**
  * ... eter: and whether he hath been such a defender of **inno-cency** and innocents, the day wherein God shall make inq ...

### 13. `after-game`
* **Description:** Splittable word (rejoins to valid word 'aftergame')
* **Chapter:** *Chapter 21 - Pope.*
* **Contexts:**
  * ... desired, though they were many of them wise at an **after-game**, and turned their remoteness from them into their ...

### 14. `Christian-like`
* **Description:** Splittable word (rejoins to valid word 'Christianlike')
* **Chapter:** *Chapter 1.*
* **Contexts:**
  * ... l submit; and, therefore, that it is rational and **Christian-like** to leave these endless contentions, and resign ou ...

### 15. `pre-emi`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 3.*
* **Contexts:**
  * ... aftertimes, to obviate those towering thoughts of **pre-emi**-nency which he foresaw that some men from externa ...
  * ... came unto us from Rome, you expressly adjudge the **pre-emi**nence over us unto Rome, and determine that her we ...

### 16. `Con-stantinop`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Chapter 4.*
* **Contexts:**
  * ... oncil. Antioch. can. 13 and 15, anno 341; Concil. **Con-stantinop**. can. 2, anno 381. But this canon of the Nicene ...

### 17. `irra-diatonis`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 7.*
* **Contexts:**
  * ... us; id est, inspiratio facta divinitus et divinee **irra-diatonis** influxus certus." "But whence are we persuaded th ...

### 18. `fore-named`
* **Description:** Splittable word (rejoins to valid word 'forenamed')
* **Chapter:** *Chapter 7.*
* **Contexts:**
  * ... stionable. You may at your leisure, besides those **fore-named**, consult Psalm 19:8; Isaiah 8:20; Ezekiel 36:27; ...

### 19. `wire-draw`
* **Description:** Splittable word (rejoins to valid word 'wiredraw')
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... and it brings no small gains unto you. Hence you **wire-draw** his cathedral infallibility, legislative authorit ...

### 20. `Vice-Deus`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... e Vicar of Christ, Head and Spouse of his Church, **Vice-Deus**, Deus alter in Terris," and the like, whereby you ...

### 21. `un-acquaintedness`
* **Description:** Splittable word (rejoins to valid word 'unacquaintedness')
* **Chapter:** *Chapter 11.*
* **Contexts:**
  * ... larly your assertions and inferences, or, through **un-acquaintedness** with the stories of some things that you referred ...

### 22. `un-impeached`
* **Description:** Splittable word (rejoins to valid word 'unimpeached')
* **Chapter:** *Chapter 12.*
* **Contexts:**
  * ... lst the formal reason of faith remains absolutely **un-impeached**, different apprehensions about particular things ...

### 23. `hard-hearted`
* **Description:** Splittable word (rejoins to valid word 'hardhearted')
* **Chapter:** *Chapter 12.*
* **Contexts:**
  * ... len into somewhat an unhappy age, wherein men are **hard-hearted**, and will not give away their faith and reason to ...

### 24. `over-confident`
* **Description:** Splittable word (rejoins to valid word 'overconfident')
* **Chapter:** *Chapter 13.*
* **Contexts:**
  * ... that you back your request with nothing but some **over-confident** asseverations, subscribed with "Teste meipso," I ...

### 25. `pre-eminences`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 17.*
* **Contexts:**
  * ... of your pope, with the authority, privileges, and **pre-eminences** which by virtue thereof he lays claim unto, but h ...

### 26. `transubstan-tiating`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 19.*
* **Contexts:**
  * ... in the canon of the mass immediately ensues your **transubstan-tiating** consecration before the oblation itself, and so m ...

### 27. `Bibliothe-carius`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Chapter 21.*
* **Contexts:**
  * ... umenical or Universal Patriarch; which Anastasius **Bibliothe-carius**, in his dedication of his translation of the Acts ...

### 28. `hear-say`
* **Description:** Splittable word (rejoins to valid word 'hearsay')
* **Chapter:** *Chapter 21.*
* **Contexts:**
  * ... es they talked of, so that they had them all upon **hear-say**. Acts 4:1 4. Αλλὰ, saith he, μήτις εἴτῃ τίνος ἕν ...

### 29. `Minu-tius`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Chapter 21.*
* **Contexts:**
  * ... in those days heard of in the world. Arnobius or **Minu-tius** Felix acknowledgeth the same: "Cruces nec colimus ...

### 30. `not-withstanding`
* **Description:** Splittable word (rejoins to valid word 'notwithstanding')
* **Chapter:** *Chapter 21.*
* **Contexts:**
  * ... olten statue," Judges 18:Would it not, think you, **not-withstanding** the gaiety of all this provision, have been a mad ...

### 31. `Syro-Chaldean`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Chapter 22.*
* **Contexts:**
  * ... their own tongue, and most of them understood the **Syro-Chaldean**, wherein about that time some small parts of the ...
  * ... soon as their language began to be mixed with the **Syro-Chaldean**, and the purity of it to grow into disuse, made u ...

### 32. `high-handed`
* **Description:** Splittable word (rejoins to valid word 'highhanded')
* **Chapter:** *Prefatory Note (Chapter 3 - Motive, Matter, and Method of Our Authorìs Book.)*
* **Contexts:**
  * ... rch, and more especially with the abettors of the **high-handed** measures adopted by the Court for discountenancin ...

### 33. `statesman-like`
* **Description:** Splittable word (rejoins to valid word 'statesmanlike')
* **Chapter:** *Prefatory Note (Chapter 3 - Motive, Matter, and Method of Our Authorìs Book.)*
* **Contexts:**
  * ... e calm and nervous dignity of its reasonings; the **statesman-like** view it gives of the condition and prospects of t ...

### 34. `birth-right`
* **Description:** Splittable word (rejoins to valid word 'birthright')
* **Chapter:** *The State and Fate of the Protestant Religion.*
* **Contexts:**
  * ... ountries, did secure unto them as a part of their **birth-right** inheritance. And in some places, though the name ...

### 35. `re-introduction`
* **Description:** Splittable word (rejoins to valid word 'reintroduction')
* **Chapter:** *The State and Fate of the Protestant Religion.*
* **Contexts:**
  * ... s inducements, may comply with any of them in the **re-introduction** of Popery into any of their territories, will qui ...

---

## Punctuation Spacing Blemishes

### 1. `VI .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 2 - Heathen Pleas - General Principles.*
* **Contexts:**
  * ... irect means, and entertained for sinister ends." **VI .** "That our departure from Rome hath been the cause ...

### 2. `through .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 2 - Heathen Pleas - General Principles.*
* **Contexts:**
  * ... se, being converted by their means, do afterward, **through .**the craft and subtlety of seducers, fall in sundry ...

### 3. `rule ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 6.*
* **Contexts:**
  * ... eyes also. The Scripture doth its work as a moral **rule ;** which men are not necessitated or compelled to at ...

### 4. `there ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... was at Rome; 3. That he fixed his episcopal see **there ;** — whereof the second is very questionable, the fi ...

### 5. `Secondly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 16.*
* **Contexts:**
  * ... ove him and keep his commandments, and no other. **Secondly ,** You may also as easily discern the frivolousness ...

### 6. `10 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 17.*
* **Contexts:**
  * ... d confirmed their formerly rejected pretensions. **10 .** That when they began to perceive and feel the per ...

---

## OCR & Bracket Residues

No anomalies found in this category.

## Mixed-Case Capitalization Errors

### 1. `necLatina`
* **Description:** Mixed-case capitalization error
* **Chapter:** *Chapter 7.*
* **Contexts:**
  * ... in domiclio eogitationis, nec Hebrae, nec Graeca, **necLatina**, nec barbara, veritas, sine otis et linguae organ ...

---

## Unresolved Citation References

### 1. `lib. 3`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *To the Reader (Chapter 3 - Motive, Matter, and Method of Our Authorìs Book.)*
* **Contexts:**
  * ... θέντας εῖναι ζείους λόγους, τὸ γενέσθαι αἱρέσεις, **lib. 3** Con. Cel. cap. 1; — "When many were converted unt ...

### 2. `lib. 2, cap.

7`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 4.*
* **Contexts:**
  * ... ispensably he-cessary for your defense, De Idol., lib. 2, cap. 7. St Peter, he tells us, insinuates some "worship ...

### 3. `lib. 4`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 12.*
* **Contexts:**
  * ... etter information you may do well to consult him, **lib. 4** epist. 32, 36, 38; and sundry other instances may ...

### 4. `epist. 32, 36, 38`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 12.*
* **Contexts:**
  * ... nformation you may do well to consult him, lib. 4 **epist. 32, 36, 38**; and sundry other instances may be given out of h ...

### 5. `lib. 3`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 13.*
* **Contexts:**
  * ... ing is defended by Hosius, DeAuthoritat. Script., **lib. 3**, who adds unto it of his own: "Revera nisi nos au ...

### 6. `lib. 1`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 21.*
* **Contexts:**
  * ... th the adoration of them. Theodoret. Haeret. sub. **lib. 1**, tells us that Simon Magus gave his own image and ...
  * ... to be worshipped by his followers. And Irenaeus, **lib. 1** cap. 23, that the followers of Basilides used ima ...
  * ... they adored. And so doth Epiphanius also, tom. 2 **lib. 1**, Haer. 27. Carpocrates procured the images of Chr ...

---

## Structural Nesting Sequence Jumps

### 1. `V. ... VII.`
* **Description:** List sequence jump (skipped from 5 to 7)
* **Chapter:** *Chapter 2 - Heathen Pleas - General Principles.*
* **Contexts:**

### 2. `3. ... 5.`
* **Description:** List sequence jump (skipped from 3 to 5)
* **Chapter:** *Chapter 3 - Motive, Matter, and Method of Our AuthorÌs Book.*
* **Contexts:**

### 3. `41.`
* **Description:** List sequence starts at 41 instead of 1
* **Chapter:** *Chapter 2.*
* **Contexts:**
  * ... hurch explained by Suarez, tom. 1 in Thom. 3, d. **41.** "A supernatural work," saith he, "proceeding from ...

### 4. `4.`
* **Description:** List sequence starts at 4 instead of 1
* **Chapter:** *Chapter 4.*
* **Contexts:**
  * [[CHAPTER]] CHAPTER **4.** [[SUMMARY]] Farther vindication of second chapte ...
  * ... ermines which is the heaviest, 22ae q. 94, a. ad **4.** The church in the wilderness fell by its μοσχοποι ...
  * ... ocate only him in whom we do believe," Romans 10:1**4.** It believed that the "command to abstain from me ...

### 5. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 4.*
* **Contexts:**

### 6. `3. ... 6.`
* **Description:** List sequence jump (skipped from 3 to 6)
* **Chapter:** *Chapter 4.*
* **Contexts:**

### 7. `6. ... 381.`
* **Description:** List sequence jump (skipped from 6 to 381)
* **Chapter:** *Chapter 4.*
* **Contexts:**

### 8. `4. ... 11.`
* **Description:** List sequence jump (skipped from 4 to 11)
* **Chapter:** *Chapter 4.*
* **Contexts:**

### 9. `5. ... 7.`
* **Description:** List sequence jump (skipped from 5 to 7)
* **Chapter:** *Chapter 4.*
* **Contexts:**

### 10. `7. ... 9.`
* **Description:** List sequence jump (skipped from 7 to 9)
* **Chapter:** *Chapter 4.*
* **Contexts:**

### 11. `9. ... 754.`
* **Description:** List sequence jump (skipped from 9 to 754)
* **Chapter:** *Chapter 4.*
* **Contexts:**

### 12. `6. ... 794.`
* **Description:** List sequence jump (skipped from 6 to 794)
* **Chapter:** *Chapter 4.*
* **Contexts:**

### 13. `II. ... XII.`
* **Description:** List sequence jump (skipped from 2 to 12)
* **Chapter:** *Chapter 4.*
* **Contexts:**

### 14. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Chapter 8.*
* **Contexts:**

### 15. `V. ... VII.`
* **Description:** List sequence jump (skipped from 5 to 7)
* **Chapter:** *Chapter 8.*
* **Contexts:**

### 16. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Chapter 12.*
* **Contexts:**

### 17. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 13.*
* **Contexts:**

### 18. `5. ... 9.`
* **Description:** List sequence jump (skipped from 5 to 9)
* **Chapter:** *Chapter 13.*
* **Contexts:**

### 19. `1. ... 4.`
* **Description:** List sequence jump (skipped from 1 to 4)
* **Chapter:** *Chapter 16.*
* **Contexts:**

### 20. `III.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Chapter 16.*
* **Contexts:**
  * ... 9? and whether Queen Elizabeth, King James, Henry **III.** and IV. of France, had cause to believe it? and w ...

### 21. `9. ... 11.`
* **Description:** List sequence jump (skipped from 9 to 11)
* **Chapter:** *Chapter 17.*
* **Contexts:**

### 22. `II.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Chapter 17.*
* **Contexts:**
  * ... as did one at Rome, under Otho the emperor, John X**II.**, a sweet bishop, anno 963; another at Sutrinum, a ...
  * ... ainst the usurpations and innovations of Gregory V**II.**, as at Worms, Papia, Brixia, Mentz, and elsewhere ...
  * ... is with their pope's now claimed authority. Henry **II.** of Germany both deposed popes and limited their p ...

### 23. `4. ... 490.`
* **Description:** List sequence jump (skipped from 4 to 490)
* **Chapter:** *Chapter 21.*
* **Contexts:**

### 24. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 21.*
* **Contexts:**

### 25. `2. ... 19.`
* **Description:** List sequence jump (skipped from 2 to 19)
* **Chapter:** *Chapter 21.*
* **Contexts:**

### 26. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Chapter 21.*
* **Contexts:**

---

## Invalid Bible References

### 1. `Philippians 50`
* **Description:** Invalid Bible reference (chapter 50 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 19.*
* **Contexts:**
  * ... "sacrificing," Romans 15:16; so is faith itself, **Philippians 50**:17 2:17; so prayers and thanksgiving are an oblat ...

---

## List Formatting Inconsistencies

No anomalies found in this category.

