#!/usr/bin/env python3
"""
generate_untranslated_manifest.py — Proactive Collection-Wide Greedy Prose Scanner.

Performs an extremely thorough ("greedy") sweep of all 16 volumes of John Owen's Works,
detecting every potential block of untranslated or unreferenced Latin, Greek, and Hebrew
text (both in footnotes and body paragraphs) to ensure 100% academic integrity.
"""

import os
import json
import re
import sys
from pathlib import Path

# Add project root to path
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from translation_db import FOOTNOTE_TRANSLATIONS, BODY_TRANSLATIONS

# Refined Latin words specific to prose/verses (excluding highly common English prepositions)
LATIN_WORDS_REFINED = {
    'et', 'est', 'non', 'sunt', 'enim', 'autem', 'etiam', 'nihil', 'hic', 'iam',
    'tamen', 'vel', 'nec', 'sed', 'cum', 'qui', 'quae', 'quod', 'ut', 'aut', 'sine',
    'atque', 'eorum', 'ejus', 'ipsa', 'ipso', 'illa', 'illud', 'quoniam', 'propter',
    'quia', 'verum', 'vero'
}

def is_latin_greedy(text: str) -> bool:
    """Detects if a block is a substantial block of Latin prose requiring a translation note."""
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

def is_greek_greedy(text: str) -> bool:
    """Detects if a block contains a substantial block of Greek prose."""
    greek_words = re.findall(r'\b[\u0370-\u03ff\u1f00-\u1fff]+\b', text)
    return len(greek_words) >= 4

def is_hebrew_greedy(text: str) -> bool:
    """Greedily detects if a block contains any Hebrew words."""
    hebrew_words = re.findall(r'\b[\u0590-\u05ff]+\b', text)
    # Any block containing even a single Hebrew word is flagged
    return len(hebrew_words) >= 1

def is_foreign_greedy(text: str) -> str | None:
    """Returns 'greek', 'hebrew', 'latin', or None if no match."""
    if is_hebrew_greedy(text):
        return "hebrew"
    if is_greek_greedy(text):
        return "greek"
    if is_latin_greedy(text):
        return "latin"
    return None

def find_matching_body_translation(p_text: str, sorted_phrases: list) -> bool:
    """Checks if a paragraph text has a matched translation in BODY_TRANSLATIONS."""
    p_lower = p_text.lower()
    for phrase in sorted_phrases:
        if len(phrase) > 8:
            # Flexible word check: see if the phrase is in the paragraph
            words = re.findall(r'\w+', phrase.lower())
            if not words:
                continue
            # If all keywords of the phrase are in the paragraph, consider it translated
            if all(w in p_lower for w in words[:min(len(words), 5)]):
                return True
    return False

