# Text Integrity & Anomaly Audit Report: Volume 6

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 324281
* **Total Suspected Anomalies Found:** 94

Add corrections to `text_replacements` inside `volumes/v6/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 26 items
* **Punctuation Spacing Blemishes:** 38 items
* **OCR & Bracket Residues:** 3 items
* **Mixed-Case Capitalization Errors:** 1 items
* **Unresolved Citation References:** 0 items
* **Structural Nesting Sequence Jumps:** 23 items
* **Invalid Bible References:** 3 items
* **List Formatting Inconsistencies:** 0 items

---

## Hyphenation Anomalies

### 1. `sign-post`
* **Description:** Splittable word (rejoins to valid word 'signpost')
* **Chapter:** *Chapter 7.*
* **Contexts:**
  * ... h from true mortification as the sun painted on a **sign-post** from the sun in the firmament; they had neither l ...

### 2. `sermon-proof`
* **Description:** Splittable word (rejoins to valid word 'sermonproof')
* **Chapter:** *Chapter 10.*
* **Contexts:**
  * ... ctions, wilt grow as some have profanely spoken, "**sermon-proof** and sickness-proof." Thou that didst tremble at t ...

### 3. `sickness-proof`
* **Description:** Splittable word (rejoins to valid word 'sicknessproof')
* **Chapter:** *Chapter 10.*
* **Contexts:**
  * ... as some have profanely spoken, "sermon-proof and **sickness-proof**." Thou that didst tremble at the presence of God, ...

### 4. `Christ-dishonoring`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Chapter 3*
* **Contexts:**
  * ... of the truth, and their naked, barren, fruitless, **Christ-dishonoring** profession, it is said of the temptation that fel ...

### 5. `good-man`
* **Description:** Splittable word (rejoins to valid word 'goodman')
* **Chapter:** *Chapter 2.*
* **Contexts:**
  * ... use, and yet not be always meddling with what the **good-man** of the house hath to do (that so we may keep to t ...

### 6. `Proper-ties`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Chapter 3.*
* **Contexts:**
  * ... the law of sin, the heart — What meant thereby — **Proper-ties** of the heart as possessed by sin, unsearchable, d ...

### 7. `work-house`
* **Description:** Splittable word (rejoins to valid word 'workhouse')
* **Chapter:** *Chapter 3.*
* **Contexts:**
  * ... actual sin, is here described. And its seat, its **work-house**, is said to be the heart; and so it is called by ...

### 8. `under-earth`
* **Description:** Splittable word (rejoins to valid word 'underearth')
* **Chapter:** *Chapter 3.*
* **Contexts:**
  * ... o watch its first appearances, to catch its first **under-earth** heavings and workings, and to set ourselves in op ...

### 9. `under-ground`
* **Description:** Splittable word (rejoins to valid word 'underground')
* **Chapter:** *Chapter 6.*
* **Contexts:**
  * ... e convictions and resolutions, or makes itself an **under-ground** passage by some secret lust, that shall give a fu ...

### 10. `spring-head`
* **Description:** Splittable word (rejoins to valid word 'springhead')
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... of God and his grace. This evidently lies at the **spring-head** of gospel obedience. The way whereby sin draws of ...

### 11. `day-star`
* **Description:** Splittable word (rejoins to valid word 'daystar')
* **Chapter:** *Chapter 12.*
* **Contexts:**
  * ... be in them all a principle of saving light, — the **day-star** is risen in their hearts, — yet all the shades of ...

### 12. `such-like`
* **Description:** Splittable word (rejoins to valid word 'suchlike')
* **Chapter:** *Chapter 13.*
* **Contexts:**
  * ... he dealt with him, so also would he do with some **such-like** sinners: "For this cause I obtained mercy, that i ...

### 13. `eye-salve`
* **Description:** Splittable word (rejoins to valid word 'eyesalve')
* **Chapter:** *Chapter 14.*
* **Contexts:**
  * ... t met not with such opposition; so is it with the **eye-salve** and the healing grace which we have abundantly fr ...

### 14. `land-flood`
* **Description:** Splittable word (rejoins to valid word 'landflood')
* **Chapter:** *Chapter 15.*
* **Contexts:**
  * ... holiness, fruitfulness, and obedience; as upon a **land-flood**, when many lesser streams run into a river, it sw ...

### 15. `ale-house`
* **Description:** Splittable word (rejoins to valid word 'alehouse')
* **Chapter:** *Chapter 16.*
* **Contexts:**
  * ... ghts of it, — the fellowship of the saints for an **ale-house** or a brothel-house, after a man hath been admitte ...

### 16. `Under-valuations`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *What Sins Usually Bring Believers Into Great Spiritual Distresses:*
* **Contexts:**
  * ... o the heart of God, and shall not be passed over. **Under-valuations** of love are great provocations. "Hath Nabal thus ...

### 17. `safe-guard`
* **Description:** Splittable word (rejoins to valid word 'safeguard')
* **Chapter:** *What Sins Usually Bring Believers Into Great Spiritual Distresses:*
* **Contexts:**
  * ... e, seeketh thy life; but with me thou shalt be in **safe-guard**;" — "Sin is my enemy no less than thine; it seeke ...

### 18. `heart-blood`
* **Description:** Splittable word (rejoins to valid word 'heartblood')
* **Chapter:** *The True Nature of Gospel Forgiveness*
* **Contexts:**
  * ... sue forth from the heart of the Father but by the **heart-blood** of the Son; and so do they stream unto the heart ...

### 19. `El-shaddai`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *The Name of God Confirming the Truth and Reality of Forgiveness With Him*
* **Contexts:**
  * ... hem." It is certain that both these names of God, **El-shaddai** and Jehovah, were known among his people before. ...
  * ... t said that God appeared unto them by the name of **El-shaddai**, but not by the name of Jehovah? The reason is, ...
  * ... braham: Genesis 17:1, שַׁ דַּי אֲנִי־אֵל, — "I am **El-shaddai**," "God Almighty," "God All-sufficient." And when ...

### 20. `peace-making`
* **Description:** Splittable word (rejoins to valid word 'peacemaking')
* **Chapter:** *Forgiveness Manifested in the Sending of the Son of God to Die for Sin*
* **Contexts:**
  * ... sends him, and himself. There lay the counsel of **peace-making** between God and man, in due time accomplished by ...

### 21. `sad-hearted`
* **Description:** Splittable word (rejoins to valid word 'sadhearted')
* **Chapter:** *Exhortation Unto the Belief of the Forgiveness That Is With God*
* **Contexts:**
  * ... shall tender this new wine of the gospel to poor, **sad-hearted**, conscience-distressed sinners, — sinners that ar ...

### 22. `Self-determinations`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Rule 1.*
* **Contexts:**
  * ... , then, is our first general rule and direction — **Self-determinations** concerning men's spiritual state and condition, b ...

### 23. `home-bred`
* **Description:** Splittable word (rejoins to valid word 'homebred')
* **Chapter:** *Rule 2.*
* **Contexts:**
  * ... g wholly taken up with the consideration of these **home-bred** perplexities, and not clearly acquainted with the ...

### 24. `after-reckoning`
* **Description:** Splittable word (rejoins to valid word 'afterreckoning')
* **Chapter:** *Rule 4.*
* **Contexts:**
  * ... , full, close work in this kind as they ought. An **after-reckoning** may come in on this hand to their own disturbance ...

### 25. `Self-judging`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Rule 9.*
* **Contexts:**
  * ... s of special use in the case under consideration. **Self-judging** in reference unto sin and the demerit of it is ou ...

### 26. `make-bate`
* **Description:** Splittable word (rejoins to valid word 'makebate')
* **Chapter:** *Second General Head of the Application of the Truth Insisted on*
* **Contexts:**
  * ... which he hath nothing to do withal. Let not this **make-bate** by any means inflame the difference. 5. Learn to ...

---

## Punctuation Spacing Blemishes

### 1. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 12.*
* **Contexts:**
  * ... e know of him; we see but his back parts. For, — **1st .** The intendment of all gospel revelation is, not t ...

### 2. `him :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 1*
* **Contexts:**
  * ... Savior expostulates the matter in particular with **him :** verse 40, "He saith unto Peter, Could you not wat ...

