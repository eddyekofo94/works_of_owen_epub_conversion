import json
import re
import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from translation_db import FOOTNOTE_TRANSLATIONS, BODY_TRANSLATIONS

LATIN_WORDS = {
    'et', 'est', 'non', 'sunt', 'satis', 'sicut', 'vero', 'enim', 'autem', 'etiam',
    'nihil', 'hic', 'iam', 'tamen', 'vel', 'nec', 'sed', 'cum', 'qui', 'quae', 'quod',
    'pro', 'ad', 'ab', 'ex', 'per', 'in', 'ut', 'se', 'aut', 'sine', 'atque', 'sub',
    'illud', 'illa', 'ipso', 'ipsa', 'tibi', 'mihi', 'nobis', 'vobis', 'eorum', 'ejus'
}

ENGLISH_WORDS = {
    'the', 'of', 'and', 'to', 'is', 'that', 'was', 'for', 'on', 'are', 'with', 'as',
    'his', 'they', 'he', 'she', 'it', 'from', 'this', 'but', 'not', 'have', 'had'
}

def is_latin_text(text: str) -> bool:
    # Clean text to words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if not words:
        return False
    
    latin_count = sum(1 for w in words if w in LATIN_WORDS)
    english_count = sum(1 for w in words if w in ENGLISH_WORDS)
    
    # If there are many Latin words and very few English words, it is Latin
    if latin_count > 0 and latin_count >= english_count:
        return True
    
    # Or if the text has classic Latin indicators like lib., cap., orat. but has very high Latin-to-English ratio
    if re.search(r'\b(lib|cap|epist|serm|orat|tract|homil|haer|dial|adv)\.', text.lower()):
        if english_count < 3:
            return True
            
    return False

def scan_volume_12():
    with open('volumes/v12/intermediate/volume_12.json') as f:
        data = json.load(f)
        
    print("=" * 80)
    print("SCANNING VOLUME 12 FOR UNTRANSLATED LATIN / REFERENCES")
    print("=" * 80)
    
    # 1. Scan Footnotes
    untranslated_footnotes = []
    footnotes = data.get('footnotes', {})
    for fnum_str, fn in footnotes.items():
        text = fn.get('text', '')
        # Check if already translated
        trans_key = f"v12_fn{fnum_str}"
        if trans_key in FOOTNOTE_TRANSLATIONS:
            continue
            
        # Is it Latin?
        if is_latin_text(text):
            untranslated_footnotes.append((fnum_str, text))
            
    print(f"\nFound {len(untranslated_footnotes)} untranslated Latin footnotes:")
    for fnum, text in untranslated_footnotes:
        print(f"  - Footnote {fnum}: {text}")
        
    # 2. Scan Body Paragraphs
    untranslated_body_paragraphs = []
    sorted_phrases = sorted(BODY_TRANSLATIONS.keys(), key=len, reverse=True)
    
    for ch_idx, ch in enumerate(data.get('chapters', [])):
        title = ch.get('title', '')
        text = ch.get('raw_text', '')
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        for p_idx, p in enumerate(paragraphs):
            # Exclude headers or system tags
            if p.startswith('[[') or p.startswith('**'):
                continue
                
            # Check if already translated via BODY_TRANSLATIONS
            is_translated = False
            for phrase in sorted_phrases:
                # Simple check: if a decent-sized phrase is in this paragraph
                if len(phrase) > 15 and phrase.lower()[:30] in p.lower():
                    is_translated = True
                    break
                    
            if is_translated:
                continue
                
            # Check if it has Latin markers or blocks of Latin text
            # Especially looking for quotes inside quotes or blockquotes or classic references
            if is_latin_text(p):
                untranslated_body_paragraphs.append((title, p_idx, p))
            elif re.search(r'\b(lib|cap|epist)\.\s*\d+', p.lower()):
                # If it has a reference but might not be fully Latin, let's flag for review
                untranslated_body_paragraphs.append((title, p_idx, p))
                
    print(f"\nFound {len(untranslated_body_paragraphs)} untranslated / unannotated body paragraphs:")
    for ch_title, p_idx, p in untranslated_body_paragraphs[:30]:  # Limit output
        print(f"  - [{ch_title}] P{p_idx}: {p[:200]}...")
        
if __name__ == '__main__':
    scan_volume_12()
