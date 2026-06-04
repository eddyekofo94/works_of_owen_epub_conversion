import re, zipfile
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET
from shared import (
    FOOTNOTE_MARKER_RE, FT_MARKER_RE, LOOSE_FOOTNOTE_MARKER_RE,
    EMPTY_BRACKET_RE,
    clean_greek_text, is_greek_font, is_hebrew_font,
    convert_greek_word, convert_gideon_hebrew,
    normalize_characters, _normalize_spaced_caps,
    _normalize_i_will, _normalize_scholarly_citation_artifacts
)
from scripts.ages_verse_translator import translate_ages_verse_markers
from scripts.pdf_coordinates import _repair_glued_scripture_book_references

@dataclass
class Footnote:
    fnum: int
    text: str
    source: str = 'pdf'       # 'pdf' or 'thml'
    pages: list = field(default_factory=list)  # PDF pages where referenced

def _converted_pdf_line(line):
    converted_parts = []
    for span in line['spans']:
        span_text = span['text']
        font = span.get('font', '')
        if is_greek_font(font):
            span_text = convert_greek_word(span_text)
        elif is_hebrew_font(font):
            span_text = convert_gideon_hebrew(span_text)
        converted_parts.append(span_text)
    return ''.join(converted_parts).strip()


def _page_has_ages_footnote_marker(page):
    for block in page.get_text('dict').get('blocks', []):
        if block.get('type') != 0:
            continue
        for line in block.get('lines', []):
            line_text = ''.join(s['text'] for s in line.get('spans', [])).strip()
            if FT_MARKER_RE.match(line_text):
                return True
    return False


def _find_ages_footnote_start_page(doc):
    """Find the AGES back-matter footnote section, with a marker fallback."""
    heading_pages = [
        pg for pg in range(len(doc))
        if 'FOOTNOTES' in doc[pg].get_text().upper()
    ]
    if heading_pages:
        return heading_pages[0]

    # Some AGES PDFs omit or garble the heading but still use ftN markers in
    # the back matter. Limit the fallback to the tail of the book so inline
    # prose cannot be mistaken for note text.
    tail_start = max(0, len(doc) - 20)
    for pg in range(tail_start, len(doc)):
        if _page_has_ages_footnote_marker(doc[pg]):
            return pg
    return None


def extract_footnotes_from_pdf(doc):
    """
    Extract AGES footnotes from the PDF back matter.

    The normal AGES scheme is a FOOTNOTES section whose notes begin with
    ftN/FTN markers. A fallback also recognizes those markers in the final
    pages when the section heading is missing or damaged.
    """
    footnotes = {}
    current_fn = None
    current_text = []
    start_page = _find_ages_footnote_start_page(doc)
    
    if start_page is None:
        return footnotes

    for pg in range(start_page, len(doc)):
        page = doc[pg]
        blocks = page.get_text('dict')['blocks']
        for b in blocks:
            if b['type'] != 0:
                continue
            for line in b['lines']:
                line_text = ''.join(s['text'] for s in line['spans'])
                line_text = line_text.strip()
                
                if not line_text:
                    continue
                
                line_text_converted = _converted_pdf_line(line)
                if not line_text_converted:
                    continue
                
                # Check for FT marker in raw text (before conversion might mess it up)
                line_text_raw = ''.join(s['text'] for s in line['spans']).strip()
                ft_match = FT_MARKER_RE.match(line_text_raw)
                
                if ft_match:
                    # Save previous footnote
                    if current_fn is not None and current_text:
                        footnotes[current_fn] = ' '.join(current_text).strip()
                    
                    current_fn = int(ft_match.group(1))
                    # Use converted text for the content part
                    rest = line_text_converted[ft_match.end():].strip()
                    current_text = [rest] if rest else []
                elif current_fn is not None:
                    current_text.append(line_text_converted)
    
    # Save last footnote
    if current_fn is not None and current_text:
        combined = ' '.join(current_text).strip()
        if combined:
            footnotes[current_fn] = combined
    
    return footnotes


