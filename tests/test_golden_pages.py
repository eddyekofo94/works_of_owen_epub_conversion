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


def _requested_volumes() -> list[str] | None:
    """Return the subset of volumes requested via OWEN_REGRESSION_VOLUMES.

    Returns None to signal "all volumes" (the default when the env var is unset
    or set to 'all'), matching the convention used elsewhere in the test suite.
    """
    raw = os.environ.get("OWEN_REGRESSION_VOLUMES", "all").strip()
    if raw.lower() == "all":
        return None
    return [p for p in raw.replace(",", " ").split() if p.strip()]


def load_golden_pages():
    with open(GOLDEN_PAGES_JSON, "r") as f:
        data = json.load(f)
    vols = _requested_volumes()
    if vols is not None:
        data = {k: v for k, v in data.items() if k in vols}
    return data

@pytest.mark.parametrize("vol_num,pages", load_golden_pages().items())
def test_golden_pages(vol_num, pages):
    if str(vol_num).lower().startswith('h'):
        pytest.skip("Hebrews volumes do not have source PDFs for golden page checks.")
        
    from shared import get_volume_dir
    vol_dir = get_volume_dir(vol_num)
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
    """Verify that get_pages_text correctly heals a cross-page paragraph break.

    Pages 7–8 of Volume 1 are a good test case: the General Preface runs
    across the page boundary and the paragraph must be joined.  The default
    healer_mode=True behaviour is tested here.
    """
    vols = _requested_volumes()
    if vols is not None and "1" not in vols:
        pytest.skip("Volume 1 not in OWEN_REGRESSION_VOLUMES")
    vol_num = "1"
    from shared import get_volume_dir
    vol_dir = get_volume_dir(vol_num)
    pdf_path = vol_dir / "input" / f"owen-v{vol_num}.pdf"

    if not pdf_path.exists():
        pytest.skip(f"PDF for volume {vol_num} not found")

    doc = fitz.open(pdf_path)

    pages_md = pymupdf4llm.to_markdown(
        str(pdf_path),
        pages=[6, 7],
        page_chunks=True,
        show_progress=False,
    )

    # get_pages_text expects pages_md indexed by global page index
    mock_pages_md = [None] * 8
    mock_pages_md[6] = pages_md[0]
    mock_pages_md[7] = pages_md[1]

    # healer_mode=True is the default; call without it to test default behaviour
    extracted_text = get_pages_text(doc, mock_pages_md, 6, 7)

    baseline_path = BASELINES_DIR / f"v{vol_num}_p7-8_healed.txt"

    if os.environ.get("GOLDEN_GENERATE") == "1":
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        with open(baseline_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        return

    if not baseline_path.exists():
        pytest.fail(
            f"Baseline missing for v1 p7-8 healed.\n"
            f"Run:  GOLDEN_GENERATE=1 pytest tests/test_golden_pages.py::"
            f"test_page_continuation_healing\n"
            f"to generate it."
        )

    with open(baseline_path, "r", encoding="utf-8") as f:
        expected_text = f.read()

    assert extracted_text == expected_text, "Healed extraction mismatch for v1 pages 7-8"
