from typing import Iterable
from django.shortcuts import get_object_or_404

from board.models import Hold


def hold_list() -> Iterable[Hold]:
    return Hold.objects.all()


def hold_get(pk: int) -> Hold | None:
    hold = get_object_or_404(Hold, pk=pk)
    return hold
