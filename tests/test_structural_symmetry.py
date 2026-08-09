import os
import re
import zipfile
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.parent


def _requested_volumes() -> list[str]:
    raw = os.environ.get("OWEN_REGRESSION_VOLUMES", "1").strip()
    if raw.lower() == "all":
        vols = []
        for path in sorted((BASE_DIR / "volumes").glob("v[0-9]*")):
            v_num = path.name[1:]
            if (path / "output" / f"volume_{v_num}.epub").exists():
                vols.append(v_num)
        for path in sorted((BASE_DIR / "volumes").glob("h[0-9]*")):
            v_num = path.name
            if (path / "output" / f"volume_{v_num}.epub").exists():
                vols.append(v_num)
        return vols
    return [part for part in raw.replace(",", " ").split() if part]


def _epub_path(volume: str) -> Path:
    from shared import get_volume_dir

    volume_dir = get_volume_dir(volume)
    return volume_dir / "output" / f"volume_{volume}.epub"


def _load_epub(volume: str) -> dict[str, str]:
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


def roman_to_int(s: str) -> int | None:
    roman_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
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


def _marker_parts(raw_marker: str) -> list[tuple[str, int, str]]:
    parts = []
    for rm in [m for m in re.split(r"\s+", raw_marker.strip()) if m.strip()]:
        cm = rm.strip(".,:; \t\n\r*()[]")
        family = None
        val = None
        if rm.startswith("(") and rm.endswith(")") and cm.isdigit():
            family = "paren_decimal"
            val = int(cm)
        elif rm.startswith("[") and rm.endswith("]") and cm.isdigit():
            family = "bracket_decimal"
            val = int(cm)
        elif re.match(r"^[IVXLCDM]+\.?$", cm, re.I):
            family = "roman"
            val = roman_to_int(cm)
        elif cm.isdigit() and (rm.endswith(".") or rm.isdigit()):
            family = "decimal"
            val = int(cm)
        if family and val is not None:
            parts.append((family, val, rm))
    return parts


def _structural_level(cls: str) -> str | None:
    classes = cls.split()
    for item in classes:
        if item.startswith("list-level-") or item == "roman-subheading":
            return item
    if "roman-list-item" in classes or "list-item" in classes:
        return "list-level-1"
    return None


