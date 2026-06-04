To build a truly conclusive semantic parsing engine for John Owen’s 16-volume Works and 7-volume Hebrews commentary, your script cannot rely solely on standard English dictionary parsing. Owen was a Protestant Scholastic who wrote in an English heavily saturated with Latinate syntax, technical theological categories (loci), and Aristotelian-Ramist logical distinctions.
To help your technical_glossary.py achieve maximum precision across the Banner of Truth (BoT) sets, here is a categorized, exhaustive blueprint of the technical lexicon Owen deploys.
1. Trinitarian & Christological Frameworks
Owen’s polemics against the Socinians (found heavily in Works volumes 2, 12, and Hebrews 1–2) rely on rigorous ontological terms. Your script must flag these to capture his exact arguments:
• Autotheos (\alpha \upsilon \tau \sigma \theta \varepsilon o \varsigma): God-in-of-himself; applied to Christ to assert He is not subordinate in His divine essence.
• Appropriation: Ascribing a specific operation of the undivided Trinity to one particular Person (e.g., creation to the Father, perfecting to the Spirit).
• Circumincession / Perichoresis: The mutual indwelling and interpenetration of the three distinct Persons within the single divine essence.
• Hypostatic Union: The union of Christ's divine and human natures in one single hypostasis (person) without mixture or change.
• Inseparable Operations (Opera ad extra sunt indivisa): The rule that all external works of the Trinity are performed by all three Persons concurrently.
• Subsistence: The technical Latinate rendering of hypostasis—how an individual person possesses the divine essence.
• Communicatio Idiomatum: The communication of properties; how attributes of either the human or divine nature are predicated of the one person of Christ.
2. Anthropological & Soteriological Faculties
When Owen diagnoses the anatomy of sin and regeneration (Works volumes 3, 6, and 7), he maps out the soul using precise scholastic categories. Look for:
• Habit / Habitual Grace (Habitus): An infused, permanent disposition or spiritual capacity wrought in the soul by the Holy Spirit, prior to any actual gospel actions.
• Act / Actual Grace: The moving or exciting of those infused habits into concrete exercises of faith, love, or repentance.
• Subjective Light: The internal, spiritual capacity given to the intellect by the Holy Spirit to perceive spiritual truths.
• Objective Evidence: The external truth of God's Word presented to the rational mind.
• Concupiscence: The innate inclination of the fallen human nature toward sin, operating prior to the consent of the will.
• Illumination: The work of the Spirit on the mind (intellectus) removing natural blindness, distinct from saving regeneration.
3. Federal (Covenantal) Distinctives
In his monumental exposition of the covenants (Hebrews volume 6, handling chapter 8), Owen shifts through precise legal and federal terminology:
• Sponsorship / Suretyship (Sponsor): Christ’s legal position under the Covenant of Redemption, stepping into the legal debt-obligation of the elect.
• Federal Headship: The legal representation of a collective group by one individual (Adam in the Covenant of Works; Christ in the Covenant of Grace).
• Covenant of Redemption (Pactum Salutis): The eternal, intra-trinitarian counsel and agreement between the Father and the Son for the salvation of the elect.
• Protoevangelium: The first announcement of the gospel and the Covenant of Grace in Genesis 3:15.
4. Aristotelian-Scholastic Causality
Owen builds his arguments using the traditional fourfold schema of causation. If your python script does not flag these, it will miss the logical syntax of The Death of Death (Works v10) and Justification (Works v5):
• Efficient Cause: The primary agent that produces an effect (e.g., God’s sovereign grace).
• Material Cause: The matter or substance upon which the efficient cause works, or that which constitutes the object (e.g., Christ's passive and active obedience).
• Formal Cause: The defining design, pattern, or legal reality that makes a thing what it is (e.g., the imputation of righteousness in justification).
• Final Cause: The ultimate purpose, end, or goal for which the thing is accomplished (e.g., the manifestation of God’s glory).
• Instrumental Cause: The means through which an effect is applied (e.g., faith as the instrument, not the ground, of justification).
5. Prolegomena & Epistemological Distinctions
At the start of his theological arguments (Works volume 4 on Reason and Prayer), Owen establishes how man can know God:
• Archetypal Theology: The infinite, uncreated, comprehensive self-knowledge that God has of Himself.
• Ectypal Theology: The finite, created, accommodated knowledge of God revealed to creatures (theology "according to our capacity").
• Theologia Viatorum: The theology of pilgrims on the way; our partial, finite knowledge of God in this earthly life.
• Theologia Beatorum: The theology of the blessed; the perfect, immediate vision of God enjoyed by saints in glory.
Python Regex Expansion Recommendation
To capture Owen's variations across the 16 volumes, configure your script to look for both the Anglicized forms and their direct Latin counterparts, accounting for 17th-century typography (such as matching phrases with "u" for "v", or archaic spelling variants like habite, concupiscence, imputative).
Is there a specific volume or treatise you are running this parser against first where you want to test these logical and causal distinctions?


Yes, an absolute gold standard for this exact task exists. If you want a comprehensive, industry-accepted lexicon to feed into your system, you need Richard A. Muller’s Dictionary of Latin and Greek Theological Terms: Drawn Principally from Protestant Scholastic Theology (specifically the 2nd Edition, 2017).
While it is an external reference volume rather than part of your primary physical bookshelf, it is universally recognized by historical theologians as the definitive "source code" for the exact technical, linguistic, and logical framework that John Owen, Francis Turretin, and Petrus van Mastricht utilized.
Integrating a comprehensive scholastic vocabulary into your text-parsing system requires looking beyond individual words to target specific linguistic, logical, and structural patterns.
Technical Mapping Guide for technical_glossary.py
To expand your script effectively across all 16 volumes of Owen's Works and the 7 volumes of Hebrews, configure your parser to flag three distinct structural layers:
1. The Latin-to-English Morphological Shift
Owen frequently oscillates between the native Latin scholastic phrase and his own direct English translations. Your script's dictionary arrays should match both dynamically.
Latin Scholastic Term	Owenian English Equivalent	System Targeting Logic
Habitus	Habit / Spiritual Capacity	Look for "habit" when not paired with "customary" or "routine".
Actus	Act / Actual / Egress	Flag when discussing the execution or fruit of a faculty.
Terminus	Term / Boundary / Scope	Flag when Owen defines the legal limits of a covenant or decree.
Ex nihilo	Out of nothing / Original nothing	Flag in Creation/Covenant loci (Works v1).
In abstracto / In concreto	Abstractly / Concretely	Flag in Christological/Nature-Person arguments (Works v2).
2. Scholastic Disputation Markers
Because Owen employs the scholastic quaestio methodology (even when smoothed out into prose paragraphs), his logical pivots are highly predictable. You can train your script to map the flow of his arguments by flagging these exact transition markers:
• Distinctions: Look for strings like "distinguish", "distribution", "on the one hand... on the other", or "under a twofold consideration".
• Objections: Look for "It is objected", "Our adversaries plead", "They argue from", or "Hence they infer".
• Refutations: Look for "To this I answer", "This is of no force", "The fallacy lies in", or "Which distinction removes the difficulty".
3. Aristotelian Causal Taxonomies
When Owen parses a doctrine (like Justification in Volume 5 or Redemption in Volume 10), he systematically applies Ramist or Aristotelian logical syntax. Your parser can capture the Ratio (the reason/cause) of his arguments by building an array centered entirely on Causality:
# Conceptual dictionary structure for your python script
causal_taxonomy = {
    "efficient_cause": ["efficient cause", "impelling cause", "author thereof", "principal agent"],
    "material_cause": ["material cause", "matter thereof", "subject matter", "meritorious cause"],
    "formal_cause": ["formal cause", "form thereof", "formal reason", "imputation"],
    "final_cause": ["final cause", "ultimate end", "scope intended", "chief end"],
    "instrumental_cause": ["instrumental cause", "instrument thereof", "organical means"]
}

Script Implementation Strategy
If you want your system to catch these automatically without manual data-entry for thousands of terms, leverage Python's re module to account for 17th-century orthography and typography.
1. Catch Archaic Typographical Shifts: Account for internal "u" replacing "v" (e.g., vniuersal for universal) or double "f" (e.g., effectual written with distinct ligature spacing in older digitized texts).
2. Stemming Scholastic Terms: Ensure your search terms use roots that capture multiple parts of speech (e.g., matching imputat will catch imputation, imputed, imputative, and imputatively).
Would you like to review a specific regex pattern or sample text block from one of Owen's volumes to see how the system handles parsing his logical syntax?
