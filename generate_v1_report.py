#!/usr/bin/env python3
"""
Comprehensive EPUB Report Generator for Owen Works
Extracts and documents: metadata, fonts, CSS, structure, chapters, and more.

Usage:
    # Generate report for Volume 1 (default)
    .venv/bin/python3 generate_v1_report.py
    
    # Generate report for a specific volume
    .venv/bin/python3 generate_v1_report.py 3
    
    # Generate report for a custom EPUB path
    .venv/bin/python3 generate_v1_report.py 1 --epub /path/to/custom.epub
"""

import os
import sys
import zipfile
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

EPUB_NAMESPACES = {
    'opf': 'http://www.idpf.org/2007/opf',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'container': 'urn:oasis:names:tc:opendocument:xmlns:container',
}

def get_size_str(size_bytes):
    """Convert bytes to human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def extract_epub(epub_path, extract_dir):
    """Extract EPUB to directory."""
    with zipfile.ZipFile(epub_path, 'r') as zf:
        zf.extractall(extract_dir)
    return extract_dir

def parse_opf(opf_path):
    """Parse OPF file for metadata, manifest, spine."""
    tree = ET.parse(opf_path)
    root = tree.getroot()
    
    # Metadata
    metadata = root.find('opf:metadata', EPUB_NAMESPACES)
    meta = {}
    if metadata is not None:
        for child in metadata:
            tag = child.tag.split('}')[-1]
            if child.text and child.text.strip():
                if tag not in meta:
                    meta[tag] = []
                meta[tag].append(child.text.strip())
        
        for meta_elem in metadata.findall('opf:meta', EPUB_NAMESPACES):
            name = meta_elem.get('name')
            content = meta_elem.get('content')
            if name and content:
                if 'meta_properties' not in meta:
                    meta['meta_properties'] = {}
                meta['meta_properties'][name] = content
    
    # Manifest
    manifest = root.find('opf:manifest', EPUB_NAMESPACES)
    manifest_items = []
    if manifest is not None:
        for item in manifest.findall('opf:item', EPUB_NAMESPACES):
            manifest_items.append({
                'id': item.get('id'),
                'href': item.get('href'),
                'media_type': item.get('media-type'),
                'properties': item.get('properties'),
            })
    
    # Spine
    spine = root.find('opf:spine', EPUB_NAMESPACES)
    spine_items = []
    if spine is not None:
        for itemref in spine.findall('opf:itemref', EPUB_NAMESPACES):
            spine_items.append({
                'idref': itemref.get('idref'),
                'linear': itemref.get('linear', 'yes'),
            })
    
    # Guide (if exists)
    guide = root.find('opf:guide', EPUB_NAMESPACES)
    guide_items = []
    if guide is not None:
        for ref in guide.findall('opf:reference', EPUB_NAMESPACES):
            guide_items.append({
                'type': ref.get('type'),
                'title': ref.get('title'),
                'href': ref.get('href'),
            })
    
    return {
        'metadata': meta,
        'manifest': manifest_items,
        'spine': spine_items,
        'guide': guide_items,
        'package_attributes': root.attrib,
    }

def analyze_css(css_path):
    """Analyze CSS file for key styles."""
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract key rule blocks
    import re
    
    rules = {
        'font_faces': [],
        'body_rules': [],
        'noteref_rules': [],
        'footnote_rules': [],
        'heading_rules': [],
        'title_page_rules': [],
        'language_rules': [],
        'other_rules': [],
    }
    
    # Find @font-face blocks
    font_face_pattern = r'@font-face\s*\{[^}]+\}'
    for match in re.finditer(font_face_pattern, content, re.DOTALL):
        rules['font_faces'].append(match.group(0))
    
    # Find .noteref rules
    noteref_pattern = r'\.noteref\s*\{[^}]+\}'
    for match in re.finditer(noteref_pattern, content, re.DOTALL):
        rules['noteref_rules'].append(match.group(0))
    
    # Find .footnote rules
    footnote_pattern = r'\.footnote\s*\{[^}]+\}'
    for match in re.finditer(footnote_pattern, content, re.DOTALL):
        rules['footnote_rules'].append(match.group(0))
    
    # Find heading rules (h1, h2, etc.)
    heading_pattern = r'(h[1-6])\s*\{[^}]+\}'
    for match in re.finditer(heading_pattern, content, re.DOTALL):
        rules['heading_rules'].append(match.group(0))
    
    # Find language-specific rules [lang=...]
    lang_pattern = r'\[lang[^\]]*\]\s*\{[^}]+\}'
    for match in re.finditer(lang_pattern, content, re.DOTALL):
        rules['language_rules'].append(match.group(0))
    
    # Count total rules
    total_selectors = len(re.findall(r'[.#@][^{]+\{', content))
    rules['total_estimated_rules'] = total_selectors
    rules['raw_content'] = content
    
    return rules

def list_fonts(extract_dir):
    """List all font files in EPUB."""
    fonts = []
    for root, dirs, files in os.walk(extract_dir):
        for f in files:
            if f.lower().endswith(('.ttf', '.otf', '.woff', '.woff2')):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, extract_dir)
                size = os.path.getsize(full_path)
                fonts.append({
                    'filename': f,
                    'path': rel_path,
                    'size_bytes': size,
                    'size_str': get_size_str(size),
                })
    return fonts

def count_chapters_by_type(manifest_items, spine_items):
    """Count chapters by type (cover, title, front matter, content, notes, etc.)."""
    spine_idrefs = [s['idref'] for s in spine_items]
    manifest_by_id = {m['id']: m for m in manifest_items}
    
    counts = {
        'cover': 0,
        'title_page': 0,
        'frontispiece': 0,
        'front_matter': 0,
        'content_chapters': 0,
        'title_chapters': 0,
        'endnotes': 0,
        'nav': 0,
        'toc': 0,
        'images': 0,
        'fonts': 0,
        'css': 0,
        'other': 0,
    }
    
    for item in manifest_items:
        href = item.get('href', '').lower()
        props = (item.get('properties') or '').lower()
        media_type = item.get('media_type', '')
        
        if 'image' in media_type:
            counts['images'] += 1
        elif 'font' in media_type or href.endswith(('.ttf', '.otf', '.woff')):
            counts['fonts'] += 1
        elif 'css' in media_type or href.endswith('.css'):
            counts['css'] += 1
        elif 'nav' in props:
            counts['nav'] += 1
        elif 'cover' in props or 'cover' in href:
            counts['cover'] += 1
        elif 'title' in href and 'page' in href:
            counts['title_page'] += 1
        elif 'frontis' in href:
            counts['frontispiece'] += 1
        elif 'endnote' in href or 'note' in href:
            counts['endnotes'] += 1
        elif 'toc' in href or 'contents' in href:
            counts['toc'] += 1
        elif 'chapter' in href or 'ch' in href:
            if 'title' in href:
                counts['title_chapters'] += 1
            else:
                counts['content_chapters'] += 1
        elif 'front' in href or 'fm' in href:
            counts['front_matter'] += 1
        else:
            counts['other'] += 1
    
    return counts

def sample_chapter_content(extract_dir, num_samples=3):
    """Sample content from a few chapters to show structure."""
    samples = []
    
    # Find XHTML files
    xhtml_files = []
    for root, dirs, files in os.walk(extract_dir):
        for f in files:
            if f.endswith(('.xhtml', '.html', '.htm')):
                xhtml_files.append(os.path.join(root, f))
    
    # Sort and pick samples
    xhtml_files.sort()
    sample_files = []
    for f in xhtml_files:
        if 'ch' in f.lower() or 'chapter' in f.lower():
            sample_files.append(f)
            if len(sample_files) >= num_samples:
                break
    
    if not sample_files and xhtml_files:
        sample_files = xhtml_files[:num_samples]
    
    for f in sample_files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Extract just the body content for preview
            import re
            body_match = re.search(r'<body[^>]*>(.*)</body>', content, re.DOTALL | re.IGNORECASE)
            if body_match:
                preview = body_match.group(1)[:2000]
            else:
                preview = content[:2000]
            
            samples.append({
                'file': os.path.relpath(f, extract_dir),
                'preview': preview,
            })
        except Exception as e:
            samples.append({
                'file': os.path.relpath(f, extract_dir),
                'error': str(e),
            })
    
    return samples

def generate_report(epub_path, output_path):
    """Generate comprehensive HTML/Markdown report."""
    extract_dir = '/tmp/owen_v1_report_extract'
    
    print(f"Extracting EPUB: {epub_path}")
    if os.path.exists(extract_dir):
        import shutil
        shutil.rmtree(extract_dir)
    extract_epub(epub_path, extract_dir)
    
    # Find OPF file
    container_path = os.path.join(extract_dir, 'META-INF', 'container.xml')
    opf_path = None
    if os.path.exists(container_path):
        tree = ET.parse(container_path)
        root = tree.getroot()
        for rootfile in root.findall('.//container:rootfile', EPUB_NAMESPACES):
            opf_path = os.path.join(extract_dir, rootfile.get('full-path'))
            break
    
    if not opf_path or not os.path.exists(opf_path):
        # Try to find OPF manually
        for root, dirs, files in os.walk(extract_dir):
            for f in files:
                if f.endswith('.opf'):
                    opf_path = os.path.join(root, f)
                    break
            if opf_path:
                break
    
    print(f"Parsing OPF: {opf_path}")
    opf_data = parse_opf(opf_path)
    
    # Find CSS
    css_files = []
    for root, dirs, files in os.walk(extract_dir):
        for f in files:
            if f.endswith('.css'):
                css_files.append(os.path.join(root, f))
    
    css_analysis = {}
    for css_file in css_files:
        css_analysis[os.path.relpath(css_file, extract_dir)] = analyze_css(css_file)
    
    # List fonts
    fonts = list_fonts(extract_dir)
    
    # Count chapters
    chapter_counts = count_chapters_by_type(
        opf_data['manifest'], 
        opf_data['spine']
    )
    
    # Sample chapters
    chapter_samples = sample_chapter_content(extract_dir)
    
    # Get file size
    epub_size = os.path.getsize(epub_path)
    
    # Generate Markdown report
    report = []
    report.append(f"# John Owen Works — Volume 1 Comprehensive Report")
    report.append(f"\nGenerated: {datetime.now().isoformat()}")
    report.append(f"\n---\n")
    
    # Basic File Info
    report.append(f"## 1. Basic File Information")
    report.append(f"\n| Attribute | Value |")
    report.append(f"|-----------|-------|")
    report.append(f"| Filename | `{os.path.basename(epub_path)}` |")
    report.append(f"| File Size | {get_size_str(epub_size)} ({epub_size:,} bytes) |")
    report.append(f"| EPUB Version | {opf_data['package_attributes'].get('version', 'Unknown')} |")
    report.append(f"| Unique Identifier | {opf_data['package_attributes'].get('unique-identifier', 'Unknown')} |")
    
    # Metadata
    report.append(f"\n## 2. Metadata (Dublin Core)")
    meta = opf_data['metadata']
    for key, values in meta.items():
        if key == 'meta_properties':
            continue
        for val in values:
            report.append(f"\n- **{key}:** {val}")
    
    if 'meta_properties' in meta:
        report.append(f"\n### Additional Meta Properties")
        for name, value in meta['meta_properties'].items():
            report.append(f"\n- **{name}:** {value}")
    
    # Structure Overview
    report.append(f"\n---\n## 3. Structure Overview")
    report.append(f"\n| Component | Count |")
    report.append(f"|-----------|-------|")
    report.append(f"| Manifest Items | {len(opf_data['manifest'])} |")
    report.append(f"| Spine Items | {len(opf_data['spine'])} |")
    report.append(f"| Guide Items | {len(opf_data['guide'])} |")
    report.append(f"| CSS Files | {len(css_files)} |")
    report.append(f"| Font Files | {len(fonts)} |")
    
    report.append(f"\n### Chapter Breakdown")
    report.append(f"\n| Type | Count |")
    report.append(f"|------|-------|")
    for key, count in chapter_counts.items():
        if count > 0:
            report.append(f"| {key.replace('_', ' ').title()} | {count} |")
    
    # Spine Order
    report.append(f"\n---\n## 4. Reading Order (Spine)")
    report.append(f"\nThe following is the order of content as the reader will experience it:\n")
    for i, item in enumerate(opf_data['spine'], 1):
        idref = item['idref']
        manifest_item = next((m for m in opf_data['manifest'] if m['id'] == idref), None)
        linear = item.get('linear', 'yes')
        linear_note = " (non-linear)" if linear == 'no' else ""
        if manifest_item:
            report.append(f"{i}. `{idref}` → `{manifest_item['href']}`{linear_note}")
        else:
            report.append(f"{i}. `{idref}` (not found in manifest){linear_note}")
    
    # Fonts
    report.append(f"\n---\n## 5. Embedded Fonts")
    if fonts:
        total_font_size = sum(f['size_bytes'] for f in fonts)
        report.append(f"\nTotal font size: {get_size_str(total_font_size)}\n")
        report.append(f"\n| Font Filename | Size | Path |")
        report.append(f"|---------------|------|------|")
        for font in fonts:
            report.append(f"| `{font['filename']}` | {font['size_str']} | `{font['path']}` |")
    else:
        report.append(f"\nNo embedded fonts found.")
    
    # CSS Analysis
    report.append(f"\n---\n## 6. CSS Styling")
    for css_path, css_data in css_analysis.items():
        report.append(f"\n### `{css_path}`")
        report.append(f"\n- Estimated total rules: ~{css_data['total_estimated_rules']}")
        report.append(f"- @font-face rules: {len(css_data['font_faces'])}")
        report.append(f"- .noteref rules: {len(css_data['noteref_rules'])}")
        report.append(f"- .footnote rules: {len(css_data['footnote_rules'])}")
        report.append(f"- Heading rules: {len(css_data['heading_rules'])}")
        report.append(f"- Language-specific rules: {len(css_data['language_rules'])}")
        
        if css_data['noteref_rules']:
            report.append(f"\n#### Noteref Styles (Footnote References)")
            for rule in css_data['noteref_rules']:
                report.append(f"\n```css\n{rule}\n```")
        
        if css_data['font_faces']:
            report.append(f"\n#### @font-face Declarations")
            for i, ff in enumerate(css_data['font_faces'], 1):
                report.append(f"\n**Font {i}:**")
                report.append(f"\n```css\n{ff}\n```")
        
        if css_data['language_rules']:
            report.append(f"\n#### Language-Specific Styles (Greek/Hebrew)")
            for rule in css_data['language_rules']:
                report.append(f"\n```css\n{rule[:500]}...```" if len(rule) > 500 else f"\n```css\n{rule}\n```")
    
    # Manifest (all items)
    report.append(f"\n---\n## 7. Full Manifest Listing")
    report.append(f"\n| ID | Path | Media Type | Properties |")
    report.append(f"|----|------|------------|------------|")
    for item in opf_data['manifest']:
        props = item.get('properties') or '(none)'
        report.append(f"| `{item['id']}` | `{item['href']}` | `{item['media_type']}` | `{props}` |")
    
    # Chapter Samples
    if chapter_samples:
        report.append(f"\n---\n## 8. Chapter Content Samples")
        for sample in chapter_samples:
            report.append(f"\n### `{sample['file']}`")
            if 'error' in sample:
                report.append(f"\nError: {sample['error']}")
            else:
                report.append(f"\n```html\n{sample['preview']}\n```")
                if len(sample['preview']) >= 2000:
                    report.append(f"\n*(truncated at 2000 chars)*")
    
    # Full CSS Dump
    report.append(f"\n---\n## 9. Full CSS Content")
    for css_path, css_data in css_analysis.items():
        report.append(f"\n### `{css_path}`")
        report.append(f"\n```css\n{css_data['raw_content']}\n```")
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"Report written to: {output_path}")
    
    # Cleanup
    import shutil
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    
    return output_path

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate comprehensive EPUB report for an Owen volume')
    parser.add_argument('volume', nargs='?', type=int, default=1,
                        help='Volume number (default: 1)')
    parser.add_argument('--epub', type=Path, default=None,
                        help='Custom path to EPUB file (overrides volume-based path)')
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    
    if args.epub:
        epub_path = args.epub
        volume = args.volume
    else:
        volume = args.volume
        epub_path = script_dir / 'volumes' / f'v{volume}' / 'output' / f'volume_{volume}.epub'
    
    if args.epub:
        output_path = script_dir / 'volumes' / f'v{volume}' / 'bugs_fixes' / f'VOLUME_{volume}_REPORT.md'
    else:
        output_path = script_dir / 'volumes' / f'v{volume}' / 'bugs_fixes' / f'VOLUME_{volume}_REPORT.md'
    
    if not epub_path.exists():
        print(f"EPUB not found: {epub_path}")
        print(f"\nFor volume {volume}, first generate the EPUB with:")
        print(f"  .venv/bin/python3 converter.py {volume}")
        sys.exit(1)
    
    generate_report(str(epub_path), str(output_path))
