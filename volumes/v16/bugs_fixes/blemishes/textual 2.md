# Imptant
fix bugs, now I don't want partial fixes, I want thorough revisiting of algorithms/regex and audits why are these bugs here and how can they be
fixed or rewritten that these bugs are not leaking on other volumes also

## 1
— Ecclesiastes 266.
Note: do we not have audits that check for verses?

## 2
Corona, οδ >,
Fix: Greek rendering is faulty
Is the audits and cjecks not catching this?

## 3
that follow him: so he fully expresseth himself, Tractat.
124.

Fix: 
that follow him: so he fully expresseth himself, Tractat. 124.
Note: This is a false positive scholastic anchor, but the audit should be able to catch this.

## 4
IV. But this election of the church doth not actually and immediately

FixL
IV. should be centered, not left justified. 
Note: this is a formatting issue, but the audit should be able to catch this.

## 5
3. May a pastor voluntarily, or of his own accord, resign and lay down his office, and remain in a private
Fix:
"3." should be block, since 1, 2 are block.

## 6
Προι`>στημι, or προι`>ταμαι, is
Fix: Greek rendering is faulty
Note: do we not have audits that check for Greek rendering?

## 7
]Εχοντες χαρίσματα διάφορα, verse 6. And
]Εχοντες χαρίσματα,

Fix: Greek rendering is faulty, I will not repeat this, but we need to check for Greek rendering in the audits.

## 8
“ (l.) He that says, "He that exhorteth," and then adds, "He that ruleth," having distinguished before between prophecy, whereunto exhortation doth belong, and ministry, whereof rule is a part, and prefixing the prepositive indicative article to each of them, doth as plainly put a difference between them as can be done by words.


(2.) Rule is the principal work of him that ruleth, for he is to attend unto it ἐν σπουδῇ, "with diligence," — that is, such as is peculiar unto rule, in contradistinction unto what is principally required in other administrations. But rule is not the principal work of the pastor, requiring constant and continual attendance; for his labor in the word and doctrine is ordinarily sufficient for the utmost of his diligence and abilities.”

(l.) should be (1.) and if (1.) is not block neither should (2.) be block.
Note: can we have audits that check for numbering and formatting consistency? This is a clear case of inconsistency in the formatting of numbered points.
(l.) is clearly an OCR error, but the audit should be able to catch this.?

## 9
“10. There is the same evidence given unto the truth argued for in another testimony of the same apostle: 1 Corinthians 12:28, "God hath set some in, the church, first apostles, secondarily prophets, thirdly teachers, after that miracles, then gifts of healings, helps, governments, diversities of tongues." I shall not insist on this testimony and its vindication in particular, seeing many things would be required thereunto which have been treated of already. Some things may be briefly observed concerning it.”

Fix:
"10." is a higher level than previous points, I believe the previous points should be higher level. Your algorithn though it works well in alot of cases, it seems hit and miss in terms of consistency. We need to have audits that check for consistency in numbering and formatting.
I am tired of trying to fix these issues manually, we need to have a system in place that can catch these issues automatically. This is a clear case of inconsistency in the formatting of numbered points, and it should be caught by the audits.

## 10
[1.] Constant prayer for the flock;


[2.] Diligence in the dispensation of the word with wisdom, as unto times, seasons, the state of the flock in general, their light, knowledge, ways, walking, ignorance, temptations, trials, defections, weaknesses of all sorts, growth, and decays, etc;

Fix:
[1.] is not block, but [2.] is block. This is an inconsistency in formatting that should be caught by the audits. We need to have a system in place that can catch these issues automatically, as it is clear that the algorithm is not consistent in its formatting decisions.

Status: IMPLEMENTED (AWAITING VALIDATION)
