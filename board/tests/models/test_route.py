from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from board.models import Layout, Route


class RouteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model(username="test", password="test")
        cls.user.save()
        cls.layout = Layout(cols=10, rows=10, name="test")
        cls.layout.save()

    def test_route_with_tilt_not_div_by_five_fails_with_validation_error_when_full_cleaned(
        self,
    ):
        obj = Route(
            name="test", owner=self.user, layout=self.layout, grade="8c", tilt=4
        )
        with self.assertRaises(ValidationError):
            obj.full_clean()

    def test_route_with_negative_tilt_fails_with_validation_error_when_full_cleaned(
        self,
    ):
        obj = Route(
            name="test", owner=self.user, layout=self.layout, grade="8c", tilt=-10
        )
        with self.assertRaises(ValidationError):
            obj.full_clean()

    def test_route_save_with_not_unique_layout_and_name_fails_with_integrity_error(
        self,
    ):
        obj = Route(
            name="route", owner=self.user, layout=self.layout, grade="8c", tilt=5
        )
        obj.save()

        with self.assertRaises(IntegrityError):
            obj1 = Route(
                name="route", owner=self.user, layout=self.layout, grade="6c+", tilt=15
            )
            obj1.save()

    def test_route_can_be_created_when_tilt_valid_and_name_and_layout_unique(self):
        obj = Route(
            name="route", owner=self.user, layout=self.layout, grade="6b", tilt=10
        )

        self.assertEqual(0, Route.objects.count())

        obj.save()

        self.assertEqual(1, Route.objects.count())
