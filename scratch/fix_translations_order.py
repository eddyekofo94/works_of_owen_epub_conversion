import re

with open('/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/Owen-translation-citations/render.py', 'r') as f:
    content = f.read()

old_helper = """    # Translation helper
    all_translation_notes = []
    global_trans_counter = 0
    from translation_db import BODY_TRANSLATIONS, GLOSSARY_TERMS
    sorted_phrases = sorted(BODY_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    sorted_glossary = sorted(GLOSSARY_TERMS.items(), key=lambda x: len(x[0]), reverse=True)
    
    def _apply_translations(html, cid):
        nonlocal global_trans_counter
        local_notes = []
        placeholders = {}
        
        for idx, (phrase, trans) in enumerate(sorted_phrases):
            pattern = re.compile(
                rf'(<span\s+lang="(?:el|he)"[^>]*>\s*{re.escape(phrase)}\s*</span>|{re.escape(phrase)})'
            )
            if pattern.search(html):
                global_trans_counter += 1
                placeholder = f"___TRANSPHRASE_PLACEHOLDER_{idx}___"
                matched_str = pattern.search(html).group(0)
                fn_link = f'<sup><a class="noteref noteref-trans" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fntrans_{cid}_{global_trans_counter}">[{global_trans_counter}]</a></sup>'
                placeholders[placeholder] = f"{matched_str}{fn_link}"
                local_notes.append({
                    'id': f"fntrans_{cid}_{global_trans_counter}",
                    'num': global_trans_counter,
                    'phrase': phrase,
                    'translation': trans
                })
                html = pattern.sub(placeholder, html)
                
        for placeholder, replacement in placeholders.items():
            html = html.replace(placeholder, replacement)
            
        for phrase, note in sorted_glossary:
            pattern = re.compile(rf'\\b({re.escape(phrase)})\\b', re.I)
            def repl(m):
                nonlocal global_trans_counter
                global_trans_counter += 1
                matched_str = m.group(1)
                fn_link = f'<sup><a class="noteref noteref-trans" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fntrans_{cid}_{global_trans_counter}">[{global_trans_counter}]</a></sup>'
                local_notes.append({
                    'id': f"fntrans_{cid}_{global_trans_counter}",
                    'num': global_trans_counter,
                    'phrase': phrase,
                    'translation': note
                })
                return f"{matched_str}{fn_link}"
                
            parts = re.split(r'(<[^>]+>)', html)
            for i in range(0, len(parts), 2):
                if pattern.search(parts[i]):
                    parts[i] = pattern.sub(repl, parts[i])
            html = "".join(parts)
            
        if local_notes:
            all_translation_notes.extend(local_notes)
            
        return html"""

new_helper = """    # Translation helper
    all_translation_notes = []
    from translation_db import BODY_TRANSLATIONS, GLOSSARY_TERMS
    sorted_phrases = sorted(BODY_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    sorted_glossary = sorted(GLOSSARY_TERMS.items(), key=lambda x: len(x[0]), reverse=True)
    
    def _apply_translations(html, cid):
        local_notes = []
        placeholder_data = {}
        ph_counter = 0
        
        # Pass 1: Replace BODY_TRANSLATIONS with placeholders
        for phrase, trans in sorted_phrases:
            pattern = re.compile(
                rf'(<span\s+lang="(?:el|he)"[^>]*>\s*{re.escape(phrase)}\s*</span>|{re.escape(phrase)})'
            )
            # Find all matches and replace them one by one
            def repl_body(m):
                nonlocal ph_counter
                ph_counter += 1
                ph = f"___TRANS_PLACEHOLDER_{ph_counter}___"
                placeholder_data[ph] = {
                    'matched_str': m.group(0),
                    'phrase': phrase,
                    'translation': trans
                }
                return ph
            html = pattern.sub(repl_body, html)
            
        # Pass 2: Replace GLOSSARY_TERMS with placeholders (avoiding HTML tags)
        for phrase, note in sorted_glossary:
            pattern = re.compile(rf'\\b({re.escape(phrase)})\\b', re.I)
            def repl_glossary(m):
                nonlocal ph_counter
                ph_counter += 1
                ph = f"___TRANS_PLACEHOLDER_{ph_counter}___"
                placeholder_data[ph] = {
                    'matched_str': m.group(1),
                    'phrase': phrase,
                    'translation': note
                }
                return ph
                
            parts = re.split(r'(<[^>]+>)', html)
            for i in range(0, len(parts), 2):
                if pattern.search(parts[i]):
                    parts[i] = pattern.sub(repl_glossary, parts[i])
            html = "".join(parts)
            
        # Pass 3: Sequentially assign footnote numbers based on appearance in text
        trans_counter = 0
        def final_repl(m):
            nonlocal trans_counter
            ph = m.group(0)
            if ph not in placeholder_data:
                return ph
            trans_counter += 1
            data = placeholder_data[ph]
            fn_link = f'<sup><a class="noteref noteref-trans" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fntrans_{cid}_{trans_counter}">[{trans_counter}]</a></sup>'
            local_notes.append({
                'id': f"fntrans_{cid}_{trans_counter}",
                'num': trans_counter,
                'phrase': data['phrase'],
                'translation': data['translation']
            })
            return f"{data['matched_str']}{fn_link}"
            
        # Replace all placeholders in their actual document order
        html = re.sub(r'___TRANS_PLACEHOLDER_\d+___', final_repl, html)
        
        if local_notes:
            all_translation_notes.extend(local_notes)
            
        return html"""

if old_helper in content:
    content = content.replace(old_helper, new_helper)
    with open('/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/Owen-translation-citations/render.py', 'w') as f:
        f.write(content)
    print("Successfully patched render.py")
else:
    print("Old helper not found in render.py")
