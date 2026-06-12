# Text Integrity & Anomaly Audit Report: Volume 9

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 309031
* **Total Suspected Anomalies Found:** 158

Add corrections to `text_replacements` inside `volumes/v9/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 36 items
* **Punctuation Spacing Blemishes:** 65 items
* **OCR & Bracket Residues:** 0 items
* **Mixed-Case Capitalization Errors:** 0 items
* **Unresolved Citation References:** 0 items
* **Structural Nesting Sequence Jumps:** 45 items
* **Invalid Bible References:** 12 items
* **List Formatting Inconsistencies:** 0 items

---

## Hyphenation Anomalies

### 1. `Beth-arbel`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Sermon - Seasonable Words for English Protestants.*
* **Contexts:**
  * ... and smite, as in the day wherein "Shalman spoiled **Beth-arbel**," and "the mother was dashed in pieces upon her c ...

### 2. `short-hand`
* **Description:** Splittable word (rejoins to valid word 'shorthand')
* **Chapter:** *Prefatory Note (Posthumous Sermons - Part 2)*
* **Contexts:**
  * ... n London, and was in the habit of taking notes in **short-hand** of his sermons, which he afterwards transcribed i ...

### 3. `a-work`
* **Description:** Splittable word (rejoins to valid word 'awork')
* **Chapter:** *Sermon 1.*
* **Contexts:**
  * ... hey are quite cast down, then they set themselves **a-work** to get up; and when they are up to any comfortabl ...

### 4. `stout-hearted`
* **Description:** Splittable word (rejoins to valid word 'stouthearted')
* **Chapter:** *Sermon 2.*
* **Contexts:**
  * ... up the soul. So Isaiah 46:12, "Hearken to me, ye **stout-hearted**, that are far from righteousness." Here are two n ...
  * ... hteousness." Here are two notable qualifications, **stout-hearted**ness, and remoteness from righteousness. What sai ...

### 5. `stout-heartedness`
* **Description:** Splittable word (rejoins to valid word 'stoutheartedness')
* **Chapter:** *Sermon 2.*
* **Contexts:**
  * ... hteousness." Here are two notable qualifications, **stout-heartedness**, and remoteness from righteousness. What saith G ...

### 6. `new-fangled`
* **Description:** Splittable word (rejoins to valid word 'newfangled')
* **Chapter:** *Sermon 5.*
* **Contexts:**
  * ... God; and so suppose the times ruined, since this **new-fangled** preaching came up amongst you; — desiring to hear ...

### 7. `plain-hearted`
* **Description:** Splittable word (rejoins to valid word 'plainhearted')
* **Chapter:** *Sermon 6.*
* **Contexts:**
  * ... , which we have rendered, "a plain man;" that is, **plain-hearted**, without guile, — as Christ speaks of Nathanael. ...

### 8. `Earthly-mindedness`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Sermon 13.*
* **Contexts:**
  * ... greatest hinderance to the promotion of holiness. **Earthly-mindedness**, pride of spirit, elation above our brethren, sel ...

### 9. `stout-hearted`
* **Description:** Splittable word (rejoins to valid word 'stouthearted')
* **Chapter:** *Sermon 16.*
* **Contexts:**
  * ... UBTITLE]] HUMAN POWER DEFEATED. [[SUMMARY]] "The **stout-hearted** are spoiled, they have slept their sleep; and non ...
  * ... To their explication: — 1. To the reading: The "**stout-hearted**;" or, the "strong in heart," the "mighty in heart ...
  * ... ormer success, and on he will go to his ruin. The **stout-hearted** men (for a delivery from whose fury and folly we ...

### 10. `Stubborn-hearted`
* **Description:** Splittable word (rejoins to valid word 'Stubbornhearted')
* **Chapter:** *Sermon 16.*
* **Contexts:**
  * ... , ἀσύνετοι τῇ καρδίᾳ, — "the, foolish in heart." **Stubborn-hearted** men are foolish-hearted men: not to yield unto, i ...

### 11. `man-slayer`
* **Description:** Splittable word (rejoins to valid word 'manslayer')
* **Chapter:** *Sermon 16.*
* **Contexts:**
  * ... 3:15, Πᾶς ἀνθρωποκτόνος οὐκ ἔχει ζωὴν, — " Every **man-slayer** hath not life, — that is, "none hath." And so you ...

### 12. `after-drops`
* **Description:** Splittable word (rejoins to valid word 'afterdrops')
* **Chapter:** *Sermon 16.*
* **Contexts:**
  * ... because indeed I look upon this late mercy as the **after-drops** of a former refreshing shower, — as an appendix o ...

### 13. `gazing-stock`
* **Description:** Splittable word (rejoins to valid word 'gazingstock')
* **Chapter:** *Sermon 17.*
* **Contexts:**
  * ... ing? He tells you, verses 33, 34, "Ye were made a **gazing-stock**, by reproaches and afflictions, and the spoiling ...

### 14. `wine-bibber`
* **Description:** Splittable word (rejoins to valid word 'winebibber')
* **Chapter:** *Sermon 18.*
* **Contexts:**
  * ... ehend, or tongue to express. He was reproached as **wine-bibber** and a glutton; as a seditious person and mover of ...

### 15. `house-top`
* **Description:** Splittable word (rejoins to valid word 'housetop')
* **Chapter:** *Sermon 19.*
* **Contexts:**
  * ... sert. I watch, and am as a sparrow alone upon the **house-top**. Mine enemies reproach me all the day; and they t ...

### 16. `stout-hearted`
* **Description:** Splittable word (rejoins to valid word 'stouthearted')
* **Chapter:** *Sermon 19.*
* **Contexts:**
  * ... eir pressures. Isaiah 46:12, "Hearken unto me, ye **stout-hearted**, that are far from righteousness." Persons that t ...

### 17. `days-man`
* **Description:** Splittable word (rejoins to valid word 'daysman')
* **Chapter:** *Sermon 20.*
* **Contexts:**
  * ... t hath a secret respect unto Jesus Christ, as the **days-man** or umpire between God and the soul, and as him by ...

### 18. `two-fold`
* **Description:** Splittable word (rejoins to valid word 'twofold')
* **Chapter:** *Sermon 23.*
* **Contexts:**
  * ... y vow and covenant. Now, we are all of us under a **two-fold** dedication to God, — by vow and covenant: the one ...

### 19. `heart-breaking`
* **Description:** Splittable word (rejoins to valid word 'heartbreaking')
* **Chapter:** *Sermon 24.*
* **Contexts:**
  * ... n more? Where are my tears and humiliation? those **heart-breaking** sighs and groans after God which my heart was onc ...

### 20. `anti-type`
* **Description:** Splittable word (rejoins to valid word 'antitype')
* **Chapter:** *Sermon 25.*
* **Contexts:**
  * ... he type; but of Babylon, Rome, Antichrist, in the **anti-type**. And the verses from 11 to 15 express the gatheri ...

### 21. `world-like`
* **Description:** Splittable word (rejoins to valid word 'worldlike')
* **Chapter:** *Sermon 26.*
* **Contexts:**
  * ... religion, and the performance of duties, under a **world-like** conversation, are nothing but a sophistical means ...

### 22. `over-valuation`
* **Description:** Splittable word (rejoins to valid word 'overvaluation')
* **Chapter:** *Sermon 29.*
* **Contexts:**
  * ... the world, temptations, or selflove, comes in, or **over-valuation** of our relations, and indisposes them again, and ...

### 23. `well-head`
* **Description:** Splittable word (rejoins to valid word 'wellhead')
* **Chapter:** *Discourse 4.*
* **Contexts:**
  * ... an unto, and abide as much as we are able at, the **well-head** of life. Christ is the spring of our spiritual li ...
  * ... ntion how we should approach unto and lie at this **well-head** of life, let me observe to you this one thing, — ...
  * ... weariness as spoken), we are to abide more at the **well-head** of life. It is the direction of our Lord Jesus Ch ...

### 24. `long-hand`
* **Description:** Splittable word (rejoins to valid word 'longhand')
* **Chapter:** *Prefatory Note (Posthumous Sermons - Part 3)*
* **Contexts:**
  * ... , and then took the pains to transcribe them into **long-hand**; as thinking them worthy of being transmitted dow ...

### 25. `Day-spring`
* **Description:** Splittable word (rejoins to valid word 'Dayspring')
* **Chapter:** *Sermon 1.*
* **Contexts:**
  * ... ess that ariseth," Malachi 4:2; he is called "The **Day-spring** from on high," Luke 1:78; and he is called "The b ...
  * ... on 22:16. He is both a sun, and morning star, and **day-spring**. He shall be as the morning, that brings light, c ...

### 26. `out-balance`
* **Description:** Splittable word (rejoins to valid word 'outbalance')
* **Chapter:** *Sermon 1.*
* **Contexts:**
  * ... ing relief against temporal distresses will quite **out-balance** them. How is this everlasting? It is everlasting ...

### 27. `Padan-aram`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Sermon 2.*
* **Contexts:**
  * ... 3, 4: — Isaac was sending away his son Jacob unto **Padan-aram**, to take him a wife; and he might easily know, an ...

### 28. `merchant-man`
* **Description:** Splittable word (rejoins to valid word 'merchantman')
* **Chapter:** *Sermon 6*
* **Contexts:**
  * ... r. 1. In a way of value. Matthew 13:45, when the **merchant-man** had found the precious pearl, he sells all he hat ...

### 29. `Bar-jona`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Sermon 8.*
* **Contexts:**
  * ... swered and said unto him, Blessed art thou, Simon **Bar-jona**: for flesh and blood hath not revealed it unto th ...

### 30. `stout-hearted`
* **Description:** Splittable word (rejoins to valid word 'stouthearted')
* **Chapter:** *Sermon 10.*
* **Contexts:**
  * ... a reverential fear." There is no man that is not **stout-hearted** and far from righteousness, but is, upon God's wa ...

### 31. `Earthly-mindedness`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Sermon 10.*
* **Contexts:**
  * ... among ourselves, and division in churches. [4.] **Earthly-mindedness**, and love of the world, and conformity to it, tha ...

### 32. `co-pastor`
* **Description:** Splittable word (rejoins to valid word 'copastor')
* **Chapter:** *Prefatory Note (Posthumous Sermons - Part 4)*
* **Contexts:**
  * ... , an excellent and useful minister in London, the **co-pastor** and successor of the Reverend Thomas Bradbury, in ...

### 33. `short-hand`
* **Description:** Splittable word (rejoins to valid word 'shorthand')
* **Chapter:** *Preface (Posthumous Sermons - Part 4)*
* **Contexts:**
  * ... ears since, — namely, they were at first taken in **short-hand** from the Doctor's mouth, and, by the late Sir Joh ...

### 34. `long-hand`
* **Description:** Splittable word (rejoins to valid word 'longhand')
* **Chapter:** *Preface (Posthumous Sermons - Part 4)*
* **Contexts:**
  * ... Cooke's pious grandfather, were transcribed into **long-hand**. Mr Matthew Henry has this note in his annotatio ...

### 35. `evil-doer`
* **Description:** Splittable word (rejoins to valid word 'evildoer')
* **Chapter:** *Discourse 12.*
* **Contexts:**
  * ... one suffer as a murderer, or as a thief, or as an **evil-doer**," etc.; "yet if any man suffer as a Christian, le ...

### 36. `spring-head`
* **Description:** Splittable word (rejoins to valid word 'springhead')
* **Chapter:** *Discourse 22.*
* **Contexts:**
  * ... ad no conjecture of. Yet this is the fountain and **spring-head**; and all such things as love in the old and new c ...

---

## Punctuation Spacing Blemishes

### 1. `them ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon - Seasonable Words for English Protestants.*
* **Contexts:**
  * ... rd them," (until he had brought his judgment upon **them ;**) — "though Moses and Samuel stood before me, I wi ...

