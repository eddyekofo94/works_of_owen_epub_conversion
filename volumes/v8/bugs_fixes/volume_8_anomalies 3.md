# Text Integrity & Anomaly Audit Report: Volume 8

This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.

* **Total Words Audited:** 306814
* **Total Suspected Anomalies Found:** 199

Add corrections to `text_replacements` inside `volumes/v8/convert.py` to fix these.

## Summary by Category

* **Hyphenation Anomalies:** 47 items
* **Punctuation Spacing Blemishes:** 94 items
* **OCR & Bracket Residues:** 0 items
* **Mixed-Case Capitalization Errors:** 0 items
* **Unresolved Citation References:** 8 items
* **Structural Nesting Sequence Jumps:** 36 items
* **Invalid Bible References:** 14 items
* **List Formatting Inconsistencies:** 0 items

---

## Hyphenation Anomalies

### 1. `ANGLO-BRITANNORUM`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *Prefatory Note.*
* **Contexts:**
  * ... I CONVENTUI, [[SUBTITLE]] OB [[SUMMARY]] PRISCA **ANGLO-BRITANNORUM** JURA STRENUE ET FIDELITER ASSERTA; LIBERTATEM PAT ...

### 2. `pre-supposeth`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... f the gospel, but not the sending of it, which it **pre-supposeth**: secondly, Against the covenant they are under, a ...

### 3. `Sabbath-breaker`
* **Description:** Splittable word (rejoins to valid word 'Sabbathbreaker')
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... mpieties; for were a man a drunkard, a swearer, a **Sabbath-breaker**, an unclean person, so he were no Puritan, and ha ...

### 4. `eye-salve`
* **Description:** Splittable word (rejoins to valid word 'eyesalve')
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... en know not that they are blind, and seek not for **eye-salve**; they know not that they are dead, and seek not f ...

### 5. `pre-conceptions`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *A Short Defensative*
* **Contexts:**
  * ... able, if men would but a little lay aside beloved **pre-conceptions**. But the printer stays for every line; only I mus ...

### 6. `pre-discoveries`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... r. The prophet having had visions from God, and **pre-discoveries** of many approaching judgments, in the first and s ...

### 7. `lion-like`
* **Description:** Splittable word (rejoins to valid word 'lionlike')
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... iver me from the mouth of the lion," — Nero, that **lion-like** tyrant. And what then? "He shall deliver me from ...

### 8. `Christ-purchased`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... sad reckoning. (2.) In point of ordinances, and **Christ-purchased** privileges. Here it is dangerous encroaching inde ...

### 9. `evil-doer`
* **Description:** Splittable word (rejoins to valid word 'evildoer')
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... God, wound Jesus Christ, and prosecute him as an **evil-doer**? I know the usual colors, the common pleas, that ...

### 10. `slaughter-house`
* **Description:** Splittable word (rejoins to valid word 'slaughterhouse')
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... o a prison, a crown into a cottage, Christ into a **slaughter-house**. And this arises, — [1.] From the nature of fait ...

### 11. `sick-bed`
* **Description:** Splittable word (rejoins to valid word 'sickbed')
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... mfortable and full of joy. Store thy cottage, thy **sick-bed**, by faith, with all sorts of mercies; they are th ...

### 12. `fore-cited`
* **Description:** Splittable word (rejoins to valid word 'forecited')
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... odus 14:21; which the prophet also admires in the **fore-cited** psalm: "The sea saw it, and fled. What ailed thee ...

### 13. `such-like`
* **Description:** Splittable word (rejoins to valid word 'suchlike')
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... ss of blood: — all these, I say, and sundry other **such-like** things as these, are "the Lord's doing, and marve ...

### 14. `home-bred`
* **Description:** Splittable word (rejoins to valid word 'homebred')
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... have wanted them one day longer. Farther, these **home-bred** eruptions were timely seasoned, to rouse the disc ...

### 15. `top-stone`
* **Description:** Splittable word (rejoins to valid word 'topstone')
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... maninvented worship, but either the foundation or **top-stone** is laid in the blood of God's people. "The wisdom ...

### 16. `pre-imaginations`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... yet being come, because not accommodated to their **pre-imaginations**, they rejected him, as having neither form nor co ...

### 17. `such-like`
* **Description:** Splittable word (rejoins to valid word 'suchlike')
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... there a backsliding upon your spirit to these, or **such-like** things as these, the Lord will walk contrary to y ...

### 18. `co-partner`
* **Description:** Splittable word (rejoins to valid word 'copartner')
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... le. That herein the Holy One of Israel is no ways **co-partner** with the guilt of the sons of men, will appear by ...

### 19. `fore-named`
* **Description:** Splittable word (rejoins to valid word 'forenamed')
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... d let this be spoken to the third argument of the **fore-named** reverend persons, from the analogy of delinquenci ...

### 20. `after-reckoning`
* **Description:** Splittable word (rejoins to valid word 'afterreckoning')
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... promote the service of God. Let them not fear an **after-reckoning** who use the discipline of Christ according to his ...

### 21. `co-action`
* **Description:** Splittable word (rejoins to valid word 'coaction')
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... s discourse, I shall, as to any ways of corporeal **co-action** and restraint, oppose some few things. 1st . The ...

### 22. `non-submission`
* **Description:** Splittable word (rejoins to valid word 'nonsubmission')
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... them with any civil penalty in case of refusal or **non-submission**; nor yet did I ever in my life meet with any thin ...

