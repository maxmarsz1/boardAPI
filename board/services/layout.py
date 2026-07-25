from django.http import Http404
from rest_framework.exceptions import ValidationError
from board.models import Layout, LayoutHold
from board.selectors.layout import layout_get
from board.selectors.hold import hold_get


def layout_create(*, name: str, rows: int, cols: int) -> Layout:
    layout = Layout(name=name, rows=rows, cols=cols)

    layout.full_clean()
    layout.save()

    return layout


def layout_get_assigned_hold(*, layout_id: int, index: int) -> LayoutHold | None:
    layout = layout_get(layout_id)

    try:
        return LayoutHold.objects.get(layout=layout, index=index)
    except LayoutHold.DoesNotExist:
        return None


def layout_assign_hold(
    *, layout_id: int, hold_id: int, index: int, rotation: int
) -> bool:
    layout = layout_get(layout_id)
    hold = hold_get(hold_id)

    if layout is None:
        raise Http404("layout not found")

    if hold is None:
        raise Http404("hold not found")

    if index > layout.max_index:
        raise ValidationError(f"index must be in layout range: 0 - {layout.max_index}")

    layout_hold = layout_get_assigned_hold(layout_id=layout_id, index=index)

    # TODO:
    # Move to seperate service function layout_hold_update_or_create

    created = False
    if layout_hold is None:
        created = True
        layout_hold = LayoutHold(
            layout=layout, index=index, hold=hold, rotation=rotation
        )
    else:
        layout_hold.hold = hold
        layout_hold.rotation = rotation

    layout_hold.full_clean()
    layout_hold.save()

    return created
