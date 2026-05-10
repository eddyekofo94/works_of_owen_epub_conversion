def remove_repeated_phrases(text):
    if not text or len(text) < 20:
        return text
    # Search for any repeated sequence of length 10 to half the text length
    for length in range(len(text)//2, 9, -1):
        for i in range(len(text) - 2*length + 1):
            chunk = text[i:i+length]
            if chunk == text[i+length:i+2*length]:
                # Found immediate repetition
                print(f"Found repetition of length {length}: {repr(chunk)}")
                return remove_repeated_phrases(text[:i] + text[i+length:])
    return text

test = "(Acts 20:28-31; 1 Timothy 6:13, 14; Acts 20:28-31; 1 Timothy 6:13, 14; 2 Timothy 2:1, 2, 15, 23, 24; 4:1-5,)"
result = remove_repeated_phrases(test)
print(f"Result: {result}")
