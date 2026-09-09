from django.db.utils import IntegrityError
from django.test import TestCase
from django.db import transaction

from board.models import Layout


class LayoutTests(TestCase):
    def test_layout_max_index_property(self):
        obj = Layout(cols=10, rows=10, name="test")

        self.assertEqual(obj.max_index, 99)

    def test_layout_save_with_negative_row_or_and_col_fails_with_integrity_error(self):
        test_cases = [(-10, 10), (10, -10), (-10, -10)]

        for cols, rows in test_cases:
            with self.subTest(cols=cols, rows=rows):
                obj = Layout(cols=cols, rows=rows, name="test")

                with self.assertRaises(IntegrityError):
                    with transaction.atomic():
                        obj.save()
