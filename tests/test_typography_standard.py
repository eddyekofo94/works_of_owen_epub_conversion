"""Regression coverage for the universal EPUB typography standard."""

import re
from types import SimpleNamespace

from ebooklib import epub

from shared import EPUB_STYLESHEET, generate_font_styles


def _rule(selector: str) -> str:
    match = re.search(rf"{selector}\s*\{{(?P<body>.*?)\}}", EPUB_STYLESHEET, re.S)
    assert match, f"Missing CSS rule for {selector}"
    return match.group("body")


def test_body_and_bare_paragraphs_leave_base_font_size_to_reader():
    body_rule = _rule(r"body")
    paragraph_rule = _rule(r"p")

    assert "font-size" not in body_rule
    assert "font-size" not in paragraph_rule
    assert "text-align: justify" in body_rule
    assert "text-align: justify" in paragraph_rule
    assert "-webkit-hyphens: auto" in body_rule
    assert "hyphens: auto" in paragraph_rule
    assert "line-height: 1.4" in body_rule
    assert "line-height: 1.4" in paragraph_rule


def test_greek_uses_one_subtle_reader_relative_size():
    greek_sizes = re.findall(
        r'\[lang="el"\][^{]*\{[^}]*font-size:\s*([^;]+);',
        EPUB_STYLESHEET,
        re.S,
    )
    assert greek_sizes == ["1.03em"]


def test_noteref_and_sup_use_inline_popup_safe_positioning():
    anchor_rule = _rule(r'a\.noteref, a\[epub\\:type="noteref"\]')
    sup_rule = _rule(r'a\.noteref sup, a\[epub\\:type="noteref"\] sup')

    assert "display: inline !important" in anchor_rule
    assert "inline-block" not in anchor_rule
    assert "color: #2a55a0 !important" in anchor_rule
    assert "display: inline !important" in sup_rule
    assert "font-size: 0.75rem !important" in sup_rule
    assert "top: -0.32em !important" in sup_rule
    assert "line-height: 0 !important" in sup_rule


def test_citation_marker_uses_information_symbol_not_asterisk():
    from render import build_endnotes_chapter

    html = build_endnotes_chapter(
        {},
        vol_num=1,
        trans_notes=[{
            "id": "fntrans_test_1",
            "phrase": "Comment. in Psalm 66:",
            "translation": "<strong>Modern Citation:</strong> Jerome, <em>Commentary on the Psalms</em>.",
            "type": "citation",
        }],
    )

    assert '<span class="fn-link">◇</span>' in html
    assert '<span class="fn-link">*</span>' not in html


def test_inline_translation_injection_is_disabled():
    from render import apply_inline_translations

    body = '<p><span lang="la" xml:lang="la">hostis Bupalo</span>.</p>'

    assert apply_inline_translations(body) == body
    assert "[Translated:" not in apply_inline_translations(body)


def test_legacy_body_translation_notes_default_off():
    from render import body_translation_notes_enabled

    assert not body_translation_notes_enabled()
    assert not body_translation_notes_enabled({})
    assert not body_translation_notes_enabled({"unrelated": True})
    assert body_translation_notes_enabled({"enable_body_translation_notes": True})


def test_citation_anchor_rejects_truncated_latin_quote_key():
    from render import _body_translation_anchor_is_safe
    from scripts.translation_db import BODY_TRANSLATIONS

    bad_leo_key = (
        '"Quia in Christo Jesus Filio Dei non solum ad divinam essentiam, '
        'sed etiam ad humanan spectat naturam, quo dictum est per prophetam '
        "—'generationem ejus quis enarrabit?' — (utramque enim substantiam "
        'in unam convenisse personam, nisi fides credat, sermo non explicat; '
        'et ideo materia nunquam deficit laudis; qui'
    )
    body = (
        '<p><span lang="la" xml:lang="la">'
        f'{bad_leo_key} nunquam sufficit copia laudatoris'
        '</span></p>'
    )
    orig_end = body.index(' nunquam')

    assert bad_leo_key not in BODY_TRANSLATIONS
    assert not _body_translation_anchor_is_safe('citation', bad_leo_key, body, orig_end)


