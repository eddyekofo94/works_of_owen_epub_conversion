#!/usr/bin/env python3
"""Audit spelling and identify potential OCR typos in Owen Works conversion volumes.

Filters out standard 17th-century Puritan spelling variations and focuses on
genuine OCR errors, displaying results in context to make identification easy.
"""

import sys
import re
import json
import argparse
from pathlib import Path
from collections import Counter

# Set up project root on path
sys.path.insert(0, str(Path(__file__).parent.parent))

WORD_RE = re.compile(r"\b[A-Za-z'’-]+\b")

# Common 17th-century Puritan/archaic words to whitelist directly
PURITAN_WHITELIST = {
    "hath", "doth", "shalt", "wilt", "thee", "thou", "thy", "thine", "ye", "unto",
    "whoso", "hereof", "thereof", "whereof", "herein", "therein", "wherein",
    "thereto", "hitherto", "lo", "ayde", "sayest", "triall", "doe", "goe",
    "sinne", "worde", "trueth", "selfe", "worke", "bee", "hime", "onely",
    "publique", "catholique", "encrease", "publick", "catholick", "onlie",
    "bodie", "everie", "simplie", "speciallie", "darknesse", "fulnesse",
    "sinfull", "clearnesse", "allmost", "doeth", "goeth", "heareth", "speaketh",
    "worketh", "knoweth", "calleth", "maketh", "seeth", "believeth", "loveth",
    "proveth", "pleaseth", "standeth", "abideth", "liveth", "mortifieth",
    "justifieth", "concupiscence", "obnoxious", "sundry", "evidenced",
    "concernment", "considerative", "surprisals", "condited", "Antitrinitarian",
    "Nestorius", "Socinus", "Bellarmine", "Calvinistic", "Antinomianism",
    "Socinians", "Papists", "Arminianism", "Charnock", "Owen", "Owens", "Goold",
    "justification", "justifying", "evidences", "testimonies", "disquisitions",
    "suretiship", "explication", "contrivance", "frontispiece", "preface",
    "prefatory", "treatise", "apostasy", "sanctification", "glorification",
    "interjection", "forensic", "juridical", "suretyship", "implied", "coalesce",
    "deduplication", "orthography"
}

# Scripture book names to whitelist directly
SCRIPTURE_BOOKS = {
    "genesis", "exodus", "leviticus", "numbers", "deuteronomy", "joshua",
    "judges", "ruth", "samuel", "kings", "chronicles", "ezra", "nehemiah",
    "esther", "job", "psalm", "psalms", "proverbs", "ecclesiastes", "song",
    "solomon", "isaiah", "jeremiah", "lamentations", "ezekiel", "daniel",
    "hosea", "joel", "amos", "obadiah", "jonah", "micah", "nahum",
    "habakkuk", "zephaniah", "haggai", "zechariah", "malachi", "matthew",
    "mark", "luke", "john", "acts", "romans", "corinthians", "galatians",
    "ephesians", "philippians", "colossians", "thessalonians", "timothy",
    "titus", "philemon", "hebrews", "james", "peter", "jude", "revelation"
}


def load_dictionary() -> set[str]:
    """Load standard dictionary words from /usr/share/dict/words."""
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
    
    # Add standard lowercase alphabets and basic punctuation words
    for c in "abcdefghijklmnopqrstuvwxyz":
        words_set.add(c)
    return words_set


