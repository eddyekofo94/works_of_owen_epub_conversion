# Text Integrity & Anomaly Audit Report: Volume 12

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 318970
* **Total Suspected Anomalies Found:** 663

Add corrections to `text_replacements` inside `volumes/v12/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 62 items
* **Punctuation Spacing Blemishes:** 61 items
* **OCR & Bracket Residues:** 1 items
* **Mixed-Case Capitalization Errors:** 1 items
* **Unresolved Citation References:** 19 items
* **Structural Nesting Sequence Jumps:** 519 items

---

## Hyphenation Anomalies

### 1. `Wotton-under`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Prefatory Note.*
* **Contexts:**
  * ... ther of English Socinianism, was born in 1616, at **Wotton-under**-Edge. Having made considerable proficiency at the ...

### 2. `Peta-vius`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Prefatory Note.*
* **Contexts:**
  * ... nians, Arminians, and Papists. The learned Jesuit **Peta-vius** said prayers for the repose of his soul; and Boss ...

### 3. `birth-place`
* **Description:** Splittable word (rejoins to valid word 'birthplace')
* **Chapter:** *Prefatory Note.*
* **Contexts:**
  * ... ius as towns contended for the honor of being the **birth-place** of Homer. Who would not wish to rank among the ab ...

### 4. `corner-stone`
* **Description:** Splittable word (rejoins to valid word 'cornerstone')
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... nd prophets, Jesus Christ himself being the chief **corner-stone**; in whom all the building fitly framed together g ...
  * ... the work [rock?] itself, the great foundation and **corner-stone** of the church, the Lord Jesus, who is" God blesse ...

### 5. `Soci-nians`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... this great disadvantage did the persuasion of the **Soci-nians** set out in the world, that Christ is only ψιλὸς ἄ ...

### 6. `pre-existing`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... ge, though they agree not with them in allowing a **pre-existing** nature to Christ before his incarnation; but that ...

### 7. `Anti-trinitarians`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... le dealing, and after that wholly fell off to the **Anti-trinitarians**, and in the issue drowned himself in a well. An ...

### 8. `Geor-gius`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... e come off to the reformed churches; amongst whom **Geor-gius** Petrovicius, bishop of Sarmogitia, is reckoned by ...

### 9. `Cra-covia`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... dispute, and went one thousand miles (namely, to **Cra-covia** in Poland) afterward to make it good. After some ...

### 10. `So-cinus`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... escending to them on very ridiculous conditions), **So-cinus** seeming to prevail, by having most friends among ...

### 11. `by-path`
* **Description:** Splittable word (rejoins to valid word 'bypath')
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... Ahimaaz had not outrun Cushi but that he took a **by-path**. Many finding it impossible to emerge unto any co ...

### 12. `co-essential`
* **Description:** Splittable word (rejoins to valid word 'coessential')
* **Chapter:** *Mr Biddle's Preface to His Catechism.*
* **Contexts:**
  * ... he business touching the Son of God, calling him" **co-essential** with the Father," this opened a gap for others af ...

### 13. `over-strict`
* **Description:** Splittable word (rejoins to valid word 'overstrict')
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**
  * ... the church, δἰ ὀλίγην δογμάτων ἀκρίβειαν, for an **over-strict** observance of opinions, it being but one word, in ...

### 14. `good-will`
* **Description:** Splittable word (rejoins to valid word 'goodwill')
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**
  * ... d's gracious distributions of his kindness, love, **good-will** and the receiving of them. So that it be acknowle ...

### 15. `brain-sick`
* **Description:** Splittable word (rejoins to valid word 'brainsick')
* **Chapter:** *Chapter 3 - Of the drape and bodily visible figure of God.*
* **Contexts:**
  * ... siastes Hist. lib. 6:cap. 7. As this madness of **brain-sick** men was always rejected by all persons of sobriet ...

### 16. `down-sitting`
* **Description:** Splittable word (rejoins to valid word 'downsitting')
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**
  * ... of knowledge," 1 Samuel 2:3. "Thou knowest my **down-sitting** and mine uprising, thou understandest my thought ...

### 17. `to-morrow`
* **Description:** Splittable word (rejoins to valid word 'tomorrow')
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**
  * ... shall write, or ride, or speak to another person **to-morrow**, the agent being free, is contingent both as to t ...

### 18. `common-place`
* **Description:** Splittable word (rejoins to valid word 'commonplace')
* **Chapter:** *Examination.*
* **Contexts:**
  * ... t next before. It is not my purpose to handle the **common-place** of the corruption of nature by sin: nor can I say ...

### 19. `So-cinians`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Examination.*
* **Contexts:**
  * ... the reasons and causes above insisted on from the **So-cinians**, Christ be the Son of God, then Christ is the Son ...

### 20. `to-day`
* **Description:** Splittable word (rejoins to valid word 'today')
* **Chapter:** *Examination.*
* **Contexts:**
  * ... iest; but he that said unto him, Thou art my Son, **to-day** have I begotten thee." When Mr B. proves any thin ...
  * ... his Father, who said unto him, "Thou art my Son, **to-day** have I begotten thee," declaring him so to be wit ...

### 21. `to-day`
* **Description:** Splittable word (rejoins to valid word 'today')
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**
  * ... r, nor of a pre-eternal generation; for the word "**to-day**," signifying a certain time, cannot denote pre-et ...

### 22. `to-day`
* **Description:** Splittable word (rejoins to valid word 'today')
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**
  * ... another place expresses it, "The same yesterday, **to-day**, and for ever"), "the Lord God Almighty." I shal ...

### 23. `Com-plutensis`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**
  * ... , that neither in any Greek edition (but only the **Com-plutensis**) nor in the Syriac the word" God" is found But su ...

### 24. `rup-turam`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**
  * ... icari volunt Hebraei, ut per mem aperture in fine **rup-turam**." Perhaps sometimes they do so, but here some of ...

### 25. `paralo-gisms`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Examination.*
* **Contexts:**
  * ... for his own conviction and scattering of all his **paralo-gisms** and sophistical insinuations, running through the ...

### 26. `self-same`
* **Description:** Splittable word (rejoins to valid word 'selfsame')
* **Chapter:** *Examination.*
* **Contexts:**
  * ... on 2:29. And he imparts of his own fullness, "the **self-same** Spirit dividing to every man severally as he will ...

### 27. `master-piece`
* **Description:** Splittable word (rejoins to valid word 'masterpiece')
* **Chapter:** *Mr Biddle's Sixth Chapter Considered.*
* **Contexts:**
  * ... of Christ have looked upon that book as the main **master-piece** of the adversaries, and have made it their busine ...

### 28. `non-performance`
* **Description:** Splittable word (rejoins to valid word 'nonperformance')
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**
  * ... His next question, discovering the danger of the **non-performance** of this duty of yielding divine honor and worship ...
  * ... ause to exclude any from being Christians for the **non-performance** of that which himself dares not affirm that they ...

### 29. `blood-shedding`
* **Description:** Splittable word (rejoins to valid word 'bloodshedding')
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**
  * ... is not intended that faith fixes on his blood or **blood-shedding**, or on him as shedding his blood, as the prime ob ...

### 30. `in-being`
* **Description:** Splittable word (rejoins to valid word 'inbeing')
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**
  * ... on that the eternal persons have in the manner of **in-being** in the same essence, which also is the object of ...

### 31. `under-age`
* **Description:** Splittable word (rejoins to valid word 'underage')
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**
  * ... s 9:10. They served the use of that people in the **under-age** condition wherein God was pleased to keep them. ...

### 32. `to-day`
* **Description:** Splittable word (rejoins to valid word 'today')
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**
  * ... ement. This is "Jesus Christ, the same yesterday, **to-day**, and for ever." But they plead proof of Scriptur ...

### 33. `pec-catum`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**
  * ... osopher: [[BLOCKQUOTE]] "Nemo prudens punit quia **pec-catum** est, sed ne peccetur: revocari enim praeterita no ...

### 34. `intend-ment`
* **Description:** Splittable word (rejoins to valid word 'intendment')
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**
  * ... and is evil to him that is punished, — yet if the **intend-ment** of God be not to revenge the evil past upon him i ...

### 35. `pre-appointment`
* **Description:** Splittable word (rejoins to valid word 'preappointment')
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**
  * ... them, Romans 11:33-37. 2. In respect of us, this **pre-appointment** of God was an act of grace, — that is, a sovereig ...

### 36. `Soci-nians`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**
  * ... ated in the effect and evidence of it. Nor do the **Soci-nians** themselves think that this was a full accomplishm ...

### 37. `pre-tences`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**
  * ... Ezra, Abrabanel, Lipman, with what weak and mean **pre-tences**, with what inconsistency as to the words of the t ...

### 38. `nos-tro`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**
  * ... to ipse vulneratus' (id est, male tractatus est) '**nos-tro** crimine.' In nobis culpa fuit, non in ipso. Sic e ...

### 39. `by-word`
* **Description:** Splittable word (rejoins to valid word 'byword')
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**
  * ... ctors in the eye of the world, made a scorn and a **by-word**, men wagging the head and making mouths at him in ...

### 40. `in-being`
* **Description:** Splittable word (rejoins to valid word 'inbeing')
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**
  * ... punished, for, — 1st . The worm is from the **in-being** and everlasting abiding of a man's own sin. That ...

### 41. `day-time`
* **Description:** Splittable word (rejoins to valid word 'daytime')
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**
  * ... cry for a while he says, "O my God, I cry in the **day-time**, but thou hearest not," Psalm 22:2, until he give ...

### 42. `serva-vero`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**
  * ... t foede hunt porcum macto, ai pactum foederis non **serva-vero**; " whence is that phrase of one in danger, "Sto ...

### 43. `blood-shedding`
* **Description:** Splittable word (rejoins to valid word 'bloodshedding')
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**
  * ... s actually done and accomplished in the death and **blood-shedding** of Jesus Christ, Not as though we were all then a ...

### 44. `non-payment`
* **Description:** Splittable word (rejoins to valid word 'nonpayment')
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**
  * ... nsgressions." Debt makes men liable to prison for **non-payment**; and so doth sin (without satisfaction made) to t ...

### 45. `osten-deret`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**
  * ... s goes another way. Says he, "In Christo, Deus ut **osten-deret** se veracem et fidelem esse, quod significant verb ...

### 46. `blood-shedding`
* **Description:** Splittable word (rejoins to valid word 'bloodshedding')
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**
  * ... [4.] This is all the effect here assigned to the **blood-shedding** of Jesus Christ, this is the redemption we have t ...

### 47. `good-will`
* **Description:** Splittable word (rejoins to valid word 'goodwill')
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**
  * ... , yet this hinders not but that, in his sovereign **good-will** and pleasure, he might purpose to recover us from ...
  * ... reater evidence and argument of the love of God's **good-will** and pleasure in general than in sending his Son t ...

### 48. `sur-misal`
* **Description:** Splittable word (rejoins to valid word 'surmisal')
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**
  * ... ure him that he shall be saved. It is a most vain **sur-misal**, that as to that obedience which God requires of ...

### 49. `us-ward`
* **Description:** Splittable word (rejoins to valid word 'usward')
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**
  * ... d; which, as the apostle there informs us, is "to **us-ward**," — that is, to believers, of whom he is speaking ...

### 50. `to-morrow`
* **Description:** Splittable word (rejoins to valid word 'tomorrow')
* **Chapter:** *Chapter 35 - Of the resurrection of the dead and the state of the wicked at the last day.*
* **Contexts:**
  * ... ty! Will they not say, "Let us eat and drink, for **to-morrow** we shall die?" Down we lie of a season; God, it s ...
  * ... providence, if he knows not what will befall me **to-morrow**? A. What is that to me? see you to that. Q. ...

### 51. `blood-shedding`
* **Description:** Splittable word (rejoins to valid word 'bloodshedding')
* **Chapter:** *Chapter 35 - Of the resurrection of the dead and the state of the wicked at the last day.*
* **Contexts:**
  * ... o; there is no such use or fruit of his death and **blood-shedding**. Q. 29. If he neither suffered in our stead, ...

### 52. `Antino-mianism`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... t of the Papists, should himself so freely impute **Antino-mianism** to others, an opinion which he esteems as bad, if ...

### 53. `justifica-tionem`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... e Meisnerus fidem vocet cansam instrumentalem qua **justifica-tionem** (seu justitiam) apprehendamus seu recipiamus; pat ...

### 54. `im-pulsivam`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... justificationis coram Deo causam efficientem aut **im-pulsivam** esse affirmemus, sed tantummodo," etc. — Socin. J ...

### 55. `Pater-familias`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... by Cicero in secundo [libro] de Inventione, 42: "**Pater-familias** cum liberorum nihil haberet, uxorem autem haberae ...

### 56. `nut-shell`
* **Description:** Splittable word (rejoins to valid word 'nutshell')
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... ing in them, so for my part I value them not at a **nut-shell**, properly so called. This being premised, his an ...

### 57. `sub-dean`
* **Description:** Splittable word (rejoins to valid word 'subdean')
* **Chapter:** *Prefatory Note (A Review of the Annotations of Hugo Grotius)*
* **Contexts:**
  * ... ENRY HAMMOND, the chaplain of Charles I., and the **sub-dean** of Christ Church, Oxford, from which office he wa ...

### 58. `death-bed`
* **Description:** Splittable word (rejoins to valid word 'deathbed')
* **Chapter:** *Prefatory Note (A Review of the Annotations of Hugo Grotius)*
* **Contexts:**
  * ... on certain expressions which fell from him on his **death-bed**, and partly on his Scholia on the Bible. Two volu ...
  * ... sy between them; gives a different version of his **death-bed** utterances; and maintains that the posthumous Sch ...

### 59. `Crel-lius`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**
  * ... o modo auspicatus;" yet herein he goes not beyond **Crel-lius**, who tells us, "Mortem Christus subiit duplici ra ...

### 60. `co-essential`
* **Description:** Splittable word (rejoins to valid word 'coessential')
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**
  * ... lo with them, harped on, never once dreaming of a **co-essential** and hypostatical Word of God, though the word ὑπό ...

### 61. `Me-lancthon`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**
  * ... out the Trinity, from some expressions of Luther, **Me-lancthon**, Calvin, and others; but as to Calvin's expositio ...

### 62. `sup-plice`
* **Description:** Splittable word (rejoins to valid word 'supplice')
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**
  * ... eiam. Nunc quum aliud possim nihil, Dominum Jesum **sup-plice** animo veneror, ut tibl aliisque, pietatem promove ...

---

## Punctuation Spacing Blemishes

### 1. `e  )`
* **Description:** Spaced closing parenthesis
* **Chapter:** *The Heads and Governors of the Colleges and Halls,*
* **Contexts:**
  * ... art of his Annotations will not allow it to be true ), I must needs abide in my dissatisfaction as to t ...

### 2. `Christ ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... lain of the carnal apprehensions of a kingdom of **Christ ,** which too many amongst ourselves have filled thei ...

