from django.db.models import QuerySet

from common.utils import get_object
from board.models import Hold


def hold_list() -> QuerySet[Hold]:
    return Hold.objects.all()


def hold_get(hold_id: int) -> Hold | None:
    hold = get_object(Hold, pk=hold_id)
    return hold


def hold_get_assigned_layouts_count(hold_id: int) -> int:
    hold = hold_get(hold_id=hold_id)

    try:
        assigned_layouts = hold.layouts_using
        return assigned_layouts.count()

    except Hold.DoesNotExist:
        return 0
