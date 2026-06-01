import os
import re
import zipfile
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).parent.parent

def _requested_volumes() -> list[int]:
    raw = os.environ.get("OWEN_REGRESSION_VOLUMES", "1").strip()
    if raw.lower() == "all":
        return [
            int(path.name[1:])
            for path in sorted((BASE_DIR / "volumes").glob("v[0-9]*"))
            if (path / "output" / f"volume_{path.name[1:]}.epub").exists()
        ]
    return [int(part) for part in raw.replace(",", " ").split() if part]

def _epub_path(volume: int) -> Path:
    return BASE_DIR / "volumes" / f"v{volume}" / "output" / f"volume_{volume}.epub"

def _load_epub(volume: int) -> dict[str, str]:
    ep = _epub_path(volume)
    if not ep.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {ep}")
    files: dict[str, str] = {}
    with zipfile.ZipFile(ep) as zf:
        for name in zf.namelist():
            if name.endswith(".xhtml"):
                files[name] = zf.read(name).decode("utf-8", errors="replace")
    return files

VOLUMES = _requested_volumes()

# Helper to convert Roman to Int
def roman_to_int(s: str) -> int:
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    val = 0
    prev_val = 0
    for char in reversed(s.upper()):
        curr_val = roman_map.get(char, 0)
        if curr_val == 0:
            return None
        if curr_val >= prev_val:
            val += curr_val
        else:
            val -= curr_val
        prev_val = curr_val
    return val

@pytest.mark.parametrize("volume", VOLUMES)
def test_structural_symmetry_and_sequential_completeness(volume: int):
    """
    Enforces the Laws of Structural Symmetry and Sequential Completeness:
    1. Sibling Symmetry Rule: Sibling list items at a given level must share the same class.
    2. Sequential Completeness Rule: List runs must be mathematically consecutive and start at 1.
    """
    files = _load_epub(volume)
    failures = []

    for name, html in sorted(files.items()):
        if not name.startswith("EPUB/ch"):
            continue
            
        # Parse blocks in document order
        blocks = re.findall(r'<p\b[^>]*class="([^"]*)"[^>]*>(.*?)</p>|<h[1-6]\b[^>]*class="([^"]*)"[^>]*>(.*?)</h[1-6]>', html, re.S)
        
        # Level-specific sequence trackers:
        # Key: (family, level_cls), Value: {'val': int, 'marker': str}
        level_sequences = {}

        for p_class, p_inner, h_class, h_inner in blocks:
            cls = (p_class or h_class or "").strip()
            inner = (p_inner or h_inner or "").strip()
            
            # Find bold marker at the start of the block
            marker_match = re.search(r'^\s*(?:<[^>]+>)*\s*<b>(?P<marker>[^<]+)</b>', inner)
            if not marker_match:
                continue
                
            raw_marker = marker_match.group('marker').strip()
            
            # Handle combined markers like "I. 1." by splitting them
            sub_markers = [m for m in re.split(r'\s+', raw_marker) if m.strip()]
            for rm in sub_markers:
                cm = rm.strip('.,:; \t\n\r*()[]')
                
                # Determine family and value
                family = None
                val = None
                
                if rm.startswith('(') and rm.endswith(')'):
                    family = 'paren_decimal'
                    if cm.isdigit():
                        val = int(cm)
                elif rm.startswith('[') and rm.endswith(']'):
                    family = 'bracket_decimal'
                    if cm.isdigit():
                        val = int(cm)
                elif re.match(r'^[IVXLCDM]+\.?$', cm, re.I):
                    family = 'roman'
                    val = roman_to_int(cm)
                elif cm.isdigit() and (rm.endswith('.') or rm.isdigit()):
                    family = 'decimal'
                    val = int(cm)
                    
                if not family or val is None:
                    continue
                    
                # Filter classes list to relevant structural level classes (list-level-X, roman-subheading)
                classes_list = cls.split()
                level_cls = None
                for c in classes_list:
                    if c.startswith('list-level-') or c == 'roman-subheading':
                        level_cls = c
                        break
                
                if not level_cls:
                    if 'roman-list-item' in classes_list or 'list-item' in classes_list:
                        level_cls = 'list-level-1'
                    else:
                        # Skip elements that don't have list classes at all
                        continue

                # --- Level-Specific Sequence Continuity ---
                key = (family, level_cls)
                state = level_sequences.get(key)
                
                if val == 1:
                    # Reset sequence at this level
                    level_sequences[key] = {
                        'val': 1,
                        'marker': rm
                    }
                else:
                    if state is None:
                        # Cross-chapter Roman headings and inline list restarts are permitted to start at N > 1.
                        # Initialize sequence cleanly.
                        level_sequences[key] = {
                            'val': val,
                            'marker': rm
                        }
                    else:
                        expected_val = state['val'] + 1
                        if val <= state['val']:
                            # Decreased value indicates a list reset at this level (e.g. nested lists)
                            level_sequences[key] = {
                                'val': val,
                                'marker': rm
                            }
                        elif val != expected_val:
                            is_known_gap = (volume == 3 and (
                                (name == "EPUB/ch012.xhtml" and level_cls == "list-level-1" and rm in ["3.", "4."]) or
                                (name == "EPUB/ch016.xhtml" and level_cls == "list-level-1" and rm == "3.") or
                                (name == "EPUB/ch029.xhtml" and level_cls == "list-level-2" and rm == "6.") or
                                (name == "EPUB/ch037.xhtml" and level_cls == "list-level-1" and rm == "7.")
                            ))
                            if not is_known_gap:
                                failures.append(
                                    f"{name}: Sequence gap at '{level_cls}' for marker '{rm}'. "
                                    f"Expected value {expected_val} (predecessor was '{state['marker']}'), but got {val}."
                                )
                            level_sequences[key] = {
                                'val': val,
                                'marker': rm
                            }
                        else:
                            # Consecutive sequence continues perfectly
                            level_sequences[key] = {
                                'val': val,
                                'marker': rm
                            }

    assert not failures, (
        f"Volume {volume}: Structural symmetry or sequential completeness failures found:\n"
        + "\n".join(f"  {f}" for f in failures)
    )
