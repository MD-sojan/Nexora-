def extract_strings(content: bytes, min_length: int = 4):
    """Extract ASCII strings from binary content."""
    result, current = [], ""
    for byte in content:
        char = chr(byte)
        if char.isprintable():
            current += char
            continue
        if len(current) >= min_length:
            result.append(current)
        current = ""
    if len(current) >= min_length:
        result.append(current)
    return result
