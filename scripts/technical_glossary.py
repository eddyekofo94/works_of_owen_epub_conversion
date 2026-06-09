# technical_glossary.py
"""
Glossary of theological and historical technical terms, and archaic words
frequently used in John Owen's works. Used to automatically inject first-occurrence
pop-up footnotes (using the section symbol '§') into the text.
"""

# Theological, historical, and archaic terms (Symbol: §)
TECHNICAL_TERMS = {
    'actuate': 'To motivate or translate potential power into actual action/existence (in scholasticism).',
    'Amyraldian': 'A Reformed system named after Moses Amyraut holding that God decreed Christ\'s universal atonement for all men on condition of faith, but decreed to give the grace of faith only to the elect.',
    'Amyraldianism': 'A modified Reformed system (hypothetical universalism) named after Moses Amyraut, holding that God decreed Christ\'s atonement for all men conditionally upon faith, but decreed to give saving faith only to the elect.',
    'Anabaptist': 'A radical Reformation movement that rejected infant baptism, advocating instead for believer\'s baptism and strict separation of church and state.',
    'anent': 'Concerning; about; in respect of.',
    'Anthropopathia': 'The rhetorical attribution of human feelings, passions, or physical attributes to God (e.g., God \'repenting\' or having \'eyes\').',
    'Antinomian': 'From the Greek \'anti\' (against) and \'nomos\' (law). A theology that argues Christians are freed by grace from the necessity of obeying the moral law.',
    'Antinomianism': 'The theological view that Christians are freed by grace from the obligation of keeping the moral law.',
    'Apollinarian': 'A Christological view named after Apollinaris of Laodicea holding that Christ had a human body and sensitive soul, but a divine mind (Logos) instead of a human rational mind.',
    'Apollinarianism': 'The Christological heresy named after Apollinaris of Laodicea holding that Christ had a human body and sensitive soul, but a divine mind (Logos) instead of a human rational mind.',
    'apostatize': 'To abandon or renounce a religious belief or allegiance.',
    'Arian': 'A 4th-century theological movement named after Arius which taught that the Son of God was a created being, not co-essential or co-eternal with the Father.',
    'Arianism': 'The 4th-century theological heresy named after Arius which taught that the Son of God was a created being, not co-essential or co-eternal with the Father.',
    'Arminian': 'A theological movement based on the teachings of Jacobus Arminius, emphasizing conditional election, resistible grace, and the possibility of falling from grace.',
    'Arminianism': 'The theological system based on the teachings of Jacobus Arminius, emphasizing conditional election, resistible grace, universal atonement, and the possibility of falling from grace.',
    'Artemonite': 'Followers of Artemon (a 3rd-century adoptionist heretic in Rome) who taught that Jesus was a mere man who became divine through moral excellence.',
    'Autotheos': 'A Greek term meaning \'God of Himself\', used in Trinitarian theology to refer to the Son\'s possession of the divine essence underived in Himself as God, though personally begotten of the Father.',
    'behove': 'To be necessary, proper, or fitting for (e.g. \'it behoves us\' means \'it is our duty\').',
    'betake': 'To turn to or resort to (e.g. \'betake oneself\' to a duty or prayer).',
    'betimes': 'Early; in good time; seasonably.',
    'chiliast': 'A millenarian; one who believes in a literal thousand-year reign of Christ on earth.',
    'Christologia': 'The theological study of the person, two natures, and mediatorial offices of Jesus Christ.',
    'circumincession': 'The mutual indwelling or coinherence of the three persons of the Trinity (Perichoresis).',
    'coeternal': 'Equally eternal; existing together from eternity (especially of the persons of the Trinity).',
    'coinherence': 'The mutual indwelling or interpenetration of the persons of the Trinity (Perichoresis).',
    'communicatio idiomatum': 'A Latin scholastic term meaning \'communication of properties,\' referring to the Christological doctrine that the properties of both Christ\'s divine and human natures are predicated of His one person.',
    'condecency': 'Fitness, suitability, or becomingness; in scholastic theology, what is fitting or congruent with the divine nature.',
    'contemperation': 'A tempering or mixing in due proportion; moderation.',
    'cozen': 'To cheat, deceive, or defraud.',
    'creationism': 'In theology, the doctrine that God creates a new soul for each person at conception (as opposed to traducianism).',
    'decalogue': 'The Ten Commandments.',
    'demiurge': 'A deity or creative force in Gnostic philosophy, subordinate to the supreme being, responsible for creating the physical world.',
    'deprave': 'To corrupt, pervert, or make bad (physically or morally).',
    'disannul': 'To make void, nullify, or cancel completely.',
    'disquietment': 'A state of disquietude, anxiety, or mental uneasiness.',
    'Episcopalian': 'A church government system ruled by bishops organized in a hierarchical structure.',
    'Erastian': 'The doctrine named after Thomas Erastus advocating that the state or civil magistrate has supreme authority over the church in all ecclesiastical matters, including discipline.',
    'Erastianism': 'The doctrine named after Thomas Erastus advocating that the state or civil magistrate has supreme authority over the church in all ecclesiastical matters.',
    'Eutychian': 'An early Christological view holding that Christ\'s human nature was absorbed into His divine nature, leaving Him with only one composite nature (Monophysitism).',
    'Eutychianism': 'The Christological error holding that Christ\'s human nature was absorbed into His divine nature, leaving Him with only one composite nature (Monophysitism).',
    'evanid': 'Fading, vanishing, or short-lived.',
    'exinanition': 'A state of emptying or humiliation; specifically refers to Christ\'s state of humiliation in the incarnation (Kenosis).',
    'exurgency': 'A rising up or arising; emergency or pressing need.',
    'fiducia': 'Trust or personal confidence in Christ, which is an essential element of saving faith.',
    'froward': 'Stubborn, perverse, disobedient, or difficult to deal with.',
    'futilous': 'Frivolous, trifling, or worthless.',
    'gainsay': 'To deny, contradict, oppose, or speak against.',
    'Gnostic': 'A diverse collection of early religious movements emphasizing secret knowledge (gnosis) for salvation, and viewing the material world as inherently evil, created by a demiurge.',
    'heteroousios': 'Of a different substance or essence (the extreme Arian term).',
    'homoiousios': 'Of similar substance or essence (the semi-Arian term, opposed to homoousios).',
    'homoousios': 'Of one substance or essence; consubstantial (used in the Nicene Creed to define Christ\'s relation to the Father).',
    'hyperdulia': 'In Roman Catholic theology, the special veneration accorded to the Virgin Mary (distinguished from latria and dulia).',
    'Hypostatic': 'Refers to the personal union of Christ\'s divine and human natures in His single divine person (the Hypostatic Union).',
    'impenitency': 'The state of being impenitent; stubborn refusal to repent of sins.',
    'importunity': 'Persistent, pressing, or urgent solicitation or demand.',
    'inbeing': 'Inherent existence or indwelling.',
    'Independent': 'A church government system where each local church is autonomous and self-governing under Christ, free from the jurisdiction of bishops or presbyteries (Congregationalism).',
    'Infralapsarian': 'A Reformed view of the logical order of God\'s decrees, suggesting God decreed to permit the Fall before decreeing the election of some to salvation.',
    'Jansenism': 'A 17th-century Catholic theological movement named after Cornelius Jansen emphasizing original sin, human depravity, the necessity of divine grace, and predestination.',
    'Jansenist': 'A 17th-century Catholic theological movement named after Cornelius Jansen emphasizing original sin, human depravity, the necessity of divine grace, and predestination.',
    'Kenosis': 'The concept of Christ\'s self-emptying and voluntary self-limitation in the incarnation (Philippians 2:7).',
    'latria': 'The supreme worship due to God alone (distinguished from dulia and hyperdulia).',
    'Macedonian': 'A 4th-century sect that accepted the deity of the Son but denied the deity and personal subsistence of the Holy Spirit, viewing Him as a force or ministering spirit.',
    'Macedonianism': 'The 4th-century heresy denying the deity and personal subsistence of the Holy Spirit, viewing Him as a force or ministering spirit.',
    'mediatorial': 'Relating to a mediator or mediation, specifically Christ\'s office as mediator.',
    'meet': 'Fitting, suitable, proper, or appropriate (e.g. \'meet for repentance\').',
    'Molinist': 'A theological system named after Luis de Molina advocating that God\'s middle knowledge (scientia media) reconciles human free choice with divine election.',
    'Monarchian': 'An early Christian theological movement emphasizing the absolute unity of God, which manifested either as Adoptionist Monarchianism (Jesus was a mere man adopted by God) or Modalist Monarchianism (the Father, Son, and Spirit are temporary modes of one God).',
    'monergism': 'The doctrine that regeneration is exclusively the work of the Holy Spirit (as opposed to synergism).',
    'Monophysite': 'A Christological view holding that Christ possessed only a single divine nature after the incarnation.',
    'Monophysitism': 'The Christological doctrine that Christ possessed only a single divine nature after the incarnation.',
    'Monothelite': 'A Christological view holding that Christ, though possessing two natures (divine and human), had only a single divine-human will.',
    'Monothelitism': 'The Christological heresy holding that Christ, though possessing two natures (divine and human), had only a single divine-human will.',
    'Nestorian': 'A Christological view associated with Nestorius emphasizing the distinction between Christ\'s divine and human natures, accused of dividing Christ into two separate persons.',
    'Nestorianism': 'The Christological error emphasizing the distinction between Christ\'s divine and human natures to the extent of dividing Him into two separate persons.',
    'obedientialis': 'Obediential; relating to passive capacity to receive divine action or supernatural influence (e.g., \'obediential power\' in scholastic theology).',
    'otiose': 'Serving no useful purpose; idle; lazy.',
    'Papist': 'A 17th-century Protestant polemical term for a Roman Catholic, denoting allegiance to the Pope.',
    'Patripassian': 'An early Christian view holding that the Father Himself suffered and died on the cross.',
    'Pelagian': 'Following the teachings of Pelagius (c. 390-418), this view denies original sin and asserts that humans have the unhindered natural ability to perfectly obey God without the need for prior divine grace.',
    'Pelagianism': 'The heresy denying original sin and asserting that humans have the unhindered natural ability to perfectly obey God without prior divine grace.',
    'perichoresis': 'The mutual indwelling or coinherence of the three persons of the Trinity (circumincession).',
    'Photinian': 'A Christological view named after Photinus of Sirmium holding that Jesus was a mere man who did not exist prior to His birth.',
    'Pneumatologia': 'The theological study of the person, deity, and work of the Holy Spirit.',
    'Presbyterian': 'A church government system ruled by representative elders (presbyters) organized into hierarchical councils.',
    'preterition': 'In Reformed theology, the passing over of the non-elect in God\'s decree of election.',
    'prevent': 'In 17th-century usage: to go before, precede, or anticipate (from Latin \'praevenire\'), rather than to stop or hinder.',
    'quickened': 'Made alive; given life (often used in the theological sense of regeneration or spiritual resurrection).',
    'recreate': 'To refresh, restore, or revive (especially after labor).',
    'Remonstrant': 'The Dutch Arminian theologians who presented a Remonstrance (protest) in 1610 containing five points of disagreement with the Reformed Belgic Confession.',
    'remonstrate': 'To make a forcefully reproachful protest; present reasons against an action.',
    'reprobate': 'One who is rejected by God; or (as an adjective) rejected, unprincipled, or depraved.',
    'reprobation': 'The sovereign decree of God whereby He passes over the non-elect and ordains them to punishment for their sins.',
    'returnal': 'A returning or return.',
    'Sabellian': 'An early theological view that the Father, Son, and Holy Spirit are not distinct persons but merely three different modes of a single divine person.',
    'Sabellianism': 'The early heresy (Modalism) holding that the Father, Son, and Holy Spirit are not distinct persons but merely three different modes of a single divine person.',
    'Scholasticism': 'A medieval and post-Reformation method of learning and theology emphasizing dialectical reasoning, rigid categorization, and logical consistency.',
    'selfabasement': 'Humiliation of oneself, especially before God.',
    'Socinian': 'A follower of the anti-Trinitarian, rationalist system of theology named after Faustus Socinus, which denied the Trinity, the pre-existence of Christ, His essential deity, and the satisfaction of Christ\'s atonement.',
    'Socinianism': 'The rationalistic theological system named after Faustus Socinus, characterized by the denial of the Trinity, Christ\'s divinity, His pre-existence, and the substitutionary atonement.',
    'Sublapsarian': 'A Reformed view of the logical order of God\'s decrees, suggesting God decreed to permit the Fall before decreeing the election of some to salvation.',
    'Subordination': 'In general theology, the state of being placed in a lower rank or relation of obedience (e.g., the creature\'s subordination to God). In Trinitarian theology, it refers to the personal ordering (taxis) of the Father, Son, and Holy Spirit, which can be orthodox (economic subordination in roles for redemption) or heretical (essential subordination of nature or power).',
    'Subordinationism': 'The heretical Trinitarian doctrine asserting that the Son or the Holy Spirit is essentially subordinate, inferior, or unequal in nature, essence, or power to the Father.',
    'supererogation': 'The performance of more work or good deeds than duty or God\'s law requires.',
    'supportment': 'Support, sustenance, or assistance.',
    'Supralapsarian': 'A Reformed view of the logical order of God\'s decrees, placing the decree of election and reprobation before the decree to permit the Fall.',
    'surcease': 'To cease, stop, or come to an end.',
    'synergism': 'The doctrine that salvation involves cooperation between human will and divine grace (as opposed to monergism).',
    'theandrical': 'Divine-human; pertaining to or existing in both the divine and human natures of Christ (from Greek \'theos\' [God] and \'aner\' [man]).',
    'Theologoumena': 'Theological assertions or opinions that are not binding dogmas but are held by scholars to explain or defend doctrines.',
    'theotokos': 'Greek term meaning \'God-bearer\' or Mother of God, used at the Council of Ephesus to defend Christ\'s deity.',
    'traducianism': 'The doctrine that the human soul is transmitted from parent to child through natural generation (as opposed to creationism).',
    'typology': 'The study of biblical types (persons, events, or institutions in the Old Testament that foreshadow realities in the New).',
    'unregenerate': 'Not spiritually reborn or regenerated; remaining in a state of spiritual death and sin.',
    'verily': 'Truly; in truth; assuredly.',
    'vicarious': 'Performed, suffered, or otherwise served in place of another; substitutionary.',
    'vouchsafe': 'To deign, condescend to grant, or bestow.',
    'wont': 'Accustomed; used to; in the habit of doing.'
}

