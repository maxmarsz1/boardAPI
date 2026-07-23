from typing import Iterable

from common.utils import get_object
from board.models import Hold


def hold_list() -> Iterable[Hold]:
    return Hold.objects.all()


def hold_get(pk: int) -> Hold | None:
    hold = get_object(Hold, pk=pk)
    return hold