### 3. `unto :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 3*
* **Contexts:**
  * ... is, — its power and efficacy, with what it leads **unto :** — (1.) For ourselves, we are weakness itself. We ...

### 4. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Chapter 3*
* **Contexts:**
  * ... in the subject, not in the object, — in the heart**,,** not in the world. But they are said to be "in the ...

### 5. `heart ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Prefatory Note (The Nature, Power, Deceit, and Prevalency of the Remainders of Indwelling Sin in Believers)*
* **Contexts:**
  * ... "a law;" — the seat and subject of this law, the **heart ;** — its nature generally, as enmity against God; — ...

### 6. `God !`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 1.*
* **Contexts:**
  * ... f you in whose hearts is any thing of the ways of **God !** Your enemy is not only upon you, as on Samson of ...

### 7. `members ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 2.*
* **Contexts:**
  * ... , "It is present with me;" verse 23, "It is in my **members ;**" — yea, it is so far in a man, as in some sense i ...

### 8. `discovered !`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 2.*
* **Contexts:**
  * ... assistance of the Holy Ghost, will be hence also **discovered !** I fear we have few of us a diligence proportionab ...

### 9. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... danger of sin. And this is done several ways: — **1st .** The soul, having frequent need of relief by gospe ...

### 10. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... assengers, secures his journey beyond the other. **2dly .** The deceitfulness of sin takes advantage from the ...

