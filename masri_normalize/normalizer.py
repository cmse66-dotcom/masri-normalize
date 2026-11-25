"""masri_normalize: تنضيف وتطبيع النص المصري لنماذج الذكاء الاصطناعي.

دوال صغيرة ومستقلة، كل واحدة بتعمل حاجة واحدة، وفى الآخر دالة normalize()
بتجمّعهم كلهم في خطوة واحدة.
"""

import re
import unicodedata

# ---------- التشكيل والتطويل ----------

# نطاقات دقيقة عشان الأرقام العربية (٠-٩) والفارسية (۰-۹) متتمسحش بالغلط
_DIACRITICS_RE = re.compile(r"[ً-ٰٟۖ-ۭ]")
_TATWEEL_RE = re.compile("ـ")


def remove_diacritics(text: str) -> str:
    """بيشيل التشكيل (فتحة، ضمة، سكون، تنوين...) من النص."""
    return _DIACRITICS_RE.sub("", text)


def remove_tatweel(text: str) -> str:
    """بيشيل التطويل: 'مـــرحبا' -> 'مرحبا'."""
    return _TATWEEL_RE.sub("", text)


# ---------- تطبيع الحروف ----------

_ALEF_TABLE = str.maketrans({
    "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
})


def normalize_alef(text: str) -> str:
    """بيوحّد أشكال الألف: 'أحمد إبراهيم آية' -> 'احمد ابراهيم اية'."""
    return text.translate(_ALEF_TABLE)


def normalize_ya(text: str) -> str:
    """بيحوّل الألف المقصورة لياء: 'على' -> 'علي'."""
    return text.replace("ى", "ي")


def normalize_ta_marbuta(text: str) -> str:
    """بيحوّل التاء المربوطة لهاء: 'مدرسة' -> 'مدرسه'.

    استخدمها بحذر: ممكن تغيّر معنى كلمة لو رجّعت النص للعرض.
    مناسبة أكتر قبل البحث أو المطابقة، مش قبل العرض.
    """
    return text.replace("ة", "ه")


def reduce_repeated_chars(text: str, max_repeat: int = 2) -> str:
    """بيقلّص تكرار الحرف لعدد معيّن: 'جمااااال' -> 'جماال'.

    الافتراضي 2 عشان يحافظ على التأكيد الشائع في المصري
    ('جميييل' بتفضل 'جمييل' مش 'جميل').
    """
    if max_repeat < 1:
        raise ValueError("max_repeat لازم يكون 1 أو أكتر")
    # حروف بس: التطويل والأرقام والرموز متتقلّصش هنا (للتطويل خطوته الخاصة)
    return re.sub(r"([^\W\d_ـ])\1{%d,}" % max_repeat, r"\1" * max_repeat, text)


# ---------- الأرقام ----------

_DIGIT_TABLE = {}
for _i in range(10):
    _DIGIT_TABLE[0x0660 + _i] = ord(str(_i))   # أرقام عربية مشرقية ٠١٢٣
    _DIGIT_TABLE[0x06F0 + _i] = ord(str(_i))   # أرقام فارسية/أردو ۰۱۲۳


def normalize_digits(text: str) -> str:
    """بيحوّل الأرقام العربية والفارسية لأرقام إنجليزية: '١٢٣' -> '123'."""
    return text.translate(_DIGIT_TABLE)


# ---------- العربيزي ----------

# خريطة تقريبية للأرقام المشهورة في العربيزي المصري.
# تحويل حرفي بحت (heuristic): مناسب كخطوة أولى، مش ترجمة كاملة.
ARABIZI_DIGIT_MAP = {
    "2": "ء",   # همزة / قاف
    "3": "ع",
    "5": "خ",
    "7": "ح",
    "8": "غ",
}


def arabizi_digits_to_arabic(text: str) -> str:
    """بيستبدل أرقام العربيزي جوه الكلمات: '7abibi' -> 'حabibi'.

    بيشتغل بس على كلمات فيها حروف لاتينية مع أرقام، عشان
    أرقام التليفونات والكميات الحقيقية متتأثرش.
    """
    def _fix(match: re.Match) -> str:
        word = match.group(0)
        return "".join(ARABIZI_DIGIT_MAP.get(ch, ch) for ch in word)

    return re.sub(
        r"\b(?=[A-Za-z0-9]*[A-Za-z])(?=[A-Za-z0-9]*[0-9])[A-Za-z0-9]+\b",
        _fix,
        text,
    )


# ---------- تنضيف عام ----------

_URL_RE = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
_MENTION_RE = re.compile(r"@\w+")
_EMAIL_RE = re.compile(r"\S+@\S+\.\S+")
_HASHTAG_RE = re.compile(r"#(\w+)")
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "\U0000FE00-\U0000FE0F"
    "\U0000200D"
    "]+"
)
_EXTRA_SPACES_RE = re.compile(r"\s+")


def clean_text(text: str, keep_hashtag_text: bool = True, remove_emoji: bool = True) -> str:
    """تنضيف عام: بيشيل لينكات ومنشن وإيميلات وإيموجي، وبيظبط المسافات.

    keep_hashtag_text=True بيخلي الهاشتاج كنص من غير علامة #
    ('#مصر' -> 'مصر'). False بيشيل الهاشتاج كله.
    """
    text = _URL_RE.sub(" ", text)
    text = _EMAIL_RE.sub(" ", text)
    text = _MENTION_RE.sub(" ", text)
    if keep_hashtag_text:
        text = _HASHTAG_RE.sub(r"\1", text)
    else:
        text = _HASHTAG_RE.sub(" ", text)
    if remove_emoji:
        text = _EMOJI_RE.sub(" ", text)
    text = _EXTRA_SPACES_RE.sub(" ", text)
    return text.strip()


# ---------- الخطوة الكاملة ----------

def normalize(
    text: str,
    diacritics: bool = True,
    tatweel: bool = True,
    alef: bool = True,
    ya: bool = True,
    ta_marbuta: bool = False,
    digits: bool = True,
    arabizi: bool = True,
    max_repeat: int = 2,
    clean: bool = True,
) -> str:
    """بيطبّق كل خطوات التطبيع على النص بترتيب منطقي.

    كل خطوة ليها مفتاح تقدر تقفلها بيه. ta_marbuta مقفولة افتراضياً
    لأنها بتغيّر شكل الكلمة المعروض.
    """
    if clean:
        text = clean_text(text)
    if diacritics:
        text = remove_diacritics(text)
    if tatweel:
        text = remove_tatweel(text)
    if arabizi:
        text = arabizi_digits_to_arabic(text)
    if digits:
        text = normalize_digits(text)
    if alef:
        text = normalize_alef(text)
    if ya:
        text = normalize_ya(text)
    if ta_marbuta:
        text = normalize_ta_marbuta(text)
    if max_repeat:
        text = reduce_repeated_chars(text, max_repeat=max_repeat)
    return text.strip()
