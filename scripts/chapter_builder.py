import re
from dataclasses import dataclass, field
from shared import title_case
from scripts.markdown_skeleton import get_merged_page_text
# ================================================================
# STAGE 5: Chapter Building from TOC
# ================================================================


@dataclass
class Chapter:
    cid: str
    title: str
    level: int          # 1=treatise, 2=chapter, 3=subsection
    body_html: str = ''
    raw_text: str = ''  # Precisely truncated raw text from build_chapters_from_toc
    page_start: int = 0
    page_end: int = 0
    is_treatise: bool = False
    is_endnotes: bool = False
    footnote_refs: list = field(default_factory=list)


def _trim_to_matching_structural_marker(raw_text: str, title: str) -> str:
    """Drop carried-over page text before the marker for the current TOC entry."""
    if not raw_text or not title:
        return raw_text

    def norm(value: str) -> str:
        value = re.sub(r'\[\[[A-Z_]+\]\]', ' ', value)
        value = re.sub(r'[^A-Z0-9]+', ' ', value.upper())
        return re.sub(r'\s+', ' ', value).strip()

    title_norm = norm(title)
    if not title_norm:
        return raw_text
    markers = list(re.finditer(
        r'\[\[(?:PART|CHAPTER|DIGRESSION|ROMAN_HEAD|SUBTITLE|SUMMARY)\]\]\s*([^\n]*)',
        raw_text,
        re.I,
    ))
    if not markers:
        return raw_text
    for marker in markers:
        if marker.start() == 0:
            continue
        marker_text = norm(marker.group(1))
        if marker_text and (title_norm in marker_text or marker_text in title_norm):
            return raw_text[marker.start():].strip()
    return raw_text


def _keep_only_prerendered_treatise_title_page(raw_text: str) -> str:
    """Keep a pre-rendered title section without same-page body spillover."""
    if not raw_text:
        return raw_text
    match = re.match(
        r'(?P<section>\s*<section\b[^>]*class="[^"]*\btreatise-title-page\b.*?</section>)',
        raw_text,
        re.I | re.S,
    )
    if not match:
        return raw_text
    return match.group('section').strip()