### 23. `Jehovah-nissi`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge*
* **Contexts:**
  * ... in that work, did never sacrifice at the altar of **Jehovah-nissi**, nor consider that the Lord hath sworn to have wa ...

### 24. `mitred-confirmations`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... g and pursuing their unjust conquests, or foolish **mitred-confirmations** of sword-purchases, he got them all framed to his ...

### 25. `under-propping`
* **Description:** Splittable word (rejoins to valid word 'underpropping')
* **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the*
* **Contexts:**
  * ... antics under the windows, that make some show of **under-propping** it: — here you have a magistrate, there an army, ...

### 26. `shittim-wood`
* **Description:** Splittable word (rejoins to valid word 'shittimwood')
* **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the*
* **Contexts:**
  * ... r remission were offered. The other less, made of **shittim-wood**, all overlaid with pure gold, and a crown of beat ...

### 27. `eye-salve`
* **Description:** Splittable word (rejoins to valid word 'eyesalve')
* **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the*
* **Contexts:**
  * ... dviseth the church of Laodicea to come to him for **eye-salve**, that she might see, Revelation 3:18. At his comi ...

### 28. `hog-sty`
* **Description:** Splittable word (rejoins to valid word 'hogsty')
* **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the*
* **Contexts:**
  * ... dwells in a stately palace of his own, show him a **hog-sty**, tell him, "This is your house; here you dwell; t ...

### 29. `Beerlahai-roi`
* **Description:** Capitalized hyphenation with unrecognized left particle
* **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the*
* **Contexts:**
  * ... They may call every spring of their refreshment, **Beerlahai-roi** [The well of Him that liveth and seeth me]. (2dl ...

### 30. `top-stone`
* **Description:** Splittable word (rejoins to valid word 'topstone')
* **Chapter:** *The Laboring Saint's Dismission to Rest.*
* **Contexts:**
  * ... as very rare, who saw the foundation and also the **top-stone** of the temple laid; and yet the work of Jerusalem ...

### 31. `sea-shore`
* **Description:** Splittable word (rejoins to valid word 'seashore')
* **Chapter:** *Christ's Kingdom and the Magistrate's Power.*
* **Contexts:**
  * ... ied like the stars of heaven and the sands of the **sea-shore**, shall possess the gates of their enemies, and sh ...

### 32. `short-sighted`
* **Description:** Splittable word (rejoins to valid word 'shortsighted')
* **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.*
* **Contexts:**
  * ... ence to them may lie therein. Alas! we are poor, **short-sighted** creatures; we know nothing that is before us, — m ...

### 33. `pole-star`
* **Description:** Splittable word (rejoins to valid word 'polestar')
* **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.*
* **Contexts:**
  * ... ll not wonder if you err in your ways. It is your **pole-star**, and will be so, by which your whole course is to ...
  * ... my directions: — (2.) Make this work of God your **pole-star**, that you may steer and guide your course by it. ...

### 34. `pre-required`
* **Description:** Hyphenated word with unrecognized particles on both sides
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * ... itherto taken care for us. This, then, I say, is **pre-required**, as a qualification of any person to the performa ...

### 35. `Giles-inthe`
* **Description:** Capitalized hyphenation with unrecognized right particle
* **Chapter:** *Prefatory Note (Sermon 7 — Advantage of the Kingdom of Christ)*
* **Contexts:**
  * ... of them may be given: — "The Morning Exercise at **Giles-inthe**-Fields, May 1655, printed for Richard Gibbs, in C ...

### 36. `busy-body`
* **Description:** Splittable word (rejoins to valid word 'busybody')
* **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.*
* **Contexts:**
  * ... so to do, unless he design the just reproach of a **busy-body** for his reward. The command is general, with resp ...

### 37. `hard-heartedness`
* **Description:** Splittable word (rejoins to valid word 'hardheartedness')
* **Chapter:** *Except.*
* **Contexts:**
  * ... s their actual unbelief to be the effect of their **hard-heartedness**; which, though it might be judicial, they being l ...

### 38. `deutero-canonical`
* **Description:** Splittable word (rejoins to valid word 'deuterocanonical')
* **Chapter:** *Except.*
* **Contexts:**
  * ... Papists to the Old Testament, and called by them "**deutero-canonical**," and by us no better still than "apocryphal," su ...

### 39. `how-ever`
* **Description:** Splittable word (rejoins to valid word 'however')
* **Chapter:** *The Chamber of Imagery in the Church of Rome Laid Open.*
* **Contexts:**
  * ... be its efficacy unto all the proper ends of it — **how-ever** it be ordered according unto the prescription of ...

### 40. `over-numerous`
* **Description:** Splittable word (rejoins to valid word 'overnumerous')
* **Chapter:** *The Chamber of Imagery in the Church of Rome Laid Open.*
* **Contexts:**
  * ... ey call them, or a surcharge of friars from their **over-numerous** fraternities, upon their errands into remote nati ...

### 41. `foot-breadth`
* **Description:** Splittable word (rejoins to valid word 'footbreadth')
* **Chapter:** *The Chamber of Imagery in the Church of Rome Laid Open.*
* **Contexts:**
  * ... rights or enjoyments, nor gave to his apostles a **foot-breadth** of inheritance among them. But upon this grant, t ...

### 42. `god-like`
* **Description:** Splittable word (rejoins to valid word 'godlike')
* **Chapter:** *The Chamber of Imagery in the Church of Rome Laid Open.*
* **Contexts:**
  * ... st, and good: but, since the ascription of such a **god-like** authority unto men, as to secure blind obedience ...
  * ... emolish this cursed image, or the ascription of a **god-like** power unto men to require blind obedience unto th ...

### 43. `such-like`
* **Description:** Splittable word (rejoins to valid word 'suchlike')
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... ng the best cause, as they suppose; and with many **such-like** notions are the minds of men possessed. But the t ...

### 44. `fore-signify`
* **Description:** Splittable word (rejoins to valid word 'foresignify')
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... unt of these things, as they were to foretell and **fore-signify** the fatal destruction of Jerusalem, is given us b ...

### 45. `over-neglect`
* **Description:** Splittable word (rejoins to valid word 'overneglect')
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... zeal, what exercise of all gospel grace, with the **over-neglect** of these things among many, — it would take up a ...

### 46. `stout-heartedness`
* **Description:** Splittable word (rejoins to valid word 'stoutheartedness')
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... ections may be made use of: — First. Take heed of **stout-heartedness**, and a contempt or neglect thereby of divine warn ...

### 47. `stout-hearted`
* **Description:** Splittable word (rejoins to valid word 'stouthearted')
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... ections may be made use of: — First. Take heed of **stout-hearted**ness, and a contempt or neglect thereby of divine ...
  * ... either really or in pretense, are bold, fearless, **stout-hearted**, regardless of these things; they seem to provoke ...

---

## Punctuation Spacing Blemishes

### 1. `D .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Prefatory Note.*
* **Contexts:**
  * ... nder their handwriting. H. ELSYINGE, Cler. Parl. **D .** Com.

### 2. `sight ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... nt. Even so, Father; for so it seemed good in thy **sight ;**" and with Acts 14:16, — he "suffered all nations ...

### 3. `indignity ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... clear it. There is, then, a twofold demerit and **indignity ;** — one merely negative, or a not deserving to have ...

### 4. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... iration, and a little after violently assaulted. **1st ,** In the first way, how do we find the Jews putting ...

### 5. `Behold ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... 13:41, Paul concludes his sermon to thorn with, "**Behold ,** ye despisers, and wonder, and perish;" — and vers ...

### 6. `2dly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... the martyrs of Jesus that suffered amongst them! **2dly ,** After some continuance. So the Church of Laodicea ...
  * ... s and glorious fancies, became head of that fatal **2dly ,** After some continuance. So the Church of Laodicea ...

### 7. `3dly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... not professedly found in any party amongst us. **3dly ,** Which was worst of all, they had centred in their ...

### 8. `old :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... hout him are liars, like the devil, who was so of **old :** — he is the Life; (John 1:3-5; Ephesians 4:18; Jo ...

### 9. `from ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... age than any by your means we have been delivered **from ;** — if you leave us thus, all your protection will ...

### 10. `God .`
* **Description:** Spaced period (space before period)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... n, is of the mere free grace and good pleasure of **God .** "Stay not in Asia;" etc. III. No men in the worl ...

### 11. `continuance .`
* **Description:** Spaced period (space before period)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... patience, long-suffering, and forbearance in the **continuance .** He bears with our manners, whilst we grieve his S ...

### 12. `1 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... s example. These things being presupposed, — Use **1 .** Let no flesh glory in themselves, but let every m ...

### 13. `e )`
* **Description:** Spaced closing parenthesis
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... g how this vial was poured out upon the very thron**e )**, and then let us all be ashamed and confounded in ...