### 2. `things :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 1.*
* **Contexts:**
  * ... treating upon this subject, I shall do these two **things :** — [[ROMANHEAD]] I. Explain the terms of the prop ...

### 3. `him ?`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 1.*
* **Contexts:**
  * ... would we have that our believing is acceptable to **him ?** It is said, Hebrews 10:38, "If any man draw back ...

### 4. `things ?`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 2.*
* **Contexts:**
  * ... ture. "How, then, will he show and manifest these **things ?**" See Isaiah 55:7, He will have mercy: he is love, ...

### 5. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 2.*
* **Contexts:**
  * ... g, I desire to add the following observations: — **1st .** I acknowledge that all that can be said, by all o ...
  * ... nts. Two things, then, may hence be deducted: — **1st .** The willingness of God that we should be establis ...

### 6. `4thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 2.*
* **Contexts:**
  * ... n closing with his faithfulness in his promises. **4thly .** Observe who it is of whom I am speaking. It is be ...

### 7. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 2.*
* **Contexts:**
  * ... ter security can we expect or desire? So that, — **2dly .** All unbelief must needs be at length totally reso ...

### 8. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 4*
* **Contexts:**
  * ... hey are the things on which the whole doth turn. **3dly .** As always from the foundation of the world, so in ...

### 9. `Use .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 5.*
* **Contexts:**
  * ... hatred of reformation, that is found amongst us? **Use .** If there be so many things required to walking wi ...

