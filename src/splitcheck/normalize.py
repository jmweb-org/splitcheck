"""Text normalization used to detect near-duplicate rows.

Two rows are "near duplicates" when they are equal after normalization: case
folded, punctuation removed, and whitespace collapsed. This is deterministic
and dependency-free, and catches the common leakage case where the same example
appears in two splits with cosmetic differences.
"""

from __future__ import annotations

import re
import unicodedata

_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.casefold()
    text = _PUNCT.sub(" ", text)
    text = _WS.sub(" ", text)
    return text.strip()
