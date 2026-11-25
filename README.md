# masri-normalize

مكتبة بايثون صغيرة بتنضّف وتطبّع النص المصري (العامية) قبل ما تدخّله في نماذج الذكاء الاصطناعي أو معالجة اللغة: تشكيل، تطويل، حروف مكررة، أرقام عربية، وعربيزي.

A small Python library that cleans and normalizes Egyptian Arabic text (diacritics, tatweel, repeated letters, Arabic digits, Arabizi) before feeding it to AI/NLP models.

## ليه؟

النص المصري اللي بنكتبه كل يوم مليان حاجات بتبوّظ النماذج:

- تشكيل وتطويل: `مُحَمَّد` ، `مـــرحبا`
- تكرار حروف للتأكيد: `جمااااال`
- أرقام عربية: `١٢٣`
- عربيزي: `7abibi`
- لينكات ومنشن وإيموجي: `شوف https://x.com عند @ahmed 😂`

المكتبة دي بتظبط كل ده في سطر واحد.

## التثبيت

```bash
pip install masri-normalize
```

أو من الكود مباشرة:

```bash
git clone https://github.com/cmse66-dotcom/masri-normalize.git
cd masri-normalize
pip install .
```

## الاستخدام

```python
from masri_normalize import normalize

normalize("أهلاً بالـــــزماااائل ١٢٣")
# 'اهلا بالزماائل 123'

normalize("7abibi عامل ايه")
# 'حabibi عامل ايه'

normalize("شوف https://example.com عند @ahmed 😂")
# 'شوف عند'
```

كل خطوة تقدر تقفلها بمفتاح:

```python
normalize("مدرسة")                    # 'مدرسة'  (التاء المربوطة بتفضل زي ما هي)
normalize("مدرسة", ta_marbuta=True)   # 'مدرسه'
normalize("مـــرحبا", tatweel=False)  # 'مـــرحبا'
normalize("جماااال", max_repeat=1)    # 'جمال'
```

أو استخدم أي دالة لوحدها:

```python
from masri_normalize import (
    remove_diacritics, remove_tatweel, normalize_alef, normalize_ya,
    normalize_ta_marbuta, normalize_digits, reduce_repeated_chars,
    arabizi_digits_to_arabic, clean_text,
)

remove_diacritics("مُحَمَّد")     # 'محمد'
remove_tatweel("مـــرحبا")        # 'مرحبا'
normalize_alef("أحمد إبراهيم")     # 'احمد ابراهيم'
normalize_ya("على")               # 'علي'
normalize_digits("١٢٣")           # '123'
reduce_repeated_chars("جماااال")  # 'جماال'
clean_text("يا #مصر 😂")          # 'يا مصر'
```

## ملاحظات مهمة

- **العربيزي تحويل تقريبي:** الأرقام (2, 3, 5, 7, 8) بتتبدل بالحروف المشهورة (ء، ع، خ، ح، غ) جوه الكلمات اللي فيها حروف لاتينية. مش ترجمة كاملة، لكنه بيفيد كخطوة أولى. أرقام التليفونات والكميات متتأثرش.
- **التاء المربوطة مقفولة افتراضياً** لأنها بتغيّر شكل الكلمة. شغّلها بس لو بتجهّز نص للبحث أو المطابقة، مش للعرض.
- **تكرار الحروف بيتقلّص لـ 2 مش 1** عشان يحافظ على التأكيد الشائع في المصري (`جميييل` -> `جمييل`).

## التطوير

شغّل الاختبارات:

```bash
python -m unittest discover -s tests -v
```

وشغّل الأمثلة:

```bash
python examples/basic_usage.py
```

## المساهمة

أي مساهمة مرحب بيها: Issues للمشاكل والاقتراحات، وPull Requests للتحسينات. لو عندك كلمة عربيزي أو حالة المكتبة بتغلط فيها، ابعتهالنا.

## الترخيص

MIT — شوف ملف [LICENSE](LICENSE).

---

## English summary

`masri-normalize` normalizes Egyptian Arabic text for NLP pipelines: strips diacritics and tatweel, unifies alef/ya forms, optionally converts ta marbuta, converts Eastern Arabic/Persian digits to ASCII, replaces common Arabizi digits inside Latin-script words (2, 3, 5, 7, 8), collapses repeated characters (default max 2 to keep emphasis), and cleans URLs, mentions, hashtags, and emoji. Everything is toggleable via keyword arguments. No dependencies, Python 3.8+.
