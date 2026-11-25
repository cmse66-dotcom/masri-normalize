"""أمثلة سريعة على استخدام masri_normalize.

شغّل الملف ده من جذر المشروع:
    python examples/basic_usage.py
"""

from masri_normalize import normalize, clean_text, arabizi_digits_to_arabic

samples = [
    "أهلاً بالـــــزماااائل 🔥 ١٢٣",
    "7abibi عامل ايه النهاردة",
    "شوف https://example.com واسأل @ahmed",
    "السَّلَامُ عَلَيْكُمْ يا جماااااعة",
]

print("=== normalize: الخطوة الكاملة ===")
for s in samples:
    print("قبل:", s)
    print("بعد:", normalize(s))
    print()

print("=== clean_text لوحده ===")
print(clean_text("تابعني على @mohamed وشوف #مصر 😂"))

print()
print("=== عربيزي لوحده ===")
print(arabizi_digits_to_arabic("ana 3ayez aro7 el gam3a"))

print()
print("=== تعطيل خطوات معينة ===")
print(normalize("مدرسة", ta_marbuta=True))   # التاء المربوطة -> هاء
print(normalize("مـــرحبا", tatweel=False))   # سيب التطويل زي ما هو
