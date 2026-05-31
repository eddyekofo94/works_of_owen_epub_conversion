import re
import sys
sys.path.insert(0, '/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen')

from render import (
    normalize_characters, _split_tail_signature, _repair_sermon_prefatory_note_splits,
    _repair_owen_ocr_errors, _repair_markdown_tables, _repair_fused_word_ordinals,
    _repair_mid_sentence_blockquote_splits, _repair_scholastic_blockquote_boundaries,
    _repair_unbalanced_bracket_splits, _repair_lowercase_continuation_splits,
    _repair_transitional_word_isolation, _repair_scholastic_anchor_splits,
    _repair_dangling_initial_splits, normalize_footnote_markers,
    _merge_reference_continuation_paragraphs, _coalesce_roman_list_paragraphs,
    _split_inline_catechism_questions, _split_inline_structural_markers,
    _repair_known_catechism_ghosts, MARKDOWN_STRUCTURAL_START_RE,
    SCRIPTURE_BOOK_RE, emphasize_structural_prefix, tag_unicode_ranges,
    _restore_footnote_placeholders, _split_rendered_inline_structural_html,
    _detect_signature
)

raw = '''**QUESTION 2.** _A second inquiry is, Whether the persons before mentioned and_ _described may lawfully, and in a consistency with or without a_ _renunciation of their former principles and practice, go to and_ _receive the sacrament of the Lord\\'s supper in the parish churches,_ _under their present constitution and administration?_ **ANSWER.** It appears that they may not, or cannot so do; for, — **1** _**.**_ _Their so doing would be..._'''

print("INITIAL:", repr(raw))

text_html = raw

# 2. Cleanup leading/trailing bold artifacts
if not MARKDOWN_STRUCTURAL_START_RE.match(text_html):
    text_html = re.sub(r'^\*\*(?:\*\*)?', '', text_html)
    text_html = re.sub(r'\*\*(?:\*\*)?$', '', text_html)
# Specifically remove surviving .** artifact
text_html = text_html.replace('.**', '.')
print("AFTER STRIP:", repr(text_html))

# Standardize Q/A labels for bolding (CASE-SENSITIVE, anchored)
text_html = re.sub(r'^(Q\.|Ans\.|Ques\.|A\.\s*\d+\.)\s+', r'**\1** ', text_html)
text_html = re.sub(r'^(Q\.\s*\d+\.|A\.\s*\d+\.|Ques\.\s*\d+\.|Ans\.\s*\d+\.)\s+', r'**\1** ', text_html)
print("AFTER QA STANDARD:", repr(text_html))

text_html = _repair_owen_ocr_errors(text_html, config=None)
print("AFTER OCR ERRORS:", repr(text_html))

# Cleanup unbalanced bold markers
if text_html.count('**') % 2 != 0:
    text_html = text_html.replace('**', '')
print("AFTER UNBALANCED REPLACE:", repr(text_html))

def _repair_bold_marker(m):
    if text_html[:m.start()].count('**') % 2 != 0:
        return m.group(0)
    return f"**{m.group(1)}**"
    
text_html = re.sub(r'(?<!\*)\b(\d+\.)\*\*(?=\s+)', _repair_bold_marker, text_html)
print("AFTER BOLD REPAIR:", repr(text_html))

text_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_html)
print("AFTER MD BOLD:", repr(text_html))

text_html = re.sub(r'(?<!\*)_(.+?)_(?!\*)', r'<i>\1</i>', text_html)
print("AFTER MD ITALIC:", repr(text_html))

text_html = re.sub(rf'\s*\*\*\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', ' ', text_html, flags=re.I)
print("AFTER SCRIPTURE MD:", repr(text_html))

text_html = re.sub(r'<b>(Q\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
text_html = re.sub(r'<b>(A\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
text_html = re.sub(r'<b>(Q\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
text_html = re.sub(r'<b>(A\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
text_html = re.sub(r'<b>(Ques\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
text_html = re.sub(r'<b>(Ans\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
text_html = re.sub(r'<b>(Ans\.)</b>\s+', r'<b>\1</b> ', text_html)
text_html = re.sub(r'<b>(Ques\.)</b>\s+', r'<b>\1</b> ', text_html)
text_html = re.sub(r'^<b>([IVXLCDM]+\.)</b>\s+(\d+\.)\s+', r'<b>\1 \2</b> ', text_html)
print("AFTER QA NUMS:", repr(text_html))

text_html = re.sub(r'<b>([QA])\.</b>\s*,\s*', r'<b>\1.</b> ', text_html)
print("AFTER COMMA ART:", repr(text_html))

text_html = re.sub(
    r'^(<b>A\.</b>\s+)([^<]{6,180}?[.!?;])\s+<b>A\.</b>\s+\2',
    r'\1\2',
    text_html,
    flags=re.I,
)
print("AFTER A DUPLICATE:", repr(text_html))

text_html = emphasize_structural_prefix(text_html)
print("AFTER EMPHASIZE STRUCTURAL:", repr(text_html))

text_html = re.sub(r'^<b>([IVXLCDM]+\.)</b>\s+(?:<b>)?(\d+\.)(?:</b>)?\s+', r'<b>\1 \2</b> ', text_html)
text_html = re.sub(r'(\b(?:verse|verses|chap|chapter)\.?\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html, flags=re.I)
text_html = re.sub(r'(\b\d+:\d+(?:[-,]\s*\d+)*,\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html)
print("AFTER OTHER STRIP:", repr(text_html))
