#!/usr/bin/env python3
"""Audit a volume's intermediate JSON for text anomalies (OCR typos, bad hyphenation, punctuation spacing).

Generates a detailed Markdown and JSON report listing all flagged items with surrounding context
to allow easy triage and correction.
"""

import sys
import re
import json
import argparse
from pathlib import Path

# Set up project root on path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Whitelists for known false positives
HYPHEN_WHITELIST = {
    "after-times", "ammi-nadib", "anti-christ", "anti-christian", "anti-evangelical", "anti-trinitarians",
    "antino-mianism", "arch-apostle", "bare-foot", "ben-lafrad", "birth-place", "blood-shedding",
    "blood-thirsty", "brain-sick", "broken-hearted", "by-laws", "by-path", "by-word",
    "ca-ari", "chal-dean", "church-censures", "co-equal", "co-essential", "co-eternal",
    "co-witnessing", "com-plutensis", "common-place", "corner-stone", "cra-covia", "crel-lius",
    "day-time", "death-bed", "down-sitting", "ever-blessed", "ever-living", "eye-sore",
    "faith-constituted", "fellow-creature", "fellow-heir", "fellow-servant", "fly-leaf", "fore-knowledge",
    "fore-mentioned", "free-will", "geor-gius", "god-ward", "good-will", "heart-cleansing",
    "hedge-hog", "honey-comb", "im-pulsivam", "in-being", "intend-ment", "jaw-bone",
    "justifica-tionem", "like-wise", "master-piece", "me-lancthon", "meeting-house", "never-failing",
    "new-covenant", "non-admission", "non-compliance", "non-improvement", "non-institution", "non-payment",
    "non-performance", "noon-day", "nos-tro", "nut-shell", "osten-deret", "over-compliant",
    "over-solicitous", "over-strict", "paralo-gisms", "pater-familias", "peace-maker", "pec-catum",
    "peta-vius", "praise-worthy", "pre-appointment", "pre-eminence", "pre-existing", "pre-requisite",
    "pre-signify", "pre-tences", "ramoth-gilead", "re-admission", "re-delivery", "re-introduce",
    "rup-turam", "scape-goat", "scare-crow", "self-denial", "self-evidencing", "self-examination",
    "self-existent", "self-love", "self-same", "self-seeking", "serva-vero", "so-cinians",
    "so-cinus", "soci-nians", "son-in-law", "sub-dean", "sup-plice", "sur-misal",
    "there-with", "to-day", "to-morrow", "touch-stone", "under-age", "under-valuation",
    "us-ward", "vain-glory", "watch-tower", "way-side", "well-ordering", "well-pleasing",
    "world-without-end", "wotton-under"
}

PUNCT_WHITELIST = {
    "i.e.", "e.g.", "viz.", "a.d.", "b.c.", "vol.", "chap.", "v.", "vv.", "p.", "pp.", "sec.", "sect."
}

GLOBAL_SPLIT_WHITELIST = {
    # Heuristic 4b false positives
    "be loved", "be held", "be paid", "be done", "be met", "be run", "be set",
    "be led", "be put", "be got", "be sent", "within doors", "without doors",
    "not withstanding", "non licet", "fore mentioned", "or leans", "amor et",
    # Heuristic 4a false positives (primarily Latin prepositions or specific names)
    "e sacris", "e coelo", "e scriptis", "e mundo", "e medio", "e latere",
    "e cruce", "e nihilo", "e magis", "e min", "d ie", "in ner"
}

def load_dictionary() -> set[str]:
    """Load standard dictionary words from common system paths."""
    words_set = set()
    dict_paths = [
        Path("/usr/share/dict/words"),
        Path("/etc/dictionaries-common/words"),
        Path("/usr/dict/words")
    ]
    for path in dict_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        w = line.strip().lower()
                        if w:
                            words_set.add(w)
                break
            except Exception as e:
                print(f"[Warning] Failed to read {path}: {e}")
    
    # Basic fallbacks if no system dictionary is present
    for c in "abcdefghijklmnopqrstuvwxyz":
        words_set.add(c)
    
    # Add standard whitelisted theological terms
    extra_terms = {
        "hath", "doth", "shalt", "wilt", "thee", "thou", "thy", "thine", "ye", "unto",
        "whoso", "hereof", "thereof", "whereof", "herein", "therein", "wherein",
        "thereto", "hitherto", "lo", "puritan", "owen", "goold", "socinian", "socinianism",
        "arminian", "arminianism", "calvinist", "calvinistic", "papist", "pope", "popish",
        "petavius", "bellarmine", "grotius", "biddle", "crellius", "schlichtingius"
    }
    words_set.update(extra_terms)
    return words_set