### 10. `2dly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 6.*
* **Contexts:**
  * ... as one from whom we receive, — 1st., Direction; **2dly ,** Protection; 3dly , Examination and trial. 1st.. ...

### 11. `3dly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 6.*
* **Contexts:**
  * ... receive, — 1st., Direction; 2dly , Protection; **3dly ,** Examination and trial. 1st.. Direction. So before ...

### 12. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 6.*
* **Contexts:**
  * ... us, and we shall have direction, Proverbs 22:12. **2dly .** Protection in our walking in our obedience: Psalm ...

### 13. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 6.*
* **Contexts:**
  * ... he lays at the bottom of all their deliverance. **3dly .** For trial and examination: Psalm 11:4, 5, His e ...

### 14. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Sermon 6.*
* **Contexts:**
  * **..**. y , Protection; 3dly , Examination and trial. 1st**..** Direction. So before, — " I will guide thee with **..**.

### 15. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 7.*
* **Contexts:**
  * ... point all men's attempts for walking with God: — **1st .** That men without it will go forth, somewhat, at l ...
  * ... the receiving of it sweet and easy to us; as, — **1st .** That he doth not correct us for his pleasure, but ...

### 16. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 7.*
* **Contexts:**
  * ... subjection to the law of grace whereof we speak. **2dly .** His obedience will build him up in that state whe ...
  * ... nt we may rest on his sovereign will and wisdom. **2dly .** That he will make all things work together for ou ...

### 17. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 7.*
* **Contexts:**
  * ... provement, why should they not be welcome to us? **3dly .** That conformity and likeness to Jesus Christ is h ...