def _is_known_gap(volume, name: str, level_cls: str, rm: str) -> bool:
    known = {
        3: {
            ("EPUB/ch012.xhtml", "list-level-1", "3."),
            ("EPUB/ch012.xhtml", "list-level-1", "4."),
            ("EPUB/ch016.xhtml", "list-level-1", "3."),
            ("EPUB/ch016.xhtml", "list-level-1", "5."),
            ("EPUB/ch027.xhtml", "list-level-1", "3."),
            ("EPUB/ch028.xhtml", "list-level-1", "3."),
            ("EPUB/ch029.xhtml", "list-level-1", "4."),
            ("EPUB/ch029.xhtml", "list-level-2", "6."),
            ("EPUB/ch037.xhtml", "list-level-1", "7."),
        },
        6: {
            ("EPUB/ch074.xhtml", "roman-subheading", "III."),
            ("EPUB/ch025.xhtml", "list-level-2", "(4.)"),
            ("EPUB/ch047.xhtml", "list-level-2", "[4.]"),
            ("EPUB/ch063.xhtml", "list-level-2", "(4.)"),
            ("EPUB/ch071.xhtml", "list-level-1", "3."),
        },
        7: {
            ("EPUB/ch003.xhtml", "list-level-1", "VIII."),
            ("EPUB/ch005.xhtml", "list-level-1", "III."),
            ("EPUB/ch016.xhtml", "list-level-1", "3."),
            ("EPUB/ch022.xhtml", "list-level-1", "XIX."),
            ("EPUB/ch039.xhtml", "list-level-1", "3."),
            ("EPUB/ch039.xhtml", "list-level-1", "5."),
            ("EPUB/ch040.xhtml", "list-level-1", "4."),
            ("EPUB/ch049.xhtml", "list-level-1", "V."),
            ("EPUB/ch055.xhtml", "list-level-1", "3."),
            ("EPUB/ch056.xhtml", "list-level-1", "5."),
        },
        8: {
            ("EPUB/ch015.xhtml", "list-level-1", "5."),
            ("EPUB/ch015.xhtml", "list-level-1", "14."),
            ("EPUB/ch015.xhtml", "list-level-1", "3."),
            ("EPUB/ch015.xhtml", "list-level-1", "50."),
            ("EPUB/ch023.xhtml", "list-level-1", "III."),
            ("EPUB/ch053.xhtml", "roman-subheading", "III."),
            ("EPUB/ch066.xhtml", "roman-subheading", "III."),
        },
        9: {
            ("EPUB/ch029.xhtml", "list-level-1", "III."),
            ("EPUB/ch030.xhtml", "list-level-1", "IV."),
            ("EPUB/ch090.xhtml", "list-level-1", "3."),
            ("EPUB/ch091.xhtml", "list-level-1", "3."),
        },
        10: {
            ("EPUB/ch011.xhtml", "list-level-1", "3."),
            ("EPUB/ch046.xhtml", "list-level-2", "(3.)"),
            ("EPUB/ch046.xhtml", "list-level-2", "(5.)"),
            ("EPUB/ch046.xhtml", "list-level-2", "(7.)"),
            ("EPUB/ch054.xhtml", "list-level-1", "5."),
            ("EPUB/ch084.xhtml", "list-level-1", "8."),
            ("EPUB/ch084.xhtml", "list-level-1", "117."),
            ("EPUB/ch048.xhtml", "list-level-1", "4."),
            ("EPUB/ch048.xhtml", "list-level-1", "8."),
            ("EPUB/ch058.xhtml", "roman-subheading", "VI."),
        },
        11: {
            ("EPUB/ch006.xhtml", "list-level-1", "3."),
            ("EPUB/ch006.xhtml", "list-level-1", "9."),
            ("EPUB/ch006.xhtml", "list-level-1", "23."),
            ("EPUB/ch006.xhtml", "list-level-1", "30."),
            ("EPUB/ch006.xhtml", "list-level-1", "417."),
            ("EPUB/ch008.xhtml", "list-level-1", "4."),
            ("EPUB/ch009.xhtml", "list-level-1", "39."),
            ("EPUB/ch010.xhtml", "list-level-1", "5."),
            ("EPUB/ch010.xhtml", "list-level-1", "6."),
            ("EPUB/ch011.xhtml", "list-level-1", "4."),
            ("EPUB/ch011.xhtml", "list-level-1", "7."),
            ("EPUB/ch011.xhtml", "list-level-1", "8."),
            ("EPUB/ch012.xhtml", "list-level-1", "5."),
            ("EPUB/ch012.xhtml", "list-level-1", "6."),
            ("EPUB/ch013.xhtml", "list-level-1", "75."),
            ("EPUB/ch014.xhtml", "list-level-1", "3."),
            ("EPUB/ch014.xhtml", "list-level-1", "21."),
            ("EPUB/ch015.xhtml", "list-level-1", "12."),
            ("EPUB/ch015.xhtml", "list-level-1", "20."),
            ("EPUB/ch015.xhtml", "list-level-1", "22."),
            ("EPUB/ch015.xhtml", "list-level-1", "31."),
            ("EPUB/ch017.xhtml", "list-level-1", "3."),
            ("EPUB/ch017.xhtml", "list-level-1", "5."),
            ("EPUB/ch017.xhtml", "list-level-1", "21."),
            ("EPUB/ch022.xhtml", "list-level-1", "4."),
            ("EPUB/ch022.xhtml", "list-level-1", "23."),
        },
        12: {
            ("EPUB/ch008.xhtml", "list-level-1", "4."),
            ("EPUB/ch011.xhtml", "list-level-1", "11."),
            ("EPUB/ch011.xhtml", "list-level-1", "5."),
            ("EPUB/ch014.xhtml", "list-level-2", "(4.)"),
            ("EPUB/ch017.xhtml", "list-level-1", "16."),
            ("EPUB/ch018.xhtml", "list-level-1", "3."),
            ("EPUB/ch019.xhtml", "list-level-1", "6."),
            ("EPUB/ch019.xhtml", "list-level-1", "4."),
            ("EPUB/ch019.xhtml", "list-level-1", "24."),
            ("EPUB/ch021.xhtml", "list-level-1", "3."),
            ("EPUB/ch023.xhtml", "list-level-1", "4."),
            ("EPUB/ch024.xhtml", "list-level-1", "3."),
            ("EPUB/ch024.xhtml", "list-level-1", "4."),
            ("EPUB/ch039.xhtml", "list-level-1", "52."),
            ("EPUB/ch042.xhtml", "list-level-2", "(4.)"),
            ("EPUB/ch044.xhtml", "list-level-1", "4."),
            ("EPUB/ch050.xhtml", "list-level-1", "3."),
        },
        13: {
            ("EPUB/ch022.xhtml", "list-level-1", "10."),
            ("EPUB/ch022.xhtml", "list-level-1", "22."),
            ("EPUB/ch023.xhtml", "list-level-1", "7."),
            ("EPUB/ch045.xhtml", "list-level-1", "4."),
            ("EPUB/ch059.xhtml", "list-level-1", "3."),
            ("EPUB/ch059.xhtml", "roman-subheading", "V."),
        },
        14: {
            ("EPUB/ch006.xhtml", "list-level-1", "VII."),
            ("EPUB/ch007.xhtml", "list-level-1", "5."),
            ("EPUB/ch033.xhtml", "list-level-1", "4."),
            ("EPUB/ch033.xhtml", "list-level-1", "6."),
            ("EPUB/ch033.xhtml", "list-level-1", "7."),
            ("EPUB/ch033.xhtml", "list-level-1", "11."),
            ("EPUB/ch033.xhtml", "list-level-1", "381."),
            ("EPUB/ch033.xhtml", "list-level-1", "754."),
            ("EPUB/ch033.xhtml", "list-level-1", "794."),
            ("EPUB/ch033.xhtml", "list-level-2", "(7.)"),
            ("EPUB/ch033.xhtml", "list-level-2", "(11.)"),
            ("EPUB/ch041.xhtml", "list-level-1", "5."),
            ("EPUB/ch042.xhtml", "list-level-1", "4."),
            ("EPUB/ch042.xhtml", "list-level-1", "9."),
            ("EPUB/ch045.xhtml", "list-level-1", "4."),
            ("EPUB/ch046.xhtml", "list-level-1", "11."),
            ("EPUB/ch048.xhtml", "list-level-1", "3."),
            ("EPUB/ch050.xhtml", "list-level-1", "4."),
            ("EPUB/ch050.xhtml", "list-level-1", "490."),
            ("EPUB/ch051.xhtml", "list-level-1", "6."),
        },
        15: {
            ("EPUB/ch025.xhtml", "list-level-2", "(3.)"),
            ("EPUB/ch026.xhtml", "list-level-1", "4."),
            ("EPUB/ch026.xhtml", "list-level-2", "(3.)"),
            ("EPUB/ch026.xhtml", "list-level-2", "(5.)"),
            ("EPUB/ch028.xhtml", "list-level-1", "150."),
            ("EPUB/ch029.xhtml", "list-level-1", "42."),
            ("EPUB/ch032.xhtml", "list-level-2", "[3.]"),
            ("EPUB/ch034.xhtml", "list-level-1", "12."),
            ("EPUB/ch034.xhtml", "list-level-2", "(7.)"),
            ("EPUB/ch038.xhtml", "list-level-1", "15."),
            ("EPUB/ch045.xhtml", "list-level-1", "3."),
            ("EPUB/ch050.xhtml", "list-level-1", "3."),
            ("EPUB/ch081.xhtml", "list-level-1", "3."),
            ("EPUB/ch057.xhtml", "list-level-1", "3."),
            ("EPUB/ch061.xhtml", "list-level-1", "4."),
            ("EPUB/ch063.xhtml", "list-level-1", "4."),
            ("EPUB/ch082.xhtml", "list-level-1", "4."),
            ("EPUB/ch090.xhtml", "list-level-1", "4."),
            ("EPUB/ch069.xhtml", "list-level-1", "4."),
            ("EPUB/ch072.xhtml", "list-level-1", "7."),
            ("EPUB/ch072.xhtml", "list-level-1", "6."),
        },
        16: {
            ("EPUB/ch006.xhtml", "list-level-1", "5."),
            ("EPUB/ch007.xhtml", "list-level-1", "124."),
            ("EPUB/ch010.xhtml", "list-level-1", "7."),
            ("EPUB/ch010.xhtml", "list-level-1", "10."),
            ("EPUB/ch012.xhtml", "list-level-1", "5."),
            ("EPUB/ch012.xhtml", "list-level-1", "6."),
            ("EPUB/ch013.xhtml", "list-level-2", "(3.)"),
            ("EPUB/ch013.xhtml", "list-level-2", "[3.]"),
            ("EPUB/ch013.xhtml", "list-level-1", "6."),
            ("EPUB/ch047.xhtml", "list-level-1", "3."),
            ("EPUB/ch052.xhtml", "list-level-1", "3."),
            ("EPUB/ch052.xhtml", "list-level-1", "9."),
            ("EPUB/ch052.xhtml", "list-level-1", "12."),
            ("EPUB/ch055.xhtml", "list-level-1", "14."),
            ("EPUB/ch056.xhtml", "list-level-1", "3."),
            ("EPUB/ch056.xhtml", "list-level-1", "7."),
            ("EPUB/ch057.xhtml", "list-level-1", "22."),
            ("EPUB/ch058.xhtml", "list-level-1", "9."),
            ("EPUB/ch058.xhtml", "list-level-1", "11."),
            ("EPUB/ch058.xhtml", "list-level-1", "150."),
        },
    }
    return (name, level_cls, rm) in known.get(volume, set())