### 14. `s )`
* **Description:** Spaced closing parenthesis
* **Chapter:** *A Country Essay*
* **Contexts:**
  * ... nasius and others in the east deposed by the Arian**s )**. Now, who would not have thought, that his standi ...

### 15. `you ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *To the Worthy and Honored Sir William Masham, Sir William Rowe,*
* **Contexts:**
  * ... fear but that that God who hath so appeared with **you ,** and for you, will so indulge to y spirits the pre ...

### 16. `Colchester ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... neral mercies we have received . The surrender of **Colchester ,** the particular celebrated this day, though marchi ...

### 17. `portion .`
* **Description:** Spaced period (space before period)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... servation 15. The measuring out of God's people's **portion .**fills Cushan with affliction and Midian with tremb ...

### 18. `received .`
* **Description:** Spaced period (space before period)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... our trust. I speak of the general mercies we have **received .** The surrender of Colchester , the particular cele ...

### 19. `Behold ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... e curse of a professing people at the same time. "**Behold ,** I and the children whom God hath given me, are fo ...

### 20. `Observation .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... entreaty, it cannot, it shall not, be reversed. **Observation .** There is a time when sin grows ripe for ruin: "Fo ...
  * ... rd be your guide; — poor England lieth at stake. **Observation .** The greatest difficulty that lieth in bringing of ...
  * ... authority of God, in this general proposition: — **Observation .** Plausible compliances of men in authority with th ...

### 21. `Obj .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... their own deliverers, if ever they be delivered. **Obj .** But is not a people's contending with the instrum ...

### 22. `5thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... his own, — hardening whom he will, Romans 9:18. **5thly .** He positively sends upon their understandings tha ...

### 23. `6thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... give them up to contend with their only helpers. **6thly .** Suitably upon the will and affections he hath sev ...

### 24. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * **..**. ith their only supporters and means of deliverance**..** Jeremiah had labored with God for them, and with **..**.

### 25. `1 ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... i. cap. 24; Greg. de Valen. de Idol, lib. i. cap. **1 ;** — suitable to the description of it given by the ...