### 18. `comes ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 10.*
* **Contexts:**
  * ... . He who thus comes is the King of saints, and he **comes ,**as the King of saints, — he comes to exert his reg ...

### 19. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 11.*
* **Contexts:**
  * ... g pleads with his saints. One or more of them: — **1st .** On the account of some secret lusts that have def ...
  * ... his own, on these accounts, are also various: — **1st .** He doth it by the afflictions, trials, and troubl ...

### 20. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 11.*
* **Contexts:**
  * ... eaves not until their dross and tin be consumed. **2dly .** On the account of some way or ways wherein they m ...
  * ... n hath unto these ends are commonly spoken unto. **2dly .** He doth it by pouring out of his Spirit in a sing ...

### 21. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 11.*
* **Contexts:**
  * ... acts as refiner's fire," and as "fullers' soap." **3dly .** On the account of inordinate cleaving unto the sh ...

### 22. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 11.*
* **Contexts:**
  * ... ore scattered abroad? Is not the contrary true?" **Ans .** It cannot be denied but that many grievous and en ...

### 23. `world !`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 12.*
* **Contexts:**
  * ... little difference between them and the men of the **world !** How like to one another! What oneness is found in ...

### 24. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 12.*
* **Contexts:**
  * ... esent business. Jehu's spirit spoiled his work. **2dly .** There is a particular end that regulates the publ ...

### 25. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 13.*
* **Contexts:**
  * ... oly conversation and godliness?" But consider, — **1st .** What success this design prosecuted hath had in o ...

### 26. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 13.*
* **Contexts:**
  * ... on, and was thereon blasted and rejected of God! **2dly .** God can suffer temptation to pursue us into a wil ...
  * ... gland out of the hand of the Lord, Joshua 22:31. **2dly .** In that it may be an effectual means for the refo ...
  * ... tongues, that work not out the glory of Christ. **2dly .** Thereby we bear witness unto what sort of kingdom ...

### 27. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 13.*
* **Contexts:**
  * ... to expect under them, that we are to look after. **3dly .** Not our communion [our intercourse with men], but ...
  * ... of a nation; — and this the only means of that. **3dly .** This is the most effectual way of standing in the ...
  * ... the ignorance of foolish men is put to silence. **3dly .** This brings honor unto Christ, and glorifies him ...

### 28. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 14.*
* **Contexts:**
  * ... r own lusts are the immediate cause of it; as, — **1st .** They shall have some prejudices against them by w ...

### 29. `ground ?`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 16.*
* **Contexts:**
  * ... aith in his heart, Who shall bring me down to the **ground ?**" Obadiah 1:3. Was it not the ruin of Amaziah, of ...

### 30. `ground !`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 16.*
* **Contexts:**
  * ... rch." Their voice was, "Down with it! even to the **ground !**" Poor creatures! they dashed themselves against t ...

### 31. `Ah !`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 16.*
* **Contexts:**
  * ... God, if not seasoned with grace and watchfulness. **Ah !** how many baits have Satan and the world suited to ...

### 32. `Observation .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 16.*
* **Contexts:**
  * ... owing narration, to afford us this observation: — **Observation .** The care of Salem, of Zion, lies at the bottom of ...
  * ... 2. And these also have their particular mention. **Observation .** In the deliverance of his people, God hath a spec ...

### 33. `them ?`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 17.*
* **Contexts:**
  * ... ospel, that we may take care not to be ashamed of **them ?**" I answer, In two things: — (1.) The first is, ...

### 34. `Use .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 18.*
* **Contexts:**
  * ... the gospel, or any duty of it. And that is this:— **Use .** Get an experience of the power of the gospel, and ...

### 35. `Observation .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 19.*
* **Contexts:**
  * ... ak to you, from the words thus opened, is this: — **Observation .** In the most overwhelming, calamitous distresses t ...

### 36. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 19.*
* **Contexts:**
  * ... s Jeremiah was, yet they can say, "God is here." **2dly .** It is so likewise with respect to time. The suffe ...

### 37. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 19.*
* **Contexts:**
  * ... But God is the same through all times and ages. **3dly .** There is relief to be found in God, and only in h ...

### 38. `4thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 19.*
* **Contexts:**
  * ... n the Lord, and joy in the God of my salvation." **4thly .** The last circumstance of distress is death. The w ...

### 39. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 20.*
* **Contexts:**
  * ... f his power; but "Fury is not in me," saith God. **3dly .** It is impossible for faith ever to consider the n ...

### 40. `Use .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 20.*
* **Contexts:**
  * ... oo much time. One word of use, and I have done. **Use .** This is an overwhelming time, — a time wherein ma ...

### 41. `3dly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 23.*
* **Contexts:**
  * ... ith them; 2dly . In the good example they give; **3dly ,** In their industry in the world: — 1st . There is ...

### 42. `Observation .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 23.*
* **Contexts:**
  * ... bservation I shall make from the words is this: — **Observation .** In the most calamitous season, in the greatest in ...