### 11. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... occasion to speak more hereafter in particular. **3dly .** In times of temptation, this deceitfulness of sin ...

### 12. `,,`
* **Description:** Duplicate comma
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... deeply sensible of sin, it becomes on any account**,,** or by any means whatever, to have less, fewer, sl ...

### 13. `God ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 9.*
* **Contexts:**
  * ... ticular duties, according to the mind and will of **God ,** — namely, to endeavor after a sound and steadfast ...

### 14. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 9.*
* **Contexts:**
  * ... nds the place of it, and sets itself against it. **3dly .** Whilst the soul can thus constantly engage itself ...

### 15. `4thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 9.*
* **Contexts:**
  * ... appointment, yea, to the ruin of the law of sin. **4thly .** If the heart be not deceived by cursed hypocrisy, ...

### 16. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 10.*
* **Contexts:**
  * ... t they may do all according as he had commanded. **2dly .** The affections of the heart and mind in duties be ...
  * ... d what we are in them, that we are, and no more. **2dly .** It draws off the mind from the duties before ment ...

### 17. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 10.*
* **Contexts:**
  * ... themselves. And this it attempts several ways: — **1st .** By persuading the mind to content itself with gen ...

### 18. `in :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 12.*
* **Contexts:**
  * ... a large field for its deceit and subtlety to lurk **in :** — "Though it is an evil indeed to be relinquished ...

### 19. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 13.*
* **Contexts:**
  * ... , before I go hence, and be no more." But yet, — **2dly .** There are some cases wherein God may and doth tak ...
  * ... ey cannot do all the wickedness that they would. **2dly .** God doth it not to leave them to wrestle with sin ...

### 20. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 13.*
* **Contexts:**
  * ... rom the same dispensation towards others; for, — **1st .** It is so only in cases of extraordinary temptatio ...

### 21. `4thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 13.*
* **Contexts:**
  * ... hearts are full of anxiety, trouble, and sorrow. **4thly .** Do we see sometimes the flood-gates of men's lust ...

### 22. `5thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 13.*
* **Contexts:**
  * ... , or chain up their wrath; and who can oppose him **5thly .** Those who have received benefit by any of the way ...

### 23. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 15.*
* **Contexts:**
  * ... e several ways whereby it brings this to pass: — **1st .** It works by sloth and negligence. It prevails in ...
  * ... necessary to preserve men from this infection: — **1st .** In the body of professors there is a great number ...

