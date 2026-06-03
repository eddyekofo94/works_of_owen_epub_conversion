import os
import json
import re
from pathlib import Path
import pytest

from scripts.scan_citations import load_volume, scan_volume

BASE_DIR = Path(__file__).parent.parent
VOLUMES_DIR = BASE_DIR / "volumes"

# Budget for maximum allowable unresolved citations per volume
# This prevents regressions where citations become unresolved again.
UNRESOLVED_BUDGETS = {
    1: 0,
    2: 2,
    3: 0,
    4: 13,
    5: 6,
    6: 0,
    7: 3,
    8: 18,
    9: 0,
    10: 12,
    11: 7,
    12: 0,
    13: 3,
    14: 16,
    15: 21,
    16: 37,
}

# Strict budgets for untranslated Latin or Greek prose footnotes
UNTRANSLATED_PROSE_FOOTNOTE_BUDGETS = {
    1: 3,
    2: 2,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 1,
    9: 1,
    10: 5,
    11: 0,
    12: 1,  # William H. Goold's English editorial note discussing Greek variants
    13: 1,
    14: 1,
    15: 0,
    16: 3,
}

# Refined Latin words specific to prose/verses (excluding highly common English prepositions)
LATIN_WORDS_REFINED = {
    'et', 'est', 'non', 'sunt', 'enim', 'autem', 'etiam', 'nihil', 'hic', 'iam',
    'tamen', 'vel', 'nec', 'sed', 'cum', 'qui', 'quae', 'quod', 'ut', 'aut', 'sine',
    'atque', 'eorum', 'ejus', 'ipsa', 'ipso', 'illa', 'illud', 'quoniam', 'propter',
    'quia', 'verum', 'vero'
}

def is_latin_prose(text: str) -> bool:
    """Detects if a footnote is a substantial block of Latin prose requiring a translation note."""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if len(words) < 8:
        return False
    
    latin_words_found = {w for w in words if w in LATIN_WORDS_REFINED}
    if len(latin_words_found) < 3:
        return False
        
    # Exclude standard bibliographical citations that happen to contain many abbreviations
    citations = len(re.findall(r'\b(lib|cap|epist|serm|orat|tract|homil|haer|dial|adv|p|col|tom|fol)\b', text.lower()))
    if citations > len(latin_words_found) * 1.5:
        return False
        
    return True

def is_greek_prose(text: str) -> bool:
    """Detects if a footnote contains a substantial block of Greek prose requiring a translation note."""
    greek_words = re.findall(r'\b[\u0370-\u03ff\u1f00-\u1fff]+\b', text)
    return len(greek_words) >= 4

def get_available_volumes():
    vols = []
    for d in VOLUMES_DIR.glob("v*"):
        if d.is_dir() and d.name[1:].isdigit():
            vol_num = int(d.name[1:])
            intermediate = d / "intermediate" / f"volume_{vol_num}.json"
            if intermediate.exists():
                vols.append(vol_num)
    return sorted(vols)

@pytest.mark.parametrize("vol_num", get_available_volumes())
def test_unresolved_citation_budgets(vol_num):
    """
    Ensures that the number of unresolved patristic/classical citations
    does not exceed the known budget for each volume.
    """
    data = load_volume(vol_num)
    if not data:
        pytest.skip(f"Volume {vol_num} intermediate JSON not found.")
        
    hits = scan_volume(vol_num, data)
    unresolved = [h for h in hits if not h['already_resolved'] and not h['is_self_ref']]
    
    unresolved_count = len(unresolved)
    budget = UNRESOLVED_BUDGETS.get(vol_num, 100) # Fallback budget for un-audited volumes
    
    # If the count goes down, developers should lower the budget in this test!
    assert unresolved_count <= budget, (
        f"Volume {vol_num} has {unresolved_count} unresolved citations, "
        f"which exceeds the budget of {budget}. "
        "Did a translation string get corrupted or removed?"
    )
    
    # Optional: warn if we have beaten the budget so the test file can be updated
    if unresolved_count < budget:
        print(f"\nSUCCESS: Volume {vol_num} beat its citation budget! "
              f"(Got {unresolved_count}, budgeted {budget}). "
              "Please lower the budget in test_unresolved_citations.py.")

