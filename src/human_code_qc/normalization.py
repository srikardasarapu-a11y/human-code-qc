from enum import Enum
from typing import Optional

NORMALIZATION_VERSION = "1.0"

class NormalizationMode(str, Enum):
    RAW = "RAW"
    LINE_ENDING_NORMALIZED = "LINE_ENDING_NORMALIZED"
    WHITESPACE_NORMALIZED = "WHITESPACE_NORMALIZED"

def normalize(data: bytes, mode: NormalizationMode) -> Optional[str]:
    """
    Returns a deterministically normalized string representation of the raw bytes.
    If the bytes cannot be decoded as valid UTF-8, this returns None, preventing
    a fabricated normalized hash.
    
    Modes:
    - RAW: Returns the original exact byte content (not implemented here since raw hashing handles bytes).
    - LINE_ENDING_NORMALIZED: Converts \r\n to \n.
    - WHITESPACE_NORMALIZED: Converts \r\n to \n and right-strips trailing spaces from each line.
    """
    if mode == NormalizationMode.RAW:
        # RAW hashing should directly use `hash_bytes` on the data, so text conversion here is just a decode check.
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return None

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None

    if mode == NormalizationMode.LINE_ENDING_NORMALIZED:
        return text.replace("\r\n", "\n")
        
    elif mode == NormalizationMode.WHITESPACE_NORMALIZED:
        lines = text.replace("\r\n", "\n").split("\n")
        # Only right-strip trailing spaces, not all whitespace (like indentation).
        normalized_lines = [line.rstrip(" \t") for line in lines]
        return "\n".join(normalized_lines)
        
    return text
