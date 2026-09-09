from django.contrib.auth import get_user_model
from django.test import TestCase
import tempfile

from board.models import Hold, Layout
from board.services.hold import hold_create
from board.selectors.layout import layout_get, layout_get_assigned_hold, layout_list
from board.services.layout import layout_assign_hold, layout_create


class LayoutListSelectorTests(TestCase):
    def test_layout_list_returns_empty_queryset(self):
        self.assertEqual(0, layout_list().count())

    def test_layout_list_returns_existing_objects(self):
        layout_create(name="layout_1", cols=10, rows=10)

        self.assertEqual(1, layout_list().count())

        layout_create(name="layout_2", cols=10, rows=10)

        self.assertEqual(2, layout_list().count())


class LayoutGetSelectorTests(TestCase):
    def test_layout_get_returns_none_when_object_doesnt_exist(self):
        self.assertIsNone(layout_get(0))

    def test_layout_get_returns_object_when_it_exists(self):
        layout: Layout = layout_create(name="layout", rows=10, cols=11)

        selected_layout: Layout = layout_get(layout.id)

        self.assertEqual(layout.id, selected_layout.id)
        self.assertEqual(layout.name, selected_layout.name)
        self.assertEqual(layout.rows, selected_layout.rows)
        self.assertEqual(layout.cols, selected_layout.cols)


class LayoutGetAssignedHoldTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.layout: Layout = layout_create(name="layout", rows=10, cols=10)

    #     model_file = tempfile.NamedTemporaryFile(suffix=".stl")
    #     user_model = get_user_model()
    #     owner = user_model(username="owner", password="password")
    #     owner.save()
    #
    #     hold: Hold = Hold(name="hold", model_file=model_file, owner=owner)
    #     hold.save()
    #     cls.layout_hold_index = 0
    #     layout_assign_hold(
    #         layout_id=cls.layout.id,
    #         hold_id=hold.id,
    #         index=cls.layout_hold_index,
    #         rotation=90,
    #     )

    def test_layout_get_assigned_hold_return_none_when_hold_not_assigned(self):
        self.assertIsNone(layout_get_assigned_hold(layout_id=self.layout.id, index=1))

    # def test_layout_get_assigned_hold_return_hold_when_assigned(self):
    #     assigned_hold = layout_get_assigned_hold(self.layout.id, self.layout_hold_index)
    #     self.assertEqual(layout, assigned_hold.layout)