### 24. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 15.*
* **Contexts:**
  * ... emselves unto those who bear the image of Satan. **2dly .** You know not what may be the present temptation o ...

### 25. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 15.*
* **Contexts:**
  * ... l for you to become sick and to be wounded also. **3dly .** Remember that of many of the best Christians, the ...

### 26. `obedience ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Chapter 16.*
* **Contexts:**
  * ... ture made for the glory of God by rational, moral **obedience ,** — rational, because by him chosen, and performed ...

### 27. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Chapter 16.*
* **Contexts:**
  * **..**. ve some worldly, cruel, or filthy and sensual lust**..** Certainly, here lies a secret efficacy, whose dep **..**.

### 28. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 17.*
* **Contexts:**
  * ... quered, not subdued, nor mortified by it; for, — **1st .** Though the course of sin may be repelled for a se ...

### 29. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Chapter 17.*
* **Contexts:**
  * ... This was the state with Pharaoh once and again. **2dly .** In such seasons sin is not conquered, but diverte ...

### 30. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *False Presumptions of Forgiveness Discovered*
* **Contexts:**
  * ... e very "first principles of the oracles of God." **Ans .** All this, then, I say, is so, and much more to th ...

### 31. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Farther Evidences of Forgiveness With God -testimonies*
* **Contexts:**
  * **..**. thus long, in the patience and forbearance of God**..** And to what end hath he thus spared us, and let p **..**.

### 32. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Evidences That Most Men Do Not Believe Forgiveness.*
* **Contexts:**
  * **..**. e forgiveness in God do thereby obtain forgiveness**..** Believing gives an interest in it; it brings it h **..**.

### 33. `peace .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Rule 2.*
* **Contexts:**
  * ... o very well consist with gospel justification and **peace .** Some men have no peace, because they have that wi ...

### 34. `together .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Rule 7.*
* **Contexts:**
  * ... er. Mix not too much foundation and building work **together .** Our foundation in dealing with God is Christ alon ...

### 35. `duty .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Rule 8.*
* **Contexts:**
  * ... omplaints when vigorous actings of grace are your **duty .** Fruitless and heartless complaints, bemoanings o ...

### 36. `matter .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Second General Head of the Application of the Truth Insisted on*
* **Contexts:**
  * ... men, and keep them off from establishment in this **matter .** And, FIRST, such disquietments and objections ag ...

### 37. `God .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Rule 2.*
* **Contexts:**
  * ... of it by an immediate testimony of the Spirit of **God .** I do grant that God doth sometimes, by this means ...

### 38. `trouble .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Rule 3.*
* **Contexts:**
  * ... of it upon your spirits now in your darkness and **trouble .** I am persuaded there are but few believers, but t ...

---

## OCR & Bracket Residues

### 1. `Adam)were`
* **Description:** OCR residue containing stray closing bracket/paren
* **Chapter:** *Discovery of Forgiveness in the First Promise*
* **Contexts:**
  * ... f mankind (He only excepted which was not then in **Adam)were** embarked in the same crime and guilt. Besides, it ...

### 2. `the]east`
* **Description:** OCR residue containing stray closing bracket/paren
* **Chapter:** *Farther Evidences of Forgiveness With God -testimonies*
* **Contexts:**
  * ... day of his solemn judgment and execution, without **the]east** intention to spare him, none will say there is pa ...

### 3. `the]ate`
* **Description:** OCR residue containing stray closing bracket/paren
* **Chapter:** *Second General Head of the Application of the Truth Insisted on*
* **Contexts:**
  * ... f them who are reduced to the utmost extremity by **the]ate** consuming fire; some have had their whole familie ...

---

## Mixed-Case Capitalization Errors

### 1. `seasonlHow`
* **Description:** Mixed-case capitalization error
* **Chapter:** *Chapter 8.*
* **Contexts:**
  * ... onviction. How sensible of sin will they be for a **seasonlHow** will they then mourn and weep under a sense of th ...

---

## Unresolved Citation References

No anomalies found in this category.

## Structural Nesting Sequence Jumps

