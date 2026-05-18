import unicodedata

from shared import HEBREW_GIDEON_MAP, convert_gideon_hebrew


# Inventory from a 16-volume scan of spans whose PDF font is Gideon-Medium.
OBSERVED_GIDEON_CHARS = {
    ' ', "'", ',', '/', '1', ';', '=', 'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
    'T', 'V', 'W', 'X', 'Y', 'Z', '[', ']', '`', 'a', 'b', 'c', 'd',
    'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
    'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '}', 'µ', 'Ë', 'Ú',
    'ã', 'æ', 'ç', 'ˆ', '˚', '‘', '’', '≈',
}


def test_observed_gideon_span_characters_are_mapped():
    missing = sorted(ch for ch in OBSERVED_GIDEON_CHARS if ch not in HEBREW_GIDEON_MAP)
    assert missing == []


def test_gideon_mapping_outputs_only_hebrew_marks_and_allowed_spacing():
    allowed = {' '}
    bad = {}
    for source, mapped in HEBREW_GIDEON_MAP.items():
        for ch in mapped:
            name = unicodedata.name(ch, '')
            if ch not in allowed and not name.startswith('HEBREW '):
                bad.setdefault(source, mapped)
    assert bad == {}


def test_known_ages_gideon_samples_convert_without_legacy_residue():
    samples = {
        'aWh': 'הוּא',
        'hT;a1': 'אַתָה',
        'jæWr': 'רוּחַ',
        'yneB]': 'בְּנֵי',
        'ˆwO[}': 'עֲוֹן',
        'µyMi[1': 'עַמִים',
        'WnL;Ku': 'כֻּלָנוּ',
        'Ël]': 'לְך',
        'ãje': 'חֵן',
        't/m': 'מוֹת',
        'rxewOy': 'יוֹצֵר',
        '≈r,a;h;': 'הָאָרֶץ',
    }
    for encoded, expected in samples.items():
        assert convert_gideon_hebrew(encoded) == expected


def test_corpus_gideon_character_inventory_has_no_unmapped_warning_residue():
    encoded = ''.join(sorted(OBSERVED_GIDEON_CHARS))
    converted = convert_gideon_hebrew(encoded)
    for ch in OBSERVED_GIDEON_CHARS - {' '}:
        assert ch not in converted
