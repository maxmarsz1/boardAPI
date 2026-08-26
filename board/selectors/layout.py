from typing import Iterable, List

from common.utils import get_object
from board.models import Layout, LayoutHold, Route


def layout_list() -> Iterable[Layout]:
    return Layout.objects.all()


def layout_get(pk: int) -> Layout | None:
    layout = get_object(Layout, pk=pk)
    return layout


def layout_get_assigned_hold(*, layout_id: int, index: int) -> LayoutHold | None:
    layout = layout_get(layout_id)

    try:
        return LayoutHold.objects.get(layout=layout, index=index)
    except LayoutHold.DoesNotExist:
        return None
