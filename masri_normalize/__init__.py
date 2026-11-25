"""masri_normalize: مكتبة بايثون لتنضيف وتطبيع النص المصري (العامية المصرية).

Usage:
    from masri_normalize import normalize

    normalize("أهلاً بالـــــزماااائل 123 7abibi")
"""

from .normalizer import (
    ARABIZI_DIGIT_MAP,
    arabizi_digits_to_arabic,
    clean_text,
    normalize,
    normalize_alef,
    normalize_digits,
    normalize_ta_marbuta,
    normalize_ya,
    reduce_repeated_chars,
    remove_diacritics,
    remove_tatweel,
)

__version__ = "0.1.0"

__all__ = [
    "normalize",
    "remove_diacritics",
    "remove_tatweel",
    "normalize_alef",
    "normalize_ya",
    "normalize_ta_marbuta",
    "normalize_digits",
    "reduce_repeated_chars",
    "arabizi_digits_to_arabic",
    "clean_text",
    "ARABIZI_DIGIT_MAP",
    "__version__",
]
