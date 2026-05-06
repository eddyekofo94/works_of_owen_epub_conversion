#!/usr/bin/env python3
"""
John Owen Works — Unified EPUB3 Converter
Merges PDF→ThML (Stage 1), ThML→EPUB3 (Stage 2), and Hebrews EPUB2→3.
Produces GEMINI.md-compliant EPUB3 with font injection, language tagging,
3-level NAV, landmarks, and Apple Books display-options.

Usage:
    python3 converter.py                  # Process all Owen Works volumes
    python3 converter.py 3                 # Process volume 3 only
    python3 converter.py --hebrews        # Process all Hebrews volumes
    python3 converter.py --hebrews 4      # Process Hebrews volume 4 only
"""

import sys
import os
import re
import uuid
import shutil
import zipfile
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime
from html import escape as _html_escape
from pathlib import Path

_SCRIPT_DIR = Path(__file__).parent.resolve()
_WORKSPACE = _SCRIPT_DIR
_Parent = _SCRIPT_DIR.parent
if str(_Parent) not in sys.path:
    sys.path.insert(0, str(_Parent))

from shared import (
    VOLUME_CONFIG, VOLUME_SUBTITLES, HEBREWS_VOLUME_CONFIG,
    FONT_POOLS, SBL_SUPPLEMENTS, EZRA_SIL_FILES,
    EPUB_STYLESHEET, EPUB3_FONT_STYLES, generate_font_styles,
    select_primary_font,
    convert_greek_word, convert_gideon_hebrew,
    GREEK_LOWER, GREEK_UPPER, GIDEON_CHAR_MAP, GIDEON_CID_MAP,
    DIACRITIC_CHARS, DIACRITIC_MAP,
    SMOOTH, ROUGH, ACUTE, GRAVE, CIRCUMFLEX, IOTASUB,
)

try:
    from ebooklib import epub
except ImportError:
    sys.exit("Error: ebooklib not installed. Run: pip install ebooklib")

try:
    from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar, LTAnno
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
except ImportError:
    PDFPageAggregator = None

FONT_BASE = os.path.join(_WORKSPACE, 'fonts')


# ============================================================================
# UTILITY: Language detection for Hebrews EPUB2 processing
# ============================================================================

_GREEK_RANGES = re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]')
_HEBREW_RANGES = re.compile(r'[\u0590-\u05FF]')


def tag_unicode_ranges(html_text):
    """Wrap untagged Greek/Hebrew Unicode runs in appropriate spans.
    
    Scans text nodes inside HTML, wrapping consecutive Greek or Hebrew
    characters in <span lang="el" xml:lang="el"> or
    <span lang="he" xml:lang="he" dir="rtl">.
    Skips text already inside lang-attributed spans.
    """
    def _process_text(text):
        segments = []
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if _GREEK_RANGES.match(ch):
                j = i
                while j < n and _GREEK_RANGES.match(text[j]):
                    j += 1
                segments.append(('el', text[i:j]))
                i = j
            elif _HEBREW_RANGES.match(ch):
                j = i
                while j < n and _HEBREW_RANGES.match(text[j]):
                    j += 1
                segments.append(('he', text[i:j]))
                i = j
            else:
                j = i
                while j < n and not _GREEK_RANGES.match(text[j]) and not _HEBREW_RANGES.match(text[j]):
                    j += 1
                segments.append((None, text[i:j]))
                i = j
        parts = []
        for lang, txt in segments:
            if lang == 'el':
                parts.append(f'<span lang="el" xml:lang="el">{txt}</span>')
            elif lang == 'he':
                parts.append(f'<span lang="he" xml:lang="he" dir="rtl">{txt}</span>')
            else:
                parts.append(txt)
        return ''.join(parts)

    outside_tags = re.split(r'(<[^>]+>)', html_text)
    result = []
    in_lang_span = False
    for segment in outside_tags:
        if segment.startswith('<'):
            if re.match(r'<span[^>]*\blang="(?:el|he)"', segment):
                in_lang_span = True
            elif segment == '</span>' and in_lang_span:
                in_lang_span = False
            result.append(segment)
        else:
            if in_lang_span:
                result.append(segment)
            else:
                result.append(_process_text(segment))
    return ''.join(result)


# ============================================================================
# STAGE 1: PDF → ThML (from pdf_to_thml.py)
# ============================================================================

class FontRun:
    def __init__(self, text, font_name, font_size, style_type):
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.style_type = style_type

    def __repr__(self):
        return f"FontRun({self.style_type}, {self.font_size}, {self.text[:20]!r})"


def classify_font(font_name, font_size):
    if not font_name:
        return 'body', False
    clean_font = font_name.split('+')[-1] if '+' in font_name else font_name
    is_greek = 'Koine' in clean_font
    is_hebrew = 'Gideon' in clean_font
    is_bold = 'Bold' in font_name
    is_italic = 'Italic' in font_name
    if is_greek:
        return 'greek', True
    if is_hebrew:
        return 'hebrew', True
    if font_size < 9:
        return 'skip', False
    if font_size >= 20:
        return 'h1', False
    if 14 <= font_size < 20:
        return 'h2', False
    if font_size < 10.5 and not is_bold:
        return 'small_caps', False
    if is_bold and is_italic:
        return 'bold_italic', False
    elif is_bold:
        return 'bold', False
    elif is_italic:
        return 'italic', False
    else:
        return 'body', False


def extract_text_with_fonts(pdf_path):
    if PDFPageAggregator is None:
        print("  Error: pdfminer.six not installed")
        return []
    runs = []
    try:
        with open(pdf_path, 'rb') as fp:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page_num, page in enumerate(PDFPage.get_pages(fp)):
                interpreter.process_page(page)
                layout = device.get_result()
                for element in layout:
                    if isinstance(element, LTTextBox):
                        if runs and runs[-1].style_type != 'para_break':
                            runs.append(FontRun('', '', 0, 'para_break'))
                        for line in element:
                            if isinstance(line, LTTextLine):
                                current_run_text = []
                                current_font = None
                                current_size = None
                                for char in line:
                                    if isinstance(char, LTChar):
                                        font_name = char.fontname or 'Unknown'
                                        font_size = char.height
                                        if (current_font is None or
                                            current_font != font_name or
                                            abs((current_size or 0) - font_size) > 0.5):
                                            if current_run_text:
                                                text = ''.join(current_run_text)
                                                style = classify_font(current_font, current_size)[0]
                                                if style != 'skip':
                                                    runs.append(FontRun(text, current_font, current_size, style))
                                            current_run_text = [char.get_text()]
                                            current_font = font_name
                                            current_size = font_size
                                        else:
                                            current_run_text.append(char.get_text())
                                    elif isinstance(char, LTAnno):
                                        current_run_text.append(char.get_text())
                                if current_run_text:
                                    text = ''.join(current_run_text)
                                    if text and not text.endswith((' ', '\n', '-')):
                                        text += ' '
                                    style = classify_font(current_font, current_size)[0]
                                    if style != 'skip':
                                        runs.append(FontRun(text, current_font, current_size, style))
    except Exception as e:
        print(f"  Error extracting text: {e}")
        return []
    return runs


def clean_text(text):
    text = ''.join(ch for ch in text if not (0xE000 <= ord(ch) <= 0xF8FF))
    text = re.sub(r'\+(?=[a-zA-Z])', '', text)
    text = re.sub(r'<[\dA-Z]{5,8}>', '', text)
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.replace('\n', ' ')
    text = text.lstrip()
    return text