### 1. `II.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Chapter 2*
* **Contexts:**
  * ... tching, and what is intended thereby — Of prayer **II.** Having showed what temptation is, I come, secondl ...
  * ... of which more in the process of our discourse. I**II.** There is means of prevention prescribed by our Sa ...

### 2. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Chapter 5*
* **Contexts:**
  * ... ein — (1.) Sense of the danger of temptation — (**2.**) That it is not in our power to keep ourselves — ...
  * ... omises of preservation — Of prayer in particular **2.** Having seen the danger of entering into temptatio ...
  * ... ion in a daily conscientious observation of it. (**2.**) There is this in it also, that it is not a thing ...

### 3. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Chapter 2.*
* **Contexts:**
  * [[CHAPTER]] CHAPTER **2.** [[SUMMARY]] Indwelling sin a law — In what sense ...
  * ... answer the danger of their state and condition! **2.** It is always ready to apply itself to every end a ...

### 4. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *A Paraphrase*
* **Contexts:**
  * ... of the depths have I cried unto thee, O LORD. **2.** Lord, hear my voice; let thine ears be attentive ...
  * ... from all his iniquities. A. PARAPHRASE Verses 1, **2.** — O Lord, through my manifold sins and provocatio ...

### 5. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Forgiveness Discovered or Revealed Only to Faith*
* **Contexts:**

### 6. `3.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Farther Evidences of Forgiveness With God -testimonies*
* **Contexts:**
  * **3.** We multiply these evidences, because they are mul ...
  * ... of all these sorts were justified and pardoned. **3.** Suppose this enumeration of sins doth not reach t ...
  * ... n, every city, every family is filled with them. **3.** That there is a common abuse of this patience of ...

### 7. `IV.`
* **Description:** List sequence starts at 4 instead of 1
* **Chapter:** *Farther Evidences of Forgiveness With God -testimonies*
* **Contexts:**
  * ... RIENCE OF THE SAINTS OF GOD TO THE SAME PURPOSE. **IV.** LET US, then, in the fourth place, as a fourth ev ...

### 8. `VIII.`
* **Description:** List sequence starts at 8 instead of 1
* **Chapter:** *The Giving & Establishing of the New Covenant*
* **Contexts:**
  * ... OATH OF GOD ENGAGED IN THE CONFIRMATION THEREOF. **VIII.** ANOTHER evidence hereof may be taken from the mak ...

### 9. `2. ... 5.`
* **Description:** List sequence jump (skipped from 2 to 5)
* **Chapter:** *The Name of God Confirming the Truth and Reality of Forgiveness With Him*
* **Contexts:**

### 10. `X.`
* **Description:** List sequence starts at 10 instead of 1
* **Chapter:** *The Name of God Confirming the Truth and Reality of Forgiveness With Him*
* **Contexts:**
  * ... HE SAME IS DONE BY THE PROPERTIES OF HIS NATURE. **X.** ANOTHER foundation of this truth, and infallible ...

### 11. `XII.`
* **Description:** List sequence starts at 12 instead of 1
* **Chapter:** *Forgiveness Manifested in the Sending of the Son of God to Die for Sin*
* **Contexts:**
  * ... OBLIGATION THAT IS ON US TO FORGIVE ONE ANOTHER. **XII.** IN the next place we shall proceed unto that evid ...

### 12. `3.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Evidences That Most Men Do Not Believe Forgiveness.*
* **Contexts:**
  * ... a great part of the books of the New Testament. **3.** It is a duty, as we have showed, of the greatest ...
  * ... covenants, as God himself declares, Hebrews 8:7-1**3.** Now, a very easy consideration of the ways and wa ...
  * ... aintance with the mystery of gospel forgiveness. **3.** Let it be inquired of them who pretend unto this ...

### 13. `2. ... 7.`
* **Description:** List sequence jump (skipped from 2 to 7)
* **Chapter:** *Evidences That Most Men Do Not Believe Forgiveness.*
* **Contexts:**

