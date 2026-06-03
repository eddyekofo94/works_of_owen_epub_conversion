#!/usr/bin/env python3
"""Unit tests for the Text Integrity & Anomaly Auditor."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.audit_anomalies import (
    load_dictionary,
    check_hyphenations,
    check_punctuation,
    check_ocr_residues,
    check_capitalization,
    check_unresolved_citations,
    check_structural_nesting
)

def test_dictionary_loading():
    """Verify that the system dictionary loads and includes extra theological/Puritan terms."""
    words = load_dictionary()
    assert len(words) > 100
    assert "hath" in words
    assert "unto" in words
    assert "socinian" in words
    assert "petavius" in words


def test_check_hyphenations():
    """Verify that bad hyphenations are caught while whitelisted ones are ignored."""
    words_dict = load_dictionary()
    
    # 1. Catch bad splits
    anomalies = check_hyphenations("The learned Calvin-ist said prayers.", words_dict)
    assert len(anomalies) > 0
    assert any(a[0] == "Calvin-ist" for a in anomalies)
    
    # 2. Catch splittable words that rejoin perfectly
    anomalies2 = check_hyphenations("This is a beautiful fire-place for him.", words_dict)
    assert len(anomalies2) > 0
    assert any("fire-place" in a[0] for a in anomalies2)
    
    # 3. Whitelisted words must NOT be flagged
    anomalies3 = check_hyphenations("Owen practiced self-denial daily.", words_dict)
    # Check that self-denial is ignored
    assert not any(a[0] == "self-denial" for a in anomalies3)


def test_check_punctuation():
    """Verify that spaced punctuation and duplicate symbols are flagged."""
    # 1. Spaced punctuation
    anomalies1 = check_punctuation("God is good , let us praise him .")
    assert len(anomalies1) >= 2
    assert any("good ," in a[0] for a in anomalies1)
    assert any("him ." in a[0] for a in anomalies1)
    
    # 2. Duplicate punctuation
    anomalies2 = check_punctuation("This is a mistake,, indeed;;")
    assert len(anomalies2) >= 2
    assert any(",," in a[0] for a in anomalies2)
    assert any(";;" in a[0] for a in anomalies2)


def test_check_ocr_residues():
    """Verify that OCR artifacts like brackets inside words are caught."""
    # 1. Stray brackets inside word
    anomalies1 = check_ocr_residues("This is on]y a test of the system.")
    assert len(anomalies1) == 1
    assert anomalies1[0][0] == "on]y"
    
    # 2. Mixed alphanumeric words
    anomalies2 = check_ocr_residues("Our sins are w1th Christ.")
    assert len(anomalies2) == 1
    assert anomalies2[0][0] == "w1th"


def test_check_capitalization():
    """Verify that mixed-casing errors are flagged."""
    anomalies = check_capitalization("Our loRd and saVior Jesus ChriSt with iraFated sins.")
    assert len(anomalies) >= 3
    assert any("loRd" in a[0] for a in anomalies)
    assert any("saVior" in a[0] for a in anomalies)
    assert any("ChriSt" in a[0] for a in anomalies)
    assert any("iraFated" in a[0] for a in anomalies)


def test_check_unresolved_citations():
    """Verify that unresolved patristic citations are caught."""
    # A patristic citation pattern with no known author context, making it unresolved
    anomalies = check_unresolved_citations("Some random text. lib. 1 said this.", "ch001")
    assert len(anomalies) == 1
    assert "lib. 1" in anomalies[0][0]


def test_check_structural_nesting():
    """Verify that jumps in outline listing sequences are caught."""
    # A numbered list skipping a number: 1. then 3. close together
    sample_text = "Here is 1. First item. And here is 3. Third item."
    anomalies = check_structural_nesting(sample_text)
    assert len(anomalies) == 1
    assert "List sequence jump" in anomalies[0][1]
    assert "1. ... 3." in anomalies[0][0]

