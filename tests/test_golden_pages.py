import os
import json
import pytest
import fitz
import pymupdf4llm
from pathlib import Path
from converter import get_merged_page_text, get_pages_text

# Path setup
BASE_DIR = Path(__file__).parent.parent
GOLDEN_PAGES_JSON = BASE_DIR / "qa" / "golden_pages.json"
BASELINES_DIR = BASE_DIR / "tests" / "baselines"

def load_golden_pages():
    with open(GOLDEN_PAGES_JSON, "r") as f:
        return json.load(f)

@pytest.mark.parametrize("vol_num,pages", load_golden_pages().items())
def test_golden_pages(vol_num, pages):
    vol_dir = BASE_DIR / "volumes" / f"v{vol_num}"
    pdf_path = vol_dir / "input" / f"owen-v{vol_num}.pdf"
    
    if not pdf_path.exists():
        pytest.skip(f"PDF for volume {vol_num} not found at {pdf_path}")

    doc = fitz.open(pdf_path)
    
    # We only need the markdown for the specific pages to be fast
    # but pymupdf4llm.to_markdown with pages=[] is not always reliable in older versions
    # so we'll just extract what we need.
    
    for entry in pages:
        page_idx = entry["page"] - 1 # 0-indexed internally
        
        # Get pages_md for just this page
        pages_md = pymupdf4llm.to_markdown(
            str(pdf_path),
            pages=[page_idx],
            page_chunks=True,
            show_progress=False
        )
        
        # In to_markdown(pages=[idx]), the result pages_md will have 1 element at index 0
        # BUT our converter expect pages_md to be indexed by global page_idx.
        # So we mock a sparse list or a dict if needed.
        # Actually, let's just make it a list where index 0 is our page.
        # But get_merged_page_text uses page_idx. 
        # Let's create a dummy list of the correct length.
        mock_pages_md = [None] * (page_idx + 1)
        mock_pages_md[page_idx] = pages_md[0]

        # Extract text using converter logic
        # Most golden pages check single page extraction
        extracted_text = get_merged_page_text(doc, mock_pages_md, page_idx)
        
        baseline_path = BASELINES_DIR / f"v{vol_num}_p{entry['page']}.txt"
        
        if os.environ.get("GOLDEN_GENERATE") == "1":
            with open(baseline_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            continue

        if not baseline_path.exists():
            pytest.fail(f"Baseline missing for v{vol_num} page {entry['page']}. Run with GOLDEN_GENERATE=1 to create it.")
        
        with open(baseline_path, "r", encoding="utf-8") as f:
            expected_text = f.read()
        
        assert extracted_text == expected_text, f"Extraction mismatch for v{vol_num} page {entry['page']}"

def test_page_continuation_healing():
    # Specific test for v1 pages 7-8 continuation
    vol_num = "1"
    vol_dir = BASE_DIR / "volumes" / f"v{vol_num}"
    pdf_path = vol_dir / "input" / f"owen-v{vol_num}.pdf"
    
    if not pdf_path.exists():
        pytest.skip(f"PDF for volume {vol_num} not found")

    doc = fitz.open(pdf_path)
    start_page = 6 # page 7 (0-indexed)
    end_page = 7   # page 8 (0-indexed)
    
    pages_md = pymupdf4llm.to_markdown(
        str(pdf_path),
        pages=[6, 7],
        page_chunks=True,
        show_progress=False
    )
    
    # Mock pages_md for get_pages_text
    mock_pages_md = [None] * 8
    mock_pages_md[6] = pages_md[0]
    mock_pages_md[7] = pages_md[1]
    
    extracted_text = get_pages_text(doc, mock_pages_md, 6, 7, healer_mode=True)
    
    baseline_path = BASELINES_DIR / f"v{vol_num}_p7-8_healed.txt"
    
    if os.environ.get("GOLDEN_GENERATE") == "1":
        with open(baseline_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        return

    if not baseline_path.exists():
        pytest.fail(f"Baseline missing for v1 p7-8 healed. Run with GOLDEN_GENERATE=1 to create it.")
        
    with open(baseline_path, "r", encoding="utf-8") as f:
        expected_text = f.read()
        
    assert extracted_text == expected_text, "Healed extraction mismatch for v1 pages 7-8"