def _record_marker(
    family: str,
    val: int,
    rm: str,
    level_cls: str,
    level_sequences: dict[tuple[str, str], dict[str, int | str]],
    failures: list[str],
    name: str,
    volume,
) -> None:
    key = (family, level_cls)
    state = level_sequences.get(key)
    if val == 1:
        level_sequences[key] = {"val": 1, "marker": rm}
        return
    if state is None:
        level_sequences[key] = {"val": val, "marker": rm}
        return
    expected_val = int(state["val"]) + 1
    if val <= int(state["val"]):
        level_sequences[key] = {"val": val, "marker": rm}
        return
    if val != expected_val and not _is_known_gap(volume, name, level_cls, rm):
        failures.append(
            f"{name}: Sequence gap at '{level_cls}' for marker '{rm}'. "
            f"Expected value {expected_val} (predecessor was '{state['marker']}'), but got {val}."
        )
    level_sequences[key] = {"val": val, "marker": rm}


@pytest.mark.parametrize("volume", VOLUMES)
def test_structural_symmetry_and_sequential_completeness(volume: str):
    """
    Enforces structural sequence continuity for visible block markers.

    Paragraphs marked as syllabus anchors may contain additional inline markers
    such as "8. ... 9. ... 10." after the leading block marker. Those inline
    markers are reader-visible sequence members and must advance the sequence
    tracker, or the next block marker is falsely reported as a source gap.
    """
    if str(volume).lower().startswith("h"):
        pytest.skip("Hebrews volumes are EPUB2-sourced and do not require layout-based sequence symmetry checks.")

    files = _load_epub(volume)
    volume = int(volume) if str(volume).isdigit() else volume
    failures = []

    for name, html in sorted(files.items()):
        if not name.startswith("EPUB/ch"):
            continue

        blocks = re.findall(
            r'<p\b[^>]*class="([^"]*)"[^>]*>(.*?)</p>|<h[1-6]\b[^>]*class="([^"]*)"[^>]*>(.*?)</h[1-6]>',
            html,
            re.S,
        )
        level_sequences = {}

        for p_class, p_inner, h_class, h_inner in blocks:
            cls = (p_class or h_class or "").strip()
            inner = (p_inner or h_inner or "").strip()
            level_cls = _structural_level(cls)
            if not level_cls:
                continue

            marker_matches = list(re.finditer(r"<strong>(?P<marker>[^<]+)</strong>", inner))
            if not marker_matches:
                continue

            for idx, marker_match in enumerate(marker_matches):
                if idx > 0 and "syllabus-anchor" not in cls.split():
                    continue
                if idx == 0:
                    prefix = inner[: marker_match.start()]
                    if re.sub(r"<[^>]+>", "", prefix).strip():
                        continue

                for family, val, rm in _marker_parts(marker_match.group("marker")):
                    _record_marker(family, val, rm, level_cls, level_sequences, failures, name, volume)

    assert not failures, (
        f"Volume {volume}: Structural symmetry or sequential completeness failures found:\n"
        + "\n".join(f"  {f}" for f in failures)
    )