def build_chapters_from_toc(doc, pages_md, nav_entries, footnote_map, config=None,
                            vol_num=None, progress_callback=None):
    """
    Build chapters by grouping pages based on PDF TOC entries.
    Merges consecutive same-level entries and handles hierarchy.
    """
    if not nav_entries:
        # Fallback: treat each page as a chapter
        return _build_flat_chapters(doc, pages_md, footnote_map)
    
    chapters = []
    seen_titles = set()
    cid_counter = 0
    
    # Filter out metadata entries (book-level entries, contents pages)
    # Also skip all children of filtered-out entries (tree-aware)
    filtered_nav = []
    skip_level = None  # level of the currently skipped metadata entry
    metadata_patterns = re.compile(
        r'^(Owen Librarian|The Works of John Owen|Contents|The Works of John Owen Vol\.\s*\d+)$|'
        r'^The Works of John Owen\s*[-–]|'
        r'^Contents\s+of\b', re.I
    )
    for level, title, page in nav_entries:
        title_stripped = title.strip()
        is_meta = bool(metadata_patterns.match(title_stripped))
        
        if is_meta:
            skip_level = level
            continue
        
        if skip_level is not None:
            if level <= skip_level:
                skip_level = None  # back to sibling level, stop skipping
            else:
                continue  # still a child of a skipped entry
        
        filtered_nav.append((level, title_stripped, page))
    
    nav_entries = filtered_nav
    
    if not nav_entries:
        return _build_flat_chapters(doc, pages_md, footnote_map)
    
    # Process TOC entries
    current_treatise = ""
    configured_treatises = (config or {}).get('treatises', [])
    
    for i, (level, title, page_0idx) in enumerate(nav_entries):
        if re.fullmatch(r'\s*FOOTNOTES\.?\s*', title, re.I):
            continue
        # Determine if this is a treatise title page
        title_upper = title.upper()
        
        # Use relative matching against configured treatises (Issue 108)
        # We check if the TOC title contains any of our configured treatise titles
        matched_treatise = None
        for t in configured_treatises:
            if t.upper() in title_upper or title_upper in t.upper():
                matched_treatise = t
                break
                
        standalone_catechism_title = bool(re.match(
            r'^(?:THE\s+)?(?:GREATER|LESSER)\s+CATECHISM\.?$',
            title_upper,
        ))
        is_treatise = (
            bool(matched_treatise)
            or any(kw in title_upper for kw in ['PART', 'BOOK'])
            or standalone_catechism_title
        )
        
        if is_treatise:
            if matched_treatise:
                current_treatise = matched_treatise
            else:
                current_treatise = title_case(title)

        # Determine end page (next entry's page - 1, or end of doc)
        if i + 1 < len(nav_entries):
            end_page = nav_entries[i + 1][2] - 1
        else:
            end_page = len(doc) - 1
        
        if end_page < page_0idx:
            end_page = page_0idx
        
        # Skip if bookends/empty
        shares_previous_start = bool(chapters and chapters[-1].page_end == page_0idx)
        allow_treatise_title_page = not (shares_previous_start and not is_treatise)
        raw_text = get_pages_text(
            doc,
            pages_md,
            page_0idx,
            end_page,
            title=title,
            config=config,
            allow_treatise_title_page=allow_treatise_title_page,
        )
        raw_text = _trim_to_matching_structural_marker(raw_text, title)
        
        # Handle shared start page: if this chapter starts on a page shared with previous,
        # extract only from the heading onwards.
        if chapters and chapters[-1].page_end == page_0idx:
            # If this is a chapter starting on the same page as a treatise/part,
            # we must start at the CHAPTER marker, not the PART marker.
            if not is_treatise:
                marker = re.search(r'\[\[CHAPTER\]\]', raw_text)
                if marker:
                    raw_text = raw_text[marker.start():]
            else:
                marker = re.search(r'\[\[(?:PART|CHAPTER|DIGRESSION)\]\]', raw_text)
                if marker:
                    raw_text = raw_text[marker.start():]

        # Handle shared end page: if the NEXT chapter starts on the same page this one ends,
        # OR if it starts on the very same page (shared start), truncate this one.
        if i + 1 < len(nav_entries):
            next_start_page = nav_entries[i + 1][2]
            if page_0idx == next_start_page:
                # This entry and the next one share the SAME START PAGE.
                # We must truncate THIS entry before the next one's heading.
                # Usually happens for Treatise title pages that are followed immediately by Chapter 1.
                if is_treatise:
                    raw_text = _keep_only_prerendered_treatise_title_page(raw_text)
                
                # Find all markers
                markers = list(re.finditer(r'\[\[(?:PART|CHAPTER|DIGRESSION|ROMAN_HEAD|SUBTITLE|SUMMARY)\]\]\s*([^\n]*)', raw_text))
                if len(markers) > 1:
                    # Find the first 'major' marker after the initial one to truncate at.
                    # If current is PART/TREATISE, we stop at the next CHAPTER or PART.
                    truncate_at = len(raw_text)
                    next_title_norm = re.sub(r'[^A-Z0-9]+', ' ', nav_entries[i + 1][1].upper()).strip()
                    for m in markers[1:]:
                        marker_token = re.match(r'\[\[([A-Z_]+)\]\]', m.group(0)).group(1)
                        marker_text_norm = re.sub(r'[^A-Z0-9]+', ' ', (m.group(1) or '').upper()).strip()
                        matches_next_title = bool(
                            marker_text_norm
                            and next_title_norm
                            and (next_title_norm in marker_text_norm or marker_text_norm in next_title_norm)
                        )
                        if marker_token in ('PART', 'CHAPTER', 'DIGRESSION') or matches_next_title:
                            truncate_at = m.start()
                            break
                    raw_text = raw_text[:truncate_at].strip()
            elif end_page == next_start_page - 1:
                # We need to check the actual start page of the next entry.
                # If it has content before the heading, it belongs here.
                next_page_raw = get_merged_page_text(doc, pages_md, next_start_page)
                marker = re.search(r'\[\[(?:PART|CHAPTER|DIGRESSION|ROMAN_HEAD|SUBTITLE|SUMMARY)\]\]', next_page_raw)
                if marker:
                    pre_heading = next_page_raw[:marker.start()].strip()
                    if pre_heading:
                        # Only join if it doesn't look like a standalone title (Issue 99/11)
                        # and if the current text didn't end with a signature
                        if (len(pre_heading) > 40 or not pre_heading.isupper()) and \
                           not re.search(r'_\*\*J\.O\.\*\*|_August_ 18\d{2}', raw_text):
                            raw_text = raw_text + "\n\n" + pre_heading
        
        if not raw_text.strip():
            continue
        
        cid_counter += 1
        cid = f'ch{cid_counter:03d}'
        
        display_title = title_case(title) if not is_treatise else title
        if not is_treatise and current_treatise:
            # Differentiate Prefatory Notes and Prefaces
            # Match titles like "Prefatory Note", "Preface", "The Preface", "To the Reader"
            normalized_title = title.strip().rstrip('.').upper()
            if any(kw in normalized_title for kw in {
                'PREFATORY NOTE', 'PREFACE', 'TO THE READER'
            }):
                # Keep it concise: "Prefatory Note (Treatise Name)"
                # Extract the base name (e.g. "THE PREFACE" -> "Preface")
                base = "Prefatory Note" if "PREFATORY" in normalized_title else \
                       "Preface" if "PREFACE" in normalized_title else \
                       "To the Reader"
                display_title = f"{base} ({current_treatise})"

        chap = Chapter(
            cid=cid,
            title=display_title,
            level=level,
            raw_text=raw_text,
            page_start=page_0idx,
            page_end=end_page,
            is_treatise=is_treatise,
        )
        chapters.append(chap)

        if progress_callback:
            progress_callback(i + 1, len(nav_entries),
                              f"[extract] Volume {vol_num}")

    return chapters



