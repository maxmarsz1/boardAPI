from typing import Iterable
from django.shortcuts import get_object_or_404

from board.models import Layout


def layout_list() -> Iterable[Layout]:
    return Layout.objects.all()


def layout_get(pk: int) -> Layout | None:
    layout = get_object_or_404(Layout, pk=pk)
    return layout