### 26. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... rranted zeal. Now, concerning these, I affirm, — **1st ,** That the magistrate ought not to make provision o ...
  * ... truth so owned, as before, and act accordingly. **1st ,** For the first of these, or such as dissent about ...

### 27. `6 ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... accordingly performed this duty, 2 Chronicles 17:**6 ,** 30:14, are enough to confirm it, and to bottom th ...

### 28. `experience .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... uthority. It is but too clearly made out by daily **experience .** If they close with them, they are "custodes utriu ...

### 29. `2 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... te's duty can be stretched to cover them. Reason **2 .** Neither party, I am persuaded, in their retired t ...

### 30. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... t do. Now, it cannot be his duty to further sin. **2dly .** Outward monuments — ways of declaring and holding ...
  * ... tions sufficient to make an article fundamental. **2dly .** That the persons holding the error are convinced, ...
  * ... ed in this case, I refer to another opportunity. **2dly .** Gospel constitutions in the case of heresy or err ...

### 31. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... f, there are sundry things gratis assumed; as, — **1st .** That it is known and confessed what articles in r ...
  * ... co-action and restraint, oppose some few things. **1st .** The non-constitution of a judge in case of heresy ...

### 32. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... ht forth to the joy of all the children of Zion. **3dly .** Sundry other arguments, taken from the nature of ...

### 33. `..`
* **Description:** Duplicate period (double dot)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * **..**. and Eunomians, Sozom. Ecclesiastes Hist., lib. vii**..** cap. 1. Many more the like examples might be pro **..**.

### 34. `in ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge*
* **Contexts:**
  * ... the vine. "God," saith he, "is able to graft them **in ;**" though now they seem as dead bones, yet the Lord ...

### 35. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge*
* **Contexts:**
  * ... is often spoken of, seldom driven to any close! **1st .** Pray. "Pray the Lord of the harvest, that he woul ...

### 36. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge*
* **Contexts:**
  * ... into the fields that are white for the harvest. **2dly .** Make such provision, that those who will go may b ...