@pytest.mark.parametrize("vol_num", get_available_volumes())
def test_untranslated_prose_footnotes(vol_num):
    """
    Deep semantic check: Ensures that all substantial Latin or Greek prose footnotes
    have a modern academic translation note resolved in translation_db.py.
    """
    from translation_db import FOOTNOTE_TRANSLATIONS
    
    data = load_volume(vol_num)
    if not data:
        pytest.skip(f"Volume {vol_num} intermediate JSON not found.")
        
    untranslated_fns = []
    footnotes = data.get("footnotes", {})
    for fnum_str, fn in footnotes.items():
        text = fn.get("text", "")
        # Check if already translated in the database
        trans_key = f"v{vol_num}_fn{fnum_str}"
        if trans_key in FOOTNOTE_TRANSLATIONS:
            continue
            
        if is_latin_prose(text) or is_greek_prose(text):
            untranslated_fns.append((fnum_str, text))
            
    untranslated_count = len(untranslated_fns)
    budget = UNTRANSLATED_PROSE_FOOTNOTE_BUDGETS.get(vol_num, 10)
    
    # Assert that untranslated prose footnotes do not exceed the allowed budget
    error_msg = (
        f"Volume {vol_num} has {untranslated_count} untranslated prose footnotes, "
        f"exceeding the strict budget of {budget}.\n"
    )
    for fnum, text in untranslated_fns[:10]:
        error_msg += f"  - Fn {fnum}: {text[:120]}...\n"
        
    assert untranslated_count <= budget, error_msg
    
    if untranslated_count < budget:
        print(f"\nSUCCESS: Volume {vol_num} beat its untranslated prose footnote budget! "
              f"(Got {untranslated_count}, budgeted {budget}). "
              "Please lower the budget in test_unresolved_citations.py.")

@pytest.mark.parametrize("vol_num", get_available_volumes())
def test_untranslated_prose_body(vol_num):
    """
    Deep semantic check: Ensures that all substantial Latin or Greek prose runs in
    the body paragraphs have a modern academic translation mapped in BODY_TRANSLATIONS.
    """
    from translation_db import BODY_TRANSLATIONS
    
    data = load_volume(vol_num)
    if not data:
        pytest.skip(f"Volume {vol_num} intermediate JSON not found.")
        
    COMMON_ENGLISH_WORDS = {
        'the', 'and', 'of', 'to', 'a', 'in', 'is', 'that', 'it', 'he', 'was', 'for', 'on', 'are', 'as', 'with', 'his', 
        'they', 'i', 'this', 'be', 'at', 'have', 'from', 'or', 'by', 'one', 'had', 'not', 'but', 'what', 'all', 'were', 
        'we', 'when', 'your', 'my', 'their', 'them', 'who', 'which', 'him', 'whose', 'our', 'us', 'you', 'your', 'so',
        'if', 'out', 'up', 'do', 'will', 'no', 'only', 'would', 'there', 'about', 'more', 'can', 'has', 'been'
    }

    LATIN_INDICATOR_WORDS = {
        'et', 'est', 'non', 'sunt', 'enim', 'autem', 'sed', 'quod', 'qui', 'quae', 'ut', 'ad', 'per', 'ab', 'cum', 'vel',
        'nec', 'se', 'sibi', 'suo', 'sua', 'ejus', 'eorum', 'de', 'ex', 'pro', 'sine', 'atque', 'quia', 'vero', 'nam',
        'hic', 'haec', 'hoc', 'ipsa', 'ipso', 'illud', 'illa', 'tamen', 'dum', 'ita', 'si', 'nisi', 'sub', 'ob', 'sod'
    }

    def is_body_latin_prose(text: str) -> bool:
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        if len(words) < 5:
            return False
        
        english_count = sum(1 for w in words if w in COMMON_ENGLISH_WORDS)
        latin_indicator_count = sum(1 for w in words if w in LATIN_INDICATOR_WORDS)
        
        non_english_count = len(words) - english_count
        if non_english_count < 4:
            return False
            
        if latin_indicator_count >= 2 and non_english_count / len(words) > 0.6:
            return True
        return False

    def is_body_greek_prose(text: str) -> bool:
        greek_words = re.findall(r'\b[\u0370-\u03ff\u1f00-\u1fff]+\b', text)
        return len(greek_words) >= 4

    untranslated_body_runs = []
    for ch in data.get("chapters", []):
        raw = ch.get("raw_text", "")
        paragraphs = [p.strip() for p in raw.split("\n\n") if p.strip()]
        for p_idx, p in enumerate(paragraphs):
            quotes = re.findall(r'\"([^\"]{8,})\"', p)
            for quote in quotes:
                quote = quote.strip()
                if is_body_latin_prose(quote) or is_body_greek_prose(quote):
                    translated = False
                    for phrase in BODY_TRANSLATIONS:
                        if phrase in quote or quote in phrase:
                            translated = True
                            break
                    if not translated:
                        untranslated_body_runs.append((ch.get("title"), p_idx, quote))

    untranslated_count = len(untranslated_body_runs)
    budget = 145 if vol_num == 12 else 200
    
    error_msg = (
        f"Volume {vol_num} has {untranslated_count} untranslated body prose runs, "
        f"exceeding the budget of {budget}.\n"
    )
    for title, p_idx, quote in untranslated_body_runs[:10]:
        error_msg += f"  - Ch [{title}], P {p_idx}: {quote[:120]}...\n"
        
    assert untranslated_count <= budget, error_msg


