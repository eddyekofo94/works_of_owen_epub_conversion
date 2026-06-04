import re

def _apply_premium_signatures(html: str, ch_title: str) -> str:
    """Detect signature paragraphs in prefaces/introductions and format them as premium signature blocks."""
    if not html:
        return html
        
    def replacer(match):
        p_html = match.group(0)
        p_content = match.group(1)
        
        # Skip if already part of an epub-signature or pre-formatted signature class
        if 'class="signature-' in p_html or 'epub-signature' in p_html:
            return p_html
            
        parsed = parse_signature_paragraph(p_content)
        if parsed:
            return format_signature_html(parsed)
        return p_html
        
    def parse_signature_paragraph(content):
        # Strip HTML tags and markdown symbols to look for a signature name
        cleaned = re.sub(r'<[^>]+>', '', content).strip()
        cleaned = re.sub(r'[\*_]+', '', cleaned).strip()
        
        name_patterns = [
            r"\bJOHN\s+OWEN\b", r"\bJohn\s+Owen\b", r"\bJ\.\s*O\.", 
            r"\bWILLIAM\s+H\.\s+GOOLD\b", r"\bWilliam\s+H\.\s+Goold\b", r"\bW\.\s*H\.\s*G\.",
            r"\bSir\s+John\s+Hartopp\b", r"\bMrs\s+Cooke\b", r"\bDANIEL\s+BURGESS\b"
        ]
        
        matched_name = None
        for pattern in name_patterns:
            m = re.search(pattern, cleaned, re.I)
            if m:
                matched_name = m.group(0)
                break
                
        if not matched_name:
            return None
            
        name_plain = matched_name.strip()
        
        # Find where it occurs in the plain text
        m = re.search(re.escape(name_plain), cleaned)
        start_idx, end_idx = m.start(), m.end()
        
        # ── Strict Signature Criteria ─────────────────────────────
        total_len = len(cleaned)
        dist_from_end = total_len - start_idx
        
        is_short = total_len < 200
        is_near_end = dist_from_end <= 120
        
        if not (is_short or is_near_end):
            return None  # Standard body prose mentioning the name
            
        prefix = cleaned[:start_idx].strip()
        suffix = cleaned[end_idx:].strip()
        
        def clean_block(t):
            t = re.sub(r'^[\s,.\—\-_—\-]+|[\s,.\—\-_—\-]+$', '', t)
            t = t.strip()
            return t
            
        intro_plain = clean_block(prefix)
        date_loc_plain = clean_block(suffix)
        
        split_patterns = [
            r"\bYour\s+(?:devoted|humble|humblest|obedient|loving)?\s*Servant\b",
            r"\bSo\s+prays\b",
            r"\bunworthy\s+author\b",
            r"(?:\bwho\s+is\s+your\s+)?\bloving\s+brother\b",
            r"\bYour\s+Excellency's\s+Most\s+humble\s+and\s+devoted\s*Servant\b",
            r"(?:\bwho\s+is\s+your\s+)?\bunworthy\s+(?:fellow[- ])?laborer\b",
            r"(?:\bwho\s+is\s+your\s+)?\bunworthy\s+(?:fellow[- ])?labourer\b",
            r"(?:\bwho\s+is\s+your\s+)?\bobliged\s+servant\b",
            r"(?:\bwho\s+is\s+your\s+)?\bunworthy\s+servant\b"
        ]
        
        found_split_idx = -1
        for sp in split_patterns:
            m_sp = re.search(sp, intro_plain, re.I)
            if m_sp:
                if found_split_idx == -1 or m_sp.start() > found_split_idx:
                    found_split_idx = m_sp.start()
                    
        # If it's a long paragraph and we didn't find an explicit valediction split,
        # reject it to prevent body text false positives
        if total_len >= 200 and found_split_idx == -1:
            return None
            
        # If it is a shorter paragraph but:
        # - Has no valediction split
        # - Has no date/location
        # - The text before the name is a long sentence (> 20 characters)
        # Reject it as it's a standard sentence (e.g., "...preached by Dr John Owen.")
        if found_split_idx == -1 and not date_loc_plain and len(intro_plain) > 20:
            return None
            
        # Map plain-text split indices back to HTML indices for original preservation
        html_start_idx = map_plain_to_html_index(content, start_idx)
        html_end_idx = map_plain_to_html_index(content, end_idx)
        
        body_text_html = ""
        intro_html = ""
        
        if found_split_idx != -1:
            html_split_idx = map_plain_to_html_index(content, found_split_idx)
            body_text_html = content[:html_split_idx].strip()
            intro_html = content[html_split_idx:html_start_idx].strip()
        else:
            intro_html = content[:html_start_idx].strip()
            
        name_html = content[html_start_idx:html_end_idx].strip()
        date_loc_html = content[html_end_idx:].strip()
        
        def clean_html_block(h):
            h = h.strip()
            h = re.sub(r'^[\s,.\—\-_—\-]+|[\s,.\—\-_—\-]+$', '', h)
            return h.strip()
            
        body_text_html = clean_html_block(body_text_html)
        intro_html = clean_html_block(intro_html)
        name_html = clean_html_block(name_html)
        date_loc_html = clean_html_block(date_loc_html)
        
        name = name_plain
        # Normalize name casing
        if name.lower() in ("john owen", "john owen."):
            name = "John Owen"
        elif name.lower() in ("j.o.", "j. o.", "j.o", "j. o"):
            name = "J.O."
        elif name.lower() in ("william h. goold", "william h. goold."):
            name = "William H. Goold"
            
        return {
            "body_text": body_text_html,
            "intro": intro_html,
            "name": name,
            "date_loc": date_loc_html
        }

    def format_signature_html(sig):
        parts = []
        if sig["body_text"]:
            parts.append(f'<p class="front-matter-prose">{sig["body_text"]}</p>')
        parts.append('<div class="epub-signature">')
        if sig["intro"]:
            parts.append(f'  <p class="signature-intro">{sig["intro"]}</p>')
        parts.append(f'  <p class="signature-name">{sig["name"]}</p>')
        if sig["date_loc"]:
            parts.append(f'  <p class="signature-date">{sig["date_loc"]}</p>')
        parts.append('</div>')
        return "\n".join(parts)
        
    return re.sub(r'<p\b[^>]*>(.*?)</p>', replacer, html, flags=re.I | re.S)

