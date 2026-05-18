from scripts.audit_text_integrity import greek_hebrew_clause_fidelity
from extract import convert_span_text, page_has_special_fonts


def test_koine_subset_font_names_are_converted():
    converted = convert_span_text("uJpo>stativ", "ABCDEE+Koine-Regular")

    assert "ὑπόστατις" in converted


def test_unicode_greek_page_uses_font_aware_path():
    page = type(
        "FakePage",
        (),
        {
            "get_text": lambda self, kind: {
                "blocks": [
                    {
                        "type": 0,
                        "lines": [
                            {
                                "spans": [
                                    {
                                        "text": "ordinary text with ὑπόστατις",
                                        "font": "TimesNewRomanPSMT",
                                    }
                                ]
                            }
                        ],
                    }
                ]
            }
        },
    )()

    assert page_has_special_fonts(page) == "greek"


def test_greek_clause_audit_does_not_join_across_english_prose():
    pdf_page = (
        "ἀλφα βητα γαμμα δελτα εψιλον "
        "English prose separates these quotations. "
        "ζητα ητα θητα ιωτα καππα"
    )
    epub_text = pdf_page

    result = greek_hebrew_clause_fidelity([pdf_page], epub_text)

    assert result["greek_clauses_checked"] == 2
    assert result["missing_greek_clause_count"] == 0
