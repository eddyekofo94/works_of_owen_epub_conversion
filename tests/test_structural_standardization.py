import pytest
import re
from converter import markdown_to_html, reconstruct_paragraphs

def test_structural_tokens_preserve_hierarchy():
    """Verify that [[PART]] and [[CHAPTER]] tokens are correctly converted and preserved."""
    # Input must be separated by double newlines for markdown_to_html
    md = "[[PART]] PART 1.\n\n[[CHAPTER]] CHAPTER 1.\n\n[[SUMMARY]] This is a summary.\n\nThis is body text."
    
    # 1. Test HTML conversion
    html, _, _ = markdown_to_html(md)
    assert '<h1 class="primary"' in html
    assert 'PART 1.' in html
    assert '<h1 class="secondary">CHAPTER 1.</h1>' in html
    assert '<p class="chapter-summary">This is a summary.</p>' in html
    # First body paragraph of Chapter 1 gets the drop cap (triggered by PART)
    assert '<p class="chapter-opening">This is body text.</p>' in html

def test_drop_cap_constraint():
    """Verify that drop caps only apply to paragraphs immediately following a PART heading."""
    
    # Case A: PART heading present
    md_part = "[[PART]] PART 1\n\n[[CHAPTER]] CHAPTER 1\n\nFirst paragraph of chapter 1."
    html_part, _, _ = markdown_to_html(md_part)
    assert 'class="chapter-opening"' in html_part
    
    # Case B: Standard Chapter (No PART)
    md_ch2 = "[[CHAPTER]] CHAPTER 2\n\nFirst paragraph of chapter 2."
    html_ch2, _, _ = markdown_to_html(md_ch2)
    assert 'class="chapter-opening"' not in html_ch2
    
    # Case C: Sub-point in any chapter
    md_real = "[[PART]] PART 1\n\nFirst paragraph.\n\n(2.) Sub-point paragraph."
    html_real, _, _ = markdown_to_html(md_real)
    assert 'class="chapter-opening">First paragraph.' in html_real
    assert 'class="chapter-opening">(2.)' not in html_real

def test_front_matter_states():
    """Verify FRONT_MATTER state logic."""
    md = "ANALYSIS.\n\nThis is editorial note."
    html, mode, _ = markdown_to_html(md)
    assert mode == "FRONT_MATTER"
    assert 'class="front-matter-title">ANALYSIS.</h3>' in html
    assert 'class="front-matter-body">This is editorial note.</p>' in html
    assert 'class="chapter-opening"' not in html

def test_greek_artifact_stripping():
    """Verify that 'j' noise is stripped."""
    from shared import clean_greek_text
    
    raw = "j Εγὼ τὴν ἀλήθειαν λέγω"
    cleaned = clean_greek_text(raw)
    assert "j" not in cleaned
    assert "Εγὼ" in cleaned
