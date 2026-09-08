from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
import tempfile

from board.models import Hold


class HoldTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model(username="test_user", password="password")
        cls.user.save()

    def test_hold_save_with_not_unique_name_fails_with_integrity_error(self):
        model_file = tempfile.NamedTemporaryFile(suffix=".stl").name
        obj = Hold(name="test", model_file=model_file, owner=self.user)
        obj.save()

        obj1 = Hold(name="test", model_file=model_file, owner=self.user)
        with self.assertRaises(IntegrityError):
            obj1.save()
