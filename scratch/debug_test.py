import re as _re

def _parse_roman(s: str) -> int:
    s = s.upper().strip('.,:;()[]')
    if not s or not _re.match(r'^[IVXLCDM]+$', s):
        return 0
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    val = 0
    prev_val = 0
    for char in reversed(s):
        curr_val = roman_map.get(char, 0)
        if curr_val >= prev_val:
            val += curr_val
        else:
            val -= curr_val
        prev_val = curr_val
    return val

def _get_marker_val_and_type(marker_text: str) -> tuple[str, int]:
    clean = _re.sub(r'<[^>]+>', '', marker_text).strip()
    clean = clean.strip('.,:; \t\n\r*')
    if not clean:
        return ('empty', 0)
    
    clean_upper = clean.upper()
    
    if clean.startswith('(') and clean.endswith(')'):
        inner = clean[1:-1].strip('.,:; ')
        if inner.isdigit():
            return ('arabic_paren', int(inner))
        if len(inner) == 1 and inner.isalpha():
            return ('alpha_paren', ord(inner.lower()) - ord('a') + 1)
        roman_val = _parse_roman(inner)
        if roman_val > 0:
            return ('roman_paren', roman_val)
            
    if clean.startswith('[') and clean.endswith(']'):
        inner = clean[1:-1].strip('.,:; ')
        if inner.isdigit():
            return ('arabic_bracket', int(inner))
        if len(inner) == 1 and inner.isalpha():
            return ('alpha_bracket', ord(inner.lower()) - ord('a') + 1)
        roman_val = _parse_roman(inner)
        if roman_val > 0:
            return ('roman_bracket', roman_val)

    w = clean_upper
    if 'FIRST' in w or '1ST' in w: return ('ordinal', 1)
    if 'SECOND' in w or '2ND' in w or '2DLY' in w: return ('ordinal', 2)
    if 'THIRD' in w or '3RD' in w or '3DLY' in w: return ('ordinal', 3)
    if 'FOURTH' in w or '4TH' in w or '4THLY' in w: return ('ordinal', 4)
    if 'FIFTH' in w or '5TH' in w or '5THLY' in w: return ('ordinal', 5)
    if 'SIXTH' in w or '6TH' in w: return ('ordinal', 6)
    if 'SEVENTH' in w or '7TH' in w: return ('ordinal', 7)
    if 'EIGHTH' in w or '8TH' in w: return ('ordinal', 8)
    if 'NINTH' in w or '9TH' in w: return ('ordinal', 9)
    if 'TENTH' in w or '10TH' in w: return ('ordinal', 10)

    if clean.isdigit():
        return ('arabic_bare', int(clean))
        
    roman_val = _parse_roman(clean)
    if roman_val > 0:
        return ('roman_bare', roman_val)
        
    if len(clean) == 1 and clean.isalpha():
        return ('alpha_bare', ord(clean.lower()) - ord('a') + 1)
        
    return ('unknown', 0)

def _is_sequential_sequence(pairs) -> bool:
    parsed = [_get_marker_val_and_type(mk) for mk, _ in pairs]
    known_parsed = [(t, v) for t, v in parsed if t != 'unknown' and t != 'empty' and v > 0]
    if len(known_parsed) < 2:
        return True
        
    first_type = known_parsed[0][0]
    if not all(t == first_type for t, _ in known_parsed):
        return False
        
    for idx in range(1, len(known_parsed)):
        if known_parsed[idx][1] <= known_parsed[idx-1][1]:
            return False
    return True

# Let's test the sequence validation
test_pairs_1 = [('<b>(1.)</b>', 'Its light.'), ('<b>(2.)</b>', 'Its efficacy...'), ('<b>(1.)</b>', 'No truth...')]
test_pairs_2 = [('<b>(1.)</b>', 'Its light.'), ('<b>(2.)</b>', 'Its efficacy...')]

print("Pairs 1 is sequential:", _is_sequential_sequence(test_pairs_1))
print("Pairs 2 is sequential:", _is_sequential_sequence(test_pairs_2))