### 43. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 23.*
* **Contexts:**
  * ... ein the people of God are useful in the world: — **1st .** In the secret blessing that goes along with them; ...
  * ... give; 3dly , In their industry in the world: — **1st .** There is a secret blessing goes along with them; ...

### 44. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 23.*
* **Contexts:**
  * ... n the secret blessing that goes along with them; **2dly .** In the good example they give; 3dly , In their i ...

### 45. `it ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 23.*
* **Contexts:**
  * ... ." If that were all, they would not much care for **it ;** — but, "Evil shall come upon them, saith the LORD ...

### 46. `fear ?`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 24.*
* **Contexts:**
  * ... r from thy ways, and hardened our hearts from thy **fear ?**' And then, V. What is to be done for relief in t ...

### 47. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 24.*
* **Contexts:**
  * ... 1st. They are the vain imaginations of the mind; **2dly .** The corrupt actings of the affections of the hear ...
  * ... ect of the eye, and sight, and knowledge of God. **2dly .** The corrupt actings and desires of our affections ...

### 48. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 24.*
* **Contexts:**
  * ... upt actings of the affections of the heart; and, **3dly .** A frame of soul suited unto them. These are the t ...
  * ... e corrupt desires and actings of our affections. **3dly .** And both these, if indulged in any measure, will ...

### 49. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Sermon 24.*
* **Contexts:**
  * **..**. hese are the things I intend by secret sins: — 1st**..** The vain imaginations of the mind. The Holy Ghost **..**.

### 50. `Observation .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 25.*
* **Contexts:**
  * ... speak a little very briefly and plainly to it: — **Observation .** A diligent search into, and consideration of, the ...

### 51. `III .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Sermon 25.*
* **Contexts:**
  * ... art to her bulwarks, consider her palaces," etc. **III .** What are those causes and means of the church's p ...

### 52. `delivered ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Discourse 11.*
* **Contexts:**
  * ... were set up, and they that tempted God were even **delivered ;**" that is, "appeared to be delivered." It is the g ...