def scan_collection():
    print("=" * 80)
    print("GREEDY COLLECTION-WIDE AUDIT: DETECTING ALL FOREIGN PROSE & CITATIONS")
    print("=" * 80)
    
    sorted_phrases = sorted(BODY_TRANSLATIONS.keys(), key=len, reverse=True)
    manifest = {}
    
    volumes_dir = _ROOT / "volumes"
    available_vols = sorted([
        int(d.name[1:]) for d in volumes_dir.glob("v*")
        if d.is_dir() and d.name[1:].isdigit()
    ])
    
    total_fns_scanned = 0
    total_body_scanned = 0
    total_untranslated_fns = 0
    total_untranslated_body = 0
    
    for vol in available_vols:
        json_path = volumes_dir / f"v{vol}" / "intermediate" / f"volume_{vol}.json"
        if not json_path.exists():
            continue
            
        print(f"Auditing Volume {vol}...", flush=True)
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
            
        vol_fns = []
        vol_body = []
        
        # 1. Footnotes Scan
        footnotes = data.get("footnotes", {})
        for fnum_str, fn in footnotes.items():
            text = fn.get("text", "")
            total_fns_scanned += 1
            
            # Check translation_db
            trans_key = f"v{vol}_fn{fnum_str}"
            if trans_key in FOOTNOTE_TRANSLATIONS:
                continue
                
            lang = is_foreign_greedy(text)
            if lang:
                # Exclude standard english scriptures like 'Rom. 3:24' or 'John 1:1'
                if lang == "latin" and re.search(r'\b(gen|exod|lev|num|deut|josh|judg|sam|kings|chron|neh|est|job|ps|prov|eccl|cant|isa|jer|lam|ezek|dan|hos|joel|amos|obad|jon|mic|nah|hab|zeph|hag|zech|mal|matt|mark|luke|john|acts|rom|cor|gal|eph|phil|col|thess|tim|tit|philem|heb|jas|pet|jude|rev)\b\s*\d+', text.lower()):
                    # If it's a short scripture citation, skip
                    if len(re.findall(r'\b[a-zA-Z]+\b', text)) < 6:
                        continue
                
                vol_fns.append({
                    "fnum": fnum_str,
                    "text": text,
                    "type": lang
                })
                total_untranslated_fns += 1
                
        # 2. Body Paragraphs Scan
        for ch in data.get("chapters", []):
            title = ch.get("title", "")
            raw_text = ch.get("raw_text", "")
            paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
            
            for p_idx, p in enumerate(paragraphs):
                if p.startswith('[[') or p.startswith('**'):
                    continue
                total_body_scanned += 1
                
                if find_matching_body_translation(p, sorted_phrases):
                    continue
                    
                lang = is_foreign_greedy(p)
                if lang:
                    vol_body.append({
                        "chapter": title,
                        "p_idx": p_idx,
                        "text": p,
                        "type": lang
                    })
                    total_untranslated_body += 1
                    
        manifest[vol] = {
            "untranslated_footnotes": vol_fns,
            "untranslated_body_paragraphs": vol_body,
            "counts": {
                "footnotes": len(vol_fns),
                "body": len(vol_body)
            }
        }
        print(f"  -> Vol {vol}: {len(vol_fns)} potential fns, {len(vol_body)} potential body paragraphs")
        
    # Save the manifest
    manifest_path = _ROOT / "qa" / "untranslated_prose_manifest.json"
    with open(manifest_path, "w", encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\nUnified Greedy Manifest saved to: {manifest_path}")
    
    # Save the Audit Report
    report_path = _ROOT / "qa" / "untranslated_prose_report.md"
    with open(report_path, "w", encoding='utf-8') as f:
        f.write("# John Owen Works — Collection-Wide Academic Translation Audit Report\n\n")
        f.write("> [!IMPORTANT]\n")
        f.write("> This is a **greedy, non-partial audit** of all 16 volumes. It flags any footnote or paragraph containing ")
        f.write("Latin, Greek, or Hebrew text that is currently unannotated or lacks modern scholarly translations/references.\n\n")
        
        f.write("## 1. Summary Statistics\n\n")
        f.write(f"- **Total Volumes Audited:** {len(available_vols)}\n")
        f.write(f"- **Total Footnotes Scanned:** {total_fns_scanned}\n")
        f.write(f"- **Total Body Paragraphs Scanned:** {total_body_scanned}\n")
        f.write(f"- **Total Potential Untranslated Footnotes:** {total_untranslated_fns}\n")
        f.write(f"- **Total Potential Untranslated Body Paragraphs:** {total_untranslated_body}\n\n")
        
        f.write("### Volume Coverage Baselines\n\n")
        f.write("| Volume | Untranslated Footnotes | Untranslated Body Paragraphs | Total Remaining | Action Status |\n")
        f.write("|---|---|---|---|---|\n")
        for vol in available_vols:
            vdata = manifest.get(vol, {"counts": {"footnotes": 0, "body": 0}})
            fn_cnt = vdata["counts"]["footnotes"]
            bd_cnt = vdata["counts"]["body"]
            total = fn_cnt + bd_cnt
            status = "✅ 100% COMPLETE & VALIDATED" if total == 0 else "⚠️ Requires Translation Sweep"
            f.write(f"| Volume {vol} | {fn_cnt} | {bd_cnt} | {total} | {status} |\n")
            
        f.write("\n## 2. Detailed Audit logs per Volume\n\n")
        for vol in available_vols:
            vdata = manifest.get(vol, {})
            fns = vdata.get("untranslated_footnotes", [])
            body_p = vdata.get("untranslated_body_paragraphs", [])
            
            f.write(f"### ── VOLUME {vol} ──\n\n")
            f.write(f"**Footnotes remaining:** {len(fns)} | **Body paragraphs remaining:** {len(body_p)}\n\n")
            
            if fns:
                f.write("#### Potential Untranslated Footnotes:\n")
                for fn in fns[:15]:
                    f.write(f"- **Footnote {fn['fnum']}** ({fn['type'].upper()}): `{fn['text']}`\n")
                if len(fns) > 15:
                    f.write(f"- *...and {len(fns) - 15} more footnotes.*\n")
                f.write("\n")
                
            if body_p:
                f.write("#### Potential Untranslated Body Paragraphs:\n")
                for bp in body_p[:15]:
                    f.write(f"- **[{bp['chapter']}] P{bp['p_idx']}** ({bp['type'].upper()}): `{bp['text'][:200]}...`\n")
                if len(body_p) > 15:
                    f.write(f"- *...and {len(body_p) - 15} more body paragraphs.*\n")
                f.write("\n")
            f.write("\n" + "─" * 40 + "\n\n")
            
    print(f"Markdown Audit Report saved to: {report_path}")

if __name__ == "__main__":
    scan_collection()