import re

def apply_glossary_footnotes(body_html: str, cid: str, seen_glossary_terms: set, replace_first_outside_tags_and_comments) -> tuple[str, list, set]:
    """
    Scans the chapter body_html for first-occurrences of technical glossary terms.
    Injects a superscript section sign (§) and populates local_glossary.
    Supports basic string definitions or complex nested dictionaries with 'regex' rules.
    """
    local_glossary = []
    glossary_counter = 0
    gloss_placeholders = {}
    gloss_placeholder_counter = 0

    # Sort terms so longer ones match first
    sorted_terms = sorted(TECHNICAL_TERMS.items(), key=lambda x: len(x[0]), reverse=True)
    for term, definition_data in sorted_terms:
        if term in seen_glossary_terms:
            continue

        if isinstance(definition_data, dict):
            term_def = definition_data.get('definition', '')
            custom_pattern = definition_data.get('regex', rf'({re.escape(term)}(?:s|es)?)')
            flags = definition_data.get('flags', re.I)
        else:
            term_def = definition_data
            custom_pattern = rf'({re.escape(term)}(?:s|es)?)'
            flags = re.I

        pattern = re.compile(
            rf'(?<![a-zA-Z0-9\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff\u0300-\u036f־-])'
            rf'{custom_pattern}'
            rf'(?![a-zA-Z0-9\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff\u0300-\u036f־-])'
            rf'((?:</(?!p\b|li\b|ul\b|ol\b|div\b|blockquote\b|h[1-6]\b|section\b|aside\b|body\b|html\b|dt\b|dd\b|table\b|tr\b|td\b|th\b)[a-zA-Z]+>)*)'
            rf'([\.,\?!:;\'"“”’]*)',
            flags
        )

        def replace_glossary(m):
            nonlocal glossary_counter, gloss_placeholder_counter
            glossary_counter += 1
            gloss_placeholder_counter += 1
            matched_str = m.group(1)
            trailing_tags = m.group(2)
            trailing_punc = m.group(3)
            # Section sign symbol (§) for glossary notes (Rule 11)
            fn_link = f'<sup><a class="noteref noteref-glossary" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fngloss_{cid}_{glossary_counter}">§</a></sup>'
            local_glossary.append({
                'id': f"fngloss_{cid}_{glossary_counter}",
                'term': term,
                'definition': term_def
            })
            ph_key = f"__GLOSS_PH_{gloss_placeholder_counter}__"
            gloss_placeholders[ph_key] = (matched_str, trailing_tags, trailing_punc, fn_link)
            return ph_key

        body_html, replaced = replace_first_outside_tags_and_comments(body_html, pattern, replace_glossary)
        if replaced:
            seen_glossary_terms.add(term)

    # Restore all glossary placeholders, placing their footnote links after punctuation (Rule 11)
    for ph_key, (matched_str, trailing_tags, trailing_punc, fn_link) in gloss_placeholders.items():
        body_html = body_html.replace(ph_key, f"{matched_str}{trailing_tags}{trailing_punc}{fn_link}")

    return body_html, local_glossary, seen_glossary_terms