### 3. `sin ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... d obnoxious to death, that there was no original **sin ,** that Christ was not a high-priest on the earth, ...

### 4. `day ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... be utterly confined and annihilated at the last **day ,** with the rest of his opinions, which afterward he ...

### 5. `True  ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... God blessed for ever, and the Socinians tell us, "True , but he is a God by office , not by nature," i ...

### 6. `office ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**
  * ... Socinians tell us, "True , but he is a God by **office ,** not by nature," is it not lawful for us to say, ...

### 7. `Ehejeh ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**
  * ... hat God that revealed himself by Moses, Jehovah, **Ehejeh ,** it doth not appear that ever they entertained in ...

### 8. `numen ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**
  * ... ntertained in their thoughts any thing but purum **numen ,** a most simple, spiritual, eternal Being, as I sha ...

### 9. `one ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**
  * ... res, not only to be the rule, but the only **one ,** of walking with God. If you take any others into ...

### 10. `of .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**
  * ... 's being our surety, of Christ's paying our debt, **of .**our sins iraFated to Christ, of Christ's righteous ...

### 11. `s  )`
* **Description:** Spaced closing parenthesis
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**
  * ... illed sheep, and supposed they had been his enemies ), upon the account of that enmity which he finds i ...

### 12. `is  ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**
  * ... The conclusion which Mr B. guides unto from hence is , that God knew not that which he inquired after, ...

### 13. `present ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**
  * ... e of man, they conclude him not to know things **present ,** the frame of the heart of any man in the world to ...

### 14. `also  .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**
  * ... th in respect of the effect and of its causes also . Such was the soldier's piercing of the side of C ...

### 15. `dead ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Examination.*
* **Contexts:**
  * ... of the world," John 1:29. 2. In whom all are **dead ,** and in whom they have contracted the guilt of dea ...

### 16. `ante ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Examination.*
* **Contexts:**
  * ... ingly or exclusively to actual sins, not a parte **ante ,** or from the causes of it, but from its effects. T ...

### 17. `priori ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Examination.*
* **Contexts:**
  * ... titutive cause of the sonship of Jesus Christ, a **priori ,** is in his participation of the divine nature, and ...

### 18. `1  .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Examination.*
* **Contexts:**
  * ... . lays at the bottom of this appellation, are, — 1 . His birth of the Virgin, from Luke 1:30-35. 2. ...

### 19. `and .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Examination.*
* **Contexts:**
  * ... aid to be his God upon the account of his sonship **and .**personality, in which regard he hath his deity of ...

### 20. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Examination.*
* **Contexts:**
  * ... he) whereby Christ is in the Scripture κατ ἐξοχὴν**,,** called the "Son of God," is in that as man he was ...

### 21. `came ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**
  * ... said in the next verse, which expounds this, "He **came ,**εἰς τὰ ἴδια," "to his own," for then "his own," οἱ ...

### 22. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**
  * ... he Virgin; — which if it be disproved, they do not**,,** they cannot, deny but that it must be on the acco ...

### 23. `m  )`
* **Description:** Spaced closing parenthesis
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**
  * ... holar as the world enjoyed in his days from atheism ) we proceed. He that was in the beginning before ...

### 24. `disobedient .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**
  * ... d unto the spirits in prison, which sometime were **disobedient .** . . . . in the days of Noah." He who was in the d ...

### 25. `2  .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**
  * ... t describes him in his divine nature and being. 2 . To translate out of one condition into another ...

### 26. `ejus  ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 12 - All-ruling and disposing providence assigned unto Christ, and his eternal Godhead ...*
* **Contexts:**
  * ... vidisse gloriam Christi, sicut Abrahamus diem ejus ;" — "Isaiah saw his glory, as Abraham saw his da ...

### 27. `est  ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**
  * ... retation of. "He took the seed of Abraham." " Id est , Id agit ut vos Hebroaeos liberet a peccatis et ...

### 28. `death ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**
  * ... he apostle is about the undertaking of Christ by **death ,** and his being fitted thereunto by partaking of f ...

### 29. `office  .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**
  * ... ed in that and the following verses, and not his office . 2. The title given to God, whose image he is, ...

### 30. `e  )`
* **Description:** Spaced closing parenthesis
* **Chapter:** *Examination.*
* **Contexts:**
  * ... t was the opinion of some of his friends heretofore ), for "if we have not the Spirit of Christ we are ...

### 31. `heard ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**
  * ... hat it was SAID to THEM OF OLD TIME;" — "Ye have **heard ,**" not. "Ye have read." "Ye have heard it of th ...

### 32. `m  )`
* **Description:** Spaced closing parenthesis
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**
  * ... indeed, a kind of modest and subtile Mohammedanism ), of Christ's seeing God, as did Moses, seems to b ...

### 33. `confess .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**
  * ... tterly impossible and contradictory to itself. We **confess .**that there be most weighty causes why Christ shoul ...

### 34. `Ans   .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**
  * ... down on the right hand of the Majesty on high." Ans . That Christ is a high priest there also we grant ...

### 35. `were .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**
  * ... then, verse 3, that in the other tabernacle there **were .**priests that offered daily sacrifices: so that, sa ...

### 36. `1  )`
* **Description:** Spaced closing parenthesis
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**
  * ... rs after, as himself telleth us (Ep. ad Niemojev. 1 ), he wrote his answer to Volanus, wherein he confi ...

### 37. `2dly   .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**
  * ... rincipally to the person, God-man, who offered. 2dly . The free will of his human nature was in it al ...

### 38. `comeliness ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**
  * ... at Anathoth, a poor village. 'He hath no form nor **comeliness ;**' — He shall be heavy and sad. 'And when we shall ...

### 39. `the .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**
  * ... , and treading-on of every one; yet, preserved by **the .**providence of God, under whose eye and before whom ...

### 40. `t  )`
* **Description:** Spaced closing parenthesis
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**
  * ... ning his dispute with a learned Jew on that subject ), yet it appears that by this they are confessedly ...

### 41. `two .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**
  * ... s comprehending his punishment, may be considered **two .**ways: 1. In itself; 2. In reference to the law. ...

### 42. `1st   .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**
  * ... of its relation to the persons punished, for, — 1st . The worm is from the in-being and everlasting ab ...

### 43. `2dly   .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**
  * ... of God against themselves about their own sin. 2dly . That this worm never dies, that this fire can ne ...

### 44. `name .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**
  * ... give occasion of blaspheming the holy and blessed **name .**of the Son of God. Vaninus, that great atheist, w ...

### 45. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**
  * **..**. aled, though revealed in expressions of doing them**..** These things being premised, I proceed to manifes **..**.

### 46. `A   .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**
  * ... which witness that we are redeemed of Christ? A . It is hence evident that satisfaction cannot be ...

### 47. `spiritual .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**
  * ... l, temporal deliverances; which yet doth not make **spiritual .**redemption to be improper, nay, rather the other i ...

### 48. `there .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**
  * ... tention spoken of is peculiar and distinguishing, **there .**is express mention of another sort of men who are ...

### 49. `fieri  ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**
  * ... in us; or, 2. Such as mention a perfection in "fieri , " but not in "facto esse," as we speak, — a pre ...