### 37. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge*
* **Contexts:**
  * ... is be the business of an unpursued order. But, — **3dly .** Let some be appointed (generals die and sink by t ...

### 38. `pretences ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... e Pharisees' hypocrisy, notwithstanding all their **pretences ,** and possession of Moses' chair, that they were wi ...

### 39. `2dly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... lly in four sinful things: — 1st, Sinful cares; **2dly ,** Sinful fears; 3dly , Sinful follies; 4thly , Si ...

### 40. `3dly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... ngs: — 1st, Sinful cares; 2dly , Sinful fears; **3dly ,** Sinful follies; 4thly , Sinful negligence. 1st ...

### 41. `4thly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... s; 2dly , Sinful fears; 3dly , Sinful follies; **4thly ,** Sinful negligence. 1st . Sinful cares, — anxious ...

### 42. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... greatness or power; which he sets out two ways. **1st .** Absolutely, as he is God, to be "blessed for ever ...
  * ... ly , Sinful follies; 4thly , Sinful negligence. **1st .** Sinful cares, — anxious and dubious thoughts abou ...

### 43. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... into the hands of the living God," chap. 10:31. **2dly .** Comparatively, as he is the mediator of the new c ...
  * ... quaintedness with the work and mind of the Lord. **2dly .** Sinful fears. Luke 21:28, our Savior having told ...

### 44. `Observation .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... hristian consideration this following position: — **Observation .** The Lord Jesus Christ, by his mighty power, in th ...

### 45. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... ll things working together to the appointed end. **3dly .** Sinful follies. Toil and labor in vain is, of all ...

### 46. `4thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... r;" and all because they discern not the season. **4thly .** Sinful negligence. You are no way able to do the ...

### 47. `me ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the*
* **Contexts:**
  * ... g out, "If it be possible, let this cup pass from **me ;**" but he recollects himself, and says, "I am conte ...

### 48. `pieces .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the*
* **Contexts:**
  * ... hidden, against which they dash themselves all to **pieces .** I say, then, Christ, as the foundation of this ho ...

### 49. `them ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Advantage of the Kingdom of Christ*
* **Contexts:**
  * ... as were the residue of their types, every one of **them ;** — yea, the most glorious enjoyments whatsoever wh ...

### 50. `dismission :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Laboring Saint's Dismission to Rest.*
* **Contexts:**
  * ... n the most useful employments, must receive their **dismission :** — be their work of never so great importance, be ...

### 51. `world :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Laboring Saint's Dismission to Rest.*
* **Contexts:**
  * ... nd of his life and pilgrimage. 2. The end of the **world :** "Go thy ways to the end of the world: till then t ...

### 52. `therein :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Christ's Kingdom and the Magistrate's Power.*
* **Contexts:**
  * ... hand. And these three things he mentions of them **therein :** — (1.) Their rise; (2.) Nature; (3.) Destructi ...

### 53. `5thly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Christ's Kingdom and the Magistrate's Power.*
* **Contexts:**
  * ... rience what will be the issue of such allowance. **5thly .** I shall only propose one thing more to your consi ...

### 54. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Christ's Kingdom and the Magistrate's Power.*
* **Contexts:**
  * ... the present, these brief directions following: — **1st .** Labor to be fully persuaded in your own minds, th ...

### 55. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Christ's Kingdom and the Magistrate's Power.*
* **Contexts:**
  * ... ion of them whom God will spew out of his mouth. **2dly .** Know that error and falsehood have no fight or ti ...

### 56. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Christ's Kingdom and the Magistrate's Power.*
* **Contexts:**
  * ... nor morally they are a disturbance unto others. **3dly .** Know that in things of practice, so of persuasion ...

### 57. `Zion ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.*
* **Contexts:**
  * ... ven in is the work of God. "The Lord hath founded **Zion ;**" — Zion , that is, his church, his people, his ch ...

### 58. `Zion ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.*
* **Contexts:**
  * ... the work of God. "The Lord hath founded Zion ;" — **Zion ,** that is, his church, his people, his chosen ones, ...

### 59. `founded ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.*
* **Contexts:**
  * ... ordinances of worship. This God "hath founded;"—**founded ,** or established, strengthened, that it shall not b ...

### 60. `Joseph ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.*
* **Contexts:**
  * ... that there rise not up a generation that know not **Joseph ;** — that knew us not in the days of our distress an ...

### 61. `1 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.*
* **Contexts:**
  * ... n part touched before; I shall add but two more. **1 .** Discontentment with our peculiar lot and portion ...

### 62. `supposition :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * ... hetical propositions, or promissory assertions on **supposition :** — "If you abide with the Lord, he will be with yo ...

### 63. `General ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * ... ntial dispensations. And this is twofold: — (1.) **General ;** — ordering, disposing, guiding, ruling all things ...

### 64. `say ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * ... ffice as an instance in every kind. But you will **say ,** How shall we inquire of God? The nations had the ...

### 65. `First .`
* **Description:** Spaced period (space before period)
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * ... ngs are, then, principally to be inquired into: — **First .** What it is for God to be with any people. Secondl ...

### 66. `Secondly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * ... First . What it is for God to be with any people. **Secondly .** What it is for a people to be or abide with God. ...

### 67. `peace .`
* **Description:** Spaced period (space before period)
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * ... f Christ: our being with God is in him who is our **peace .** Two cannot walk together, unless they be agreed, ...

### 68. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * ... few things that are signally required thereunto. **1st .** That they inquire of God, ask counsel at his hand ...

### 69. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * ... sting of him in reference to special protection. **3dly .** A third thing I should fix upon is, a people's un ...

### 70. `1st ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * ... offense, in these few ensuing considerations: — **1st ,** Then, I shall willingly lay this down for a princ ...

### 71. `3dly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * ... om owning the portion and inheritance of Christ! **3dly ,** It cannot be denied, but that many of them who do ...

### 72. `4thly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * ... miscarriages of others, have most of their own. **4thly ,** That differences of judgments, in civil affairs o ...

### 73. `5thly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * ... on such accounts, it is because they will be so. **5thly ,** This hath ever been the way of the men of the wor ...

### 74. `6thly ,`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * ... power of grace, harden themselves to their ruin. **6thly ,** This remnant of Christ, with whom his presence is ...

### 75. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * ... hat is here expressed as to the type and figure; **2dly .** What is here intended as to the substance of the ...

### 76. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * ... ended as to the substance of the mercy promised. **1st .** For the figure; by the "glory" and "defense," a d ...
  * ... uation pleaded for be cast? To this I answer, — **1st .** Some do say so, and plead thus, it cannot be deni ...

### 77. `will .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * ... as is their deportment towards this remnant, such **will .**their issue be. But what shall this remnant do? Wh ...

### 78. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * ... ," they will flourish again in peace and beauty. **3dly .** Let not Satan cheat you of your duty by this triv ...

### 79. `Observation .`
* **Description:** Spaced period (space before period)
* **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.*
* **Contexts:**
  * ... n may be comprised in this general observation: — **Observation .** Reproofs, though accompanied with some sharpness, ...

### 80. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.*
* **Contexts:**
  * ... nsidered, that it may not be unuseful unto us: — **1st .** The circumstances of the reprover; as, first, Whe ...

### 81. `2dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.*
* **Contexts:**
  * ... are reproved for that whereof we are not guilty. **2dly .** Consider aright the difference between a reproof ...

### 82. `3dly .`
* **Description:** Spaced period (space before period)
* **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.*
* **Contexts:**
  * ... and if it be false, it is, moreover, a calumny. **3dly .** Where a man, in such cases, is fully justified by ...

### 83. `1 .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Testimony of the Church Is Not the Only Nor the Chief Reaso*
* **Contexts:**
  * ... agree with them; 2. In some we differ from them. **1 .** In some we agree. (1.) That the scripture of the ...

### 84. `testimony .`
* **Description:** Spaced period (space before period)
* **Chapter:** *The Testimony of the Church Is Not the Only Nor the Chief Reaso*
* **Contexts:**
  * ... manifest itself to us, even without the church's **testimony .** The reason of the consequence is, because faith ...

### 85. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Except. III.*
* **Contexts:**
  * ... g, together with the apostles', they were built. **Ans .** The preaching [of] the truth, or writing it, make ...

### 86. `Ans .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Except. IV.*
* **Contexts:**
  * ... g, together with the apostles', they were built. **Ans .** The preaching [of] the truth, or writing it, make ...

### 87. `V .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Except.*
* **Contexts:**
  * ... church, because she says she is the church. Arg. **V .** If we are to believe the divinity of the Scriptur ...

### 88. `1st .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Except.*
* **Contexts:**
  * ... aith, and comfort, and obedience, all at once: — **1st .** It is destructive to our faith. It leaves us no f ...

### 89. `2d .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Except.*
* **Contexts:**
  * ... eived them, when the rest are, because she hath. **2d .** It is as destructive to our comfort. When our gre ...

### 90. `3d .`
* **Description:** Spaced period (space before period)
* **Chapter:** *Except.*
* **Contexts:**
  * ... tainties for the very foundation of their faith. **3d .** It is as destructive to our obedience as to eithe ...

### 91. `the :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *Prefatory Note (Sermon 7 — Advantage of the Kingdom of Christ)*
* **Contexts:**
  * ... n had been agitated with stormy discussions about **the :**Exclusion Bill. The Whig party were bent on preven ...

### 92. `privileges ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... ot repent nor reform their ways. First. By their **privileges ;** — that they were the only church and people of Go ...

### 93. `sorts :`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... and ready to seize on us?" And they are of three **sorts :** — First. Such as are absolute, decretory, and uni ...

### 94. `therein ;`
* **Description:** Spaced punctuation (space before character)
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... udgments, and of our reverence of the name of God **therein ;** — much fruitfulness in charity and good works be ...

---

## OCR & Bracket Residues

No anomalies found in this category.

## Mixed-Case Capitalization Errors

No anomalies found in this category.

## Unresolved Citation References

### 1. `lib. ii`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... nd worship due to the Creator, Rainold. de Idol., **lib. ii**. cap. 1, sect. 1. " Idololatria est circa omne i ...
  * ... olatry, say the Papists, Bell, de Ecclea Triumph, **lib. ii**. cap. 24; Greg. de Valen. de Idol, lib. i. cap. 1 ...
  * ... rnment do and ought to enjoy. So Cicero tells us, **lib. ii**., De Leg., "Suosque deos, aut novos, aut alienige ...

### 2. `lib. i`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... nd worship due to the Creator, Rainold. de Idol., **lib. i**i. cap. 1, sect. 1. " Idololatria est circa omne ...
  * ... servitutem exhibent, quae debertur Deo, " August, **lib. i**. de Trinit. cap. 6 — " They are idolaters who giv ...
  * ... olatry, say the Papists, Bell, de Ecclea Triumph, **lib. i**i. cap. 24; Greg. de Valen. de Idol, **lib. i**. cap. ...

### 3. `lib. 5`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... things no way conducing to monarchy," Hist. Rom., **lib. 5**2:36. Hence, doubtless, was that opposition which ...

### 4. `Epist. lii`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... And long after these, Gregory of Rome, lib. ii. **Epist. lii**., tells us, " Nova et inaudita est ista praedicat ...

### 5. `lib. iv`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... "Yea, to be the first-born of the devil," Euseb., **lib. iv**. cap. 14. Ignatius's epistles are full of the li ...
  * ... hodox professors of the Deity of Christ, Socrat., **lib. iv**. cap 27. 5. Lastly, add unto all that hath been ...
  * ... hut up Pagans' temples, Euseb. de Vita Constant., **lib. iv**. cap. 23, 24; and demolished some of the most fil ...

### 6. `lib. iii`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... e building fall on us where Cerinthus is," Iren., **lib. iii**. cap. 3; Euseb. Ecclesiastes Hist., **lib. iii**. cap ...
  * ... en., **lib. iii**. cap. 3; Euseb. Ecclesiastes Hist., **lib. iii**. cap. 28. Marcion meeting Polycarpus, and asking ...
  * ... Irenaeus says, he would have no words with them, **lib. iii**. cap. 3. Tertullian's books testify for him at la ...

### 7. `lib. v`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *Of Toleration;*
* **Contexts:**
  * ... y — first fastened on the Jews by Tacitus, Hist., **lib. v**. cap. 1, in these words, "Effigiem animalis, quo ...
  * ... inians, and Eunomians, Sozom. Ecclesiastes Hist., **lib. v**ii.. cap. 1. Many more the like examples might be ...
  * ... e two years, was slain with his children, Euseb., **lib. v**ii. cap. 1. Valerian, being taken by Sapores king ...

### 8. `lib. 53`
* **Description:** Unresolved patristic/classical citation reference (no translation found)
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... had spread themselves over all the nation, Hist., **lib. 53**:Nor is it otherwise among us at present; though n ...

---

## Structural Nesting Sequence Jumps

### 1. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...
  * ... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...
  * ... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...

### 2. `2. ... 17.`
* **Description:** List sequence jump (skipped from 2 to 17)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 3. `1. ... 4.`
* **Description:** List sequence jump (skipped from 1 to 4)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 4. `2. ... 5.`
* **Description:** List sequence jump (skipped from 2 to 5)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 5. `2. ... 7.`
* **Description:** List sequence jump (skipped from 2 to 7)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 6. `2. ... 8.`
* **Description:** List sequence jump (skipped from 2 to 8)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 7. `3. ... 9.`
* **Description:** List sequence jump (skipped from 3 to 9)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 8. `2. ... 10.`
* **Description:** List sequence jump (skipped from 2 to 10)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 9. `2. ... 12.`
* **Description:** List sequence jump (skipped from 2 to 12)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 10. `3. ... 13.`
* **Description:** List sequence jump (skipped from 3 to 13)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 11. `2. ... 14.`
* **Description:** List sequence jump (skipped from 2 to 14)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 12. `5. ... 15.`
* **Description:** List sequence jump (skipped from 5 to 15)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 13. `2. ... 16.`
* **Description:** List sequence jump (skipped from 2 to 16)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 14. `3. ... 17.`
* **Description:** List sequence jump (skipped from 3 to 17)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 15. `2. ... 18.`
* **Description:** List sequence jump (skipped from 2 to 18)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 16. `2. ... 19.`
* **Description:** List sequence jump (skipped from 2 to 19)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 17. `1. ... 20.`
* **Description:** List sequence jump (skipped from 1 to 20)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**

### 18. `3.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * SERMON **3.** RIGHTEOUS ZEAL ENCOURAGED BY DIVINE PROTECTIO ...
  * ... s just and righteous See verse 6 of this chapter. **3.** Because the people, by virtue of their retained s ...
  * ... s for Baal, and a grove, as did Ahab," 2 Kings 21:**3.** (2.) Cruelty: "He shed innocent blood very much, ...

### 19. `3. ... 6.`
* **Description:** List sequence jump (skipped from 3 to 6)
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**

### 20. `1. ... 3.`
* **Description:** List sequence jump (skipped from 1 to 3)
* **Chapter:** *Of Toleration;*
* **Contexts:**

### 21. `4.`
* **Description:** List sequence starts at 4 instead of 1
* **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge*
* **Contexts:**
  * SERMON **4.** THE STEADFASTNESS OF THE PROMISES, AND THE SI ...
  * ... and conclusions, to the end of verse 17, chapter **4.** Having laid down this, in the next place he give ...
  * ... ll, to lie down quietly in God's allsufficiency. **4.** The last is, that "he staggered not," verse 20. T ...

### 22. `5.`
* **Description:** List sequence starts at 5 instead of 1
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * SERMON **5.** THE SHAKING AND TRANSLATING OF HEAVEN AND EAR ...
  * ... al states; as Isaiah 14:12-15; Jeremiah 15:9, 51:2**5.** (Isaiah 13:13; Psalm 68:8; Joel 51:10; Revelation ...
  * ... lation 1:14-17, as also chapter 4 and chapter 11:1**5.** And both these may be again considered two ways. ...

### 23. `6.`
* **Description:** List sequence starts at 6 instead of 1
* **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the*
* **Contexts:**
  * SERMON **6.** THE BRANCH OF THE LORD THE BEAUTY OF ZION: OR ...
  * ... ious corner-stone, a sure foundation," Isaiah 28:1**6.** Now, this foundation is no other but the rock upo ...
  * ... his own house, whose house are we," Hebrews 3:5, **6.** And that you may see that he doth not own it as ...

### 24. `8.`
* **Description:** List sequence starts at 8 instead of 1
* **Chapter:** *The Laboring Saint's Dismission to Rest.*
* **Contexts:**
  * SERMON **8.** THE LABORING SAINT'S DISMISSION TO REST. "But ...
  * ... a man to be "weary and heavy laden," Matthew 11:2**8.** This oftentimes makes the inhabitants of Zion say ...

### 25. `9.`
* **Description:** List sequence starts at 9 instead of 1
* **Chapter:** *Christ's Kingdom and the Magistrate's Power.*
* **Contexts:**
  * SERMON **9.** CHRIST'S KINGDOM AND THE MAGISTRATE'S POWER. ...
  * ... pt of the gospel, 2 Corinthians 2:16; Hebrews 10:2**9.** He sends his Spirit to convince even the perishin ...
  * ... gh never so glorious and excellent, Revelation 22:**9.** 2dly. For Satan, as he came to bind the strong m ...

### 26. `10.`
* **Description:** List sequence starts at 10 instead of 1
* **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.*
* **Contexts:**
  * SERMON **10.** GOD'S WORK IN FOUNDING ZION, AND HIS PEOPLE'S ...

### 27. `11.`
* **Description:** List sequence starts at 11 instead of 1
* **Chapter:** *God's Presence With a People the Spring of Their Prosperity.*
* **Contexts:**
  * SERMON **11.** GOD'S PRESENCE WITH A PEOPLE THE SPRING OF TH ...

### 28. `12.`
* **Description:** List sequence starts at 12 instead of 1
* **Chapter:** *The Glory and Interest of Nations Professing the Gospel.*
* **Contexts:**
  * SERMON **12.** THE GLORY AND INTEREST OF NATIONS PROFESSING ...
  * ... number; yea, very few, and strangers," Psalm 105:**12.** You know what it cost David in being seduced by S ...

### 29. `13.`
* **Description:** List sequence starts at 13 instead of 1
* **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.*
* **Contexts:**
  * SERMON **13.** HOW WE MAY BRING OUR HEARTS TO BEAR REPROOFS. ...
  * ... and cutting manner," 2 Corinthians 13:10; Titus 1:**13.** But with respect unto their use, benefit, and adv ...

### 30. `2.`
* **Description:** List sequence starts at 2 instead of 1
* **Chapter:** *Except. II.*
* **Contexts:**
  * ... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...
  * ... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...
  * ... the good knowledge of the Lord," 2 Chronicles 30:2**2.**

### 31. `III.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Except. III.*
* **Contexts:**
  * Except. **III.** "But," say they again, "the Ephesians were not bu ...

### 32. `III.`
* **Description:** List sequence starts at 3 instead of 1
* **Chapter:** *Except. IV.*
* **Contexts:**
  * Except. **III.** "But," say they again, "the Ephesians were not bu ...
  * ... er, till their doctrine was first believed. Arg. **III.** The Scripture hath its authority, in relation to ...

### 33. `VI.`
* **Description:** List sequence starts at 6 instead of 1
* **Chapter:** *Except.*
* **Contexts:**
  * ... e to be before the testimony of the church. Arg. **VI.** If we must believe the Scripture to be the word o ...

### 34. `I. ... IX.`
* **Description:** List sequence jump (skipped from 1 to 9)
* **Chapter:** *Except.*
* **Contexts:**

### 35. `16.`
* **Description:** List sequence starts at 16 instead of 1
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * SERMON **16.** AN HUMBLE TESTIMONY UNTO THE GOODNESS AND SEV ...
  * ... te described by the apostle, 1 Thessalonians 2:14-**16.** But it may be said, If their destruction was so ...
  * ... ith his people as the angel dealt with Lot, verse **16.** They are apt to linger, and know not how to leave ...

### 36. `3. ... 9.`
* **Description:** List sequence jump (skipped from 3 to 9)
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**

---

## Invalid Bible References

### 1. `Jude 4`
* **Description:** Invalid Bible reference (chapter 4 exceeds max 1 for Jude)
* **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G*
* **Contexts:**
  * ... have fulfilled, John 12:37-41; in men described, **Jude 4**, and 1 Peter 2:8. But here we must strike sail, t ...

### 2. `Obadiah 9`
* **Description:** Invalid Bible reference (chapter 9 exceeds max 1 for Obadiah)
* **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.*
* **Contexts:**
  * ... Teman (Genesis 36:15; Jeremiah 49:7; Habakkuk 1:9 **Obadiah 9**.) was a city of the Edomites, whose land the peop ...

### 3. `2 Kings 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 22 for Kings)
* **Chapter:** *Righteous Zeal Encouraged by Divine Protection.*
* **Contexts:**
  * ... this Manasseh, he recalls his thoughts of mercy, **2 Kings 23**:26, 27. The deposing of divine and human things i ...

### 4. `Joel 51`
* **Description:** Invalid Bible reference (chapter 51 exceeds max 3 for Joel)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... Jeremiah 15:9, 51:25. (Isaiah 13:13; Psalm 68:8; **Joel 51**:10; Revelation 8:12; Matthew 24:29; Luke 21:25; I ...

### 5. `Obadiah 4`
* **Description:** Invalid Bible reference (chapter 4 exceeds max 1 for Obadiah)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... on 8:12; Matthew 24:29; Luke 21:25; Isaiah 60:20; **Obadiah 4**; Revelation 8:13, 40:12, 20:11.) Furthermore, to ...

### 6. `Jude 4`
* **Description:** Invalid Bible reference (chapter 4 exceeds max 1 for Jude)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... n of the sense and matter thereof. (Hebrews 11:5; **Jude 4**:1; Galatians 1:6; Hebrews 6:18, 7:12.) Understand ...

### 7. `Obadiah 21`
* **Description:** Invalid Bible reference (chapter 21 exceeds max 1 for Obadiah)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... administrations. (Psalm 45:6, 45:13; Isaiah 9:7; **Obadiah 21**) So is Christ described as a king in the midst of ...

### 8. `Hosea 52`
* **Description:** Invalid Bible reference (chapter 52 exceeds max 14 for Hosea)
* **Chapter:** *The Shaking and Translating of Heaven and Earth*
* **Contexts:**
  * ... ah 37:31; Jeremiah 30:9; Ezekiel 34:27, 37:24,25; **Hosea 52**:5; Amos 9:11.) and in answer to millions of praye ...

### 9. `2 Kings 24`
* **Description:** Invalid Bible reference (chapter 24 exceeds max 22 for Kings)
* **Chapter:** *Advantage of the Kingdom of Christ*
* **Contexts:**
  * ... appoints Zedekiah a titulary governor under him. (**2 Kings 24**:1-3) But the wrath of God being to come upon them ...
  * ... es with Egypt, rebels against him (Jeremiah 37:1; **2 Kings 24**:17; 2 Chronicles 36:10) by whose appointment alon ...

### 10. `Obadiah 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 1 for Obadiah)
* **Chapter:** *Advantage of the Kingdom of Christ*
* **Contexts:**
  * ... destroy the residue, when at any time straitened, **Obadiah 14**:1. How many in the late trial rejoiced in the str ...

### 11. `Philippians 20`
* **Description:** Invalid Bible reference (chapter 20 exceeds max 4 for Philippians)
* **Chapter:** *Advantage of the Kingdom of Christ*
* **Contexts:**
  * ... , 22, 13:55, 8:19; John 4:28, 29; Isaiah 53:2, 3; **Philippians 20**:7 2:7,8, etc.) Thus lays he the foundation of the ...

### 12. `Obadiah 12`
* **Description:** Invalid Bible reference (chapter 12 exceeds max 1 for Obadiah)
* **Chapter:** *Christ's Kingdom and the Magistrate's Power.*
* **Contexts:**
  * ... abound. In such a day Edom will appear an enemy, (**Obadiah 12**, 13; Isaiah 7:1.) and Ephraim with the son of Rem ...

### 13. `Jude 14`
* **Description:** Invalid Bible reference (chapter 14 exceeds max 1 for Jude)
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... st recorded of them are in the prophecy of Enoch, **Jude 14**,15. And they have been since continued in all age ...
  * ... e coming of God to take vengeance on ungodly men, **Jude 14**,15. And this message was scoffed at, as is eviden ...

### 14. `2 Kings 23`
* **Description:** Invalid Bible reference (chapter 23 exceeds max 22 for Kings)
* **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi*
* **Contexts:**
  * ... onish captivity, as an account is given us of it, **2 Kings 23**:25-27, "Like unto him was there no king before hi ...

---

## List Formatting Inconsistencies

No anomalies found in this category.

