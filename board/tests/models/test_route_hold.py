from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from board.models import Layout, Route, RouteHold


class RouteHoldTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        owner = user_model(username="owner", password="password")
        owner.save()
        layout = Layout(name="test_layout", cols=10, rows=10)
        layout.save()
        cls.route = Route(
            name="test_route", owner=owner, layout=layout, grade="4", tilt=5
        )
        cls.route.save()

    def test_route_hold_invalid_type_fails(self):
        obj = RouteHold(route=self.route, index=0, type="INVALID_TYPE")

        with self.assertRaises(ValidationError):
            obj.full_clean()