def parse_thml_footnotes(thml_path):
    """Parse existing ThML XML FOOTNOTES section for enriched footnote text."""
    from lxml import etree
    footnotes = {}

    if not os.path.exists(thml_path):
        return footnotes

    try:
        parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=True)
        root = etree.parse(thml_path, parser).getroot()

        # Find all fnmarkers anywhere in the document
        markers = root.xpath('.//a[@class="fnmarker"]')
        for i, marker in enumerate(markers):
            fn_num = int(marker.get('data-fn', '0') or 0)
            if not fn_num:
                continue

            parts = []
            # Use a stateful approach: collect everything until the next marker
            # We look for all text nodes and other elements between this marker and the next
            # We'll use the markers list to define boundaries

            # Start collecting from this marker's position
            next_marker = markers[i+1] if i + 1 < len(markers) else None

            def get_all_text_between(start_node, end_node):
                collected = []

                # 1. Start with start_node's tail
                if start_node.tail:
                    collected.append(start_node.tail)

                # 2. Iterate through siblings and their descendants
                curr = start_node
                while curr is not None:
                    # Move to next sibling
                    sibling = curr.getnext()
                    if sibling is None:
                        # Go up to parent's next sibling
                        curr = curr.getparent()
                        if curr is None or curr == root:
                            break
                        # When moving to a new paragraph/div, add a newline
                        if curr.tag in ('p', 'div', 'div1', 'div2'):
                            collected.append('\n\n')
                        continue

                    if sibling == end_node:
                        break

                    # Does this sibling contain the end_node?
                    if end_node is not None and end_node in sibling.xpath('.//*'):
                        # Need to recurse into this sibling to find exact boundary
                        # But simpler: just get text until end_node
                        for sub_node in sibling.xpath('.//text() | .//*'):
                             if sub_node == end_node:
                                 break
                             # (This is getting complex, let's use a simpler approach)
                             pass
                        break

                    # Add all text from this sibling
                    collected.append(''.join(sibling.itertext()))
                    if sibling.tail:
                        collected.append(sibling.tail)
                    curr = sibling

                return ''.join(collected)

            # Simpler approach: use xpath to get all following text/elements
            # and stop when we see the next marker.
            # Actually, let's use a very simple paragraph-based heuristic again
            # but fix the "sibling" vs "descendant" issue.

            parts = []
            if marker.tail:
                parts.append(marker.tail)

            # Collect following siblings in same parent
            curr = marker.getnext()
            found_next = False
            while curr is not None:
                if curr.tag == 'a' and curr.get('class') == 'fnmarker':
                    found_next = True
                    break
                parts.append(''.join(curr.itertext()))
                if curr.tail:
                    parts.append(curr.tail)
                curr = curr.getnext()

            # If we didn't hit a marker in the same paragraph, check following paragraphs
            if not found_next:
                p = marker.getparent()
                while p is not None:
                    next_p = p.getnext()
                    if next_p is None:
                        break
                    # If this paragraph has a marker, stop.
                    # IMPORTANT: it might have multiple markers, we stop at the first one.
                    m_in_next = next_p.xpath('.//a[@class="fnmarker"]')
                    if m_in_next:
                        # Add text BEFORE the first marker in this paragraph
                        first_m = m_in_next[0]
                        # This part is tricky. Let's just take the whole paragraph if
                        # the marker is at the very end, or if it's the marker we want?
                        # No, if it has ANY marker, it belongs to the next footnote.
                        break

                    parts.append('\n\n' + ''.join(next_p.itertext()))
                    p = next_p

            text = re.sub(r'[ \t]+', ' ', ''.join(parts)).strip()
            if text:
                footnotes[fn_num] = text
    except Exception as e:
        print(f"  Warning: Could not parse ThML footnotes: {e}")

    return footnotes
def merge_footnotes(pdf_footnotes, thml_footnotes):
    """
    Merge footnotes from PDF and ThML, preferring ThML for quality.
    """
    all_nums = set(pdf_footnotes.keys()) | set(thml_footnotes.keys())
    merged = {}
    for num in sorted(all_nums):
        text = thml_footnotes.get(num) or pdf_footnotes.get(num) or ''
        text = normalize_characters(text)
        text = _normalize_spaced_caps(text)
        text = _normalize_i_will(text)
        text = translate_ages_verse_markers(text)
        text = _repair_glued_scripture_book_references(text)
        text = EMPTY_BRACKET_RE.sub('', text)
        text = re.sub(r'\s+', ' ', text).strip()
        merged[num] = Footnote(
            fnum=num,
            text=text,
            source='thml' if num in thml_footnotes else 'pdf'
        )
    return merged


def find_footnote_refs_in_text(text):
    """
    Find [fN] footnote markers in text and return (cleaned_text, list of fn_numbers).
    """
    markers = FOOTNOTE_MARKER_RE.findall(text)
    fn_nums = [int(m) for m in markers]
    cleaned = FOOTNOTE_MARKER_RE.sub('', text)
    return cleaned, fn_nums

def _normalize_extracted_footnote_markers(text):
    """Normalize AGES inline markers before paragraph healing can merge words."""
    def repl(match):
        fn = next(group for group in match.groups() if group)
        return f'[f{fn}]'

    text = LOOSE_FOOTNOTE_MARKER_RE.sub(repl, text)
    # A recurring AGES overlap can read "Himself. His kingdom." as
    # "Himsel[f2]. His kingdom." The "f" belongs to the word, and the 2 is the
    # next enumerator, not a footnote marker.
    text = re.sub(
        r'\bHimsel\s*\[f2\]\.\s+His kingdom\.\s+1\.\s+Himself\b\.?',
        'Himself.',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\bHimsel\s*\[f2\]\.\s+His kingdom\b',
        'Himself',
        text,
        flags=re.I,
    )
    # Insert space between word character and footnote marker: word[fN] -> word [fN]
    text = re.sub(r'([A-Za-z])(\[f\d+\])', r'\1 \2', text)
    # Insert space after footnote marker when followed by letter: [fN]word -> [fN] word
    text = re.sub(r'(\[f\d+\])(?=[A-Za-z])', r'\1 ', text)
    return text