def test_citation_anchor_rejects_source_title_continuation():
    from render import _body_translation_anchor_is_safe
    from scripts.patristic_refs import _citation_tail_continues_source_title
    from scripts.translation_db import BODY_TRANSLATIONS

    body = '<p>Cyril. Alexand., lib. 5 cap. 6, lib. 1. De Fide ad Regin.;</p>'
    orig_end = body.index(' Fide')

    assert not _body_translation_anchor_is_safe('citation', 'lib. 1. De', body, orig_end)
    assert _citation_tail_continues_source_title(body, body.index('De'))
    assert (
        'Irenaeus, lib. 3, cap. 20, 21; Eusebius, Demonst. Evangel., '
        'lib. 4 cap. 1-4, etc.; Cyril. Alexand., lib. 5 cap. 6, lib. 1. De'
    ) not in BODY_TRANSLATIONS
    assert (
        'Rupertus, lib. 3, De Gloria et Honore Filii Hominis; '
        'Albertus Magnus, in 3 distinct. 10'
    ) not in BODY_TRANSLATIONS


def test_patristic_citation_regex_keeps_numeric_ranges_together():
    from scripts.patristic_refs import PATRISTIC_CITATION_RE

    text = 'Augustine, De Trinit., lib. 13 cap. 13-20; Leo follows.'
    match = PATRISTIC_CITATION_RE.search(text)

    assert match
    assert match.group(0) == 'lib. 13 cap. 13-20'


def test_footnote_classes_are_justified_hyphenated_and_reader_sized():
    footnote_rule = _rule(r"\.footnote")
    translation_rule = _rule(r"\.footnote-modern-translation")

    for rule in (footnote_rule, translation_rule):
        assert "font-size: 1.0em !important" in rule
        assert "line-height: 1.30 !important" in rule
        assert "text-align: justify !important" in rule
        assert "-webkit-hyphens: auto !important" in rule
        assert "hyphens: auto !important" in rule
        assert "text-indent: 0 !important" in rule


def test_primary_font_is_injected_into_both_popup_paragraph_classes():
    css = generate_font_styles("Test Primary", {}, "Test Heading", {})
    assert "body, div, p, span, .footnote, .footnote-modern-translation" in css
    assert 'font-family: "Test Primary", "SBL BibLit", serif !important' in css
    assert not re.search(r'\[lang="el"\][^{]*\{[^}]*font-size:', css, re.S)


def test_enriched_footnote_translation_has_inline_apple_books_line_height():
    from render import build_endnotes_chapter

    footnotes = {5: SimpleNamespace(fnum=5, text="Original editorial note.")}
    html = build_endnotes_chapter(footnotes, vol_num=1)

    assert '<p class="footnote" style="line-height: 1.30 !important;">' in html
    assert (
        '<p class="footnote-modern-translation" '
        'style="line-height: 1.30 !important;">'
    ) in html
    assert "Modern Citation:" in html


def test_every_declared_font_file_is_added_to_epub_package():
    from render import embed_fonts_and_stylesheet

    book = epub.EpubBook()
    style_item, _ = embed_fonts_and_stylesheet(
        book,
        1,
        {
            "body_font": "adobe-garamond-pro",
            "heading_font": "proxima-nova",
            "secondary_languages": ["el", "he"],
        },
    )
    css = style_item.get_content().decode("utf-8")
    declared = {name.rsplit("/", 1)[-1] for name in re.findall(r'url\("\.\./Fonts/([^"?]+)"\)', css)}
    packaged = {
        item.get_name().rsplit("/", 1)[-1]
        for item in book.get_items()
        if item.get_name().startswith("Fonts/")
    }

    assert declared <= packaged, f"CSS references unpackaged fonts: {sorted(declared - packaged)}"
    assert "GFSPorson.ttf" not in declared
    assert "Proxima Nova Light.ttf" not in declared
    assert "Proxima Nova Semibold.ttf" not in declared
