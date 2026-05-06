#!/usr/bin/env python3
"""
Stage 1: PDF → ThML XML for John Owen Works.

Converts AGES Digital Library PDFs to ThML (Theological Markup Language) XML.
Run from the directory containing the PDF files.

Usage:
    python3 pdf_to_thml.py [work_dir]

Outputs one volume_N.thml.xml per PDF found.
Skips volumes where the .thml.xml already exists (delete to reconvert).
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime

_SCRIPT_DIR = Path(__file__).parent
_WORKSPACE = _SCRIPT_DIR.parent
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from scripts.shared import (
    VOLUME_SUBTITLES,
    GREEK_LOWER,
    GREEK_UPPER,
    GIDEON_CHAR_MAP,
    GIDEON_CID_MAP,
    convert_greek_word,
    convert_gideon_hebrew,
    is_hebrew_vowel,
    DIACRITIC_CHARS,
    DIACRITIC_MAP,
    SMOOTH,
    ROUGH,
    ACUTE,
    GRAVE,
    CIRCUMFLEX,
    IOTASUB,
)

try:
    from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar, LTAnno
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
except ImportError:
    sys.exit("Error: pdfminer.six not installed. Run: pip install pdfminer.six")


# ============================================================================
# FONT ANALYSIS AND CLASSIFICATION
# ============================================================================

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


def is_page_number(text, font_size):
    if font_size > 10:
        return False
    return text.strip().isdigit() and len(text.strip()) <= 3


def is_scripture_code(text):
    return bool(re.match(r'<[\dA-Z]{5,8}>', text.strip()))


# ============================================================================
# PDF TEXT EXTRACTION WITH FONT TRACKING
# ============================================================================

class FontRun:
    def __init__(self, text, font_name, font_size, style_type):
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.style_type = style_type

    def __repr__(self):
        return f"FontRun({self.style_type}, {self.font_size}, {self.text[:20]!r})"


def extract_text_with_fonts(pdf_path):
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
                                                    runs.append(FontRun(
                                                        text, current_font, current_size, style
                                                    ))
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


# ============================================================================
# PDF CLEANUP AND PARAGRAPH DETECTION
# ============================================================================

def clean_text(text):
    text = ''.join(ch for ch in text if not (0xE000 <= ord(ch) <= 0xF8FF))
    text = re.sub(r'\+(?=[a-zA-Z])', '', text)
    text = re.sub(r'<[\dA-Z]{5,8}>', '', text)
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.replace('\n', ' ')
    text = text.lstrip()
    return text


def should_merge_chunks(prev_chunk, next_chunk):
    if not prev_chunk or not next_chunk:
        return True

    prev = prev_chunk.strip()
    next_start = next_chunk.strip()

    if not prev or not next_start:
        return True

    heading_patterns = r'(?:CHAPTER|SERMON|DISCOURSE|PREFACE|INTRODUCTION|CONTENTS|INDEX)'
    if re.match(heading_patterns, next_start, re.IGNORECASE):
        return False

    if not prev[-1] in '.!?;:':
        return True

    if next_start[0].islower():
        return True

    bible_pattern = (
        r'^(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|'
        r'1\s*Samuel|2\s*Samuel|1\s*Kings|2\s*Kings|'
        r'1\s*Chronicles|2\s*Chronicles|Ezra|Nehemiah|Esther|Job|'
        r'Psalms?|Proverbs?|Ecclesiastes|Isaiah|Jeremiah|Lamentations|'
        r'Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|'
        r'Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|'
        r'Matthew|Mark|Luke|John|Acts|Romans|1\s*Corinthians|2\s*Corinthians|'
        r'Galatians|Ephesians|Philippians|Colossians|'
        r'1\s*Thessalonians|2\s*Thessalonians|1\s*Timothy|2\s*Timothy|'
        r'Titus|Philemon|Hebrews|James|1\s*Peter|2\s*Peter|1\s*John|2\s*John|'
        r'3\s*John|Jude|Revelation)\s+\d'
    )
    if re.match(bible_pattern, next_start, re.IGNORECASE):
        return True

    if re.search(r'\b(?:chap|vol|pp?|ed|etc)\.$', prev, re.IGNORECASE):
        return True

    if re.match(r'^\d+:\d+', next_start):
        return True

    return False


# ============================================================================
# FOOTNOTE EXTRACTION
# ============================================================================

def extract_footnotes(pdf_path):
    footnotes = {}
    all_runs = extract_text_with_fonts(pdf_path)
    if not all_runs:
        return footnotes

    ft_section_start = None
    non_ft_count = 0

    for i in range(len(all_runs) - 1, -1, -1):
        run_text = all_runs[i].text.strip()
        if run_text in ('FT', 'ft', 'NOTES', 'Notes'):
            ft_section_start = i + 1
            break
        if run_text and run_text not in ('FT', 'ft'):
            non_ft_count += 1
            if non_ft_count > 50:
                break

    if ft_section_start is None:
        return footnotes

    footnote_text = ' '.join(run.text for run in all_runs[ft_section_start:])
    pattern = r'(\d+)\s+(.+?)(?=\d+\s+|$)'
    for match in re.finditer(pattern, footnote_text, re.DOTALL):
        num = int(match.group(1))
        text = clean_text(match.group(2)).strip()
        if text:
            footnotes[num] = text

    return footnotes


# ============================================================================
# ThML XML GENERATION
# ============================================================================

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
                self.current_chapter = {
                    'title': text,
                    'level': run.style_type,
                    'paragraphs': []
                }
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
                self.current_chapter = {
                    'title': text.strip(),
                    'level': 'h3',
                    'paragraphs': []
                }
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
                if (prev_text and curr_text
                        and prev_text[-1] not in SENTENCE_ENDERS
                        and len(prev_text) > 10
                        and curr_text[0].islower()):
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
        from xml.etree import ElementTree as ET
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
        from xml.etree import ElementTree as ET
        from xml.dom import minidom

        root = self.to_xml()
        rough = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough)
        return reparsed.toprettyxml(indent='  ')


# ============================================================================
# PDF DISCOVERY AND UTILITIES
# ============================================================================

def extract_volume_number(filename):
    match = re.search(r'vol[_\s]*(\d{1,2})', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r'[-_]v(\d{1,2})[-_.]', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r'(\d{1,2})', filename)
    if match:
        num = int(match.group(1))
        if 1 <= num <= 16:
            return num
    return None


def discover_pdfs(work_dir):
    pdfs = []
    for file in os.listdir(work_dir):
        if not file.lower().endswith('.pdf'):
            continue
        if 'works_of_john_owen' in file.lower():
            continue
        pdf_path = os.path.join(work_dir, file)
        volume_num = extract_volume_number(file)
        if volume_num and 1 <= volume_num <= 16:
            pdfs.append((volume_num, pdf_path, file))
    return sorted(pdfs, key=lambda x: x[0])


# ============================================================================
# MAIN CONVERSION
# ============================================================================

def pdf_to_thml(pdf_path, output_xml_path, volume_num):
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


def process_volume(pdf_path, work_dir, volume_num):
    basename = os.path.basename(pdf_path)
    print(f"\nProcessing Volume {volume_num}: {basename}")

    thml_path = os.path.join(work_dir, f'volume_{volume_num}.thml.xml')

    if os.path.exists(thml_path):
        print(f"  Skipping (ThML already exists: {thml_path})")
        return True, thml_path

    if not pdf_to_thml(pdf_path, thml_path, volume_num):
        return False, None

    return True, thml_path


def main():
    if len(sys.argv) > 1:
        work_dir = sys.argv[1]
    else:
        work_dir = os.getcwd()

    work_dir = os.path.abspath(work_dir)

    print(f"John Owen Works — PDF → ThML XML")
    print(f"Working directory: {work_dir}\n")

    if not os.path.isdir(work_dir):
        print(f"Error: Directory not found: {work_dir}")
        sys.exit(1)

    pdfs = discover_pdfs(work_dir)
    if not pdfs:
        print(f"No suitable PDF files found in {work_dir}")
        sys.exit(1)

    print(f"Found {len(pdfs)} PDF(s):\n")
    for vol_num, _, filename in pdfs:
        print(f"  Vol {vol_num}: {filename}")

    print(f"\n{'=' * 70}\n")
    results = []

    for vol_num, pdf_path, filename in pdfs:
        success, thml_path = process_volume(pdf_path, work_dir, vol_num)
        results.append((vol_num, success, thml_path))

    print(f"\n{'=' * 70}")
    print(f"SUMMARY\n")
    succeeded = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]
    print(f"Succeeded: {len(succeeded)}/{len(results)}")
    for vol_num, _, thml_path in succeeded:
        print(f"  Vol {vol_num}: {thml_path}")
    if failed:
        print(f"\nFailed: {len(failed)}/{len(results)}")
        for vol_num, _, _ in failed:
            print(f"  Vol {vol_num}")
    print(f"\n{'=' * 70}")


if __name__ == '__main__':
    main()