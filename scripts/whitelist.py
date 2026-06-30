import json
from pathlib import Path

def load_whitelist(path: Path) -> dict:
    if not path.exists():
        return {}
    
    try:
        wl = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
        
    legacy_wl = {}
    
    def unwrap(item, cat):
        if not isinstance(item, dict):
            return item # already legacy or invalid, just pass through
            
        if "page" in item:
            return item["page"]
            
        if cat == "ignored_warnings" and "code" in item:
            return item["code"]
            
        if "sample" in item:
            return item["sample"]
            
        if "phrase" in item:
            return item["phrase"]
            
        if "text" in item:
            return item["text"]
            
        # For missing enumerator markers
        if "marker" in item and "context" in item:
            # wait, missing_enumerator_markers expects dicts even in legacy!
            return item
            
        # For paragraph_splits
        if "previous" in item and "next" in item:
            return item
            
        return item # fallback

    for main_cat in ["text_integrity", "anomalies", "epub_warnings"]:
        if main_cat not in wl:
            continue
            
        legacy_wl[main_cat] = {}
        for sub_cat, items in wl[main_cat].items():
            if not isinstance(items, list):
                continue
            
            unwrapped_items = []
            for item in items:
                if isinstance(item, dict):
                    if item.get("verification_status") != "verified":
                        continue # Skip unverified!
                unwrapped_items.append(unwrap(item, sub_cat))
                
            if unwrapped_items:
                legacy_wl[main_cat][sub_cat] = unwrapped_items

    # Keep any other keys (like "used_items" though it's generated at runtime)
    for k, v in wl.items():
        if k not in legacy_wl and k != "review_queue":
            legacy_wl[k] = v

    return legacy_wl