class ThMLBuilder:
    FRONT_MATTER_RE = re.compile(
        r'(?:AGES\s*[DI]\s*[GI]\s*[TI]|B\s*o\s*o\s*k\s*s\s*F\s*o\s*r|'
        r'T\s*HE\s*AGES|AGES\s*Software|AGES\s*Library|'
        r'Albany,?\s*OR|www\.ageslibrary|'
        r'OHN\s*WEN\s*OLLECTION|IGITAL\s*IBRARY)',
        re.IGNORECASE
    )

    def __init__(self, title, author, volume_num):
        self.title = title
        self.author = author
        self.volume_num = volume_num
        self.chapters = []
        self.current_chapter = None
        self.current_paragraph = []
        self.in_heading = False
        self._past_front_matter = False

    def _is_front_matter(self, text):
        if self._past_front_matter:
            return False
        if self.FRONT_MATTER_RE.search(text):
            return True
        stripped = re.sub(r'\s+', '', text)
        if len(stripped) < 3:
            return True
        words = text.strip().split()
        if words and all(len(w) <= 2 for w in words) and len(words) > 3:
            return True
        return False

    def add_run(self, run):
        if run.style_type == 'para_break':
            if self.current_paragraph:
                self._flush_paragraph()
            return
        if run.style_type in ('h1', 'h2', 'h3'):
            if self.current_paragraph:
                self._flush_paragraph()
            text = clean_text(run.text)
            if not text:
                return
            if self._is_front_matter(text):
                return
            if self.in_heading and self.current_chapter and not self.current_chapter['paragraphs']:
                self.current_chapter['title'] += ' ' + text
                level_order = {'h1': 0, 'h2': 1, 'h3': 2}
                if level_order.get(run.style_type, 9) < level_order.get(self.current_chapter['level'], 9):
                    self.current_chapter['level'] = run.style_type
            else:
                if self.current_chapter and self.current_chapter['paragraphs']:
                    self.chapters.append(self.current_chapter)
                self.current_chapter = {'title': text, 'level': run.style_type, 'paragraphs': []}
            self.in_heading = True
        else:
            self.in_heading = False
            text = clean_text(run.text)
            if not text:
                return
            if self._is_front_matter(text):
                return
            if not self._past_front_matter and len(text.strip()) > 50:
                self._past_front_matter = True
            if run.style_type == 'bold' and re.match(
                r'^(?:CHAPTER|SERMON|DISCOURSE|EXERCITATION|PREFACE|'
                r'PREFATORY NOTE|DEDICATION|APPENDIX)\b',
                text.strip()
            ):
                if self.current_paragraph:
                    self._flush_paragraph()
                if self.current_chapter and self.current_chapter['paragraphs']:
                    self.chapters.append(self.current_chapter)
                self.current_chapter = {'title': text.strip(), 'level': 'h3', 'paragraphs': []}
                return
            if (run.style_type == 'small_caps' and
                    self.current_paragraph and
                    len(self.current_paragraph) >= 1):
                prev_type, prev_text = self.current_paragraph[-1]
                if (prev_type in ('body', 'bold') and
                        len(prev_text.strip()) == 1 and
                        prev_text.strip().isupper()):
                    self.current_paragraph.pop()
                    text = prev_text.strip() + text
                    self.current_paragraph.append(('small_caps', text))
                    return
            if run.style_type == 'greek':
                words = re.split(r'(\s+)', text)
                converted = []
                for w in words:
                    if w.strip():
                        converted.append(convert_greek_word(w))
                    else:
                        converted.append(w)
                text = ''.join(converted)
                self.current_paragraph.append(('greek', text))
            elif run.style_type == 'hebrew':
                text = convert_gideon_hebrew(text)
                self.current_paragraph.append(('hebrew', text))
            elif run.style_type == 'italic':
                self.current_paragraph.append(('italic', text))
            elif run.style_type == 'bold':
                self.current_paragraph.append(('bold', text))
            elif run.style_type == 'bold_italic':
                self.current_paragraph.append(('bold_italic', text))
            elif run.style_type == 'small_caps':
                if text.strip().isdigit():
                    return
                self.current_paragraph.append(('small_caps', text))
            else:
                self.current_paragraph.append(('body', text))

    def _flush_paragraph(self):
        if not self.current_paragraph:
            return
        if not self.current_chapter:
            self.current_chapter = {'title': 'Untitled', 'level': 'h1', 'paragraphs': []}
        self.current_chapter['paragraphs'].append(self.current_paragraph)
        self.current_paragraph = []

    def finalize(self):
        self._flush_paragraph()
        if self.current_chapter and self.current_chapter['paragraphs']:
            self.chapters.append(self.current_chapter)
        self._merge_broken_paragraphs()
        self._remove_empty_chapters()
        self._merge_title_fragments()
        self._clean_titles()
        self._remove_empty_chapters()

    def _merge_broken_paragraphs(self):
        SENTENCE_ENDERS = set('.?!:;"\u201c\u201d')
        for ch in self.chapters:
            if len(ch['paragraphs']) < 2:
                continue
            merged = [ch['paragraphs'][0]]
            for para in ch['paragraphs'][1:]:
                prev = merged[-1]
                prev_text = ''
                for _, t in reversed(prev):
                    prev_text = t.rstrip()
                    if prev_text:
                        break
                curr_text = ''
                for _, t in para:
                    curr_text = t.lstrip()
                    if curr_text:
                        break
                should_merge = False
                if (prev_text and curr_text and
                        prev_text[-1] not in SENTENCE_ENDERS and
                        len(prev_text) > 10 and curr_text[0].islower()):
                    should_merge = True
                if prev_text and prev_text.endswith('-') and curr_text:
                    should_merge = True
                if should_merge:
                    if prev_text and not prev_text.endswith((' ', '-')):
                        merged[-1] = list(merged[-1])
                        merged[-1].append(('body', ' '))
                    merged[-1] = list(merged[-1]) + list(para)
                else:
                    merged.append(para)
            ch['paragraphs'] = merged

    def _merge_title_fragments(self):
        if len(self.chapters) < 2:
            return
        merged = [self.chapters[0]]
        for ch in self.chapters[1:]:
            prev = merged[-1]
            prev_content_size = sum(len(t) for para in prev['paragraphs'] for _, t in para)
            if prev_content_size < 100 and len(prev['paragraphs']) <= 3:
                ch['title'] = prev['title'] + ' — ' + ch['title']
                ch['paragraphs'] = prev['paragraphs'] + ch['paragraphs']
                level_order = {'h1': 0, 'h2': 1, 'h3': 2}
                if level_order.get(prev['level'], 9) < level_order.get(ch['level'], 9):
                    ch['level'] = prev['level']
                merged[-1] = ch
            else:
                merged.append(ch)
        self.chapters = merged

    def _remove_empty_chapters(self):
        if not self.chapters:
            return
        real_start = 0
        for i, ch in enumerate(self.chapters):
            total = sum(len(t) for para in ch['paragraphs'] for _, t in para)
            if total > 2000:
                real_start = i
                break
        cleaned = []
        for i, ch in enumerate(self.chapters):
            total_text = sum(len(t) for para in ch['paragraphs'] for _, t in para)
            if self.FRONT_MATTER_RE.search(ch['title']):
                continue
            title_stripped = re.sub(r'\s+', '', ch['title'])
            if len(title_stripped) < 5 and total_text < 100:
                continue
            if i < real_start and total_text < 500:
                continue
            cleaned.append(ch)
        self.chapters = cleaned

    def _clean_titles(self):
        for ch in self.chapters:
            ch['title'] = re.sub(r'\s{2,}', ' ', ch['title']).strip()
            ch['title'] = ch['title'].strip(' —-:')
            ch['title'] = re.sub(r'\s*—\s*—\s*', ' — ', ch['title'])

    def to_xml(self):
        from xml.dom import minidom
        root = ET.Element('ThML')
        head = ET.SubElement(root, 'ThML.head')
        einfo = ET.SubElement(head, 'electronicEdInfo')
        dc = ET.SubElement(einfo, 'DC')
        title_elem = ET.SubElement(dc, 'DC.Title')
        title_elem.text = self.title
        creator = ET.SubElement(dc, 'DC.Creator')
        creator.set('sub', 'Author')
        creator.text = self.author
        date_elem = ET.SubElement(dc, 'DC.Date')
        date_elem.text = datetime.now().isoformat()
        body = ET.SubElement(root, 'ThML.body')
        for ch_idx, chapter in enumerate(self.chapters):
            div = ET.SubElement(body, 'div1')
            div.set('title', chapter['title'])
            div.set('id', f"ch{ch_idx + 1:03d}")
            h_tag = chapter['level']
            h_elem = ET.SubElement(div, h_tag)
            h_elem.text = chapter['title']
            for para_runs in chapter['paragraphs']:
                p_elem = ET.SubElement(div, 'p')
                p_elem.set('class', 'Body')
                for run_type, run_text in para_runs:
                    if run_type == 'body':
                        if len(p_elem):
                            p_elem[-1].tail = (p_elem[-1].tail or '') + run_text
                        else:
                            p_elem.text = (p_elem.text or '') + run_text
                    elif run_type == 'greek':
                        span = ET.SubElement(p_elem, 'span')
                        span.set('lang', 'EL')
                        span.set('class', 'Greek')
                        span.text = run_text
                    elif run_type == 'hebrew':
                        span = ET.SubElement(p_elem, 'span')
                        span.set('lang', 'HE')
                        span.set('class', 'Hebrew')
                        span.text = run_text
                    elif run_type == 'italic':
                        i_elem = ET.SubElement(p_elem, 'i')
                        i_elem.text = run_text
                    elif run_type == 'bold':
                        b_elem = ET.SubElement(p_elem, 'b')
                        b_elem.text = run_text
                    elif run_type == 'bold_italic':
                        b_elem = ET.SubElement(p_elem, 'b')
                        i_elem = ET.SubElement(b_elem, 'i')
                        i_elem.text = run_text
                    elif run_type == 'small_caps':
                        span = ET.SubElement(p_elem, 'span')
                        span.set('style', 'font-variant:small-caps')
                        span.text = run_text
                    else:
                        if len(p_elem):
                            p_elem[-1].tail = (p_elem[-1].tail or '') + run_text
                        else:
                            p_elem.text = (p_elem.text or '') + run_text
        return root

    def to_xml_string(self):
        from xml.dom import minidom
        root = self.to_xml()
        rough = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough)
        return reparsed.toprettyxml(indent='  ')


def pdf_to_thml(pdf_path, output_xml_path, volume_num):
    """Stage 1: Convert AGES PDF to ThML XML."""
    print(f"  Extracting text from PDF...")
    runs = extract_text_with_fonts(pdf_path)
    if not runs:
        print(f"  Warning: No text extracted from PDF")
        return False
    print(f"  Building ThML document ({len(runs)} runs)...")
    subtitle = VOLUME_SUBTITLES.get(volume_num, "")
    title = f"The Works of John Owen, Vol. {volume_num}"
    if subtitle:
        title += f" — {subtitle}"
    builder = ThMLBuilder(title, "John Owen", volume_num)
    for run in runs:
        builder.add_run(run)
    builder.finalize()
    print(f"  Writing ThML XML...")
    xml_str = builder.to_xml_string()
    try:
        with open(output_xml_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        size = os.path.getsize(output_xml_path)
        print(f"  Saved ThML: {output_xml_path} ({size / 1024:.0f} KB)")
        return True
    except Exception as e:
        print(f"  Error writing ThML: {e}")
        return False


# ============================================================================
# STAGE 2: ThML → EPUB3 (from thml_to_epub.py, enhanced)
# ============================================================================

def _find_parent(container, target):
    """Walk *container* and return the element whose direct child is *target*."""
    for child in container:
        if child is target:
            return container
        result = _find_parent(child, target)
        if result is not None:
            return result
    return None


def _next_sibling(elem, parent):
    """Return the next sibling element after *elem* under *parent*, or None."""
    found = False
    for child in parent:
        if found:
            return child
        if child is elem:
            found = True
    return None


def _escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                 .replace('>', '&gt;').replace('"', '&quot;'))


def _make_xhtml(title, body_html, css_href='style/main.css',
                font_styles=None):
    safe_title = _escape_xml(title)
    style_block = ''
    if font_styles:
        style_block = f'\n<style type="text/css">{font_styles}</style>\n'
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">'
        '<head>'
        '<meta charset="utf-8"/>'
        f'<title>{safe_title}</title>'
        f'<link rel="stylesheet" type="text/css" href="{css_href}"/>'
        f'{style_block}'
        '</head>'
        f'<body>{body_html}</body>'
        '</html>'
    )