def is_valid_word(word: str, dict_words: set[str]) -> bool:
    """Check if word is in dictionary or matches standard inflection endings."""
    if word in dict_words or word in PURITAN_WHITELIST or word in SCRIPTURE_BOOKS:
        return True

    # 1. Plurals and third-person singulars: trailing 's'
    if word.endswith("s") and len(word) > 2:
        if word[:-1] in dict_words or word[:-1] in PURITAN_WHITELIST:
            return True
        if word.endswith("es"):
            if word[:-2] in dict_words or word[:-2] in PURITAN_WHITELIST:
                return True
            if word.endswith("ies"):
                stem = word[:-3] + "y"
                if stem in dict_words or stem in PURITAN_WHITELIST:
                    return True

    # 2. Past tense and participles: trailing 'ed' or 'd'
    if word.endswith("ed") and len(word) > 3:
        if word[:-1] in dict_words or word[:-1] in PURITAN_WHITELIST:  # e.g., loved -> love
            return True
        if word[:-2] in dict_words or word[:-2] in PURITAN_WHITELIST:  # e.g., walked -> walk
            return True
        # Doubled consonants: e.g., admitted -> admit
        stem = word[:-2]
        if len(stem) > 2 and stem[-1] == stem[-2]:
            if stem[:-1] in dict_words or stem[:-1] in PURITAN_WHITELIST:
                return True

    # 3. Present participles: trailing 'ing'
    if word.endswith("ing") and len(word) > 4:
        if word[:-3] in dict_words or word[:-3] in PURITAN_WHITELIST:  # e.g., walking -> walk
            return True
        if (word[:-3] + "e") in dict_words or (word[:-3] + "e") in PURITAN_WHITELIST:  # e.g., loving -> love
            return True
        # Doubled consonants: e.g., admitting -> admit
        stem = word[:-3]
        if len(stem) > 2 and stem[-1] == stem[-2]:
            if stem[:-1] in dict_words or stem[:-1] in PURITAN_WHITELIST:
                return True

    # 4. Adverbs: trailing 'ly'
    if word.endswith("ly") and len(word) > 3:
        if word[:-2] in dict_words or word[:-2] in PURITAN_WHITELIST:  # e.g., quickly -> quick
            return True
        if word.endswith("ily"):  # e.g., happily -> happy
            stem = word[:-3] + "y"
            if stem in dict_words or stem in PURITAN_WHITELIST:
                return True

    # 5. Comparatives/superlatives: trailing 'er', 'est'
    if word.endswith("er") and len(word) > 3:
        if word[:-2] in dict_words or word[:-2] in PURITAN_WHITELIST:
            return True
        if word[:-1] in dict_words or word[:-1] in PURITAN_WHITELIST:
            return True
    if word.endswith("est") and len(word) > 4:
        if word[:-3] in dict_words or word[:-3] in PURITAN_WHITELIST:
            return True
        if word[:-2] in dict_words or word[:-2] in PURITAN_WHITELIST:
            return True

    return False


def is_17th_century_variant(word: str, dict_words: set[str]) -> bool:
    """Heuristic to check if a word matches standard 17th-century Puritan spellings."""
    if is_valid_word(word, dict_words):
        return True

    # Pattern 1: ends in "nesse" -> standard English "ness"
    if word.endswith("nesse"):
        standard = word[:-5] + "ness"
        if is_valid_word(standard, dict_words):
            return True

    # Pattern 2: ends in "full" (with double 'l') -> standard "ful"
    if word.endswith("full"):
        standard = word[:-4] + "ful"
        if is_valid_word(standard, dict_words):
            return True

    # Pattern 3: ends in "ie" -> standard "y"
    if word.endswith("ie"):
        standard = word[:-2] + "y"
        if is_valid_word(standard, dict_words):
            return True

    # Pattern 4: ends in silent "e" with doubled final consonant
    # e.g., "sinne" -> "sin", "bee" -> "be", "selfe" -> "self", "worde" -> "word"
    if word.endswith("e") and len(word) > 3:
        # Strip final 'e'
        stripped = word[:-1]
        if is_valid_word(stripped, dict_words):
            return True
        # If final consonant is doubled, strip that too (e.g. "sinne" -> "sinn" -> "sin")
        if len(stripped) > 2 and stripped[-1] == stripped[-2]:
            if is_valid_word(stripped[:-1], dict_words):
                return True

    # Pattern 5: ends in silent 'e' after 'th' (e.g. "trueth" -> "truth")
    if word.endswith("eth") and not word.endswith("eth"):  # exclude eth verb endings
        standard = word[:-3] + "th"
        if is_valid_word(standard, dict_words):
            return True

    # Pattern 6: swapped 'i' and 'y' (e.g. "lye" -> "lie", "ayde" -> "aid")
    if "y" in word:
        standard = word.replace("y", "i")
        if is_valid_word(standard, dict_words):
            return True

    # Pattern 7: archaic verb endings: -eth, -esth, -edst (e.g. "giveth", "doeth")
    if word.endswith("eth") and len(word) > 4:
        # Strip "eth" and try adding "es", "s", or nothing
        stem = word[:-3]
        if is_valid_word(stem, dict_words) or is_valid_word(stem + "e", dict_words):
            return True
    if word.endswith("eths") and len(word) > 5:
        stem = word[:-4]
        if is_valid_word(stem, dict_words) or is_valid_word(stem + "e", dict_words):
            return True

    return False