def clean_text(text: str) -> str:
    """Strip XML tags, footnotes, and markdown formatting for cleaner matching."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\[f\d+\]", " ", text)
    text = re.sub(r"\*\*|_", "", text)
    return text


def find_contexts(text: str, target: str, limit: int = 3) -> list[str]:
    """Find occurrences of the target string and return surrounding context snippets."""
    contexts = []
    # Escape special characters
    escaped = re.escape(target)
    # If the target is a word, enforce word boundaries
    if re.match(r"^\w+$", target):
        pattern = re.compile(rf"\b{escaped}\b", re.I)
    else:
        pattern = re.compile(escaped, re.I)

    for match in pattern.finditer(text):
        start = max(0, match.start() - 50)
        end = min(len(text), match.end() + 50)
        snippet = text[start:end].strip()
        snippet = re.sub(r"\s+", " ", snippet)
        prefix = "... " if start > 0 else ""
        suffix = " ..." if end < len(text) else ""
        contexts.append(f"{prefix}{snippet}{suffix}")
        if len(contexts) >= limit:
            break
    return contexts


def check_hyphenations(text: str, dict_words: set[str]) -> list[tuple[str, str]]:
    """Identify badly hyphenated words (like 'Peta-vius')."""
    anomalies = []
    # Matches words containing exactly one hyphen
    matches = re.finditer(r"\b([A-Za-z]+)-([A-Za-z]+)\b", text)
    for m in matches:
        full_word = m.group(0)
        p1 = m.group(1)
        p2 = m.group(2)
        
        full_lower = full_word.lower()
        if full_lower in HYPHEN_WHITELIST:
            continue
            
        p1_lower = p1.lower()
        p2_lower = p2.lower()
        
        # Heuristic 1: If it's a capitalized word like Peta-vius where either part is not a valid word, flag it
        if full_word[0].isupper():
            # If p1 or p2 are nonsense words, it's highly likely to be a split anomaly
            if p1_lower not in dict_words and len(p1_lower) > 2:
                anomalies.append((full_word, "Capitalized hyphenation with unrecognized left particle"))
                continue
            if p2_lower not in dict_words and len(p2_lower) > 2:
                anomalies.append((full_word, "Capitalized hyphenation with unrecognized right particle"))
                continue
                
        # Heuristic 2: Rejoined check (if removing the hyphen yields a valid dictionary/theological word, flag it!)
        rejoined = (p1 + p2).lower()
        if rejoined in dict_words and len(rejoined) > 4:
            anomalies.append((full_word, f"Splittable word (rejoins to valid word '{p1+p2}')"))
            continue
            
        # Heuristic 3: Check if both parts are unrecognized short fragments
        if p1_lower not in dict_words and p2_lower not in dict_words:
            if len(p1_lower) > 2 or len(p2_lower) > 2:
                anomalies.append((full_word, "Hyphenated word with unrecognized particles on both sides"))
                
    return anomalies


def check_punctuation(text: str) -> list[tuple[str, str]]:
    """Identify bad punctuation spacings and duplicated punctuation anomalies."""
    anomalies = []
    
    # 1. Spaces before basic punctuation: word , or word . (except ellipsis)
    # Avoid mathematical spacing or scriptures
    matches = re.finditer(r"\b[A-Za-z0-9]+\s+([,;:!?])", text)
    for m in matches:
        anomalies.append((m.group(0), "Spaced punctuation (space before character)"))
        
    matches = re.finditer(r"\b[A-Za-z0-9]+\s+\.(?!\.)", text)
    for m in matches:
        anomalies.append((m.group(0), "Spaced period (space before period)"))

    # 2. Duplicated punctuation (,, or ;; or :: or exactly two periods ..)
    matches = re.finditer(r",,", text)
    for m in matches:
        anomalies.append((m.group(0), "Duplicate comma"))
        
    matches = re.finditer(r";;", text)
    for m in matches:
        anomalies.append((m.group(0), "Duplicate semicolon"))
        
    matches = re.finditer(r"::", text)
    for m in matches:
        anomalies.append((m.group(0), "Duplicate colon"))
        
    matches = re.finditer(r"(?<!\.)\.\.(?!\.)", text)
    for m in matches:
        anomalies.append((m.group(0), "Duplicate period (double dot)"))

    # 3. Spaces inside brackets/parentheses
    matches = re.finditer(r"\(\s+[A-Za-z0-9]", text)
    for m in matches:
        anomalies.append((m.group(0), "Spaced opening parenthesis"))
        
    matches = re.finditer(r"[A-Za-z0-9]\s+\)", text)
    for m in matches:
        anomalies.append((m.group(0), "Spaced closing parenthesis"))

    return anomalies


def check_ocr_residues(text: str, dict_words: set[str] = None) -> list[tuple[str, str]]:
    """Identify classic OCR artifacts like bracket residues, mixed alphanumeric words, and split word anomalies."""
    anomalies = []
    
    # 1. Bracket characters inside words, e.g. on]y, name]y, th[e]
    matches = re.finditer(r"\b[A-Za-z]+[\]\)]+[A-Za-z]+\b", text)
    for m in matches:
        anomalies.append((m.group(0), "OCR residue containing stray closing bracket/paren"))
        
    matches = re.finditer(r"\b[A-Za-z]+[\[\(]+[A-Za-z]+\b", text)
    for m in matches:
        anomalies.append((m.group(0), "OCR residue containing stray opening bracket/paren"))

    # 2. Mixed letters and numbers inside a word (e.g. w1th, th1s, l1ke)
    # Ignore standard ordinals (1st, 2nd, 3rd, etc.) and volume numbers or verse refs
    matches = re.finditer(r"\b[A-Za-z]+\d+[A-Za-z]+\b", text)
    for m in matches:
        anomalies.append((m.group(0), "Spliced alphanumeric word (contains inline numbers)"))

    # 3. Empty brackets [ ] or []
    matches = re.finditer(r"\[\s*\]", text)
    for m in matches:
        anomalies.append((m.group(0), "Empty square brackets"))

    # 4. Spliced/split words check using dictionary heuristics
    if dict_words:
        # Heuristic 4a: Isolated letter (except a, i, o) followed by space and then lowercase word segment.
        # Exclude possessives (e.g., "Owen's preface", "Majesty's chaplains") using lookbehind.
        # E.g. "s upernatural", "c ommon", "p erfect"
        matches = re.finditer(r"(?<!['’])\b([a-zA-Z])\s+([a-z][a-zA-Z]*)\b", text)
        for m in matches:
            let = m.group(1)
            target = m.group(0)
            if let.lower() not in ('a', 'i', 'o'):
                if target.lower().strip() not in GLOBAL_SPLIT_WHITELIST:
                    anomalies.append((target, f"Split word anomaly (isolated letter '{let}')"))

        # Heuristic 4b: Rejoined check for consecutive word tokens
        # E.g. "acknow ledged" -> rejoined "acknowledged" is valid, but "ledged" is not a valid word.
        matches = re.finditer(r"\b([A-Za-z]{2,})\s+([A-Za-z]{2,})\b", text)
        for m in matches:
            w1 = m.group(1)
            w2 = m.group(2)
            target = m.group(0)
            rejoined = (w1 + w2).lower()
            w2_lower = w2.lower()
            if len(rejoined) > 4:
                if rejoined in dict_words and w2_lower not in dict_words:
                    if target.lower().strip() not in GLOBAL_SPLIT_WHITELIST:
                        anomalies.append((target, f"Split word anomaly (rejoins to '{w1+w2}')"))

    return anomalies


def check_capitalization(text: str) -> list[tuple[str, str]]:
    """Identify mixed-case capitalization issues (e.g., 'thE', 'anD', 'ChriSt')."""
    anomalies = []
    # Matches words with mixed uppercase/lowercase inside, excluding standard acronyms
    matches = re.finditer(r"\b[a-z]+[A-Z]+[a-z]*\b", text)
    for m in matches:
        word = m.group(0)
        # Avoid standard greek/hebrew or single letter variables
        if len(word) > 2:
            anomalies.append((word, "Mixed-case capitalization error"))
            
    matches = re.finditer(r"\b[A-Z][a-z]+[A-Z]+[a-z]*\b", text)
    for m in matches:
        word = m.group(0)
        # Exclude standard compound words like McCheyne, McDonald, etc.
        if not word.startswith(("Mc", "Mac", "De")):
            anomalies.append((word, "Mixed-case capitalization error"))
            
    return anomalies


def check_unresolved_citations(text: str, cid: str) -> list[tuple[str, str]]:
    """Scan for patristic/classical citations and flag if they cannot be resolved."""
    # Local imports to avoid circular dependency issues
    from patristic_refs import PATRISTIC_CITATION_RE, SELF_REF_PATTERNS, build_citation_note
    from translation_db import BODY_TRANSLATIONS
    
    anomalies = []
    for m in PATRISTIC_CITATION_RE.finditer(text):
        cite_str = m.group(0).strip()
        ctx_start = max(0, m.start() - 120)
        ctx_end = min(len(text), m.end() + 80)
        context_before = text[ctx_start:m.start()].replace('\n', ' ')
        full_context = text[ctx_start:ctx_end].replace('\n', ' ')
        
        # Check if already resolved via BODY_TRANSLATIONS or local patristic map
        resolved = any(
            phrase in full_context
            for phrase in BODY_TRANSLATIONS
            if len(phrase) > 8
        )
        if not resolved:
            if build_citation_note(cite_str, context_before) is not None:
                resolved = True
                
        is_self_ref = bool(SELF_REF_PATTERNS.search(context_before))
        
        if not resolved and not is_self_ref:
            anomalies.append((cite_str, "Unresolved patristic/classical citation reference (no translation found)"))
            
    return anomalies


def check_structural_nesting(text: str) -> list[tuple[str, str]]:
    """Rigorous audit of sequential outline enumerators (1., 2. or I., II. or (a), (b)) to flag sequence jumps."""
    anomalies = []
    
    # Types of sequence markers to scan:
    # 1. Standard numbered lists at paragraph starts: e.g. " 1. " or " 2. "
    # 2. Parenthesized numbers: e.g. "(1)", "(2)"
    # 3. Parenthesized alphabetic: e.g. "(a)", "(b)"
    # 4. Roman numeral lists: e.g. "I.", "II.", "III."
    
    # Let's extract all matches with their positions and types
    patterns = {
        "arabic_dot": re.compile(r"\b(\d+)\.\s"),
        "arabic_paren": re.compile(r"\((\d+)\)\s"),
        "alpha_paren": re.compile(r"\(([a-z])\)\s"),
        "roman_dot": re.compile(r"\b([IVXLCDM]+)\.\s")
    }
    
    # Helper to convert roman to arabic integer
    def roman_to_int(roman: str) -> int:
        r_map = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
        val = 0
        for i in range(len(roman)):
            if i > 0 and r_map[roman[i]] > r_map[roman[i-1]]:
                val += r_map[roman[i]] - 2 * r_map[roman[i-1]]
            else:
                val += r_map[roman[i]]
        return val

    # Whitelisted books of the Bible to skip scripture references
    BOOK_NAMES = {
        'genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges', 'ruth', 'samuel', 'kings',
        'chronicles', 'ezra', 'nehemiah', 'esther', 'job', 'psalm', 'psalms', 'proverbs', 'ecclesiastes', 'canticles',
        'solomon', 'isaiah', 'jeremiah', 'lamentations', 'ezekiel', 'daniel', 'hosea', 'joel', 'amos', 'obadiah',
        'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 'haggai', 'zechariah', 'malachi', 'matthew', 'mark',
        'luke', 'john', 'acts', 'romans', 'corinthians', 'galatians', 'ephesians', 'philippians', 'colossians',
        'thessalonians', 'timothy', 'titus', 'philemon', 'hebrews', 'james', 'peter', 'jude', 'revelation'
    }

    # Scan for each pattern
    for key, regex in patterns.items():
        sequence = []
        for m in regex.finditer(text):
            val_str = m.group(1)
            
            # Context checks to filter out scripture verses and other non-outline numbers
            context_before_short = text[max(0, m.start()-15):m.start()].lower()
            
            # Skip verse numbers (preceded by colon)
            if context_before_short.endswith(':'):
                continue
                
            # Skip verse lists or ranges (preceded by comma or hyphen/dash)
            if re.search(r'[,-]\s*$', context_before_short):
                continue
                
            # Skip scripture book names immediately preceding the number
            last_word_match = re.search(r'\b([a-z]+)\b\s*$', context_before_short)
            if last_word_match and last_word_match.group(1) in BOOK_NAMES:
                continue
                
            # Skip page, chapter, volume, verse, book, lib, cap abbreviations
            if any(context_before_short.rstrip().endswith(abbrev) for abbrev in [
                'p.', 'pp.', 'vol.', 'chap.', 'v.', 'vv.', 'lib.', 'cap.', 'book', 
                'volume', 'chapter', 'section', 'sect.', 'page', 'verse', 'no.'
            ]):
                continue
                
            # Parse value to an integer index
            if key in ("arabic_dot", "arabic_paren"):
                val = int(val_str)
                if 1000 <= val <= 2100:  # Skip standard year numbers in text
                    continue
            elif key == "alpha_paren":
                val = ord(val_str) - ord('a') + 1
            else:  # roman_dot
                val = roman_to_int(val_str)
                if val > 50:  # Skip name initials like D. Petavius or M. Biddle
                    continue
            sequence.append((m.start(), m.group(0).strip(), val))
            
        # Audit the sequence for jumps
        for i in range(len(sequence) - 1):
            pos1, str1, val1 = sequence[i]
            pos2, str2, val2 = sequence[i+1]
            
            # If they are relatively close in text (within 8000 characters - a couple of pages)
            if pos2 - pos1 < 8000:
                # If val2 is exactly 1, it's a list reset/nesting restart, which is fine
                if val2 == 1:
                    continue
                # If val2 is less than or equal to val1, it could be a parent list restart or reset, which is fine
                if val2 <= val1:
                    continue
                # If val2 > val1 + 1, it's a sequence jump! (e.g. 1 then 3, or II then IV)
                if val2 > val1 + 1:
                    anomalies.append((f"{str1} ... {str2}", f"List sequence jump (skipped from {val1} to {val2})"))
                    
    return anomalies


def is_whitelisted(category: str, target: str, whitelist: dict) -> bool:
    items = whitelist.get("anomalies", {}).get(category, [])
    if target in items:
        return True
    for item in items:
        if item in target or target in item:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Audit a volume's intermediate JSON for OCR, hyphenation, and punctuation anomalies.")
    parser.add_argument("volume", type=int, help="Volume number (e.g., 12)")
    args = parser.parse_args()

    vol_num = args.volume
    here = Path(__file__).resolve().parent
    root = here.parent
    vol_dir = root / "volumes" / f"v{vol_num}"
    vol_json_path = vol_dir / "intermediate" / f"volume_{vol_num}.json"
    output_md_path = vol_dir / "bugs_fixes" / f"volume_{vol_num}_anomalies.md"
    output_json_path = vol_dir / "bugs_fixes" / f"volume_{vol_num}_anomalies.json"

    if not vol_json_path.exists():
        print(f"Error: Volume intermediate JSON not found: {vol_json_path}")
        sys.exit(1)

    print(f"Loading dictionary...")
    dict_words = load_dictionary()
    
    print(f"Reading Volume {vol_num} intermediate JSON...")
    with open(vol_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    whitelist = {}
    whitelist_path = vol_dir / "bugs_fixes" / f"volume_{vol_num}_whitelist.json"
    if whitelist_path.exists():
        try:
            whitelist = json.loads(whitelist_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[Warning] Failed to load whitelist {whitelist_path}: {e}")

    # Dictionary to hold all anomalies grouped by category
    categories = {
        "Hyphenation Anomalies": [],
        "Punctuation Spacing Blemishes": [],
        "OCR & Bracket Residues": [],
        "Mixed-Case Capitalization Errors": [],
        "Unresolved Citation References": [],
        "Structural Nesting Sequence Jumps": []
    }

    # Total counts
    total_scanned_words = 0
    
    print("Auditing chapters...")
    for ch_idx, ch in enumerate(data.get("chapters", [])):
        title = ch.get("title", f"Chapter {ch_idx}")
        raw_text = clean_text(ch.get("raw_text", "") or "")
        if not raw_text:
            continue
            
        # Count words scanned
        words = re.findall(r"\b[A-Za-z]+\b", raw_text)
        total_scanned_words += len(words)
        
        # 1. Check Hyphenations
        hyphen_hits = check_hyphenations(raw_text, dict_words)
        for target, desc in hyphen_hits:
            if is_whitelisted("Hyphenation Anomalies", target, whitelist):
                continue
            snippets = find_contexts(raw_text, target)
            categories["Hyphenation Anomalies"].append({
                "target": target,
                "description": desc,
                "chapter": title,
                "contexts": snippets
            })
            
        # 2. Check Punctuation Spacing
        punct_hits = check_punctuation(raw_text)
        for target, desc in punct_hits:
            if is_whitelisted("Punctuation Spacing Blemishes", target, whitelist):
                continue
            snippets = find_contexts(raw_text, target)
            categories["Punctuation Spacing Blemishes"].append({
                "target": target,
                "description": desc,
                "chapter": title,
                "contexts": snippets
            })
            
        # 3. Check OCR & Bracket Residues
        ocr_hits = check_ocr_residues(raw_text, dict_words)
        for target, desc in ocr_hits:
            if is_whitelisted("OCR & Bracket Residues", target, whitelist):
                continue
            snippets = find_contexts(raw_text, target)
            categories["OCR & Bracket Residues"].append({
                "target": target,
                "description": desc,
                "chapter": title,
                "contexts": snippets
            })
            
        # 4. Check Capitalization Issues
        cap_hits = check_capitalization(raw_text)
        for target, desc in cap_hits:
            if is_whitelisted("Mixed-Case Capitalization Errors", target, whitelist):
                continue
            snippets = find_contexts(raw_text, target)
            categories["Mixed-Case Capitalization Errors"].append({
                "target": target,
                "description": desc,
                "chapter": title,
                "contexts": snippets
            })
 
        # 5. Check Unresolved Citations
        cite_hits = check_unresolved_citations(raw_text, ch.get("cid", ""))
        for target, desc in cite_hits:
            if is_whitelisted("Unresolved Citation References", target, whitelist):
                continue
            snippets = find_contexts(raw_text, target)
            categories["Unresolved Citation References"].append({
                "target": target,
                "description": desc,
                "chapter": title,
                "contexts": snippets
            })
            
        # 6. Check Structural Nesting Sequence Jumps
        nest_hits = check_structural_nesting(raw_text)
        for target, desc in nest_hits:
            if is_whitelisted("Structural Nesting Sequence Jumps", target, whitelist):
                continue
            snippets = find_contexts(raw_text, target)
            categories["Structural Nesting Sequence Jumps"].append({
                "target": target,
                "description": desc,
                "chapter": title,
                "contexts": snippets
            })

    # Deduplicate hits per category (target + chapter context)
    deduped_categories = {}
    for cat_name, items in categories.items():
        seen = set()
        deduped_items = []
        for item in items:
            key = (item["target"].lower(), item["chapter"])
            if key not in seen:
                seen.add(key)
                deduped_items.append(item)
        deduped_categories[cat_name] = deduped_items

    # Total anomalies count
    total_anomalies = sum(len(items) for items in deduped_categories.values())

    # Ensure output directories exist
    vol_dir.mkdir(parents=True, exist_ok=True)
    (vol_dir / "bugs_fixes").mkdir(parents=True, exist_ok=True)

    # Write Markdown Report
    print(f"Writing Markdown report to {output_md_path}...")
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(f"# Text Integrity & Anomaly Audit Report: Volume {vol_num}\n\n")
        f.write(f"This report highlights potential OCR discrepancies, bad hyphenations (e.g., line-break remains), punctuation alignment issues, and casing anomalies.\n\n")
        f.write(f"* **Total Words Audited:** {total_scanned_words}\n")
        f.write(f"* **Total Suspected Anomalies Found:** {total_anomalies}\n\n")
        f.write(f"Add corrections to `text_replacements` inside `volumes/v{vol_num}/convert.py` to fix these.\n\n")
        f.write("## Summary by Category\n\n")
        for cat_name, items in deduped_categories.items():
            f.write(f"* **{cat_name}:** {len(items)} items\n")
        f.write("\n---\n\n")

        for cat_name, items in deduped_categories.items():
            f.write(f"## {cat_name}\n\n")
            if not items:
                f.write("No anomalies found in this category.\n\n")
                continue
                
            for idx, item in enumerate(items, 1):
                f.write(f"### {idx}. `{item['target']}`\n")
                f.write(f"* **Description:** {item['description']}\n")
                f.write(f"* **Chapter:** *{item['chapter']}*\n")
                f.write(f"* **Contexts:**\n")
                for ctx in item["contexts"]:
                    # Highlight the target in context
                    highlighted = re.sub(rf"({re.escape(item['target'])})", r"**\1**", ctx, flags=re.I)
                    f.write(f"  * {highlighted}\n")
                f.write("\n")
            f.write("---\n\n")

    # Write JSON Report
    print(f"Writing JSON report to {output_json_path}...")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "volume": vol_num,
            "total_words_audited": total_scanned_words,
            "total_anomalies_count": total_anomalies,
            "anomalies": deduped_categories
        }, f, indent=2)

    print(f"\n======================================================================")
    print(f" AUDIT COMPLETE: VOLUME {vol_num}")
    print(f" Total suspected anomalies: {total_anomalies}")
    print(f" Report written to: {output_md_path}")
    print(f"======================================================================\n")


if __name__ == "__main__":
    main()