def _elem_to_html(elem, endnotes_file='ch120.xhtml'):
    html_parts = []
    if elem.text:
        html_parts.append(_escape_xml(elem.text))
    for child in elem:
        if child.tag == 'span':
            lang = child.get('lang', '')
            cls = child.get('class', '')
            style = child.get('style', '')
            attrs = ''
            if lang:
                normalized = lang.lower()
                if normalized == 'el':
                    attrs += f' lang="el" xml:lang="el"'
                elif normalized == 'he':
                    attrs += f' lang="he" xml:lang="he" dir="rtl"'
                else:
                    attrs += f' lang="{lang}"'
            if cls:
                attrs += f' class="{cls}"'
            if style:
                attrs += f' style="{style}"'
            inner = _elem_to_html(child, endnotes_file)
            html_parts.append(f'<span{attrs}>{inner}</span>')
        elif child.tag == 'a':
            cls = child.get('class', '')
            href = child.get('href', '')
            if cls == 'fnref' and href.startswith('#fn'):
                fn_id = href[1:].strip()
                num = (child.text or '').strip()
                html_parts.append(
                    f'<a epub:type="noteref" role="doc-noteref" '
                    f'href="{endnotes_file}#{fn_id}" class="footnote-ref">'
                    f'<sup>{_escape_xml(num)}</sup></a>'
                )
            else:
                inner = _elem_to_html(child, endnotes_file)
                a_attrs = f' href="{_escape_xml(href)}"' if href else ''
                if cls:
                    a_attrs += f' class="{_escape_xml(cls)}"'
                html_parts.append(f'<a{a_attrs}>{inner}</a>')
            if child.tail:
                html_parts.append(_escape_xml(child.tail))
            continue
        elif child.tag in ('i', 'b', 'em', 'strong'):
            inner = _elem_to_html(child, endnotes_file)
            html_parts.append(f'<{child.tag}>{inner}</{child.tag}>')
        else:
            inner = _elem_to_html(child, endnotes_file)
            html_parts.append(inner)
        if child.tail:
            html_parts.append(_escape_xml(child.tail))
    return ''.join(html_parts)


def _is_treatise_title_page(div1):
    paras = div1.findall('p')
    if not paras:
        return False
    connector_re = re.compile(
        r'^(?:OR,?|OF,?|ON,?|IN,?|WITH,?|AS\s+ALSO,?|AND,?|ALSO,?|'
        r'WHEREIN,?|BEING,?)\s*$',
        re.IGNORECASE
    )
    connectors = 0
    total_body_text = 0
    leading_connectors = 0
    leading_done = False
    for p in paras:
        text = _elem_to_html(p).strip()
        plain = re.sub(r'<[^>]+>', '', text).strip()
        total_body_text += len(plain)
        is_connector = False
        if re.match(r'^<b>[^<]{1,20}</b>$', text):
            bold_text = re.sub(r'</?b>', '', text).strip()
            if connector_re.match(bold_text):
                connectors += 1
                is_connector = True
        elif connector_re.match(plain) and len(plain) < 15:
            connectors += 1
            is_connector = True
        if not leading_done:
            if is_connector:
                leading_connectors += 1
            else:
                leading_done = True
    if connectors >= 2 and total_body_text < 2000:
        return True
    if leading_connectors >= 2:
        return True
    return False


def _build_treatise_title(div1):
    connector_re = re.compile(
        r'^(?:OR,?|OF,?|ON,?|IN,?|WITH,?|AS\s+ALSO,?|AND,?|ALSO,?|'
        r'WHEREIN,?|BEING,?)\s*$',
        re.IGNORECASE
    )
    parts = ['<div class="treatise-title">']

    greek_heading = ''
    if div1.find('h2') is not None:
        greek_elem = div1.find('h2')
        greek_text = _elem_to_html(greek_elem).strip()
        if re.match(r'^[Α-Ω]+$', greek_text.replace(' ', '')):
            greek_heading = greek_text
            parts.append(f'<h2 class="greek">{_escape_xml(greek_heading)}</h2>')

    heading_text = ''
    heading_tag = 'h1'
    for h_tag in ('h1', 'h2', 'h3'):
        h_elem = div1.find(h_tag)
        if h_elem is not None:
            heading_text = _elem_to_html(h_elem).strip()
            heading_tag = h_tag
            break

    # Split combined headings (e.g., TREATISE CHAPTER 1)
    split = _split_nav_title(heading_text)
    if split:
        treatise, unit = split
        parts.append(f'<h1>{_escape_xml(treatise)}</h1>')
        parts.append(f'<h2>{_escape_xml(unit)}</h2>')
    else:
        heading_lines = [h.strip() for h in heading_text.split(' — ') if h.strip()]
        body_paras = []
        connectors_list = []
        for p_elem in div1.findall('p'):
            html = _elem_to_html(p_elem)
            trimmed = html.strip()
            if not trimmed:
                continue
            plain = re.sub(r'<[^>]+>', '', trimmed).strip()
            is_conn = False
            if re.match(r'^<b>[^<]{1,20}</b>$', trimmed):
                bold_text = re.sub(r'</?b>', '', trimmed).strip()
                if connector_re.match(bold_text):
                    connectors_list.append(bold_text)
                    body_paras.append(('connector', bold_text))
                    is_conn = True
            elif connector_re.match(plain) and len(plain) < 15:
                connectors_list.append(plain)
                body_paras.append(('connector', plain))
                is_conn = True
            if not is_conn:
                body_paras.append(('other', trimmed, plain))
        if len(heading_lines) > 1 and connectors_list:
            parts.append(f'<h1>{_escape_xml(heading_lines[0])}</h1>')
            conn_idx = 0
            for i, line in enumerate(heading_lines[1:]):
                if conn_idx < len(connectors_list):
                    parts.append(f'<p class="connector">{_escape_xml(connectors_list[conn_idx])}</p>')
                    conn_idx += 1
                parts.append(f'<h2>{_escape_xml(line)}</h2>')
            used_connectors = conn_idx
        else:
            parts.append(f'<{heading_tag}>{heading_text}</{heading_tag}>')
            used_connectors = 0
    connector_skip = 0
    for item in body_paras:
        if item[0] == 'connector':
            if connector_skip < used_connectors:
                connector_skip += 1
                continue
            bold_text = item[1]
            parts.append(f'<p class="connector">{_escape_xml(bold_text)}</p>')
            continue
        trimmed = item[1]
        plain = item[2]
        if trimmed.startswith('<i>'):
            parts.append(f'<p class="desc">{trimmed}</p>')
            continue
        if plain.startswith(('"', '\u201c', "'", '\u2018')):
            parts.append(f'<p class="epigraph">{trimmed}</p>')
            continue
        parts.append(f'<p>{trimmed}</p>')
    parts.append('</div>')
    return ''.join(parts)


def _build_normal_chapter(div1, endnotes_file='ch120.xhtml'):
    body_parts = ['<section>']
    
    heading_text = ''
    heading_tag = ''
    for h_tag in ('h1', 'h2', 'h3'):
        h_elem = div1.find(h_tag)
        if h_elem is not None:
            heading_text = _elem_to_html(h_elem, endnotes_file).strip()
            heading_tag = h_tag
            break
            
    if heading_tag:
        # Split combined headings (e.g., TREATISE CHAPTER 1)
        split = _split_nav_title(heading_text)
        if split:
            treatise, unit = split
            body_parts.append(f'<h1>{_escape_xml(treatise)}</h1>')
            body_parts.append(f'<h2>{_escape_xml(unit)}</h2>')
        else:
            body_parts.append(f'<{heading_tag}>{heading_text}</{heading_tag}>')

    para_count = 0
    for p_elem in div1.findall('p'):
        p_html = _elem_to_html(p_elem, endnotes_file)
        if not p_html.strip():
            continue
        css_class = ' class="first"' if para_count == 0 else ''
        body_parts.append(f'<p{css_class}>{p_html}</p>')
        para_count += 1
    body_parts.append('</section>')
    return ''.join(body_parts)


def _build_endnotes_chapter(root, vol_num, endnotes_file=None):
    """Extract footnotes from the FOOTNOTES div1 and build endnotes XHTML.

    Two strategies depending on ThML structure:

    * Volume 1 uses ``<a class="fnmarker" data-fn="N"/>`` self-closing
      anchors to mark where each footnote starts.  We walk the tree and
      collect text following each marker.

    * Other volumes have plain ``<p>`` elements — one paragraph per
      footnote, in sequential order matching fn1, fn2, ….
    """
    div1s = root.findall('.//div1')
    if not div1s:
        return None

    footnotes_div = None
    footnotes_div_idx = None
    for idx, div1 in enumerate(div1s):
        if (div1.get('title') or '').upper() == 'FOOTNOTES':
            footnotes_div = div1
            footnotes_div_idx = idx
            break

    if footnotes_div is None:
        return None

    if endnotes_file is None:
        for div1 in div1s:
            if (div1.get('title') or '').upper() == 'FOOTNOTES':
                endnotes_file = div1.get('id', 'ch120') + '.xhtml'
                break
        else:
            endnotes_file = 'ch120.xhtml'

    fnmarker_elems = footnotes_div.findall('.//a[@class="fnmarker"]')
    footnotes = {}

    if fnmarker_elems:
        # Volume-1 style: fnmarker elements mark footnote boundaries
        for marker in fnmarker_elems:
            fn_num = marker.get('data-fn', '').strip()
            if not fn_num:
                continue
            text_parts = []
            if marker.tail:
                t = marker.tail.strip()
                if t:
                    text_parts.append(t)
            parent = _find_parent(footnotes_div, marker)
            if parent is not None:
                collecting = False
                for child in parent:
                    if child is marker:
                        collecting = True
                        continue
                    if collecting:
                        if child.tag == 'a' and child.get('class') == 'fnmarker':
                            break
                        inner = _elem_to_html(child, endnotes_file).strip()
                        if inner:
                            text_parts.append(inner)
                        if child.tail:
                            t = child.tail.strip()
                            if t:
                                text_parts.append(t)
            note_text = ' '.join(text_parts).strip()
            if note_text:
                footnotes[fn_num] = note_text
    else:
        # Other volumes: plain <p> elements — sequential footnotes
        para_idx = 0
        for child in footnotes_div:
            if child.tag == 'h1':
                continue
            if child.tag == 'p':
                para_idx += 1
                fn_num = str(para_idx)
                inner = _elem_to_html(child, endnotes_file).strip()
                if inner:
                    footnotes[fn_num] = inner

    if not footnotes:
        return None

    aside_parts = [
        '<section epub:type="endnotes" role="doc-endnotes">',
        '<h1>FOOTNOTES</h1>',
    ]
    for fn_num in sorted(footnotes.keys(), key=lambda x: int(x)):
        fn_id = f'fn{fn_num}'
        text = footnotes[fn_num]
        aside_parts.append(
            f'<aside epub:type="endnote" role="doc-endnote" id="{fn_id}">'
            f'<p class="footnote">'
            f'<a epub:type="noteref" href="#{fn_id}" class="fn-link">'
            f'<sup>{fn_num}</sup></a> {text}</p>'
            f'</aside>'
        )
    aside_parts.append('</section>')
    return '\n'.join(aside_parts)