def map_plain_to_html_index(html: str, plain_index: int) -> int:
    """Map a character index in plain text back to the corresponding index in the original HTML string."""
    plain_idx = 0
    in_tag = False
    for html_idx, char in enumerate(html):
        if plain_idx == plain_index and not in_tag:
            return html_idx
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
        elif not in_tag:
            plain_idx += 1
    return len(html)


def _apply_premium_chapter_endings(html: str) -> str:
    """Detect 'END', 'THE END', or 'END OF PART...' at the end of chapters and format them as distinct, centered bold markers."""
    if not html:
        return html
        
    end_pattern = re.compile(
        r'(?:,\s*|\.\s*|;\s*|\s+)?'
        r'(?:<[^>]+>|[\*_]|\s)*'
        r'\b(THE\s+END|END\s+OF\s+(?:THE\s+)?(?:(?:PART|BOOK|VOLUME|TREATISE)\s+(?:FIRST|SECOND|THIRD|FOURTH|V\w+|[IVXLCDM\d\s]+)|(?:FIRST|SECOND|THIRD|FOURTH|V\w+|[IVXLCDM\d\s]+)\s*(?:PART|BOOK|VOLUME|TREATISE)|PART|BOOK|VOLUME|TREATISE)|END)\b'
        r'(?:<[^>]+>|[\*_]|\s|[,.\—\-_—\-])*$',
        re.I
    )

    def replacer(match):
        p_html = match.group(0)
        p_attrs = match.group(1)
        p_content = match.group(2).strip()
        
        m_end = end_pattern.search(p_content)
        if m_end:
            matched_txt = m_end.group(1)
            
            is_uppercase = matched_txt.isupper()
            has_formatting = '<' in p_content[m_end.start():] or '*' in p_content[m_end.start():] or '_' in p_content[m_end.start():]
            is_standalone = m_end.start() == 0 or p_content[:m_end.start()].strip() == ""
            
            if not (is_uppercase or has_formatting or is_standalone):
                return p_html
                
            prefix = p_content[:m_end.start()].strip()
            prefix = re.sub(r'[\s,.\—\-_—\-]+$', '', prefix).strip()
            
            clean_txt = re.sub(r'<[^>]+>', '', matched_txt).strip()
            clean_txt = re.sub(r'[\*_]+', '', clean_txt).strip()
            clean_txt = re.sub(r'[^a-zA-Z\d\s]', '', clean_txt).strip()
            formatted_marker = f'<p class="chapter-end-marker"><b>{clean_txt.upper()}.</b></p>'
            
            if prefix:
                return f'<p{p_attrs}>{prefix}.</p>\n{formatted_marker}'
            else:
                return formatted_marker
                
        return p_html

    return re.sub(r'<p(\b[^>]*)>(.*?)</p>', replacer, html, flags=re.I | re.S)


def _apply_premium_salutations(html: str) -> str:
    """Detect 'Christian Reader,', 'To the Christian Reader,', etc. and format them as elegant left-aligned salutations."""
    if not html:
        return html
        
    salutation_pattern = re.compile(
        r'<(p|h[1-6])(\b[^>]*)>(?:<[^>]+>)*\s*'
        r'\b((?:To\s+the\s+)?(?:Christian\s+)?Reader\b\s*[,.\—\-_—\-]*)\s*'
        r'(?:<[^>]+>)*\s*</\1>',
        re.I
    )

    def replacer(match):
        p_html = match.group(0)
        p_text = match.group(3).strip()
        
        if len(p_text) > 60:
            return p_html
            
        return f'<p class="prefatory-salutation">{p_text}</p>'

    return salutation_pattern.sub(replacer, html)
