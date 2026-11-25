import unittest

from masri_normalize import (
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


class TestDiacriticsAndTatweel(unittest.TestCase):
    def test_remove_diacritics(self):
        self.assertEqual(remove_diacritics("مُحَمَّد"), "محمد")
        self.assertEqual(remove_diacritics("السَّلَامُ عَلَيْكُمْ"), "السلام عليكم")

    def test_remove_diacritics_keeps_plain_text(self):
        self.assertEqual(remove_diacritics("عامل ايه"), "عامل ايه")

    def test_remove_tatweel(self):
        self.assertEqual(remove_tatweel("مـــرحبا"), "مرحبا")
        self.assertEqual(remove_tatweel("ياااارب"), "ياااارب")


class TestLetterNormalization(unittest.TestCase):
    def test_normalize_alef(self):
        self.assertEqual(normalize_alef("أحمد إبراهيم آية"), "احمد ابراهيم اية")

    def test_normalize_ya(self):
        self.assertEqual(normalize_ya("على موسى"), "علي موسي")
        self.assertEqual(normalize_ya("علي"), "علي")

    def test_normalize_ta_marbuta(self):
        self.assertEqual(normalize_ta_marbuta("مدرسة"), "مدرسه")

    def test_reduce_repeated_default_two(self):
        self.assertEqual(reduce_repeated_chars("جمااااال"), "جماال")
        self.assertEqual(reduce_repeated_chars("ننننعم"), "ننعم")

    def test_reduce_repeated_to_one(self):
        self.assertEqual(reduce_repeated_chars("جمااااال", max_repeat=1), "جمال")

    def test_reduce_repeated_invalid(self):
        with self.assertRaises(ValueError):
            reduce_repeated_chars("احمد", max_repeat=0)


class TestDigits(unittest.TestCase):
    def test_normalize_arabic_digits(self):
        self.assertEqual(normalize_digits("١٢٣"), "123")
        self.assertEqual(normalize_digits("رقمي ٠١٢٣٤٥"), "رقمي 012345")

    def test_normalize_persian_digits(self):
        self.assertEqual(normalize_digits("۱۲۳"), "123")


class TestArabizi(unittest.TestCase):
    def test_digit_inside_word(self):
        self.assertEqual(arabizi_digits_to_arabic("7abibi"), "حabibi")
        self.assertEqual(arabizi_digits_to_arabic("3ala"), "عala")

    def test_pure_number_untouched(self):
        self.assertEqual(arabizi_digits_to_arabic("الساعة ٥"), "الساعة ٥")
        self.assertEqual(arabizi_digits_to_arabic("call 12345"), "call 12345")


class TestCleanText(unittest.TestCase):
    def test_removes_url_and_mention(self):
        self.assertEqual(
            clean_text("شوف اللينك https://example.com عند @ahmed"),
            "شوف اللينك عند",
        )

    def test_hashtag_text_kept_by_default(self):
        self.assertEqual(clean_text("يا #مصر"), "يا مصر")

    def test_hashtag_removed_when_requested(self):
        self.assertEqual(clean_text("يا #مصر", keep_hashtag_text=False), "يا")

    def test_emoji_removed(self):
        self.assertEqual(clean_text("جميل 😂🔥 اوي"), "جميل اوي")

    def test_spaces_normalized(self):
        self.assertEqual(clean_text("يا    سلام   "), "يا سلام")


class TestNormalizePipeline(unittest.TestCase):
    def test_full_pipeline(self):
        self.assertEqual(
            normalize("أهلاً بالـــــزماااائل ١٢٣"),
            "اهلا بالزماائل 123",
        )

    def test_mixed_arabizi(self):
        self.assertEqual(normalize("7abibi عامل ايه"), "حabibi عامل ايه")

    def test_ta_marbuta_opt_in(self):
        self.assertEqual(normalize("مدرسة"), "مدرسة")
        self.assertEqual(normalize("مدرسة", ta_marbuta=True), "مدرسه")

    def test_disable_steps(self):
        self.assertEqual(
            normalize("أهلاً", alef=False),
            "أهلاً".replace("ً", ""),  # التشكيل بس بيتشال
        )
        self.assertEqual(normalize("مـــرحبا", tatweel=False), "مـــرحبا")

    def test_max_repeat_disabled(self):
        self.assertEqual(normalize("جماااال", max_repeat=0), "جماااال")

    def test_empty_and_plain(self):
        self.assertEqual(normalize(""), "")
        self.assertEqual(normalize("عامل ايه"), "عامل ايه")


if __name__ == "__main__":
    unittest.main()