# ============================================================================
# FONT INJECTION
# ============================================================================

def inject_fonts_into_epub(epub_dir, volume_name, is_hebrews=False):
    """Copy font files and create Fonts/ directory in the EPUB structure."""
    fonts_dir = os.path.join(epub_dir, 'Fonts')
    os.makedirs(fonts_dir, exist_ok=True)

    primary = select_primary_font(volume_name)
    all_font_files = {}

    for rel_path, font_file in primary['files'].items():
        src = os.path.join(FONT_BASE, font_file)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(fonts_dir, os.path.basename(font_file)))
            all_font_files[rel_path] = font_file
        else:
            print(f"    Warning: Font not found: {src}")

    for fname, fpath in SBL_SUPPLEMENTS.items():
        src = os.path.join(FONT_BASE, fpath)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(fonts_dir, fname))
        else:
            print(f"    Warning: Font not found: {src}")

    if is_hebrews or True:
        for fname, fpath in EZRA_SIL_FILES.items():
            src = os.path.join(FONT_BASE, fpath)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(fonts_dir, fname))

    return primary, all_font_files


def get_font_manifest_entries(fonts_dir):
    """Get font file entries for OPF manifest."""
    entries = []
    if os.path.isdir(fonts_dir):
        for fname in sorted(os.listdir(fonts_dir)):
            fpath = os.path.join(fonts_dir, fname)
            if os.path.isfile(fpath) and fname.endswith(('.ttf', '.otf')):
                mime = 'application/font-sfnt' if fname.endswith('.ttf') else 'application/vnd.ms-opentype'
                entries.append({
                    'id': f'font_{os.path.splitext(fname)[0]}',
                    'href': f'Fonts/{fname}',
                    'mime': mime,
                })
    return entries


def find_portrait(workspace, vol_num=None):
    """Find a portrait image for John Owen, deterministically selected per volume.

    When vol_num is provided, uses a hash-based selection from all available
    portraits so each volume gets a different (but reproducible) portrait.
    When vol_num is None, returns the first portrait found (legacy behavior).
    """
    portraits_dir = os.path.join(workspace, 'portraits')
    if not os.path.isdir(portraits_dir):
        return None

    all_portraits = []
    for ext in ('.jpeg', '.jpg', '.png', '.webp'):
        for fname in sorted(os.listdir(portraits_dir)):
            if fname.lower().endswith(ext):
                all_portraits.append(os.path.join(portraits_dir, fname))

    if not all_portraits:
        return None

    if vol_num is not None:
        import hashlib
        idx = int(hashlib.md5(f'owen-v{vol_num}'.encode()).hexdigest(), 16) % len(all_portraits)
        return all_portraits[idx]
    return all_portraits[0]


def generate_frontispiece_xhtml(portrait_filename='portrait.jpeg'):
    """Generate frontispiece.xhtml matching reference format."""
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml"'
        ' xmlns:epub="http://www.idpf.org/2007/ops"'
        ' epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#"'
        ' lang="en" xml:lang="en">\n'
        '  <head>\n'
        '    <title>Frontispiece</title>\n'
        '    <link href="style/main.css" rel="stylesheet" type="text/css"/>\n'
        '  </head>\n'
        '  <body>\n'
        '    <div class="frontispiece">\n'
        f'      <img src="images/{portrait_filename}" alt="Portrait of John Owen"/>\n'
        '      <p class="caption">John Owen (1616–1683)</p>\n'
        '    </div>\n'
        '  </body>\n'
        '</html>'
    )


def fix_cover_xhtml(oebps):
    """Fix cover.xhtml to match reference format (simple <img> without CSS link)."""
    cover_path = os.path.join(oebps, 'cover.xhtml')
    if not os.path.exists(cover_path):
        return

    with open(cover_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract image src
    img_match = re.search(r'<img[^>]+src="([^"]+)"', content)
    if not img_match:
        return

    img_src = img_match.group(1)
    alt_match = re.search(r'alt="([^"]*)"', content)
    alt_text = alt_match.group(1) if alt_match else 'Cover'

    # Rewrite to match reference format
    new_content = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml"'
        ' xmlns:epub="http://www.idpf.org/2007/ops"'
        ' epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#"'
        ' lang="en" xml:lang="en">\n'
        '  <head>\n'
        '    <title>Cover</title>\n'
        '  </head>\n'
        '  <body>\n'
        f'    <img src="{img_src}" alt="{alt_text}"/>\n'
        '  </body>\n'
        '</html>'
    )

    with open(cover_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


def inject_font_css(oebps, primary_font_name, primary_font_files):
    """Append @font-face and language override CSS to the main stylesheet."""
    font_css = generate_font_styles(primary_font_name, primary_font_files)

    css_path = os.path.join(oebps, 'style', 'main.css')
    if not os.path.exists(css_path):
        for root, dirs, files in os.walk(oebps):
            for f in files:
                if f.endswith('.css'):
                    css_path = os.path.join(root, f)
                    break

    if os.path.exists(css_path):
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write('\n' + font_css)
        return True
    return False


def write_ncx_file(oebps, title, uid, toc_entries):
    """Write the toc.ncx file for EPUB2 fallback compatibility."""
    ncx_content = generate_ncx(title, uid, toc_entries)
    ncx_path = os.path.join(oebps, 'toc.ncx')
    with open(ncx_path, 'w', encoding='utf-8') as f:
        f.write(ncx_content)
    return ncx_path


# ============================================================================
# NAV GENERATION (3-level hierarchical + landmarks)
# ============================================================================

def _extract_chapter_subtitle(div1):
    """Extract the subtitle from the first <b> tags within the first 5 <p> tags."""
    subtitle_parts = []
    for p in div1.findall('.//p')[:5]:
        for b in p.findall('b'):
            text = (b.text or '').strip()
            # Skip if it's just a number, Roman numeral, or bracketed/parenthesized marker
            if re.match(r'^[\(\[]?\d+[a-z]{0,2}[\.\),\]]?$|^[IVXLCDM]+\.?$|^\(\d+\.\)$|^\[\d+\.\]$', text, re.IGNORECASE):
                continue
            if text:
                subtitle_parts.append(text)
        if subtitle_parts and not p.findall('b'):
            break
    if subtitle_parts:
        subtitle = ' '.join(subtitle_parts)
        words = subtitle.split()
        small_words = {'and', 'or', 'of', 'in', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 'the', 'a', 'an', 'as', 'unto'}
        result = []
        for i, w in enumerate(words):
            lw = w.lower()
            if lw in small_words and i > 0 and i < len(words) - 1:
                result.append(lw)
            else:
                match = re.search(r'[a-zA-Z]', lw)
                if match:
                    idx = match.start()
                    cw = lw[:idx] + lw[idx].upper() + lw[idx+1:]
                    result.append(cw)
                else:
                    result.append(lw)
        return ' '.join(result)
    return ''

def _split_nav_title(title):
    """Split combined titles like 'TREATISE CHAPTER 1' into (treatise, chapter).

    Detects patterns where a treatise/section name is followed by a unit indicator
    (CHAPTER, BOOK, PART, SECTION + number). Returns a (treatise, chapter) tuple
    when a split is detected, or None when no split is needed.

    Does NOT split when an em-dash precedes the unit indicator (e.g., "— CHAPTER 1"),
    as that indicates a continuation of the title rather than a structural split.
    """
    m = re.match(r'^(.+?)\s+((?:CHAPTER|BOOK|PART|SECTION)\s+\d+\.?)$', title.strip(), re.IGNORECASE)
    if m:
        before_unit = m.group(1).rstrip()
        if before_unit.endswith('—') or before_unit.endswith('—'):
            return None
        treatise = before_unit.rstrip('.—:— ')
        unit = m.group(2).strip().rstrip('.')
        return (treatise, unit)
    return None


def generate_nav_xhtml(toc_entries, landmarks=None, volume_title=None):
    """Generate an EPUB3 nav.xhtml with 3-level TOC and landmarks.

    toc_entries: list of (level, text, href) tuples where level starts at 1.
    Produces properly nested <ol>/<li> structure per EPUB3 spec.
    """
    if not toc_entries:
        return '<nav epub:type="toc" id="id" role="doc-toc"><h2>Table of Contents</h2><ol></ol></nav>'

    display_title = volume_title or 'Table of Contents'
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE html>',
        '<html xmlns="http://www.w3.org/1999/xhtml"'
        ' xmlns:epub="http://www.idpf.org/2007/ops"'
        ' epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#"'
        ' lang="en" xml:lang="en">',
        '<head>',
        f'  <title>{_html_escape(display_title)}</title>',
        '  <link href="style/main.css" rel="stylesheet" type="text/css"/>',
        '</head>',
        '<body>',
        f'<nav epub:type="toc" id="id" role="doc-toc">',
        f'<h2>{_html_escape(display_title)}</h2>',
    ]

    depth = 0

    for level, text, href in toc_entries:
        if level > depth:
            while level > depth:
                lines.append('<ol>')
                depth += 1
        elif level < depth:
            while level < depth:
                lines.append('</li>')
                lines.append('</ol>')
                depth -= 1
            lines.append('</li>')
        else:
            lines.append('</li>')

        lines.append(f'<li><a href="{_html_escape(href)}">{_html_escape(text)}</a>')

    for _ in range(depth):
        lines.append('</li>')
        lines.append('</ol>')

    lines.append('</nav>')

    if landmarks is None:
        landmarks = [
            ('toc', 'Table of Contents', 'nav.xhtml'),
        ]

    if toc_entries:
        first_href = toc_entries[0][2]
        landmarks.append(('bodymatter', 'Start of Content', first_href))

    lines.append('<nav epub:type="landmarks" id="landmarks">')
    lines.append('<h1>Guide</h1>')
    lines.append('<ol>')
    for epub_type, text, href in landmarks:
        lines.append(f'<li><a epub:type="{epub_type}" href="{_html_escape(href)}">'
                     f'{_html_escape(text)}</a></li>')
    lines.append('</ol>')
    lines.append('</nav>')
    lines.append('</body>')
    lines.append('</html>')
    return '\n'.join(lines)


