from typing import Iterable

from common.utils import get_object
from board.models import Layout


def layout_list() -> Iterable[Layout]:
    return Layout.objects.all()


def layout_get(pk: int) -> Layout | None:
    layout = get_object(Layout, pk=pk)
    return layout
