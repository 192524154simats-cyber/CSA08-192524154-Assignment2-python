"""Q3 - vehicle number validator using ONLY string operations (no re)."""

def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, uppercase)."""
    # TODO 1 (done): remove spaces and hyphens, convert to upper case
    return text.strip().replace(" ", "").replace("-", "").upper()

def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    # TODO 2 (done): length 9 or 10, then check each part by slicing with isalpha()/isdigit()
    if len(reg) not in (9, 10):
        return False
    if not reg.isascii():                       # isalpha()/isdigit() also accept non-English letters and digits like '²'
        return False
    return (reg[:2].isalpha()                   # state: 2 letters
            and reg[2:4].isdigit()              # district: 2 digits
            and reg[4:-4].isalpha()             # series: 1 or 2 letters (9 -> 1 letter, 10 -> 2 letters)
            and reg[-4:].isdigit())             # number: 4 digits

def format_for_receipt(reg):
    """'TN09AB1234' -> 'TN 09 AB 1234' using slices and join."""
    return " ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])

def process(text):
    """Normalise, validate, format. Returns (normalised, valid, receipt text or None)."""
    reg = normalise(text)
    if is_valid(reg):
        return reg, True, format_for_receipt(reg)
    return reg, False, None