def generate_ncx(title, uid, toc_entries):
    """Generate toc.ncx (EPUB2 fallback) from flat or hierarchical entries."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">',
        '  <head>',
        f'    <meta content="{_html_escape(uid)}" name="dtb:uid"/>',
        '    <meta content="3" name="dtb:depth"/>',
        '    <meta content="0" name="dtb:totalPageCount"/>',
        '    <meta content="0" name="dtb:maxPageNumber"/>',
        '  </head>',
        '  <docTitle>',
        f'    <text>{_html_escape(title)}</text>',
        '  </docTitle>',
        '  <navMap>',
    ]

    order = [0]
    for level, text, href in toc_entries:
        order[0] += 1
        depth_class = {1: 1, 2: 2, 3: 3}.get(level, 1)
        safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', href or f'item_{order[0]}')
        indent = '  ' * (depth_class + 1)
        lines.append(f'{indent}<navPoint id="nav_{safe_id}" playOrder="{order[0]}">')
        lines.append(f'{indent}  <navLabel><text>{_html_escape(text)}</text></navLabel>')
        lines.append(f'{indent}  <content src="{_html_escape(href)}"/>')
        lines.append(f'{indent}</navPoint>')

    lines.append('  </navMap>')
    lines.append('</ncx>')
    return '\n'.join(lines)


# ============================================================================
# OPF UPDATE (EPUB3 compliance)
# ============================================================================

def update_opf_for_epub3(opf_path, nav_rel, font_entries=None,
                          volume_title=None, volume_authors=None):
    """Update OPF to EPUB3: version, nav, fonts, metadata."""
    ET.register_namespace('', "http://www.idpf.org/2007/opf")
    tree = ET.parse(opf_path)
    root = tree.getroot()
    root.set('version', '3.0')

    ns = {'opf': 'http://www.idpf.org/2007/opf'}
    mf = root.find('{http://www.idpf.org/2007/opf}manifest')

    if mf is not None:
        for item in list(mf):
            href = item.get('href', '')
            if '.html' in href:
                item.set('href', href.replace('.html', '.xhtml'))
            if item.get('properties') == 'nav' or '.ncx' in href:
                mf.remove(item)

        ET.SubElement(mf, 'item', id='nav', href=nav_rel,
                      properties='nav', **{'media-type': 'application/xhtml+xml'})

        if font_entries:
            for fe in font_entries:
                ET.SubElement(mf, 'item',
                              id=fe['id'], href=fe['href'],
                              **{'media-type': fe['mime']})

    meta = root.find('{http://www.idpf.org/2007/opf}metadata')
    ns_dc = 'http://purl.org/dc/elements/1.1/'
    if meta is not None:
        if volume_title:
            for t in list(meta.findall(f'{{{ns_dc}}}title')):
                meta.remove(t)
            new_title = ET.SubElement(meta, f'{{{ns_dc}}}title')
            new_title.text = volume_title

        if volume_authors:
            for c in list(meta.findall(f'{{{ns_dc}}}creator')):
                meta.remove(c)
            insert_after = meta.find(f'{{{ns_dc}}}title')
            if insert_after is None:
                insert_after = meta.find(f'{{{ns_dc}}}identifier')
            all_children = list(meta)
            if insert_after is not None:
                insert_idx = all_children.index(insert_after) + 1
            else:
                insert_idx = 0
            for i, author in enumerate(volume_authors):
                creator = ET.SubElement(meta, f'{{{ns_dc}}}creator')
                creator.set('id', 'creator')
                creator.text = author
                meta.remove(creator)
                meta.insert(insert_idx + i, creator)

    tree.write(opf_path, encoding='utf-8', xml_declaration=True)


# ============================================================================
# APPLE BOOKS DISPLAY OPTIONS
# ============================================================================

def add_apple_display_options(epub_dir):
    """Create META-INF/com.apple.ibooks.display-options.xml."""
    meta_inf = os.path.join(epub_dir, 'META-INF')
    os.makedirs(meta_inf, exist_ok=True)
    path = os.path.join(meta_inf, 'com.apple.ibooks.display-options.xml')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<display-options xmlns="http://www.apple.com/itunes/vbook/display-options">'
            '<platform name="*">'
            '<option name="specified-fonts">true</option>'
            '</platform>'
            '</display-options>'
        )


# ============================================================================
# XMLNS:EPUB INJECTION
# ============================================================================

def ensure_xmlns_epub(xhtml_path):
    """Ensure xmlns:epub namespace declaration in XHTML files."""
    with open(xhtml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'xmlns:epub' not in content:
        content = re.sub(
            r'<html\b([^>]*?)>',
            r'<html\1 xmlns:epub="http://www.idpf.org/2007/ops">',
            content, count=1, flags=re.I
        )
        with open(xhtml_path, 'w', encoding='utf-8') as f:
            f.write(content)


# ============================================================================
# EPUB POST-PROCESSING (EPUB3 compliance)
# ============================================================================

def post_process_epub3(epub_path):
    """Rewrite the EPUB ZIP for EPUB3 compliance:
    - mimetype first and uncompressed
    - version="3.0"
    - toc="ncx" in spine
    - nav.xhtml has properties="nav"
    """
    tmp_dir = tempfile.mkdtemp()
    extract_dir = os.path.join(tmp_dir, 'epub')
    try:
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(epub_path, 'r') as zf:
            zf.extractall(extract_dir)

        opf_path = None
        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f.endswith('.opf'):
                    opf_path = os.path.join(root, f)
                    break

        if opf_path:
            with open(opf_path, 'r', encoding='utf-8') as f:
                opf = f.read()
            opf = re.sub(r'version="2\.0"', 'version="3.0"', opf)
            if '<spine' in opf and 'toc="ncx"' not in opf:
                opf = opf.replace('<spine', '<spine toc="ncx"')
            opf = re.sub(
                r'(<item[^>]*href="nav\.xhtml"[^>]*)/>',
                r'\1 properties="nav"/>',
                opf,
            )
            opf = re.sub(r'properties="nav"\s+properties="nav"',
                         'properties="nav"', opf)
            with open(opf_path, 'w', encoding='utf-8') as f:
                f.write(opf)

        temp_zip = epub_path + '.tmp'
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            mt_path = os.path.join(extract_dir, 'mimetype')
            if os.path.exists(mt_path):
                zf.write(mt_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
            for dirpath, _, filenames in os.walk(extract_dir):
                for fn in sorted(filenames):
                    if fn == 'mimetype':
                        continue
                    full = os.path.join(dirpath, fn)
                    arcname = os.path.relpath(full, extract_dir)
                    zf.write(full, arcname)

        if os.path.exists(epub_path):
            os.remove(epub_path)
        os.rename(temp_zip, epub_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ============================================================================
# REPACKAGE EPUB
# ============================================================================

def repackage_epub(extract_dir, output_path):
    """Create EPUB ZIP from extracted directory."""
    temp_zip = output_path + '.tmp'
    with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        mt_path = os.path.join(extract_dir, 'mimetype')
        if os.path.exists(mt_path):
            zf.write(mt_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
        for dirpath, _, filenames in os.walk(extract_dir):
            for fn in sorted(filenames):
                if fn == 'mimetype' and dirpath == extract_dir:
                    continue
                full = os.path.join(dirpath, fn)
                arcname = os.path.relpath(full, extract_dir)
                zf.write(full, arcname)
    if os.path.exists(output_path):
        os.remove(output_path)
    os.rename(temp_zip, output_path)


# ============================================================================
# MAIN PIPELINE: Owen Works (PDF/CCEL → EPUB3)
# ============================================================================

def process_owen_volume(vol_num):
    """Process a single Owen Works volume: PDF → ThML → EPUB3."""
    config = VOLUME_CONFIG.get(vol_num)
    if not config:
        print(f"  Error: No config for volume {vol_num}")
        return False

    source_type = config['source_type']
    title = config['title']
    authors = config['authors']
    publisher = config['publisher']

    vol_dir = os.path.join(_WORKSPACE, 'volumes', f'v{vol_num}')
    input_dir = os.path.join(vol_dir, 'input')
    intermediate_dir = os.path.join(vol_dir, 'intermediate')
    output_dir = os.path.join(vol_dir, 'output')
    os.makedirs(intermediate_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    thml_path = os.path.join(intermediate_dir, f'volume_{vol_num}.thml.xml')
    epub_path = os.path.join(output_dir, f'volume_{vol_num}.epub')

    if os.path.exists(epub_path):
        print(f"  Skipping (EPUB exists): {epub_path}")
        return True

    if source_type == 'ages_pdf':
        pdf_links = os.path.join(input_dir, f'owen-v{vol_num}.pdf')
        if not os.path.exists(pdf_links):
            for ext in ('.pdf',):
                alt = os.path.join(_WORKSPACE, 'pdfs', f'owen-v{vol_num}.pdf')
                if os.path.exists(alt):
                    pdf_links = alt
                    break

        if not os.path.exists(pdf_links):
            print(f"  Error: Source PDF not found for volume {vol_num}")
            return False

        if not os.path.exists(thml_path):
            print(f"  Stage 1: PDF → ThML...")
            if not pdf_to_thml(pdf_links, thml_path, vol_num):
                return False
        else:
            print(f"  Stage 1: Using existing ThML: {thml_path}")

        source_path = thml_path
    elif source_type == 'ccel_xml':
        ccel_file = config.get('ccel_file', '')
        source_path = os.path.join(_WORKSPACE, ccel_file)
        if not os.path.exists(source_path):
            print(f"  Error: CCEL source not found: {source_path}")
            return False
        print(f"  Using CCEL XML source: {source_path}")
    else:
        print(f"  Error: Unknown source type: {source_type}")
        return False

    print(f"  Stage 2: Converting to EPUB3...")

    try:
        tree = ET.parse(source_path)
        root = tree.getroot()
    except Exception as e:
        print(f"  Error parsing source: {e}")
        return False

    dc_title = root.find('.//DC.Title')
    dc_creator = root.find('.//DC.Creator')
    if dc_title is not None and dc_title.text:
        parsed_title = dc_title.text
    else:
        parsed_title = title
    if dc_creator is not None and dc_creator.text:
        parsed_author = dc_creator.text
    else:
        parsed_author = authors[0]

    subtitle = VOLUME_SUBTITLES.get(vol_num, "")

    book = epub.EpubBook()
    vol_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f'john-owen-works-bot-vol-{vol_num}')
    book.set_identifier(f'urn:uuid:{vol_uuid}')
    book.set_title(title)
    book.set_language('en')
    for author in authors:
        book.add_author(author)
    book.add_metadata('DC', 'publisher', publisher)
    book.add_metadata('DC', 'subject', 'Theology')
    book.add_metadata('DC', 'subject', 'Puritanism')
    book.add_metadata('DC', 'description',
                      f'Volume {vol_num} of The Works of John Owen, '
                      f'edited by William H. Goold.')

    style_item = epub.EpubItem(
        uid='main-css', file_name='style/main.css',
        media_type='text/css', content=EPUB_STYLESHEET.encode('utf-8')
    )
    book.add_item(style_item)

    # Select font
    primary = select_primary_font(f'owen-v{vol_num}')
    primary_font_name = {'SBL_BLit': 'SBL BibLit', 'Cardo': 'Cardo',
                          'Libertinus': 'Libertinus Serif'}.get(primary['name'], primary['name'])
    primary_font_files = primary['files']
    font_styles = generate_font_styles(primary_font_name, primary_font_files)

    # Cover
    covers_dir = os.path.join(_WORKSPACE, 'covers')
    cover_file = None
    if os.path.isdir(covers_dir):
        for ext in ('.png', '.jpg', '.jpeg', '.webp'):
            candidate = os.path.join(covers_dir, f'v{vol_num}{ext}')
            if os.path.exists(candidate):
                cover_file = candidate
                break

    if cover_file:
        try:
            with open(cover_file, 'rb') as f:
                cover_data = f.read()
            ext = os.path.splitext(cover_file)[1].lower()
            book.set_cover(f'images/cover{ext}', cover_data)
            print(f"  Added cover image")
        except Exception as e:
            print(f"  Warning: Could not add cover: {e}")

    # Frontispiece (portrait)
    portrait_file = find_portrait(_WORKSPACE, vol_num=vol_num)
    frontispiece_item = None
    if portrait_file:
        try:
            portrait_ext = os.path.splitext(portrait_file)[1].lstrip('.')
            portrait_filename = f'portrait.{portrait_ext}'
            # Add portrait image to OPF manifest
            with open(portrait_file, 'rb') as pf:
                portrait_data = pf.read()
            portrait_mime = 'image/jpeg' if portrait_ext in ('jpeg', 'jpg') else 'image/png'
            portrait_image_item = epub.EpubItem(
                uid='portrait-img',
                file_name=f'images/{portrait_filename}',
                media_type=portrait_mime,
                content=portrait_data,
            )
            book.add_item(portrait_image_item)
            frontispiece_html = generate_frontispiece_xhtml(portrait_filename)
            frontispiece_item = epub.EpubHtml(
                title='Frontispiece', file_name='frontispiece.xhtml', lang='en'
            )
            frontispiece_item.set_content(frontispiece_html.encode('utf-8'))
            frontispiece_item.add_item(style_item)
            book.add_item(frontispiece_item)
            print(f"  Added frontispiece with portrait ({os.path.basename(portrait_file)})")
        except Exception as e:
            print(f"  Warning: Could not add frontispiece: {e}")

    # Title page — matching reference EPUB design
    title_body = (
        '<div class="title-page">'
        '<p class="ornament">\u2767</p>'
        f'<h1>The Works of<br/>{_escape_xml(parsed_author)}</h1>'
        '<hr class="rule"/>'
        f'<p class="subtitle">Volume {vol_num}</p>'
        f'<p class="subtitle">{_escape_xml(subtitle)}</p>'
        f'<p class="author"><span class="by">by</span>{_escape_xml(parsed_author)}</p>'
        f'<p class="editor">Edited by William H. Goold</p>'
        f'<p class="publisher">{_escape_xml(publisher)}</p>'
        '</div>'
    )
    title_page = epub.EpubHtml(
        title='Title Page', file_name='title.xhtml', lang='en'
    )
    title_page.set_content(
        _make_xhtml('Title Page', title_body, font_styles=font_styles).encode('utf-8')
    )
    title_page.add_item(style_item)
    book.add_item(title_page)

    # Determine endnotes file name from FOOTNOTES div1
    div1_elements = root.findall('.//div1')
    endnotes_file = None
    for div1 in div1_elements:
        if (div1.get('title') or '').upper() == 'FOOTNOTES':
            endnotes_id = div1.get('id', 'ch120')
            endnotes_file = f'{endnotes_id}.xhtml'
            break

    # Chapters
    print(f"  Converting chapters...")
    epub_chapters = []

    toc_entries = []

    for div_idx, div1 in enumerate(div1_elements):
        chapter_title = div1.get('title', f'Chapter {div_idx + 1}')
        chapter_id = div1.get('id', f'ch{div_idx + 1:03d}')

        if (div1.get('title') or '').upper() == 'FOOTNOTES':
            continue

        is_treatise = _is_treatise_title_page(div1)

        if is_treatise:
            body_html = _build_treatise_title(div1)
        else:
            body_html = _build_normal_chapter(div1, endnotes_file=endnotes_file or 'ch120.xhtml')

        level_map = {'h1': 1, 'h2': 2, 'h3': 3}
        h_tag_found = None
        for ht in ('h1', 'h2', 'h3'):
            if div1.find(ht) is not None:
                h_tag_found = ht
                break

        if chapter_id == 'ch017':
            print(f"DEBUG: ch017 h_tag_found={h_tag_found}")

        toc_level = level_map.get(h_tag_found, 2) if h_tag_found else 2
        
        subtitle = _extract_chapter_subtitle(div1)
        
        split = _split_nav_title(chapter_title)
        if split:
            treatise, unit = split
            # Treatise at its natural level, unit at +1
            toc_entries.append((toc_level, treatise, f'{chapter_id}.xhtml'))
            unit = unit.rstrip('.').title()
            if subtitle:
                unit = f"{unit} - {subtitle}"
            toc_entries.append((toc_level + 1, unit, f'{chapter_id}.xhtml'))
        else:
            # Normal entry at its natural level
            if re.match(r'^(?:CHAPTER|BOOK|PART|SECTION)\s+\d+\.?$', chapter_title.strip(), re.IGNORECASE):
                display_title = chapter_title.strip().rstrip('.').title()
                if subtitle:
                    display_title = f"{display_title} - {subtitle}"
                toc_entries.append((toc_level, display_title, f'{chapter_id}.xhtml'))
            elif re.match(r'^[IVXLCDM]+\.?$', chapter_title.strip(), re.IGNORECASE):
                # Roman numeral sub-sections go at a deeper level
                display_title = chapter_title.strip()
                if subtitle:
                    display_title = f"{display_title} {subtitle}"
                toc_entries.append((toc_level + 1, display_title, f'{chapter_id}.xhtml'))
            else:
                toc_entries.append((toc_level, chapter_title, f'{chapter_id}.xhtml'))

        ch_item = epub.EpubHtml(
            title=chapter_title[:200],
            file_name=f'{chapter_id}.xhtml',
            lang='en'
        )
        ch_item.set_content(
            _make_xhtml(chapter_title, body_html, font_styles=font_styles).encode('utf-8')
        )
        ch_item.add_item(style_item)
        book.add_item(ch_item)
        epub_chapters.append(ch_item)

    if toc_entries:
        normalized = []
        has_parent = False
        for lvl, txt, hr in toc_entries:
            if lvl == 1:
                normalized.append((1, txt, hr))
                has_parent = True
                print(f"DEBUG: TOC L1: {txt} (hr={hr}) -> has_parent=True")
            elif lvl == 2:
                if has_parent:
                    normalized.append((2, txt, hr))
                    print(f"DEBUG: TOC L2 stays L2: {txt}")
                else:
                    normalized.append((1, txt, hr))
                    print(f"DEBUG: TOC L2 -> L1: {txt}")
            else:
                normalized.append((lvl, txt, hr))
        toc_entries = normalized

    print(f"  {len(epub_chapters)} chapters created")

    # Build endnotes chapter from ThML footnotes
    endnotes_html = _build_endnotes_chapter(root, vol_num, endnotes_file=endnotes_file)
    if endnotes_html:
        if endnotes_file is None:
            endnotes_file = 'ch120.xhtml'
        endnotes_item = epub.EpubHtml(
            title='Footnotes', file_name=endnotes_file, lang='en'
        )
        endnotes_item.set_content(
            _make_xhtml('Footnotes', endnotes_html, font_styles=font_styles).encode('utf-8')
        )
        endnotes_item.add_item(style_item)
        book.add_item(endnotes_item)
        epub_chapters.append(endnotes_item)
        toc_entries.append((1, 'Footnotes', endnotes_file))
        print(f"  Added footnotes chapter (ch120.xhtml)")

    # Generate NAV with volume title from VOLUME_SUBTITLES (contains subtitle only)
    subtitle = VOLUME_SUBTITLES.get(vol_num, "")
    full_title = f'The Works of John Owen, Vol. {vol_num} — {subtitle}'
    nav_html = generate_nav_xhtml(toc_entries, volume_title=full_title)

    # Also fix OPF title to match reference format
    opf_title = full_title
    nav_item = epub.EpubHtml(
        title='Table of Contents', file_name='nav.xhtml', lang='en'
    )
    nav_item.set_content(nav_html.encode('utf-8'))
    nav_item.add_item(style_item)
    book.add_item(nav_item)

    # NCX fallback
    ncx_xml = generate_ncx(full_title, f'urn:uuid:{vol_uuid}', toc_entries)
    ncx_item = epub.EpubItem(
        uid='ncx', file_name='toc.ncx',
        media_type='application/x-dtbncx+xml',
        content=ncx_xml.encode('utf-8'),
    )
    book.add_item(ncx_item)

    # TOC for ebooklib
    toc_list = [title_page]
    if frontispiece_item:
        toc_list.append(frontispiece_item)
    book.toc = toc_list + epub_chapters

    # Spine: nav → frontispiece → title → chapters
    spine_list = ['nav']
    if frontispiece_item:
        spine_list.append(frontispiece_item)
    spine_list.append(title_page)
    spine_list.extend(epub_chapters)
    book.spine = spine_list

    # Write initial EPUB
    print(f"  Writing EPUB file...")
    temp_epub = epub_path + '.tmp'
    epub.write_epub(temp_epub, book, {})

    # Post-process: inject fonts, fix OPF, add Apple Books
    print(f"  Post-processing for EPUB3 compliance...")
    tmp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(temp_epub, 'r') as zf:
            zf.extractall(tmp_dir)

        # Find OEBPS/content dir
        oebps = None
        for root, dirs, files in os.walk(tmp_dir):
            if any(f.endswith('.opf') for f in files):
                oebps = root
                break
        if not oebps:
            oebps = tmp_dir

        # Inject fonts
        primary, font_file_map = inject_fonts_into_epub(oebps, f'owen-v{vol_num}')
        font_manifest = get_font_manifest_entries(os.path.join(oebps, 'Fonts'))

        # Copy portrait to images dir
        if portrait_file:
            images_dir = os.path.join(oebps, 'images')
            os.makedirs(images_dir, exist_ok=True)
            portrait_ext = os.path.splitext(portrait_file)[1]
            shutil.copy2(portrait_file, os.path.join(images_dir, f'portrait{portrait_ext}'))

        # Fix cover.xhtml to match reference format (simple <img> without CSS)
        fix_cover_xhtml(oebps)

        # Inject @font-face CSS into stylesheet
        inject_font_css(oebps, primary_font_name, primary_font_files)

        # Write NCX fallback
        ncx_path = write_ncx_file(oebps, full_title, f'urn:uuid:{vol_uuid}', toc_entries)

        # Find OPF
        opf_path = None
        for root, _, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith('.opf'):
                    opf_path = os.path.join(root, f)
                    break

        if opf_path:
            nav_rel = os.path.relpath(os.path.join(oebps, 'nav.xhtml'), os.path.dirname(opf_path))
            update_opf_for_epub3(opf_path, nav_rel, font_manifest,
                                  volume_title=opf_title, volume_authors=authors)

        # Ensure xmlns:epub in all XHTML files
        for root, _, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith(('.xhtml', '.html')):
                    ensure_xmlns_epub(os.path.join(root, f))

        add_apple_display_options(tmp_dir)

        repackage_epub(tmp_dir, epub_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        if os.path.exists(temp_epub):
            os.remove(temp_epub)

    file_size = os.path.getsize(epub_path)
    print(f"  Saved EPUB: {epub_path} ({file_size / 1024:.0f} KB)")
    return True


# ============================================================================
# HEBREWS PIPELINE: EPUB2 → EPUB3
# ============================================================================

def read_source_ncx(epub_path):
    """Parse the source NCX and return flat list of (label, href)."""
    with zipfile.ZipFile(epub_path, 'r') as zf:
        ncx_files = [n for n in zf.namelist() if n.endswith('.ncx')]
        if not ncx_files:
            return []
        ncx_xml = zf.read(ncx_files[0]).decode('utf-8')

    ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
    root = ET.fromstring(ncx_xml)
    nav_map = root.find('ncx:navMap', ns)
    if nav_map is None:
        return []

    entries = []

    def walk(parent):
        for np in parent.findall('ncx:navPoint', ns):
            label_el = np.find('ncx:navLabel/ncx:text', ns)
            content_el = np.find('ncx:content', ns)
            label = label_el.text.strip() if label_el is not None and label_el.text else ''
            href = content_el.get('src', '') if content_el is not None else ''
            if label:
                entries.append((label, href))
            walk(np)

    walk(nav_map)
    return entries


def _is_parent_entry(label):
    stripped = label.strip()
    if re.match(r'^PART\s+[IVXLC]+', stripped, re.IGNORECASE):
        return True
    if re.match(r'^CHAPTER\s+\d+', stripped, re.IGNORECASE):
        return True
    return False


def _is_front_matter(label):
    low = label.strip().lower()
    return any(low.startswith(k) for k in (
        'general preface', 'preface', 'the epistle dedicatory',
        'epistle dedicatory', 'prefatory', 'editor',
    ))


def build_toc_hierarchy(flat_entries):
    """Convert flat list of (label, href) into nested list of (level, label, href)."""
    result = []
    current_parent = None
    children = []

    def flush():
        nonlocal current_parent, children
        if current_parent is not None:
            result.append((1, current_parent[0], current_parent[1]))
            for cl, ch in children:
                result.append((2, cl, ch))
        current_parent = None
        children = []

    for label, href in flat_entries:
        if _is_parent_entry(label):
            flush()
            current_parent = (label, href)
            children = []
        elif _is_front_matter(label):
            flush()
            result.append((1, label, href))
        else:
            if current_parent is not None:
                children.append((label, href))
            else:
                result.append((1, label, href))
    flush()
    return result


def extract_html_chapters(epub_path):
    """Return list of (filename, html_content) for split chapter files."""
    chapters = []
    with zipfile.ZipFile(epub_path, 'r') as zf:
        html_files = sorted(
            n for n in zf.namelist()
            if 'split' in n and (n.endswith('.html') or n.endswith('.xhtml'))
        )
        for fname in html_files:
            content = zf.read(fname).decode('utf-8')
            chapters.append((fname, content))
    return chapters


def extract_epub_metadata(epub_path):
    """Read DC metadata from source EPUB."""
    with zipfile.ZipFile(epub_path, 'r') as zf:
        opf_candidates = [n for n in zf.namelist() if n.endswith('.opf')]
        if not opf_candidates:
            return {'title': 'Hebrews', 'creator': 'John Owen',
                    'language': 'en', 'publisher': 'Banner of Truth Trust'}
        content_opf = zf.read(opf_candidates[0]).decode('utf-8')

    root = ET.fromstring(content_opf)
    result = {'title': None, 'creator': None, 'language': 'en', 'publisher': None}
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
    for elem in root.findall('.//dc:*', ns):
        tag = elem.tag.split('}')[-1]
        if tag in result:
            result[tag] = elem.text

    return {
        'title': result['title'] or 'An Exposition of the Epistle to the Hebrews',
        'creator': result['creator'] or 'John Owen',
        'language': result['language'],
        'publisher': result['publisher'] or 'Banner of Truth Trust',
    }


def fix_broken_toc_hrefs(flat_entries, chapters_data):
    """Fix TOC hrefs pointing to near-empty anchors at tail of files."""
    filenames = [os.path.basename(fn) for fn, _ in chapters_data]
    content_by_name = {}
    for fn, html in chapters_data:
        content_by_name[os.path.basename(fn)] = html

    fixed = []
    num_fixed = 0
    for label, href in flat_entries:
        if '#' in href:
            fname, anchor = href.split('#', 1)
            html = content_by_name.get(fname, '')
            if html:
                anchor_pattern = f'id="{re.escape(anchor)}"'
                m = re.search(anchor_pattern, html)
                if m:
                    after = html[m.end():]
                    text_after = re.sub(r'<[^>]+>', '', after).strip()
                    if len(text_after) < 150:
                        try:
                            idx = filenames.index(fname)
                            if idx + 1 < len(filenames):
                                new_href = filenames[idx + 1]
                                fixed.append((label, new_href))
                                num_fixed += 1
                                continue
                        except ValueError:
                            pass
        fixed.append((label, href))
    if num_fixed:
        print(f"  Fixed {num_fixed} broken TOC link(s)")
    return fixed


def clean_html(html_content):
    """Strip calibre artifacts and old headers."""
    clean = re.sub(r'<head>.*?</head>', '', html_content, flags=re.DOTALL)
    clean = re.sub(r'class="calibre\d+"', '', clean)
    clean = re.sub(r'<html[^>]*>|<body[^>]*>|</body>|</html>', '', clean)
    clean = re.sub(r'<img[^>]*src="hebrews[^"]*\.jpg"[^>]*/?\s*>', '',
                   clean, flags=re.IGNORECASE)
    clean = re.sub(
        r'(<h[1-6])([^>]*)>\s*<a\s[^>]*id="([^"]+)"[^>]*/?\s*>\s*(?:</a>)?\s*',
        r'\1\2 id="\3">',
        clean,
    )
    return clean


def extract_chapter_title(html_content, default_title):
    m = re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html_content, re.DOTALL)
    if m:
        raw = re.sub(r'<[^>]+>', '', m.group(1))
        raw = re.sub(r'\s+', ' ', raw).strip()
        if 3 < len(raw) < 150:
            return raw
    return default_title


def process_hebrews_volume(vol_num):
    """Process a single Hebrews EPUB2 → EPUB3 volume."""
    config = HEBREWS_VOLUME_CONFIG.get(vol_num)
    if not config:
        print(f"  Error: No config for Hebrews volume {vol_num}")
        return False

    title = config['title']
    authors = config['authors']
    publisher = config['publisher']

    hebrews_dir = os.path.join(_WORKSPACE, 'hebrews', 'volumes', f'hb{vol_num}')
    input_dir = os.path.join(hebrews_dir, 'input')
    output_dir = os.path.join(hebrews_dir, 'output')
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Find source EPUB
    source_path = None
    for fname in os.listdir(input_dir):
        if fname.lower().endswith('.epub'):
            source_path = os.path.join(input_dir, fname)
            break

    if not source_path:
        print(f"  Error: No EPUB found in {input_dir}")
        return False

    epub_path = os.path.join(output_dir, f'hebrews_v{vol_num}.epub')
    if os.path.exists(epub_path):
        print(f"  Skipping (EPUB exists): {epub_path}")
        return True

    print(f"  Converting Hebrews Volume {vol_num}...")
    metadata = extract_epub_metadata(source_path)
    print(f"  Title: {metadata['title']}")

    chapters_data = extract_html_chapters(source_path)
    flat_toc = read_source_ncx(source_path)

    if flat_toc and flat_toc[0][0].lower().startswith('an exposition'):
        flat_toc = flat_toc[1:]
    flat_toc = fix_broken_toc_hrefs(flat_toc, chapters_data)
    toc_entries = build_toc_hierarchy(flat_toc)
    print(f"  TOC entries: {len(flat_toc)}")

    # Setup book
    book = epub.EpubBook()
    book_uid = f'urn:uuid:{uuid.uuid5(uuid.NAMESPACE_DNS, f"john-owen-hebrews-v{vol_num}")}'
    book.set_identifier(book_uid)
    book.set_title(title)
    book.set_language('en')
    for author in authors:
        book.add_author(author)
    book.add_metadata('DC', 'publisher', publisher)
    book.add_metadata('DC', 'subject', 'Theology')
    book.add_metadata('DC', 'subject', 'Puritanism')
    book.add_metadata('DC', 'subject', 'Hebrews')
    book.add_metadata('DC', 'description',
                      f"John Owen's Commentary on the Epistle to the Hebrews, Volume {vol_num}")

    # CSS
    primary = select_primary_font(f'hebrews-v{vol_num}')
    primary_font_name = {'SBL_BLit': 'SBL BibLit', 'Cardo': 'Cardo',
                          'Libertinus': 'Libertinus Serif'}.get(primary['name'], primary['name'])
    full_css = EPUB_STYLESHEET + '\n' + generate_font_styles(primary_font_name, primary['files'])

    style_item = epub.EpubItem(
        uid='main-css', file_name='style/main.css',
        media_type='text/css', content=full_css.encode('utf-8')
    )
    book.add_item(style_item)

    # Cover
    covers_dir = os.path.join(_WORKSPACE, 'hebrews', 'covers')
    cover_file = None
    if os.path.isdir(covers_dir):
        for ext in ('png', 'jpeg', 'jpg'):
            for prefix in (f'hb{vol_num}', f'Hb{vol_num}'):
                candidate = os.path.join(covers_dir, f'{prefix}.{ext}')
                if os.path.exists(candidate):
                    cover_file = candidate
                    break
            if cover_file:
                break

    if cover_file:
        try:
            with open(cover_file, 'rb') as f:
                cover_data = f.read()
            ext = os.path.splitext(cover_file)[1].lstrip('.')
            book.set_cover(f'images/cover.{ext}', cover_data)
            print(f"  Added cover: {os.path.basename(cover_file)}")
        except Exception as e:
            print(f"  Warning: Could not add cover: {e}")

    # Content chapters
    epub_chapters = []
    chapter_toc = []
    for i, (fname, content) in enumerate(chapters_data):
        old_fname = os.path.basename(fname)
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        body_content = body_match.group(1) if body_match else content
        ch_title = extract_chapter_title(body_content, f'Section {i + 1}')
        clean_content = clean_html(body_content)

        # Tag Greek/Hebrew Unicode runs
        clean_content = tag_unicode_ranges(clean_content)

        full_html = (
            '<?xml version="1.0" encoding="utf-8"?>'
            '<html xmlns="http://www.w3.org/1999/xhtml"'
            ' xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">'
            '<head><meta charset="utf-8"/>'
            f'<title>{_escape_xml(ch_title)}</title>'
            '<link rel="stylesheet" href="style/main.css" type="text/css"/>'
            '</head>'
            f'<body>{clean_content}</body>'
            '</html>'
        )

        ch = epub.EpubHtml(
            title=ch_title[:200], file_name=old_fname, lang='en'
        )
        ch.set_content(full_html.encode('utf-8'))
        ch.add_item(style_item)
        book.add_item(ch)
        epub_chapters.append(ch)
        chapter_toc.append((2, ch_title, old_fname))

    print(f"  {len(epub_chapters)} chapters processed")

    # NAV with volume title
    nav_html = generate_nav_xhtml(toc_entries + chapter_toc, volume_title=title)
    nav_item = epub.EpubHtml(
        title='Table of Contents', file_name='nav.xhtml', lang='en'
    )
    nav_item.set_content(nav_html.encode('utf-8'))
    nav_item.add_item(style_item)
    book.add_item(nav_item)

    # NCX
    ncx_xml = generate_ncx(title, book_uid, toc_entries)
    ncx_item = epub.EpubItem(
        uid='ncx', file_name='toc.ncx',
        media_type='application/x-dtbncx+xml',
        content=ncx_xml.encode('utf-8'),
    )
    book.add_item(ncx_item)

    # Build TOC
    book.toc = epub_chapters

    # Spine: nav → title → chapters (no frontispiece for Hebrews)
    book.spine = ['nav'] + epub_chapters

    # Write
    print(f"  Writing EPUB file...")
    temp_epub = epub_path + '.tmp'
    epub.write_epub(temp_epub, book, {})

    # Post-process
    print(f"  Post-processing for EPUB3 compliance...")
    tmp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(temp_epub, 'r') as zf:
            zf.extractall(tmp_dir)

        oebps = None
        for root, _, files in os.walk(tmp_dir):
            if any(f.endswith('.opf') for f in files):
                oebps = root
                break
        if not oebps:
            oebps = tmp_dir

        inject_fonts_into_epub(oebps, f'hebrews-v{vol_num}', is_hebrews=True)
        font_manifest = get_font_manifest_entries(os.path.join(oebps, 'Fonts'))

        # Fix cover.xhtml to match reference format
        fix_cover_xhtml(oebps)

        # Inject @font-face CSS into stylesheet
        primary = select_primary_font(f'hebrews-v{vol_num}')
        primary_font_name_heb = {'SBL_BLit': 'SBL BibLit', 'Cardo': 'Cardo',
                                  'Libertinus': 'Libertinus Serif'}.get(primary['name'], primary['name'])
        inject_font_css(oebps, primary_font_name_heb, primary['files'])

        # Write NCX fallback
        write_ncx_file(oebps, title, book_uid, toc_entries)

        # Ensure xmlns:epub in all XHTML files
        for root, _, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith(('.xhtml', '.html')):
                    fpath = os.path.join(root, f)
                    ensure_xmlns_epub(fpath)

        opf_path = None
        for root, _, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith('.opf'):
                    opf_path = os.path.join(root, f)
                    break

        if opf_path:
            nav_rel = os.path.relpath(os.path.join(oebps, 'nav.xhtml'), os.path.dirname(opf_path))
            update_opf_for_epub3(opf_path, nav_rel, font_manifest,
                                  volume_title=title, volume_authors=authors)

        add_apple_display_options(tmp_dir)
        repackage_epub(tmp_dir, epub_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        if os.path.exists(temp_epub):
            os.remove(temp_epub)

    size_kb = os.path.getsize(epub_path) / 1024
    print(f"  Saved: {os.path.basename(epub_path)} ({size_kb:.0f} KB)")
    return True


# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================

def main():
    args = sys.argv[1:]
    hebrews_mode = '--hebrews' in args
    if hebrews_mode:
        args.remove('--hebrews')

    specific_vol = None
    if args:
        try:
            specific_vol = int(args[0])
        except ValueError:
            print(f"Usage: python3 converter.py [volume_number] [--hebrews]")
            print(f"  python3 converter.py              # Process all Owen Works volumes")
            print(f"  python3 converter.py 3             # Process volume 3 only")
            print(f"  python3 converter.py --hebrews     # Process all Hebrews volumes")
            print(f"  python3 converter.py --hebrews 4   # Process Hebrews volume 4 only")
            sys.exit(1)

    if hebrews_mode:
        print("=" * 60)
        print("John Owen Hebrews Commentary — EPUB2 → EPUB3 Converter")
        print("=" * 60)
        volumes = [specific_vol] if specific_vol else list(HEBREWS_VOLUME_CONFIG.keys())
        results = []
        for vol_num in volumes:
            print(f"\n{'─' * 60}")
            print(f"Hebrews Volume {vol_num}")
            success = process_hebrews_volume(vol_num)
            results.append((vol_num, success))
    else:
        print("=" * 60)
        print("John Owen Works — PDF/CCEL → EPUB3 Converter")
        print("=" * 60)
        volumes = [specific_vol] if specific_vol else list(VOLUME_CONFIG.keys())
        results = []
        for vol_num in volumes:
            print(f"\n{'─' * 60}")
            print(f"Volume {vol_num}: {VOLUME_CONFIG[vol_num]['title']}")
            success = process_owen_volume(vol_num)
            results.append((vol_num, success))

    print(f"\n{'=' * 60}")
    print("SUMMARY\n")
    succeeded = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]
    print(f"Succeeded: {len(succeeded)}/{len(results)}")
    for vol_num, _ in succeeded:
        print(f"  Vol {vol_num}")
    if failed:
        print(f"\nFailed: {len(failed)}/{len(results)}")
        for vol_num, _ in failed:
            print(f"  Vol {vol_num}")
    print(f"\n{'=' * 60}")


if __name__ == '__main__':
    main()