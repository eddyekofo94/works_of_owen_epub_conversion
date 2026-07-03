from scripts.modern_notes import (
    _anchorable_citation_phrase,
    apply_modern_body_notes,
    sanitize_note_html,
)


def test_modern_notes_reject_fragment_only_citation_anchors():
    assert not _anchorable_citation_phrase("cap. 11.")
    assert not _anchorable_citation_phrase("(Tract. 1:)")
    assert not _anchorable_citation_phrase("2 Epist. 1:21")
    assert _anchorable_citation_phrase("Aquin. 22 q. 81, a. 3, ad prim.")


def test_modern_notes_strip_unknown_source_claims():
    note = (
        "<strong>Modern Translation:</strong> not in the little flowers of words, "
        "but in the weight of things. (Unknown, <em>Unknown Work</em>, Unknown Location)"
    )

    cleaned = sanitize_note_html(note)

    assert "Unknown Work" not in cleaned
    assert "Unknown Location" not in cleaned
    assert "weight of things" in cleaned


def test_manifest_body_notes_use_distinct_symbols_after_punctuation():
    manifest = {
        "items": [{
            "id": "m1",
            "scope": "body",
            "chapter": "Chapter 1",
            "action": "citation_popup",
            "confidence": "high",
            "exact_text": "Aquin. 22 q. 81, a. 3, ad prim.",
            "note_html": "<strong>Modern Citation:</strong> Thomas Aquinas, <em>Summa Theologiae</em>, II-II q. 81 a. 3 ad 1.",
        }]
    }
    html = "<p>Aquin. 22 q. 81, a. 3, ad prim.</p>"

    updated, notes, counter = apply_modern_body_notes(html, "Chapter 1", "ch001", manifest, 0)

    assert 'href="endnotes.xhtml#fnmodern_ch001_1"' in updated
    assert 'prim.<a class="noteref noteref-citation"' in updated
    assert "<sup>◇</sup>" in updated
    assert notes[0]["type"] == "citation"
    assert counter == 1


def test_overlapping_modern_reference_candidates_keep_longest_match_only():
    long_phrase = (
        "Orat. 5 con. Arian., and Epist. ad African. Basil denied them so "
        "to be, or that they were used unto the same purpose in the Council "
        "of Nice: Epist. 78."
    )
    manifest = {
        "items": [
            {
                "id": "long",
                "scope": "body",
                "chapter": "Preface",
                "action": "citation_popup",
                "confidence": "high",
                "exact_text": long_phrase,
                "note_html": "<strong>Modern Citation:</strong> Athanasius and Basil.",
            },
            {
                "id": "short",
                "scope": "body",
                "chapter": "Preface",
                "action": "citation_popup",
                "confidence": "high",
                "exact_text": "Council of Nice: Epist. 78.",
                "note_html": "<strong>Modern Citation:</strong> Basil, <em>Epistles</em>, Epistle 78.",
            },
            {
                "id": "shorter",
                "scope": "body",
                "chapter": "Preface",
                "action": "citation_popup",
                "confidence": "high",
                "exact_text": "Epist. 78",
                "note_html": "<strong>Modern Citation:</strong> Basil, Epistle 78.",
            },
        ]
    }
    html = f"<p>{long_phrase} The like difference followed.</p>"

    updated, notes, counter = apply_modern_body_notes(html, "Preface", "ch004", manifest, 0)

    assert updated.count('noteref-citation') == 1
    assert updated.count("<sup>◇</sup>") == 1
    assert notes == [{
        "id": "fnmodern_ch004_1",
        "num": 1,
        "phrase": long_phrase,
        "translation": "<strong>Modern Citation:</strong> Athanasius and Basil.",
        "type": "citation",
        "manifest_id": "long",
    }]
    assert counter == 1