### 14. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Rule 2.*
* **Contexts:**
  * RULE **2.** Self-condemnation and abhorrency for sin consist ...
  * ... e him beneath the assurance sought after. And, — **2.** I shall speak somewhat of its nature, especially ...
  * ... ng that all the heirs of promise should receive. **2.** Evangelical assurance is not a thing that consist ...

### 15. `4.`
* **Description:** List sequence starts at 4 instead of 1
* **Chapter:** *Rule 4.*
* **Contexts:**
  * ... is duty, which must be farther spoken unto. RULE **4.** Remove the hinderances of believing by a searchi ...

### 16. `5.`
* **Description:** List sequence starts at 5 instead of 1
* **Chapter:** *Rule 5.*
* **Contexts:**
  * ... undoubtedly hinder and interrupt our peace. RULE **5.** The fifth rule — Distinction between unbelief an ...

### 17. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Rule 6.*
* **Contexts:**
  * ... im to hide, withdraw, or absent himself from it. **2.** Unbelief, that works by questioning of the promis ...
  * ... forgiveness of sin that we are treating of; and, **2.** Grace of sanctification from God in Christ. Of ea ...
  * ... in due time will cause it to bring forth peace. **2.** The like may be said concerning the other head of ...

### 18. `2. ... 6.`
* **Description:** List sequence jump (skipped from 2 to 6)
* **Chapter:** *Rule 6.*
* **Contexts:**

### 19. `8.`
* **Description:** List sequence starts at 8 instead of 1
* **Chapter:** *Rule 8.*
* **Contexts:**
  * ... s the life of a believer, Ephesians 2:8-10. RULE **8.** The eighth rule — Spend not time in heartless co ...

### 20. `9.`
* **Description:** List sequence starts at 9 instead of 1
* **Chapter:** *Rule 9.*
* **Contexts:**
  * ... l together in the same soul and conscience. RULE **9.** The ninth rule — Take heed of undue expressions ...

### 21. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Objections From the Present State and Condition of the Soul*
* **Contexts:**
  * ... w, whereas we were blind by nature, now we see." **2.** Even in this matter also, we must, it may be, be ...
  * ... s necessary; to know it, sometimes a temptation (**2.**) Even duties of God's appointment, when turned in ...
  * ... of all is a great sign of somewhat in the soul. **2.** As to what was alleged as to the nothingness, the ...

### 22. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *God the Proper Object of the Soulìs Waiting in Its Distresses and Depths.*
* **Contexts:**
  * ... as the most blessed course for his deliverance. **2.** Remember that diligent use of the means for the e ...
  * ... rom, — 1. The absence of God from the soul; and, **2.** From his displeasure. 1. The absence of God from ...
  * ... ith the Lord, "when I depart from them!" Hosea 9:1**2.** And this woe, this sorrow, doth not attend only a ...

### 23. `1. ... 5.`
* **Description:** List sequence jump (skipped from 1 to 5)
* **Chapter:** *Considerations of God, Rendering Our Waiting on Him Reasonable and Necessary:*
* **Contexts:**

---

## Invalid Bible References

### 1. `Philippians 38`
* **Description:** Invalid Bible reference (chapter 38 exceeds max 4 for Philippians)
* **Chapter:** *Chapter 3.*
* **Contexts:**
  * ... n us to will and to do of his own good pleasure," **Philippians 38**:13 2:13; he works "all our works in us," Isaiah 2 ...

### 2. `Jude 4`
* **Description:** Invalid Bible reference (chapter 4 exceeds max 1 for Jude)
* **Chapter:** *Chapter 9.*
* **Contexts:**
  * ... e "turning of the grace of God into wantonness;" (**Jude 4**.) yet I doubt not but, through the craft of Satan ...

### 3. `Philippians 20`
* **Description:** Invalid Bible reference (chapter 20 exceeds max 4 for Philippians)
* **Chapter:** *Forgiveness Manifested in the Sending of the Son of God to Die for Sin*
* **Contexts:**
  * ... l flesh," Romans 8:3; in "the form of a servant," **Philippians 20**:7 2:7; being "made of a woman, made under the law ...

---

## List Formatting Inconsistencies

No anomalies found in this category.