### 50. `exact .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**
  * ... s of their best performances to the spiritual and **exact .**perfection of the law of God (things which the pro ...

### 51. `us  .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**
  * ... ie and deceive ourselves, and the truth is not in us . " He adds: — Q. Have you not examples of the ...

### 52. `law .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 35 - Of the resurrection of the dead and the state of the wicked at the last day.*
* **Contexts:**
  * ... ed in our stead, nor underwent the curse of the **law .**for us, nor satisfied justice by making reconcilia ...

### 53. `not  ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... earance, which in their own proper place they had not , or gathering up their concessions to the adversa ...

### 54. `semel ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... stification than they that say it is simul and **semel ,** or than I, whom Mr Cr. blames for it, — and so th ...

### 55. `foedere ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... can be extended unto is, that they have it ex **foedere ,** not reality, for the subject of it I place else ...

### 56. `jus ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... jus and its application. For the description of **jus ,** Mr B. relies on Grotius; and something also he me ...
  * ... nning both of the Institutions and Digests about **jus ,** and those also which they handle under the head " ...
  * ... wing what is jus in general, and what is their **jus ,** and where fixed. 2. He questions the anteceden ...

### 57. `facultas ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... right by me intended. He tells us, indeed, that **facultas ,** which the lawyers call sui , is that which prope ...

### 58. `sui ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... indeed, that facultas , which the lawyers call **sui ,** is that which properly and strictly he intends to ...

### 59. `jus  .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... t which properly and strictly he intends to call jus . But the other member of the distinction he terms ...
  * ... e justum, yet they may not be subjects of this jus . To this I have answered by showing what is jus ...

### 60. `Ans  .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... procured for us finaliter, not subjective. " Ans . They are procured for us objective, are granted ...

### 61. `necessaria  .`
* **Description:** Spaced period (space before period)
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**
  * ... bus vitam det, et quae alia ad istiusmodi labores necessaria . Mihi ad juvandam communem Christianismi causam, ...

---

## OCR & Bracket Residues

### 1. `B[AXTER`
* **Description:** OCR residue containing stray opening bracket/paren
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... ERED VINDICATED FROM THE ANIMADVERSIONS OF MR. R. **B[AXTER**.] OF this task I would complain if I durst, bu ...

---

## Mixed-Case Capitalization Errors

### 1. `iraFated`
* **Description:** Mixed-case capitalization error
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**
  * ... surety, of Christ's paying our debt, of .our sins **iraFated** to Christ, of Christ's righteousness imputed to u ...

---

## Unresolved Citation References

### 1. `lib. 1:cap. 2`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**
  * ... , verum hoc sibi placere, ut Jupiter nominetur, " **lib. 1:cap. 2**.); which, as Servius on the place observes, he ha ...

### 2. `lib. 3`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 3 - Of the drape and bodily visible figure of God.*
* **Contexts:**
  * ... om you have a large account in Epiphanius, tom. 1:**lib. 3**, Haer. 70; as also in Theodoret, Lib. 4 Ecclesias ...

### 3. `Haer. 70`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 3 - Of the drape and bodily visible figure of God.*
* **Contexts:**
  * ... ave a large account in Epiphanius, tom. 1:lib. 3, **Haer. 70**; as also in Theodoret, Lib. 4 Ecclesiastes Hist., ...

### 4. `lib. 1`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 3 - Of the drape and bodily visible figure of God.*
* **Contexts:**
  * ... a heathen, in the person of Cotta (De Nat. Deer. **lib. 1**:6), against Velleius the Epicurean, the Epicurean ...
  * ... illo nulla pars extra animum. " Natural. Quaest. **lib. 1**. Praefat. It would be burdensome, if not endless, ...

### 5. `lib. 3`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Examination.*
* **Contexts:**
  * ... t up with that distich of Greg. Naz. Sanct. Spir. **lib. 3**: — Πάντα μὲν αἰὲν ἄριστα θεοπιεπὲς ἔργα τελείσθω ...

### 6. `Ep. ad Niemojev. 1`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**
  * ... otice of. Six years after, as himself telleth us (**Ep. ad Niemojev. 1** ), he wrote his answer to Volanus, wherein he co ...

### 7. `Ep. 190`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**
  * ... into the same abomination; of whom says Bernard, **Ep. 190**, [[BLOCKQUOTE]] " Habemus in Francia novum de ve ...

### 8. `lib. 20`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**
  * ... d so is that expression explained by Ulpian, Dig. **lib. 20**: " Capitalem fraudem admittere est tale aliquid d ...

### 9. `lib. 1`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**
  * ... ption of redemption, "De Jesu Christo Servatore," **lib. 1** part. 2 cap. 1-3. To remove these difficulties ( ...
  * ... s purpose may be taken notice of, Lib. de Servat. **lib. 1** part. 2 cap. 2: — Nothing is wanting in this deli ...
  * ... ti sumus, sed gratis per gratiam Dei," De Servat. **lib. 1** part. 2 cap. 2. (2.) The end on the part of God ...

### 10. `lib. 1 cap. 1`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... this definition, as Conanus, Comment. Jur. Civil. **lib. 1 cap. 1**:That which is oequum is the subject of it. So the ...

### 11. `lib. 2 cap. i`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... tanquam comes et adjutrix," Comment. Jut. Civil. **lib. 2 cap. i**., which obligation is the foundation of action, i ...

### 12. `lib. 1`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... this definition, as Conanus, Comment. Jur. Civil. **lib. 1** cap. 1:That which is oequum is the subject of it. ...
  * ... een jus utendi, fruendi, and jus obligationis, D. **lib. 1**:1, 8, which he could not do if all and every righ ...
  * ... inions are repeated by Menochius de Arbit. Judic. **lib. 1** qu. 16, 2. And such a jus as this ariseth "ex ...

### 13. `lib. 11`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... , I question not. Again, consider that of Paulus, **lib. 11** ad Edict. D.D. de verb. signif, Titus 16: "Prince ...

### 14. `lib. 4`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... Cat. Rac. cap. 9 de fide; Volkel. de Vera Relig., **lib. 4** cap. 3 p. 179, 180; Smalc. Refut. Thes. Franz. di ...
  * ... eneficium consequamur. " — Volkel, de Vera Relig. **lib. 4** cap. 3 p. 181; Smalc. Refut. Thes. Franz. disp. 4 ...
  * ... cationis nostrae esse. " — Volkel, de Vera Relig. **lib. 4** cap. 3 p. 181. " Quod vero ad nos pertinet, non a ...

### 15. `lib. 3`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**
  * ... bono jure atque honore:" Bachid. and Paulus, in **lib. 3** ff. de servitut, urb. praed., "Ne jus sit vicino ...
  * ... that section, "Quibus modis tollitur obligatio," **lib. 3** Instit., will evince this sufficiently. The title ...

### 16. `lib. 3 cap. 15`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**
  * ... ἦ οὐ μέγα ἦ οὐκ αἰσχρὸν ἦ οὐκ ἔχον μέγεθος (Rhet. **lib. 3 cap. 15**); all which, in a plain matter of fact, may be re ...

### 17. `lib. 2 cap. 6`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**
  * ... ferre, significare," Socin. de Jes. Christ. Serv. **lib. 2 cap. 6**. What difference there is between the design of ...

### 18. `lib. 3 cap. 47`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**
  * ... entam sanguinis profusionem con-tinct," De Relig. **lib. 3 cap. 47**, p. 145. And again: "Hinc colligitur solam Christ ...

### 19. `lib. 1`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**
  * ... eak in our hearts, says Damascen. De Orthod. Fid. **lib. 1** cap 18: so Psalm 14:1, נָבָל בְּלִבּוֹ אָמַר. Thi ...

---

## Structural Nesting Sequence Jumps

### 1. `6. ... 13.`
* **Description:** List sequence jump (skipped from 6 to 13)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**

### 2. `13. ... 51.`
* **Description:** List sequence jump (skipped from 13 to 51)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**

### 3. `15. ... 366.`
* **Description:** List sequence jump (skipped from 15 to 366)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**

### 4. `49. ... 403.`
* **Description:** List sequence jump (skipped from 49 to 403)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**

### 5. `1. ... 9.`
* **Description:** List sequence jump (skipped from 1 to 9)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**

### 6. `2. ... 17.`
* **Description:** List sequence jump (skipped from 2 to 17)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**

### 7. `5. ... 28.`
* **Description:** List sequence jump (skipped from 5 to 28)
* **Chapter:** *The Preface to the Reader.*
* **Contexts:**

### 8. `4. ... 28.`
* **Description:** List sequence jump (skipped from 4 to 28)
* **Chapter:** *Mr Biddle's Preface to His Catechism.*
* **Contexts:**

### 9. `13. ... 27.`
* **Description:** List sequence jump (skipped from 13 to 27)
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**

### 10. `5. ... 14.`
* **Description:** List sequence jump (skipped from 5 to 14)
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**

### 11. `14. ... 18.`
* **Description:** List sequence jump (skipped from 14 to 18)
* **Chapter:** *Mr Biddle's Preface Briefly Examined.*
* **Contexts:**

### 12. `2. ... 6.`
* **Description:** List sequence jump (skipped from 2 to 6)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 13. `6. ... 11.`
* **Description:** List sequence jump (skipped from 6 to 11)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 14. `5. ... 11.`
* **Description:** List sequence jump (skipped from 5 to 11)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 15. `11. ... 19.`
* **Description:** List sequence jump (skipped from 11 to 19)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 16. `19. ... 200.`
* **Description:** List sequence jump (skipped from 19 to 200)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 17. `3. ... 11.`
* **Description:** List sequence jump (skipped from 3 to 11)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 18. `11. ... 27.`
* **Description:** List sequence jump (skipped from 11 to 27)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 19. `10. ... 48.`
* **Description:** List sequence jump (skipped from 10 to 48)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 20. `2. ... 11.`
* **Description:** List sequence jump (skipped from 2 to 11)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 21. `11. ... 48.`
* **Description:** List sequence jump (skipped from 11 to 48)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 22. `1. ... 4.`
* **Description:** List sequence jump (skipped from 1 to 4)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 23. `4. ... 726.`
* **Description:** List sequence jump (skipped from 4 to 726)
* **Chapter:** *Chapter 2 - Of the nature of God.*
* **Contexts:**

### 24. `2. ... 26.`
* **Description:** List sequence jump (skipped from 2 to 26)
* **Chapter:** *Chapter 3 - Of the drape and bodily visible figure of God.*
* **Contexts:**

### 25. `3. ... 23.`
* **Description:** List sequence jump (skipped from 3 to 23)
* **Chapter:** *Chapter 3 - Of the drape and bodily visible figure of God.*
* **Contexts:**

### 26. `18. ... 25.`
* **Description:** List sequence jump (skipped from 18 to 25)
* **Chapter:** *Chapter 3 - Of the drape and bodily visible figure of God.*
* **Contexts:**

### 27. `4. ... 26.`
* **Description:** List sequence jump (skipped from 4 to 26)
* **Chapter:** *Chapter 3 - Of the drape and bodily visible figure of God.*
* **Contexts:**

### 28. `1. ... 7.`
* **Description:** List sequence jump (skipped from 1 to 7)
* **Chapter:** *Chapter 3 - Of the drape and bodily visible figure of God.*
* **Contexts:**

### 29. `1. ... 17.`
* **Description:** List sequence jump (skipped from 1 to 17)
* **Chapter:** *Chapter 4 - Of the attribution of passions and affections, anger, fear, repentance, unto God —...*
* **Contexts:**

### 30. `17. ... 26.`
* **Description:** List sequence jump (skipped from 17 to 26)
* **Chapter:** *Chapter 4 - Of the attribution of passions and affections, anger, fear, repentance, unto God —...*
* **Contexts:**

### 31. `2. ... 14.`
* **Description:** List sequence jump (skipped from 2 to 14)
* **Chapter:** *Chapter 4 - Of the attribution of passions and affections, anger, fear, repentance, unto God —...*
* **Contexts:**

### 32. `4. ... 18.`
* **Description:** List sequence jump (skipped from 4 to 18)
* **Chapter:** *Chapter 4 - Of the attribution of passions and affections, anger, fear, repentance, unto God —...*
* **Contexts:**

### 33. `6. ... 27.`
* **Description:** List sequence jump (skipped from 6 to 27)
* **Chapter:** *Chapter 4 - Of the attribution of passions and affections, anger, fear, repentance, unto God —...*
* **Contexts:**

### 34. `1. ... 7.`
* **Description:** List sequence jump (skipped from 1 to 7)
* **Chapter:** *Chapter 4 - Of the attribution of passions and affections, anger, fear, repentance, unto God —...*
* **Contexts:**

### 35. `3. ... 11.`
* **Description:** List sequence jump (skipped from 3 to 11)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 36. `3. ... 6.`
* **Description:** List sequence jump (skipped from 3 to 6)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 37. `3. ... 30.`
* **Description:** List sequence jump (skipped from 3 to 30)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 38. `3. ... 5.`
* **Description:** List sequence jump (skipped from 3 to 5)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 39. `5. ... 31.`
* **Description:** List sequence jump (skipped from 5 to 31)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 40. `3. ... 23.`
* **Description:** List sequence jump (skipped from 3 to 23)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 41. `7. ... 39.`
* **Description:** List sequence jump (skipped from 7 to 39)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 42. `11. ... 20.`
* **Description:** List sequence jump (skipped from 11 to 20)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 43. `5. ... 14.`
* **Description:** List sequence jump (skipped from 5 to 14)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 44. `14. ... 28.`
* **Description:** List sequence jump (skipped from 14 to 28)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 45. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 46. `2. ... 17.`
* **Description:** List sequence jump (skipped from 2 to 17)
* **Chapter:** *Chapter 5 - Of God's prescience or foreknowledge.*
* **Contexts:**

### 47. `7. ... 19.`
* **Description:** List sequence jump (skipped from 7 to 19)
* **Chapter:** *Examination.*
* **Contexts:**

### 48. `7. ... 22.`
* **Description:** List sequence jump (skipped from 7 to 22)
* **Chapter:** *Examination.*
* **Contexts:**

### 49. `17. ... 19.`
* **Description:** List sequence jump (skipped from 17 to 19)
* **Chapter:** *Examination.*
* **Contexts:**

### 50. `2. ... 19.`
* **Description:** List sequence jump (skipped from 2 to 19)
* **Chapter:** *Examination.*
* **Contexts:**

### 51. `4. ... 15.`
* **Description:** List sequence jump (skipped from 4 to 15)
* **Chapter:** *Examination.*
* **Contexts:**

### 52. `15. ... 23.`
* **Description:** List sequence jump (skipped from 15 to 23)
* **Chapter:** *Examination.*
* **Contexts:**

### 53. `3. ... 16.`
* **Description:** List sequence jump (skipped from 3 to 16)
* **Chapter:** *Examination.*
* **Contexts:**

### 54. `1. ... 27.`
* **Description:** List sequence jump (skipped from 1 to 27)
* **Chapter:** *Examination.*
* **Contexts:**

### 55. `27. ... 31.`
* **Description:** List sequence jump (skipped from 27 to 31)
* **Chapter:** *Examination.*
* **Contexts:**

### 56. `6. ... 29.`
* **Description:** List sequence jump (skipped from 6 to 29)
* **Chapter:** *Examination.*
* **Contexts:**

### 57. `2. ... 17.`
* **Description:** List sequence jump (skipped from 2 to 17)
* **Chapter:** *Examination.*
* **Contexts:**

### 58. `12. ... 23.`
* **Description:** List sequence jump (skipped from 12 to 23)
* **Chapter:** *Examination.*
* **Contexts:**

### 59. `3. ... 23.`
* **Description:** List sequence jump (skipped from 3 to 23)
* **Chapter:** *Examination.*
* **Contexts:**

### 60. `23. ... 29.`
* **Description:** List sequence jump (skipped from 23 to 29)
* **Chapter:** *Examination.*
* **Contexts:**

### 61. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Examination.*
* **Contexts:**

### 62. `3. ... 22.`
* **Description:** List sequence jump (skipped from 3 to 22)
* **Chapter:** *Examination.*
* **Contexts:**

### 63. `3. ... 36.`
* **Description:** List sequence jump (skipped from 3 to 36)
* **Chapter:** *Examination.*
* **Contexts:**

### 64. `4. ... 14.`
* **Description:** List sequence jump (skipped from 4 to 14)
* **Chapter:** *Examination.*
* **Contexts:**

### 65. `5. ... 18.`
* **Description:** List sequence jump (skipped from 5 to 18)
* **Chapter:** *Examination.*
* **Contexts:**

### 66. `6. ... 20.`
* **Description:** List sequence jump (skipped from 6 to 20)
* **Chapter:** *Examination.*
* **Contexts:**

### 67. `5. ... 7.`
* **Description:** List sequence jump (skipped from 5 to 7)
* **Chapter:** *Examination.*
* **Contexts:**

### 68. `1. ... 21.`
* **Description:** List sequence jump (skipped from 1 to 21)
* **Chapter:** *Examination.*
* **Contexts:**

### 69. `21. ... 23.`
* **Description:** List sequence jump (skipped from 21 to 23)
* **Chapter:** *Examination.*
* **Contexts:**

### 70. `4. ... 6.`
* **Description:** List sequence jump (skipped from 4 to 6)
* **Chapter:** *Examination.*
* **Contexts:**

### 71. `6. ... 12.`
* **Description:** List sequence jump (skipped from 6 to 12)
* **Chapter:** *Examination.*
* **Contexts:**

### 72. `7. ... 15.`
* **Description:** List sequence jump (skipped from 7 to 15)
* **Chapter:** *Examination.*
* **Contexts:**

### 73. `1. ... 23.`
* **Description:** List sequence jump (skipped from 1 to 23)
* **Chapter:** *Examination.*
* **Contexts:**

### 74. `2. ... 44.`
* **Description:** List sequence jump (skipped from 2 to 44)
* **Chapter:** *Examination.*
* **Contexts:**

### 75. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Examination.*
* **Contexts:**

### 76. `1. ... 29.`
* **Description:** List sequence jump (skipped from 1 to 29)
* **Chapter:** *Examination.*
* **Contexts:**

### 77. `2. ... 23.`
* **Description:** List sequence jump (skipped from 2 to 23)
* **Chapter:** *Examination.*
* **Contexts:**

### 78. `4. ... 10.`
* **Description:** List sequence jump (skipped from 4 to 10)
* **Chapter:** *Examination.*
* **Contexts:**

### 79. `5. ... 16.`
* **Description:** List sequence jump (skipped from 5 to 16)
* **Chapter:** *Examination.*
* **Contexts:**

### 80. `2. ... 26.`
* **Description:** List sequence jump (skipped from 2 to 26)
* **Chapter:** *Examination.*
* **Contexts:**

### 81. `3. ... 12.`
* **Description:** List sequence jump (skipped from 3 to 12)
* **Chapter:** *Examination.*
* **Contexts:**

### 82. `2. ... 18.`
* **Description:** List sequence jump (skipped from 2 to 18)
* **Chapter:** *Examination.*
* **Contexts:**

### 83. `6. ... 35.`
* **Description:** List sequence jump (skipped from 6 to 35)
* **Chapter:** *Mr Biddle's Fourth Chapter.*
* **Contexts:**

### 84. `9. ... 36.`
* **Description:** List sequence jump (skipped from 9 to 36)
* **Chapter:** *Mr Biddle's Fourth Chapter.*
* **Contexts:**

### 85. `36. ... 38.`
* **Description:** List sequence jump (skipped from 36 to 38)
* **Chapter:** *Mr Biddle's Fourth Chapter.*
* **Contexts:**

### 86. `10. ... 29.`
* **Description:** List sequence jump (skipped from 10 to 29)
* **Chapter:** *Mr Biddle's Fourth Chapter.*
* **Contexts:**

### 87. `29. ... 36.`
* **Description:** List sequence jump (skipped from 29 to 36)
* **Chapter:** *Mr Biddle's Fourth Chapter.*
* **Contexts:**

### 88. `23. ... 28.`
* **Description:** List sequence jump (skipped from 23 to 28)
* **Chapter:** *Mr Biddle's Fourth Chapter.*
* **Contexts:**

### 89. `4. ... 9.`
* **Description:** List sequence jump (skipped from 4 to 9)
* **Chapter:** *Examination.*
* **Contexts:**

### 90. `2. ... 11.`
* **Description:** List sequence jump (skipped from 2 to 11)
* **Chapter:** *Examination.*
* **Contexts:**

### 91. `11. ... 49.`
* **Description:** List sequence jump (skipped from 11 to 49)
* **Chapter:** *Examination.*
* **Contexts:**

### 92. `6. ... 9.`
* **Description:** List sequence jump (skipped from 6 to 9)
* **Chapter:** *Examination.*
* **Contexts:**

### 93. `9. ... 35.`
* **Description:** List sequence jump (skipped from 9 to 35)
* **Chapter:** *Examination.*
* **Contexts:**

### 94. `2. ... 36.`
* **Description:** List sequence jump (skipped from 2 to 36)
* **Chapter:** *Examination.*
* **Contexts:**

### 95. `3. ... 18.`
* **Description:** List sequence jump (skipped from 3 to 18)
* **Chapter:** *Examination.*
* **Contexts:**

### 96. `4. ... 29.`
* **Description:** List sequence jump (skipped from 4 to 29)
* **Chapter:** *Examination.*
* **Contexts:**

### 97. `29. ... 35.`
* **Description:** List sequence jump (skipped from 29 to 35)
* **Chapter:** *Examination.*
* **Contexts:**

### 98. `4. ... 150.`
* **Description:** List sequence jump (skipped from 4 to 150)
* **Chapter:** *Examination.*
* **Contexts:**

### 99. `150. ... 158.`
* **Description:** List sequence jump (skipped from 150 to 158)
* **Chapter:** *Examination.*
* **Contexts:**

### 100. `1. ... 69.`
* **Description:** List sequence jump (skipped from 1 to 69)
* **Chapter:** *Examination.*
* **Contexts:**

### 101. `20. ... 32.`
* **Description:** List sequence jump (skipped from 20 to 32)
* **Chapter:** *Examination.*
* **Contexts:**

### 102. `14. ... 18.`
* **Description:** List sequence jump (skipped from 14 to 18)
* **Chapter:** *Examination.*
* **Contexts:**

### 103. `1. ... 4.`
* **Description:** List sequence jump (skipped from 1 to 4)
* **Chapter:** *Examination.*
* **Contexts:**

### 104. `6. ... 33.`
* **Description:** List sequence jump (skipped from 6 to 33)
* **Chapter:** *Examination.*
* **Contexts:**

### 105. `4. ... 7.`
* **Description:** List sequence jump (skipped from 4 to 7)
* **Chapter:** *Examination.*
* **Contexts:**

### 106. `7. ... 18.`
* **Description:** List sequence jump (skipped from 7 to 18)
* **Chapter:** *Examination.*
* **Contexts:**

### 107. `18. ... 25.`
* **Description:** List sequence jump (skipped from 18 to 25)
* **Chapter:** *Examination.*
* **Contexts:**

### 108. `25. ... 31.`
* **Description:** List sequence jump (skipped from 25 to 31)
* **Chapter:** *Examination.*
* **Contexts:**

### 109. `3. ... 15.`
* **Description:** List sequence jump (skipped from 3 to 15)
* **Chapter:** *Examination.*
* **Contexts:**

### 110. `18. ... 36.`
* **Description:** List sequence jump (skipped from 18 to 36)
* **Chapter:** *Examination.*
* **Contexts:**

### 111. `7. ... 9.`
* **Description:** List sequence jump (skipped from 7 to 9)
* **Chapter:** *Examination.*
* **Contexts:**

### 112. `2. ... 58.`
* **Description:** List sequence jump (skipped from 2 to 58)
* **Chapter:** *Examination.*
* **Contexts:**

### 113. `4. ... 35.`
* **Description:** List sequence jump (skipped from 4 to 35)
* **Chapter:** *Examination.*
* **Contexts:**

### 114. `1. ... 35.`
* **Description:** List sequence jump (skipped from 1 to 35)
* **Chapter:** *Examination.*
* **Contexts:**

### 115. `2. ... 32.`
* **Description:** List sequence jump (skipped from 2 to 32)
* **Chapter:** *Examination.*
* **Contexts:**

### 116. `28. ... 30.`
* **Description:** List sequence jump (skipped from 28 to 30)
* **Chapter:** *Examination.*
* **Contexts:**

### 117. `33. ... 39.`
* **Description:** List sequence jump (skipped from 33 to 39)
* **Chapter:** *Examination.*
* **Contexts:**

### 118. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Examination.*
* **Contexts:**

### 119. `4. ... 18.`
* **Description:** List sequence jump (skipped from 4 to 18)
* **Chapter:** *Examination.*
* **Contexts:**

### 120. `18. ... 35.`
* **Description:** List sequence jump (skipped from 18 to 35)
* **Chapter:** *Examination.*
* **Contexts:**

### 121. `6. ... 35.`
* **Description:** List sequence jump (skipped from 6 to 35)
* **Chapter:** *Examination.*
* **Contexts:**

### 122. `9. ... 17.`
* **Description:** List sequence jump (skipped from 9 to 17)
* **Chapter:** *Examination.*
* **Contexts:**

### 123. `3. ... 28.`
* **Description:** List sequence jump (skipped from 3 to 28)
* **Chapter:** *Examination.*
* **Contexts:**

### 124. `2. ... 8.`
* **Description:** List sequence jump (skipped from 2 to 8)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 125. `8. ... 17.`
* **Description:** List sequence jump (skipped from 8 to 17)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 126. `6. ... 25.`
* **Description:** List sequence jump (skipped from 6 to 25)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 127. `3. ... 23.`
* **Description:** List sequence jump (skipped from 3 to 23)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 128. `2. ... 58.`
* **Description:** List sequence jump (skipped from 2 to 58)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 129. `1. ... 14.`
* **Description:** List sequence jump (skipped from 1 to 14)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 130. `2. ... 23.`
* **Description:** List sequence jump (skipped from 2 to 23)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 131. `5. ... 12.`
* **Description:** List sequence jump (skipped from 5 to 12)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 132. `2. ... 5.`
* **Description:** List sequence jump (skipped from 2 to 5)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 133. `3. ... 24.`
* **Description:** List sequence jump (skipped from 3 to 24)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 134. `2. ... 6.`
* **Description:** List sequence jump (skipped from 2 to 6)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 135. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 136. `5. ... 21.`
* **Description:** List sequence jump (skipped from 5 to 21)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 137. `6. ... 29.`
* **Description:** List sequence jump (skipped from 6 to 29)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 138. `28. ... 67.`
* **Description:** List sequence jump (skipped from 28 to 67)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 139. `3. ... 5.`
* **Description:** List sequence jump (skipped from 3 to 5)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 140. `5. ... 58.`
* **Description:** List sequence jump (skipped from 5 to 58)
* **Chapter:** *Chapter 8 - An entrance into the examination of the Racovian Catechism in the business of the ...*
* **Contexts:**

### 141. `9. ... 23.`
* **Description:** List sequence jump (skipped from 9 to 23)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 142. `3. ... 7.`
* **Description:** List sequence jump (skipped from 3 to 7)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 143. `3. ... 9.`
* **Description:** List sequence jump (skipped from 3 to 9)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 144. `9. ... 12.`
* **Description:** List sequence jump (skipped from 9 to 12)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 145. `4. ... 17.`
* **Description:** List sequence jump (skipped from 4 to 17)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 146. `5. ... 42.`
* **Description:** List sequence jump (skipped from 5 to 42)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 147. `2. ... 33.`
* **Description:** List sequence jump (skipped from 2 to 33)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 148. `5. ... 18.`
* **Description:** List sequence jump (skipped from 5 to 18)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 149. `3. ... 8.`
* **Description:** List sequence jump (skipped from 3 to 8)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 150. `5. ... 7.`
* **Description:** List sequence jump (skipped from 5 to 7)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 151. `1. ... 30.`
* **Description:** List sequence jump (skipped from 1 to 30)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 152. `2. ... 29.`
* **Description:** List sequence jump (skipped from 2 to 29)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 153. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 154. `2. ... 17.`
* **Description:** List sequence jump (skipped from 2 to 17)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 155. `1. ... 4.`
* **Description:** List sequence jump (skipped from 1 to 4)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 156. `6. ... 16.`
* **Description:** List sequence jump (skipped from 6 to 16)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 157. `7. ... 14.`
* **Description:** List sequence jump (skipped from 7 to 14)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 158. `8. ... 47.`
* **Description:** List sequence jump (skipped from 8 to 47)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 159. `1. ... 11.`
* **Description:** List sequence jump (skipped from 1 to 11)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 160. `2. ... 9.`
* **Description:** List sequence jump (skipped from 2 to 9)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 161. `6. ... 24.`
* **Description:** List sequence jump (skipped from 6 to 24)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 162. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 163. `3. ... 6.`
* **Description:** List sequence jump (skipped from 3 to 6)
* **Chapter:** *Chapter 9 - The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated.*
* **Contexts:**

### 164. `10. ... 16.`
* **Description:** List sequence jump (skipped from 10 to 16)
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**

### 165. `3. ... 23.`
* **Description:** List sequence jump (skipped from 3 to 23)
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**

### 166. `23. ... 55.`
* **Description:** List sequence jump (skipped from 23 to 55)
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**

### 167. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**

### 168. `5. ... 30.`
* **Description:** List sequence jump (skipped from 5 to 30)
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**

### 169. `6. ... 38.`
* **Description:** List sequence jump (skipped from 6 to 38)
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**

### 170. `1. ... 18.`
* **Description:** List sequence jump (skipped from 1 to 18)
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**

### 171. `3. ... 12.`
* **Description:** List sequence jump (skipped from 3 to 12)
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**

### 172. `1. ... 456.`
* **Description:** List sequence jump (skipped from 1 to 456)
* **Chapter:** *Chapter 10 - Of the names of God given unto Christ.*
* **Contexts:**

### 173. `2. ... 10.`
* **Description:** List sequence jump (skipped from 2 to 10)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 174. `10. ... 18.`
* **Description:** List sequence jump (skipped from 10 to 18)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 175. `2. ... 18.`
* **Description:** List sequence jump (skipped from 2 to 18)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 176. `3. ... 24.`
* **Description:** List sequence jump (skipped from 3 to 24)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 177. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 178. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 179. `1. ... 11.`
* **Description:** List sequence jump (skipped from 1 to 11)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 180. `2. ... 11.`
* **Description:** List sequence jump (skipped from 2 to 11)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 181. `5. ... 10.`
* **Description:** List sequence jump (skipped from 5 to 10)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 182. `10. ... 32.`
* **Description:** List sequence jump (skipped from 10 to 32)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 183. `2. ... 20.`
* **Description:** List sequence jump (skipped from 2 to 20)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 184. `4. ... 6.`
* **Description:** List sequence jump (skipped from 4 to 6)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 185. `5. ... 7.`
* **Description:** List sequence jump (skipped from 5 to 7)
* **Chapter:** *Chapter 11 - Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his e...*
* **Contexts:**

### 186. `3. ... 9.`
* **Description:** List sequence jump (skipped from 3 to 9)
* **Chapter:** *Chapter 12 - All-ruling and disposing providence assigned unto Christ, and his eternal Godhead ...*
* **Contexts:**

### 187. `5. ... 41.`
* **Description:** List sequence jump (skipped from 5 to 41)
* **Chapter:** *Chapter 12 - All-ruling and disposing providence assigned unto Christ, and his eternal Godhead ...*
* **Contexts:**

### 188. `1. ... 26.`
* **Description:** List sequence jump (skipped from 1 to 26)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 189. `2. ... 9.`
* **Description:** List sequence jump (skipped from 2 to 9)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 190. `5. ... 12.`
* **Description:** List sequence jump (skipped from 5 to 12)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 191. `6. ... 14.`
* **Description:** List sequence jump (skipped from 6 to 14)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 192. `1. ... 12.`
* **Description:** List sequence jump (skipped from 1 to 12)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 193. `3. ... 26.`
* **Description:** List sequence jump (skipped from 3 to 26)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 194. `1. ... 14.`
* **Description:** List sequence jump (skipped from 1 to 14)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 195. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 196. `4. ... 47.`
* **Description:** List sequence jump (skipped from 4 to 47)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 197. `3. ... 15.`
* **Description:** List sequence jump (skipped from 3 to 15)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 198. `2. ... 18.`
* **Description:** List sequence jump (skipped from 2 to 18)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 199. `5. ... 11.`
* **Description:** List sequence jump (skipped from 5 to 11)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 200. `2. ... 55.`
* **Description:** List sequence jump (skipped from 2 to 55)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 201. `3. ... 16.`
* **Description:** List sequence jump (skipped from 3 to 16)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 202. `4. ... 19.`
* **Description:** List sequence jump (skipped from 4 to 19)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 203. `19. ... 34.`
* **Description:** List sequence jump (skipped from 19 to 34)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 204. `22. ... 29.`
* **Description:** List sequence jump (skipped from 22 to 29)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 205. `1. ... 13.`
* **Description:** List sequence jump (skipped from 1 to 13)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 206. `2. ... 14.`
* **Description:** List sequence jump (skipped from 2 to 14)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 207. `3. ... 5.`
* **Description:** List sequence jump (skipped from 3 to 5)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 208. `1. ... 22.`
* **Description:** List sequence jump (skipped from 1 to 22)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 209. `1. ... 37.`
* **Description:** List sequence jump (skipped from 1 to 37)
* **Chapter:** *Chapter 13 - Of the incarnation of Christ, and his pre-existence thereunto.*
* **Contexts:**

### 210. `3. ... 14.`
* **Description:** List sequence jump (skipped from 3 to 14)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 211. `3. ... 28.`
* **Description:** List sequence jump (skipped from 3 to 28)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 212. `5. ... 18.`
* **Description:** List sequence jump (skipped from 5 to 18)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 213. `18. ... 26.`
* **Description:** List sequence jump (skipped from 18 to 26)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 214. `5. ... 7.`
* **Description:** List sequence jump (skipped from 5 to 7)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 215. `7. ... 15.`
* **Description:** List sequence jump (skipped from 7 to 15)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 216. `4. ... 9.`
* **Description:** List sequence jump (skipped from 4 to 9)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 217. `3. ... 15.`
* **Description:** List sequence jump (skipped from 3 to 15)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 218. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 219. `3. ... 13.`
* **Description:** List sequence jump (skipped from 3 to 13)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 220. `4. ... 6.`
* **Description:** List sequence jump (skipped from 4 to 6)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 221. `2. ... 9.`
* **Description:** List sequence jump (skipped from 2 to 9)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 222. `3. ... 11.`
* **Description:** List sequence jump (skipped from 3 to 11)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 223. `3. ... 33.`
* **Description:** List sequence jump (skipped from 3 to 33)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 224. `8. ... 11.`
* **Description:** List sequence jump (skipped from 8 to 11)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 225. `12. ... 37.`
* **Description:** List sequence jump (skipped from 12 to 37)
* **Chapter:** *Chapter 14 - Sundry other testimonies given to the deity of Christ vindicated.*
* **Contexts:**

### 226. `4. ... 11.`
* **Description:** List sequence jump (skipped from 4 to 11)
* **Chapter:** *Mr Biddle's Fifth Chapter Examined.*
* **Contexts:**

### 227. `7. ... 39.`
* **Description:** List sequence jump (skipped from 7 to 39)
* **Chapter:** *Mr Biddle's Fifth Chapter Examined.*
* **Contexts:**

### 228. `14. ... 32.`
* **Description:** List sequence jump (skipped from 14 to 32)
* **Chapter:** *Examination.*
* **Contexts:**

### 229. `6. ... 13.`
* **Description:** List sequence jump (skipped from 6 to 13)
* **Chapter:** *Examination.*
* **Contexts:**

### 230. `13. ... 30.`
* **Description:** List sequence jump (skipped from 13 to 30)
* **Chapter:** *Examination.*
* **Contexts:**

### 231. `11. ... 18.`
* **Description:** List sequence jump (skipped from 11 to 18)
* **Chapter:** *Examination.*
* **Contexts:**

### 232. `4. ... 11.`
* **Description:** List sequence jump (skipped from 4 to 11)
* **Chapter:** *Examination.*
* **Contexts:**

### 233. `6. ... 19.`
* **Description:** List sequence jump (skipped from 6 to 19)
* **Chapter:** *Examination.*
* **Contexts:**

### 234. `7. ... 16.`
* **Description:** List sequence jump (skipped from 7 to 16)
* **Chapter:** *Examination.*
* **Contexts:**

### 235. `8. ... 19.`
* **Description:** List sequence jump (skipped from 8 to 19)
* **Chapter:** *Examination.*
* **Contexts:**

### 236. `3. ... 7.`
* **Description:** List sequence jump (skipped from 3 to 7)
* **Chapter:** *Examination.*
* **Contexts:**

### 237. `4. ... 22.`
* **Description:** List sequence jump (skipped from 4 to 22)
* **Chapter:** *Examination.*
* **Contexts:**

### 238. `5. ... 11.`
* **Description:** List sequence jump (skipped from 5 to 11)
* **Chapter:** *Examination.*
* **Contexts:**

### 239. `1. ... 9.`
* **Description:** List sequence jump (skipped from 1 to 9)
* **Chapter:** *Examination.*
* **Contexts:**

### 240. `4. ... 17.`
* **Description:** List sequence jump (skipped from 4 to 17)
* **Chapter:** *Examination.*
* **Contexts:**

### 241. `1. ... 20.`
* **Description:** List sequence jump (skipped from 1 to 20)
* **Chapter:** *Examination.*
* **Contexts:**

### 242. `11. ... 21.`
* **Description:** List sequence jump (skipped from 11 to 21)
* **Chapter:** *Examination.*
* **Contexts:**

### 243. `5. ... 21.`
* **Description:** List sequence jump (skipped from 5 to 21)
* **Chapter:** *Mr Biddle's Sixth Chapter Considered.*
* **Contexts:**

### 244. `17. ... 24.`
* **Description:** List sequence jump (skipped from 17 to 24)
* **Chapter:** *Chapter 17 - Of the mediation of Christ.*
* **Contexts:**

### 245. `18. ... 22.`
* **Description:** List sequence jump (skipped from 18 to 22)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 246. `1. ... 18.`
* **Description:** List sequence jump (skipped from 1 to 18)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 247. `3. ... 20.`
* **Description:** List sequence jump (skipped from 3 to 20)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 248. `2. ... 12.`
* **Description:** List sequence jump (skipped from 2 to 12)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 249. `4. ... 9.`
* **Description:** List sequence jump (skipped from 4 to 9)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 250. `8. ... 40.`
* **Description:** List sequence jump (skipped from 8 to 40)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 251. `2. ... 34.`
* **Description:** List sequence jump (skipped from 2 to 34)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 252. `4. ... 40.`
* **Description:** List sequence jump (skipped from 4 to 40)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 253. `5. ... 26.`
* **Description:** List sequence jump (skipped from 5 to 26)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 254. `1. ... 32.`
* **Description:** List sequence jump (skipped from 1 to 32)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 255. `3. ... 10.`
* **Description:** List sequence jump (skipped from 3 to 10)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 256. `10. ... 27.`
* **Description:** List sequence jump (skipped from 10 to 27)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 257. `1. ... 21.`
* **Description:** List sequence jump (skipped from 1 to 21)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 258. `2. ... 17.`
* **Description:** List sequence jump (skipped from 2 to 17)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 259. `3. ... 8.`
* **Description:** List sequence jump (skipped from 3 to 8)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 260. `4. ... 20.`
* **Description:** List sequence jump (skipped from 4 to 20)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 261. `5. ... 25.`
* **Description:** List sequence jump (skipped from 5 to 25)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 262. `3. ... 12.`
* **Description:** List sequence jump (skipped from 3 to 12)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 263. `7. ... 45.`
* **Description:** List sequence jump (skipped from 7 to 45)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 264. `12. ... 40.`
* **Description:** List sequence jump (skipped from 12 to 40)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 265. `4. ... 22.`
* **Description:** List sequence jump (skipped from 4 to 22)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 266. `1. ... 26.`
* **Description:** List sequence jump (skipped from 1 to 26)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 267. `2. ... 30.`
* **Description:** List sequence jump (skipped from 2 to 30)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 268. `3. ... 19.`
* **Description:** List sequence jump (skipped from 3 to 19)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 269. `2. ... 18.`
* **Description:** List sequence jump (skipped from 2 to 18)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 270. `7. ... 19.`
* **Description:** List sequence jump (skipped from 7 to 19)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 271. `3. ... 5.`
* **Description:** List sequence jump (skipped from 3 to 5)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 272. `2. ... 10.`
* **Description:** List sequence jump (skipped from 2 to 10)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 273. `1. ... 12.`
* **Description:** List sequence jump (skipped from 1 to 12)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 274. `3. ... 7.`
* **Description:** List sequence jump (skipped from 3 to 7)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 275. `7. ... 14.`
* **Description:** List sequence jump (skipped from 7 to 14)
* **Chapter:** *Chapter 18 - Of Christ's prophetical office*
* **Contexts:**

### 276. `8. ... 23.`
* **Description:** List sequence jump (skipped from 8 to 23)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 277. `2. ... 27.`
* **Description:** List sequence jump (skipped from 2 to 27)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 278. `3. ... 9.`
* **Description:** List sequence jump (skipped from 3 to 9)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 279. `9. ... 12.`
* **Description:** List sequence jump (skipped from 9 to 12)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 280. `2. ... 298.`
* **Description:** List sequence jump (skipped from 2 to 298)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 281. `2. ... 9.`
* **Description:** List sequence jump (skipped from 2 to 9)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 282. `1. ... 11.`
* **Description:** List sequence jump (skipped from 1 to 11)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 283. `2. ... 8.`
* **Description:** List sequence jump (skipped from 2 to 8)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 284. `3. ... 21.`
* **Description:** List sequence jump (skipped from 3 to 21)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 285. `1. ... 6.`
* **Description:** List sequence jump (skipped from 1 to 6)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 286. `6. ... 10.`
* **Description:** List sequence jump (skipped from 6 to 10)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 287. `2. ... 23.`
* **Description:** List sequence jump (skipped from 2 to 23)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 288. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 289. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 290. `4. ... 28.`
* **Description:** List sequence jump (skipped from 4 to 28)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 291. `5. ... 7.`
* **Description:** List sequence jump (skipped from 5 to 7)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 292. `2. ... 35.`
* **Description:** List sequence jump (skipped from 2 to 35)
* **Chapter:** *Chapter 19 - Of the kingly office of Jesus Christ, and of the worship that is ascribed and due ...*
* **Contexts:**

### 293. `1. ... 69.`
* **Description:** List sequence jump (skipped from 1 to 69)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 294. `2. ... 16.`
* **Description:** List sequence jump (skipped from 2 to 16)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 295. `16. ... 22.`
* **Description:** List sequence jump (skipped from 16 to 22)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 296. `2. ... 25.`
* **Description:** List sequence jump (skipped from 2 to 25)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 297. `3. ... 24.`
* **Description:** List sequence jump (skipped from 3 to 24)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 298. `3. ... 10.`
* **Description:** List sequence jump (skipped from 3 to 10)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 299. `10. ... 26.`
* **Description:** List sequence jump (skipped from 10 to 26)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 300. `26. ... 28.`
* **Description:** List sequence jump (skipped from 26 to 28)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 301. `3. ... 7.`
* **Description:** List sequence jump (skipped from 3 to 7)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 302. `4. ... 14.`
* **Description:** List sequence jump (skipped from 4 to 14)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 303. `5. ... 11.`
* **Description:** List sequence jump (skipped from 5 to 11)
* **Chapter:** *Mr Biddle's Eleventh Chapter Examined.*
* **Contexts:**

### 304. `21. ... 23.`
* **Description:** List sequence jump (skipped from 21 to 23)
* **Chapter:** *Chapter 21 - Of the death of Christ, the causes, ends, and fruits thereof, with an entrance int...*
* **Contexts:**

### 305. `23. ... 28.`
* **Description:** List sequence jump (skipped from 23 to 28)
* **Chapter:** *Chapter 21 - Of the death of Christ, the causes, ends, and fruits thereof, with an entrance int...*
* **Contexts:**

### 306. `1. ... 9.`
* **Description:** List sequence jump (skipped from 1 to 9)
* **Chapter:** *Chapter 21 - Of the death of Christ, the causes, ends, and fruits thereof, with an entrance int...*
* **Contexts:**

### 307. `3. ... 10.`
* **Description:** List sequence jump (skipped from 3 to 10)
* **Chapter:** *Chapter 21 - Of the death of Christ, the causes, ends, and fruits thereof, with an entrance int...*
* **Contexts:**

### 308. `1. ... 4.`
* **Description:** List sequence jump (skipped from 1 to 4)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 309. `4. ... 31.`
* **Description:** List sequence jump (skipped from 4 to 31)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 310. `6. ... 9.`
* **Description:** List sequence jump (skipped from 6 to 9)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 311. `9. ... 21.`
* **Description:** List sequence jump (skipped from 9 to 21)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 312. `21. ... 30.`
* **Description:** List sequence jump (skipped from 21 to 30)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 313. `4. ... 7.`
* **Description:** List sequence jump (skipped from 4 to 7)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 314. `7. ... 10.`
* **Description:** List sequence jump (skipped from 7 to 10)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 315. `9. ... 13.`
* **Description:** List sequence jump (skipped from 9 to 13)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 316. `6. ... 12.`
* **Description:** List sequence jump (skipped from 6 to 12)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 317. `12. ... 15.`
* **Description:** List sequence jump (skipped from 12 to 15)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 318. `3. ... 28.`
* **Description:** List sequence jump (skipped from 3 to 28)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 319. `10. ... 12.`
* **Description:** List sequence jump (skipped from 10 to 12)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 320. `12. ... 27.`
* **Description:** List sequence jump (skipped from 12 to 27)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 321. `3. ... 14.`
* **Description:** List sequence jump (skipped from 3 to 14)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 322. `14. ... 28.`
* **Description:** List sequence jump (skipped from 14 to 28)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 323. `5. ... 18.`
* **Description:** List sequence jump (skipped from 5 to 18)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 324. `7. ... 19.`
* **Description:** List sequence jump (skipped from 7 to 19)
* **Chapter:** *Chapter 22 - The several considerations of the death of Christ as to the expiation of our sins ...*
* **Contexts:**

### 325. `1. ... 9.`
* **Description:** List sequence jump (skipped from 1 to 9)
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**

### 326. `9. ... 32.`
* **Description:** List sequence jump (skipped from 9 to 32)
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**

### 327. `2. ... 19.`
* **Description:** List sequence jump (skipped from 2 to 19)
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**

### 328. `2. ... 40.`
* **Description:** List sequence jump (skipped from 2 to 40)
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**

### 329. `1. ... 4.`
* **Description:** List sequence jump (skipped from 1 to 4)
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**

### 330. `3. ... 10.`
* **Description:** List sequence jump (skipped from 3 to 10)
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**

### 331. `3. ... 26.`
* **Description:** List sequence jump (skipped from 3 to 26)
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**

### 332. `4. ... 12.`
* **Description:** List sequence jump (skipped from 4 to 12)
* **Chapter:** *Chapter 23 - Of the death of Christ as it was a punishment, and the satisfaction made thereby.*
* **Contexts:**

### 333. `2. ... 12.`
* **Description:** List sequence jump (skipped from 2 to 12)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 334. `12. ... 133.`
* **Description:** List sequence jump (skipped from 12 to 133)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 335. `1. ... 14.`
* **Description:** List sequence jump (skipped from 1 to 14)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 336. `3. ... 29.`
* **Description:** List sequence jump (skipped from 3 to 29)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 337. `1. ... 23.`
* **Description:** List sequence jump (skipped from 1 to 23)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 338. `23. ... 37.`
* **Description:** List sequence jump (skipped from 23 to 37)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 339. `2. ... 11.`
* **Description:** List sequence jump (skipped from 2 to 11)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 340. `3. ... 30.`
* **Description:** List sequence jump (skipped from 3 to 30)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 341. `30. ... 54.`
* **Description:** List sequence jump (skipped from 30 to 54)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 342. `1. ... 21.`
* **Description:** List sequence jump (skipped from 1 to 21)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 343. `2. ... 18.`
* **Description:** List sequence jump (skipped from 2 to 18)
* **Chapter:** *Chapter 24 - Some particular testimonies evincing the death of Christ to be a punishment, prope...*
* **Contexts:**

### 344. `1. ... 10.`
* **Description:** List sequence jump (skipped from 1 to 10)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 345. `4. ... 13.`
* **Description:** List sequence jump (skipped from 4 to 13)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 346. `13. ... 52.`
* **Description:** List sequence jump (skipped from 13 to 52)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 347. `4. ... 10.`
* **Description:** List sequence jump (skipped from 4 to 10)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 348. `2. ... 26.`
* **Description:** List sequence jump (skipped from 2 to 26)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 349. `1. ... 21.`
* **Description:** List sequence jump (skipped from 1 to 21)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 350. `2. ... 22.`
* **Description:** List sequence jump (skipped from 2 to 22)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 351. `1. ... 11.`
* **Description:** List sequence jump (skipped from 1 to 11)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 352. `2. ... 24.`
* **Description:** List sequence jump (skipped from 2 to 24)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 353. `6. ... 68.`
* **Description:** List sequence jump (skipped from 6 to 68)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 354. `3. ... 32.`
* **Description:** List sequence jump (skipped from 3 to 32)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 355. `1. ... 4.`
* **Description:** List sequence jump (skipped from 1 to 4)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 356. `4. ... 7.`
* **Description:** List sequence jump (skipped from 4 to 7)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 357. `1. ... 39.`
* **Description:** List sequence jump (skipped from 1 to 39)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 358. `3. ... 26.`
* **Description:** List sequence jump (skipped from 3 to 26)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 359. `4. ... 26.`
* **Description:** List sequence jump (skipped from 4 to 26)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 360. `21. ... 26.`
* **Description:** List sequence jump (skipped from 21 to 26)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 361. `2. ... 64.`
* **Description:** List sequence jump (skipped from 2 to 64)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 362. `4. ... 19.`
* **Description:** List sequence jump (skipped from 4 to 19)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 363. `1. ... 23.`
* **Description:** List sequence jump (skipped from 1 to 23)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 364. `1. ... 19.`
* **Description:** List sequence jump (skipped from 1 to 19)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 365. `2. ... 8.`
* **Description:** List sequence jump (skipped from 2 to 8)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 366. `8. ... 15.`
* **Description:** List sequence jump (skipped from 8 to 15)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 367. `3. ... 11.`
* **Description:** List sequence jump (skipped from 3 to 11)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 368. `4. ... 17.`
* **Description:** List sequence jump (skipped from 4 to 17)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 369. `5. ... 13.`
* **Description:** List sequence jump (skipped from 5 to 13)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 370. `5. ... 11.`
* **Description:** List sequence jump (skipped from 5 to 11)
* **Chapter:** *Chapter 25 - A digression concerning the 53d chapter of Isaiah, and the vindication of it from ...*
* **Contexts:**

### 371. `1. ... 26.`
* **Description:** List sequence jump (skipped from 1 to 26)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 372. `2. ... 23.`
* **Description:** List sequence jump (skipped from 2 to 23)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 373. `2. ... 30.`
* **Description:** List sequence jump (skipped from 2 to 30)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 374. `15. ... 26.`
* **Description:** List sequence jump (skipped from 15 to 26)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 375. `1. ... 10.`
* **Description:** List sequence jump (skipped from 1 to 10)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 376. `10. ... 26.`
* **Description:** List sequence jump (skipped from 10 to 26)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 377. `7. ... 56.`
* **Description:** List sequence jump (skipped from 7 to 56)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 378. `11. ... 69.`
* **Description:** List sequence jump (skipped from 11 to 69)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 379. `3. ... 18.`
* **Description:** List sequence jump (skipped from 3 to 18)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 380. `18. ... 38.`
* **Description:** List sequence jump (skipped from 18 to 38)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 381. `38. ... 50.`
* **Description:** List sequence jump (skipped from 38 to 50)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 382. `8. ... 37.`
* **Description:** List sequence jump (skipped from 8 to 37)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 383. `3. ... 68.`
* **Description:** List sequence jump (skipped from 3 to 68)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 384. `17. ... 46.`
* **Description:** List sequence jump (skipped from 17 to 46)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 385. `1. ... 9.`
* **Description:** List sequence jump (skipped from 1 to 9)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 386. `9. ... 23.`
* **Description:** List sequence jump (skipped from 9 to 23)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 387. `2. ... 24.`
* **Description:** List sequence jump (skipped from 2 to 24)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 388. `1. ... 15.`
* **Description:** List sequence jump (skipped from 1 to 15)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 389. `3. ... 7.`
* **Description:** List sequence jump (skipped from 3 to 7)
* **Chapter:** *Chapter 26 - Of the matter of the punishment that Christ underwent, or what he suffered.*
* **Contexts:**

### 390. `5. ... 66.`
* **Description:** List sequence jump (skipped from 5 to 66)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 391. `2. ... 18.`
* **Description:** List sequence jump (skipped from 2 to 18)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 392. `2. ... 10.`
* **Description:** List sequence jump (skipped from 2 to 10)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 393. `3. ... 9.`
* **Description:** List sequence jump (skipped from 3 to 9)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 394. `3. ... 10.`
* **Description:** List sequence jump (skipped from 3 to 10)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 395. `9. ... 28.`
* **Description:** List sequence jump (skipped from 9 to 28)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 396. `28. ... 31.`
* **Description:** List sequence jump (skipped from 28 to 31)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 397. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 398. `4. ... 28.`
* **Description:** List sequence jump (skipped from 4 to 28)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 399. `5. ... 8.`
* **Description:** List sequence jump (skipped from 5 to 8)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 400. `5. ... 24.`
* **Description:** List sequence jump (skipped from 5 to 24)
* **Chapter:** *Chapter 27 - Of the covenant between the Father and the Son, the ground and foundation of this ...*
* **Contexts:**

### 401. `12. ... 16.`
* **Description:** List sequence jump (skipped from 12 to 16)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 402. `8. ... 12.`
* **Description:** List sequence jump (skipped from 8 to 12)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 403. `12. ... 24.`
* **Description:** List sequence jump (skipped from 12 to 24)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 404. `24. ... 30.`
* **Description:** List sequence jump (skipped from 24 to 30)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 405. `4. ... 13.`
* **Description:** List sequence jump (skipped from 4 to 13)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 406. `13. ... 35.`
* **Description:** List sequence jump (skipped from 13 to 35)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 407. `2. ... 26.`
* **Description:** List sequence jump (skipped from 2 to 26)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 408. `1. ... 7.`
* **Description:** List sequence jump (skipped from 1 to 7)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 409. `7. ... 29.`
* **Description:** List sequence jump (skipped from 7 to 29)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 410. `12. ... 26.`
* **Description:** List sequence jump (skipped from 12 to 26)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 411. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 412. `4. ... 26.`
* **Description:** List sequence jump (skipped from 4 to 26)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 413. `26. ... 32.`
* **Description:** List sequence jump (skipped from 26 to 32)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 414. `2. ... 15.`
* **Description:** List sequence jump (skipped from 2 to 15)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 415. `1. ... 24.`
* **Description:** List sequence jump (skipped from 1 to 24)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 416. `24. ... 32.`
* **Description:** List sequence jump (skipped from 24 to 32)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 417. `2. ... 14.`
* **Description:** List sequence jump (skipped from 2 to 14)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 418. `14. ... 19.`
* **Description:** List sequence jump (skipped from 14 to 19)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 419. `19. ... 22.`
* **Description:** List sequence jump (skipped from 19 to 22)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 420. `4. ... 70.`
* **Description:** List sequence jump (skipped from 4 to 70)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 421. `1. ... 11.`
* **Description:** List sequence jump (skipped from 1 to 11)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 422. `9. ... 32.`
* **Description:** List sequence jump (skipped from 9 to 32)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 423. `3. ... 10.`
* **Description:** List sequence jump (skipped from 3 to 10)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 424. `4. ... 16.`
* **Description:** List sequence jump (skipped from 4 to 16)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 425. `16. ... 18.`
* **Description:** List sequence jump (skipped from 16 to 18)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 426. `18. ... 20.`
* **Description:** List sequence jump (skipped from 18 to 20)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 427. `6. ... 22.`
* **Description:** List sequence jump (skipped from 6 to 22)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 428. `14. ... 25.`
* **Description:** List sequence jump (skipped from 14 to 25)
* **Chapter:** *Chapter 28 - Of redemption by the death of Christ as it was a price or ransom.*
* **Contexts:**

### 429. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 430. `3. ... 36.`
* **Description:** List sequence jump (skipped from 3 to 36)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 431. `4. ... 13.`
* **Description:** List sequence jump (skipped from 4 to 13)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 432. `13. ... 19.`
* **Description:** List sequence jump (skipped from 13 to 19)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 433. `6. ... 17.`
* **Description:** List sequence jump (skipped from 6 to 17)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 434. `17. ... 26.`
* **Description:** List sequence jump (skipped from 17 to 26)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 435. `1. ... 32.`
* **Description:** List sequence jump (skipped from 1 to 32)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 436. `1. ... 10.`
* **Description:** List sequence jump (skipped from 1 to 10)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 437. `1. ... 7.`
* **Description:** List sequence jump (skipped from 1 to 7)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 438. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 439. `1. ... 12.`
* **Description:** List sequence jump (skipped from 1 to 12)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 440. `3. ... 25.`
* **Description:** List sequence jump (skipped from 3 to 25)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 441. `2. ... 18.`
* **Description:** List sequence jump (skipped from 2 to 18)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 442. `18. ... 22.`
* **Description:** List sequence jump (skipped from 18 to 22)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 443. `4. ... 32.`
* **Description:** List sequence jump (skipped from 4 to 32)
* **Chapter:** *Chapter 29 - Of reconciliation by the death of Christ as it is a sacrifice.*
* **Contexts:**

### 444. `2. ... 142.`
* **Description:** List sequence jump (skipped from 2 to 142)
* **Chapter:** *Chapter 30 - The satisfaction of Christ on the consideration of his death being a punishment fa...*
* **Contexts:**

### 445. `3. ... 33.`
* **Description:** List sequence jump (skipped from 3 to 33)
* **Chapter:** *Chapter 30 - The satisfaction of Christ on the consideration of his death being a punishment fa...*
* **Contexts:**

### 446. `3. ... 11.`
* **Description:** List sequence jump (skipped from 3 to 11)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 447. `2. ... 13.`
* **Description:** List sequence jump (skipped from 2 to 13)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 448. `4. ... 12.`
* **Description:** List sequence jump (skipped from 4 to 12)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 449. `12. ... 23.`
* **Description:** List sequence jump (skipped from 12 to 23)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 450. `1. ... 8.`
* **Description:** List sequence jump (skipped from 1 to 8)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 451. `8. ... 10.`
* **Description:** List sequence jump (skipped from 8 to 10)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 452. `10. ... 28.`
* **Description:** List sequence jump (skipped from 10 to 28)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 453. `28. ... 70.`
* **Description:** List sequence jump (skipped from 28 to 70)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 454. `5. ... 9.`
* **Description:** List sequence jump (skipped from 5 to 9)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 455. `6. ... 10.`
* **Description:** List sequence jump (skipped from 6 to 10)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 456. `10. ... 18.`
* **Description:** List sequence jump (skipped from 10 to 18)
* **Chapter:** *Chapter 31 - Of election and universal grace — Of the resurrection of Christ from the dead.*
* **Contexts:**

### 457. `2. ... 12.`
* **Description:** List sequence jump (skipped from 2 to 12)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 458. `4. ... 14.`
* **Description:** List sequence jump (skipped from 4 to 14)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 459. `5. ... 13.`
* **Description:** List sequence jump (skipped from 5 to 13)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 460. `13. ... 24.`
* **Description:** List sequence jump (skipped from 13 to 24)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 461. `1. ... 6.`
* **Description:** List sequence jump (skipped from 1 to 6)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 462. `2. ... 9.`
* **Description:** List sequence jump (skipped from 2 to 9)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 463. `3. ... 15.`
* **Description:** List sequence jump (skipped from 3 to 15)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 464. `4. ... 6.`
* **Description:** List sequence jump (skipped from 4 to 6)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 465. `3. ... 5.`
* **Description:** List sequence jump (skipped from 3 to 5)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 466. `5. ... 28.`
* **Description:** List sequence jump (skipped from 5 to 28)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 467. `3. ... 6.`
* **Description:** List sequence jump (skipped from 3 to 6)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 468. `4. ... 26.`
* **Description:** List sequence jump (skipped from 4 to 26)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 469. `1. ... 7.`
* **Description:** List sequence jump (skipped from 1 to 7)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 470. `7. ... 9.`
* **Description:** List sequence jump (skipped from 7 to 9)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 471. `9. ... 30.`
* **Description:** List sequence jump (skipped from 9 to 30)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 472. `2. ... 22.`
* **Description:** List sequence jump (skipped from 2 to 22)
* **Chapter:** *Chapter 33 - Of keeping the commandments of God, and of perfection of obedience — How attainabl...*
* **Contexts:**

### 473. `4. ... 26.`
* **Description:** List sequence jump (skipped from 4 to 26)
* **Chapter:** *Chapter 34 - Of prayer; and whether Christ prescribed a form of prayer to be used by believers;...*
* **Contexts:**

### 474. `1. ... 17.`
* **Description:** List sequence jump (skipped from 1 to 17)
* **Chapter:** *Chapter 34 - Of prayer; and whether Christ prescribed a form of prayer to be used by believers;...*
* **Contexts:**

### 475. `13. ... 16.`
* **Description:** List sequence jump (skipped from 13 to 16)
* **Chapter:** *Chapter 35 - Of the resurrection of the dead and the state of the wicked at the last day.*
* **Contexts:**

### 476. `3. ... 11.`
* **Description:** List sequence jump (skipped from 3 to 11)
* **Chapter:** *Chapter 35 - Of the resurrection of the dead and the state of the wicked at the last day.*
* **Contexts:**

### 477. `2. ... 9.`
* **Description:** List sequence jump (skipped from 2 to 9)
* **Chapter:** *Chapter 35 - Of the resurrection of the dead and the state of the wicked at the last day.*
* **Contexts:**

### 478. `9. ... 16.`
* **Description:** List sequence jump (skipped from 9 to 16)
* **Chapter:** *Chapter 35 - Of the resurrection of the dead and the state of the wicked at the last day.*
* **Contexts:**

### 479. `3. ... 48.`
* **Description:** List sequence jump (skipped from 3 to 48)
* **Chapter:** *Chapter 35 - Of the resurrection of the dead and the state of the wicked at the last day.*
* **Contexts:**

### 480. `1. ... 269.`
* **Description:** List sequence jump (skipped from 1 to 269)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 481. `1. ... 17.`
* **Description:** List sequence jump (skipped from 1 to 17)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 482. `17. ... 184.`
* **Description:** List sequence jump (skipped from 17 to 184)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 483. `184. ... 209.`
* **Description:** List sequence jump (skipped from 184 to 209)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 484. `209. ... 519.`
* **Description:** List sequence jump (skipped from 209 to 519)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 485. `4. ... 115.`
* **Description:** List sequence jump (skipped from 4 to 115)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 486. `2. ... 131.`
* **Description:** List sequence jump (skipped from 2 to 131)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 487. `3. ... 14.`
* **Description:** List sequence jump (skipped from 3 to 14)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 488. `7. ... 17.`
* **Description:** List sequence jump (skipped from 7 to 17)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 489. `17. ... 32.`
* **Description:** List sequence jump (skipped from 17 to 32)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 490. `4. ... 14.`
* **Description:** List sequence jump (skipped from 4 to 14)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 491. `5. ... 181.`
* **Description:** List sequence jump (skipped from 5 to 181)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 492. `11. ... 14.`
* **Description:** List sequence jump (skipped from 11 to 14)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 493. `14. ... 29.`
* **Description:** List sequence jump (skipped from 14 to 29)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 494. `29. ... 110.`
* **Description:** List sequence jump (skipped from 29 to 110)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 495. `110. ... 221.`
* **Description:** List sequence jump (skipped from 110 to 221)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 496. `5. ... 147.`
* **Description:** List sequence jump (skipped from 5 to 147)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 497. `2. ... 60.`
* **Description:** List sequence jump (skipped from 2 to 60)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 498. `60. ... 74.`
* **Description:** List sequence jump (skipped from 60 to 74)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 499. `4. ... 8.`
* **Description:** List sequence jump (skipped from 4 to 8)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 500. `8. ... 108.`
* **Description:** List sequence jump (skipped from 8 to 108)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 501. `108. ... 115.`
* **Description:** List sequence jump (skipped from 108 to 115)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 502. `7. ... 291.`
* **Description:** List sequence jump (skipped from 7 to 291)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 503. `8. ... 277.`
* **Description:** List sequence jump (skipped from 8 to 277)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 504. `9. ... 113.`
* **Description:** List sequence jump (skipped from 9 to 113)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 505. `2. ... 4.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 506. `4. ... 69.`
* **Description:** List sequence jump (skipped from 4 to 69)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 507. `1. ... 11.`
* **Description:** List sequence jump (skipped from 1 to 11)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 508. `11. ... 35.`
* **Description:** List sequence jump (skipped from 11 to 35)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 509. `35. ... 190.`
* **Description:** List sequence jump (skipped from 35 to 190)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 510. `2. ... 44.`
* **Description:** List sequence jump (skipped from 2 to 44)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 511. `3. ... 229.`
* **Description:** List sequence jump (skipped from 3 to 229)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 512. `2. ... 9.`
* **Description:** List sequence jump (skipped from 2 to 9)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 513. `2. ... 29.`
* **Description:** List sequence jump (skipped from 2 to 29)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 514. `29. ... 274.`
* **Description:** List sequence jump (skipped from 29 to 274)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 515. `3. ... 30.`
* **Description:** List sequence jump (skipped from 3 to 30)
* **Chapter:** *Of the Death of Christ, and of Justification:*
* **Contexts:**

### 516. `6. ... 53.`
* **Description:** List sequence jump (skipped from 6 to 53)
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**

### 517. `24. ... 26.`
* **Description:** List sequence jump (skipped from 24 to 26)
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**

### 518. `6. ... 145.`
* **Description:** List sequence jump (skipped from 6 to 145)
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**

### 519. `XXVI. ... XXXII.`
* **Description:** List sequence jump (skipped from 26 to 32)
* **Chapter:** *A Second Consideration of the Annotations of Hugo Grotius.*
* **Contexts:**

---