def clean_text(text: str) -> str:
    """Strip XML tags, footnotes, and markdown formatting."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\[f\d+\]", " ", text)
    text = re.sub(r"\*\*|_", " ", text)
    return text


def find_contexts(text: str, target_word: str, limit: int = 2) -> list[str]:
    """Find occurrences of the target word and return surrounding context."""
    contexts = []
    # Match word boundaries case-insensitively
    pattern = re.compile(rf"\b{re.escape(target_word)}\b", re.I)
    for match in pattern.finditer(text):
        start = max(0, match.start() - 40)
        end = min(len(text), match.end() + 40)
        snippet = text[start:end].strip()
        snippet = re.sub(r"\s+", " ", snippet)
        # Add ellipsis if truncated
        prefix = "... " if start > 0 else ""
        suffix = " ..." if end < len(text) else ""
        contexts.append(f"{prefix}{snippet}{suffix}")
        if len(contexts) >= limit:
            break
    return contexts


def main():
    parser = argparse.ArgumentParser(description="Audit spelling and OCR typos in intermediate volume JSON.")
    parser.add_argument("volume", type=int, help="Volume number (e.g., 5)")
    parser.add_argument("--min-freq", type=int, default=1, help="Minimum word frequency to report")
    args = parser.parse_args()

    # Locate volume json
    here = Path(__file__).resolve().parent
    root = here.parent
    vol_json_path = root / "volumes" / f"v{args.volume}" / "intermediate" / f"volume_{args.volume}.json"

    if not vol_json_path.exists():
        print(f"Error: Volume intermediate JSON not found: {vol_json_path}")
        sys.exit(1)

    print(f"Loading system dictionary...")
    dict_words = load_dictionary()
    print(f"Loaded {len(dict_words)} words in dictionary.")

    print(f"Reading volume {args.volume} intermediate JSON...")
    with open(vol_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Suspected typos mapping: lowercase_word -> (count, list of (chapter_idx, chapter_title, context))
    suspected_typos = {}
    total_words_checked = 0

    print(f"Auditing spelling across chapters...")
    for ch_idx, ch in enumerate(data.get("chapters", [])):
        title = ch.get("title", f"Chapter {ch_idx}")
        raw_text = clean_text(ch.get("raw_text", "") or "")
        if not raw_text:
            continue

        words = WORD_RE.findall(raw_text)
        for w in words:
            # Skip words with uppercase letters (proper nouns/capitalized starts)
            # but allow fully lowercase/archaic. If capitalized, skip to avoid names.
            if any(c.isupper() for c in w):
                continue
            
            w_lower = w.lower()
            if len(w_lower) <= 2:  # skip very short words
                continue

            total_words_checked += 1
            if not is_17th_century_variant(w_lower, dict_words):
                if w_lower not in suspected_typos:
                    # Find context in this chapter
                    snippets = find_contexts(raw_text, w_lower, limit=2)
                    suspected_typos[w_lower] = {
                        "count": 1,
                        "chapters": {title: snippets}
                    }
                else:
                    suspected_typos[w_lower]["count"] += 1
                    if title not in suspected_typos[w_lower]["chapters"]:
                        snippets = find_contexts(raw_text, w_lower, limit=2)
                        suspected_typos[w_lower]["chapters"][title] = snippets

    # Print Report
    print("\n" + "=" * 80)
    print(f" SPELLING AND OCR AUDIT REPORT: VOLUME {args.volume}")
    print(f" Total lowercase words checked: {total_words_checked}")
    print(f" Suspected unique typos: {len(suspected_typos)}")
    print("=" * 80 + "\n")

    sorted_typos = sorted(
        [(w, info) for w, info in suspected_typos.items() if info["count"] >= args.min_freq],
        key=lambda item: item[1]["count"],
        reverse=True
    )

    # Separate high-confidence OCR issues (e.g. contain bracket characters or numbers or weird symbols)
    # and general spelling errors.
    print(f"Suspected Typos (sorted by frequency descending):\n")
    
    count = 0
    for word, info in sorted_typos:
        count += 1
        print(f"{count}. **{word}** (occurs {info['count']} times)")
        for ch_title, contexts in info["chapters"].items():
            print(f"   * Chapter: *{ch_title}*")
            for ctx in contexts:
                # Highlight the word in context
                highlighted = re.sub(rf"\b({re.escape(word)})\b", r"**\1**", ctx, flags=re.I)
                print(f"     > {highlighted}")
        print()

    print(f"Audit completed. Found {len(sorted_typos)} candidate typos.")


if __name__ == "__main__":
    main()
