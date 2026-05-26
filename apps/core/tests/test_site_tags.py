from django.test import SimpleTestCase

from apps.core.templatetags.site_tags import ideal_cols


class IdealColsTests(SimpleTestCase):
    def test_single_row_when_count_le_max(self):
        self.assertEqual(ideal_cols(5, 5), 5)
        self.assertEqual(ideal_cols(3, 3), 3)

    def test_even_rows_for_composite_counts(self):
        self.assertEqual(ideal_cols(4, 3), 2)
        self.assertEqual(ideal_cols(6, 3), 3)
        self.assertEqual(ideal_cols(22, 3), 2)

    def test_prime_fallback(self):
        self.assertEqual(ideal_cols(5, 3), 3)
        self.assertEqual(ideal_cols(7, 3), 3)

    def test_minimum_one(self):
        self.assertEqual(ideal_cols(0, 3), 1)