### 53. `One ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 1.*
* **Contexts:**
  * ... r, "He that rules in the human nature is the Just **One ;**" or, "He that rules over the human nature" (in al ...

### 54. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 1.*
* **Contexts:**
  * ... ordered in all the things "of sin on our part." **1st ,** It is ordered in all the things "of grace on the ...

### 55. `of ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 3.*
* **Contexts:**
  * ... e are more eyes upon thee that thou takest notice **of ;** — God is present, Christ is present, the elect an ...

### 56. `it ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Sermon 13.*
* **Contexts:**
  * ... it; [3.] How the ruin of churches is hastened by **it ;** — which will befall them assuredly, unless God re ...

### 57. `Christ ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Discourse 3.*
* **Contexts:**
  * ... ncipal things to be regarded in this obedience of **Christ ;** — the love wherewith it was rincipled. Galatians ...

### 58. `spitting ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Discourse 3.*
* **Contexts:**
  * ... de himself, nor turn away his face from shame and **spitting ;** — one was this, "Father, thy will be done," saith ...

### 59. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Discourse 3.*
* **Contexts:**
  * ... ortably into that state, is a pure act of faith. **2dly .** It is unchangeable. It is a state wherein there i ...

### 60. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Discourse 3.*
* **Contexts:**
  * **..**. perties that make this a great act of faith: — 1st**..** The state is invisible. The soul is going into a **..**.

### 61. `darkness ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Discourse 4.*
* **Contexts:**
  * ... w," saith Christ, "is your hour, and the power of **darkness ;**" — "He comes to try what he can do." And what was ...

### 62. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Discourse 5.*
* **Contexts:**
  * ... ntecedent remembrance that God is in that place. **2dly .** We are to remember the gracious presence of God. ...

### 63. `sin ?`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Discourse 6.*
* **Contexts:**
  * ... O Lord, is this the effect of sin? is all this in **sin ?**" Here, then, take a view of sin. Others look on i ...

### 64. `representation ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Discourse 14.*
* **Contexts:**
  * ... ise up to an experience in two things, — [1.] In **representation ;** [2.] In incorporation: — [1.] The thing we are ...

### 65. `Again :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Discourse 20.*
* **Contexts:**
  * ... ng the frame of our souls into his own likeness. **Again :** 2. The love of Christ, if we are affected with it ...

---

## OCR & Bracket Residues

No anomalies found in this category.

## Mixed-Case Capitalization Errors

No anomalies found in this category.

## Unresolved Citation References

No anomalies found in this category.

## Structural Nesting Sequence Jumps

### 1. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Sermon 2.*
* **Contexts:**
  * [[CHAPTER]] SERMON **2.** THE use of the point insisted on is, to encourag ...
  * ... way which himself hath appointed and approved? (**2.**) As is his name, so is his nature. Saith he of hi ...
  * ... his love in God, Hosea 11:8, 9; Jeremiah 31:20. [**2.**] His condescension to entreat us that it may be s ...

### 2. `3.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Sermon 3.*
* **Contexts:**
  * [[CHAPTER]] SERMON **3.** [[SUMMARY]] THE NATURE AND BEAUTY OF GOSPEL WORS ...
  * ... the children which God hath given me," Hebrews 2:1**3.** This is the access of believers; thus do they ent ...
  * ... ave such an access, such a manuduction unto God. **3.** From the immediate object of this worship; and th ...

### 3. `5.`
* **Description:** List sequence starts at 5 instead of 1
* **Chapter:** *Sermon 4*
* **Contexts:**
  * [[CHAPTER]] SERMON 4 **5.** THIS also adds greatly to the glory and excellenc ...
  * ... hter" is said to be "all glorious within," Psalm 4**5.** Whatever men may think, God, that knoweth his ow ...

### 4. `5.`
* **Description:** List sequence starts at 5 instead of 1
* **Chapter:** *Sermon 5.*
* **Contexts:**
  * [[CHAPTER]] SERMON **5.** [[SUMMARY]] OF WALKING HUMBLY WITH GOD. "And to ...
  * ... h, and obtain peace, Romans 5:1; Ephesians 2:14, 1**5.** This, then, I say, in the first place, is requir ...
  * ... n the account of mere grace and mercy, Titus 3:4, **5.** God aims at the exalting of his glory in this, — ...

### 5. `6.`
* **Description:** List sequence starts at 6 instead of 1
* **Chapter:** *Sermon 6.*
* **Contexts:**
  * [[CHAPTER]] SERMON **6.** HAVING told you what things are previously requi ...
  * ... which is Christ," saith the apostle, Galatians 3:1**6.** As it is said, in general, that "he that comes to ...
  * ... ere is no going to the Father but by him, John 14:**6.** They who have believed in God, must be careful to ...

### 6. `7.`
* **Description:** List sequence starts at 7 instead of 1
* **Chapter:** *Sermon 7.*
* **Contexts:**
  * [[CHAPTER]] SERMON **7.** WHAT it is to walk with God hath been declared. ...
  * ... faith," according to the law of grace, Romans 1:1**7.** "They sought it not by faith, but as it were by t ...

### 7. `8.`
* **Description:** List sequence starts at 8 instead of 1
* **Chapter:** *Sermon 8.*
* **Contexts:**
  * [[CHAPTER]] SERMON **8.** WHAT it is to humble ourselves to the law of God ...
  * ... e our understandings thereunto. So Isaiah 40:27, 2**8.** This is that which our hearts are to rest in, whe ...
  * ... s motive, Hebrews 12:29, 4:13. So Deuteronomy 28:5**8.** The excellency of God in itself, is not only suc ...

### 8. `9.`
* **Description:** List sequence starts at 9 instead of 1
* **Chapter:** *Sermon 9.*
* **Contexts:**
  * [[CHAPTER]] SERMON **9.** We have at large considered the nature of this d ...
  * ... kid and the calf, the cow and the ox, Isaiah 11:6-**9.** It is not in our nature to humble ourselves to wa ...
  * ... look for him as one "meek and lowly," Zechariah 9:**9.** And when he calls men to a conformity to his exam ...

### 9. `10.`
* **Description:** List sequence starts at 10 instead of 1
* **Chapter:** *Sermon 10.*
* **Contexts:**
  * [[CHAPTER]] SERMON **10.** [[SUMMARY]] PROVIDENTIAL CHANGES, AN ARGUMENT FO ...

### 10. `3. ... 16.`
* **Description:** List sequence jump (skipped from 3 to 16)
* **Chapter:** *Sermon 10.*
* **Contexts:**

### 11. `2. ... 11.`
* **Description:** List sequence jump (skipped from 2 to 11)
* **Chapter:** *Sermon 10.*
* **Contexts:**

### 12. `11.`
* **Description:** List sequence starts at 11 instead of 1
* **Chapter:** *Sermon 11.*
* **Contexts:**
  * [[CHAPTER]] SERMON **11.** 2. THE second ground is, because every such day ...
  * ... it in such a day to the purpose, Revelation 16:10 **11.** Christ will providentially suffer occasions, adva ...
  * ... gs, shall at length be forced so to do, Isaiah 26:**11.** These things being premised, one principal inqui ...

### 13. `2. ... 11.`
* **Description:** List sequence jump (skipped from 2 to 11)
* **Chapter:** *Sermon 11.*
* **Contexts:**

### 14. `12.`
* **Description:** List sequence starts at 12 instead of 1
* **Chapter:** *Sermon 12.*
* **Contexts:**
  * [[CHAPTER]] SERMON **12.** Use 1. Of trial or examination. Hath Christ for ...

### 15. `14.`
* **Description:** List sequence starts at 14 instead of 1
* **Chapter:** *Sermon 14.*
* **Contexts:**
  * [[CHAPTER]] SERMON **14.** [[SUMMARY]] THE SIN AND JUDGMENT OF SPIRITUAL BA ...
  * ... s to be converted, and brought home to God, verse **14.** So at Athens, chapter 17:34. And the apostle affi ...

### 16. `15.`
* **Description:** List sequence starts at 15 instead of 1
* **Chapter:** *Sermon 15.*
* **Contexts:**
  * [[CHAPTER]] SERMON **15.** WE shall now proceed to the uses. Use 1. Wonder ...

### 17. `16.`
* **Description:** List sequence starts at 16 instead of 1
* **Chapter:** *Sermon 16.*
* **Contexts:**
  * [[PART]] SERMON **16.** [[SUBTITLE]] HUMAN POWER DEFEATED. [[SUMMARY]] ...
  * ... women, — they shall be afraid and fear, Isaiah 19:**16.** Yea, this is the way of God's usual dealing; fir ...
  * ... nified therein; as is fully set out, Exodus 15:14-**16.** The hearts and spirits of men are all in the hand ...

### 18. `17.`
* **Description:** List sequence starts at 17 instead of 1
* **Chapter:** *Sermon 17.*
* **Contexts:**
  * [[PART]] SERMON **17.** [[SUBTITLE]] THE DIVINE POWER OF THE GOSPEL. [ ...

### 19. `18.`
* **Description:** List sequence starts at 18 instead of 1
* **Chapter:** *Sermon 18.*
* **Contexts:**
  * [[PART]] SERMON **18.** 3. We are not to be ashamed of the professors o ...

### 20. `III.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Sermon 18.*
* **Contexts:**
  * ... sing the gospel without showing the power of it. **III.** I shall now give the reasons why we ought not in ...

### 21. `19.`
* **Description:** List sequence starts at 19 instead of 1
* **Chapter:** *Sermon 19.*
* **Contexts:**
  * [[PART]] SERMON **19.** [[SUBTITLE]] GOD THE SAINTS' ROCK. [[SUMMARY]] ...
  * ... h betrothed me unto himself in covenant," Hosea 2:**19.** [[BLOCKQUOTE]] "Could I get through this darknes ...

### 22. `20.`
* **Description:** List sequence starts at 20 instead of 1
* **Chapter:** *Sermon 20.*
* **Contexts:**
  * [[PART]] SERMON **20.** [[SUMMARY]] "From the end of the earth will I c ...

### 23. `I. ... III.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Sermon 24.*
* **Contexts:**

### 24. `II. ... IV.`
* **Description:** List sequence jump (skipped from 2 to 4)
* **Chapter:** *Sermon 25.*
* **Contexts:**

### 25. `II.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Sermon 29.*
* **Contexts:**
  * ... ich, if God will, I shall despatch at this time. **II.** There is required, unto this great end, a readine ...
  * ... lp me so to do; and it is this: — [[ROMANHEAD]] I**II.** Let us take heed of being surprised with death. ...

### 26. `8.`
* **Description:** List sequence starts at 8 instead of 1
* **Chapter:** *Sermon 30.*
* **Contexts:**
  * ... be the greatest offense in the world, Isaiah 8:1 **8.** He had designed him to be a stumbling-block, and ...

### 27. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Discourse 2.*
* **Contexts:**
  * [[PART]] DISCOURSE **2.** Question. Seeing the act of closing with Christ ...
  * ... on from charges of the guilt of sin and the law. **2.** Opposition from temptations unto sin: — 1. There ...
  * ... st opposition. I hope you have experience of it. **2.** There must be a permanency in our choice of Chris ...

### 28. `4.`
* **Description:** List sequence starts at 4 instead of 1
* **Chapter:** *Discourse 4.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **4.** Question. How may we recover from a decay of the ...
  * ... er spiritual life to the glory of God in Christ. **4.** And then, brethren, seeing we have, in the next p ...

### 29. `5.`
* **Description:** List sequence starts at 5 instead of 1
* **Chapter:** *Discourse 5.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **5.** Question. It was queried by some, how we may mak ...

### 30. `7.`
* **Description:** List sequence starts at 7 instead of 1
* **Chapter:** *Discourse 7.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **7.** [[BLOCKQUOTE]] Question. When our own faith is w ...

### 31. `8.`
* **Description:** List sequence starts at 8 instead of 1
* **Chapter:** *Discourse 8.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **8.** [[BLOCKQUOTE]] Question. When may any one sin, l ...

### 32. `9.`
* **Description:** List sequence starts at 9 instead of 1
* **Chapter:** *Discourse 9.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **9.** [[BLOCKQUOTE]] Question. Whether lust or corrupt ...

### 33. `10.`
* **Description:** List sequence starts at 10 instead of 1
* **Chapter:** *Discourse 10.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **10.** [[BLOCKQUOTE]] Question. What shall a person do ...

### 34. `11.`
* **Description:** List sequence starts at 11 instead of 1
* **Chapter:** *Discourse 11.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **11.** [[BLOCKQUOTE]] Question. What is our duty with r ...

### 35. `4.`
* **Description:** List sequence starts at 4 instead of 1
* **Chapter:** *Sermon 4.*
* **Contexts:**
  * [[CHAPTER]] SERMON **4.** [[SUMMARY]] "But all these worketh that one and ...

### 36. `13.`
* **Description:** List sequence starts at 13 instead of 1
* **Chapter:** *Sermon 13.*
* **Contexts:**
  * [[CHAPTER]] SERMON **13.** [[SUMMARY]] THE USE OF FAITH IN A TIME OF GENERA ...

### 37. `3.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Discourse 3.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **3.** [[BLOCKQUOTE]] "The cup of blessing which we ble ...
  * ... obtain a comfortable passage out of it. And, — [**3.**] Even death itself brings a terror with it, that ...
  * ... nding all the difficulties he was to meet with. (**3.**) We are to remember his submission to the great w ...

### 38. `6.`
* **Description:** List sequence starts at 6 instead of 1
* **Chapter:** *Discourse 6.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **6.** [[BLOCKQUOTE]] "But let a man examine himself, a ...
  * ... with God as unto the duty that lies before them. **6.** The time of preparation is to be extended and mad ...

### 39. `12.`
* **Description:** List sequence starts at 12 instead of 1
* **Chapter:** *Discourse 12.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **12.** We are met here to remember, to celebrate, and s ...

### 40. `13.`
* **Description:** List sequence starts at 13 instead of 1
* **Chapter:** *Discourse 13.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **13.** I HAVE generally, on this occasion, fixed on som ...

### 41. `14.`
* **Description:** List sequence starts at 14 instead of 1
* **Chapter:** *Discourse 14.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **14.** [[SUMMARY]] "For I have received of the Lord," e ...

### 42. `16.`
* **Description:** List sequence starts at 16 instead of 1
* **Chapter:** *Discourse 16.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **16.** To whet our minds, and lead us to a particular e ...

### 43. `18.`
* **Description:** List sequence starts at 18 instead of 1
* **Chapter:** *Discourse 18.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **18.** I SHALL offer a few words, with a view to prepar ...

### 44. `19.`
* **Description:** List sequence starts at 19 instead of 1
* **Chapter:** *Discourse 19.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **19.** [[BLOCKQUOTE]] "I am crucified with Christ: neve ...

### 45. `20.`
* **Description:** List sequence starts at 20 instead of 1
* **Chapter:** *Discourse 20.*
* **Contexts:**
  * [[CHAPTER]] DISCOURSE **20.** You have been minded of, and instructed in, the ...

---

## Invalid Bible References

### 1. `2 Kings 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 22 for Kings)
* **Chapter:** *Sermon - Seasonable Words for English Protestants.*
* **Contexts:**
  * ... nst them; — reformation shall not save them." See **2 Kings 23**:25, 26, where there is an account given of the gr ...

### 2. `Philippians 38`
* **Description:** Invalid Bible reference (chapter 38 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 7.*
* **Contexts:**
  * ... s in us "to will and to do of his good pleasure," **Philippians 38**:13 2:13. Whatever a man doth, which God works no ...

### 3. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 9.*
* **Contexts:**
  * ... ," saith the apostle, "that was in Jesus Christ," **Philippians 14**:5 2:5. What mind was this? He describes it in the ...

### 4. `Philippians 20`
* **Description:** Invalid Bible reference (chapter 20 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 17.*
* **Contexts:**
  * ... Christ, that "he made himself of no reputation," **Philippians 20**:7 2:7, 8. He forewent all the esteem he might ha ...

### 5. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 18.*
* **Contexts:**
  * ... e describe the greatness and glory of his person, **Philippians 17**:6 2:6-8, "He made himself," says he, "of no reput ...

### 6. `Philippians 44`
* **Description:** Invalid Bible reference (chapter 44 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 23.*
* **Contexts:**
  * ... f all the saints of God that they be so likewise, **Philippians 44**:15 2:15, "Be harmless in the midst of a crooked a ...

### 7. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 3.*
* **Contexts:**
  * ... he was able to give ministers. See that at large, **Philippians 17**:6 2:6-11. It was his humbling himself unto the d ...

### 8. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 6*
* **Contexts:**
  * ... preeminence above all other loves whatsoever. In **Philippians 17**:6 2:6-8, it is there set forth, where he unites t ...

### 9. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 8.*
* **Contexts:**
  * ... n nature with grace: — [1.] In his divine glory. **Philippians 17**:6 2:6, "Who being in the form of God, thought it ...

### 10. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Sermon 8.*
* **Contexts:**
  * ... that the same mind may be in us that was in him, **Philippians 14**:5 2:5; the same meekness, humility, self-denial, ...

### 11. `Philippians 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 4 for Philippians)
* **Chapter:** *Discourse 3.*
* **Contexts:**
  * ... n his death. The apostle doth propose it unto us, **Philippians 14**:5 2:5, 6, etc., [[BLOCKQUOTE]] "Let this mind be ...

### 12. `Philippians 17`
* **Description:** Invalid Bible reference (chapter 17 exceeds max 4 for Philippians)
* **Chapter:** *Discourse 6.*
* **Contexts:**
  * ... s, and washed us from our sins in his own blood." **Philippians 17**:6 2:6-8, [[BLOCKQUOTE]] "Who, being in the form ...

---

## List Formatting Inconsistencies

No anomalies found in this category.

