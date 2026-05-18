import re

def _repair_owen_ocr_errors(text: str, config: dict = None) -> str:
    if not config:
        return text
    corrections = config.get('text_replacements', {})
    regex_corrections = config.get('regex_replacements', {})
    result = text
    for wrong, right in corrections.items():
        if wrong.startswith('(') or wrong.startswith(r'\(') or wrong.endswith(r'\b'):
             result = re.sub(wrong, right, result)
        else:
             result = re.sub(r'\b' + re.escape(wrong) + r'\b', right, result)
    for pattern, repl in regex_corrections.items():
        result = re.sub(pattern, repl, result)
    return result

config = {
    'regex_replacements': {
        r'f(\d{1,3})(?=[a-z])': r'[f\1] ',
    }
}
test_text = "In three things; — first, in causing f53and things to work together for their good;"
print(f"Original: {test_text}")
print(f"Fixed:    {_repair_owen_ocr_errors(test_text, config)}")
