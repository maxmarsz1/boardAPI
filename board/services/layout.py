from django.http import Http404
from board.models import Layout, LayoutHold
from board.selectors.layout import layout_get
from board.selectors.hold import hold_get


def layout_create(*, name: str, rows: int, cols: int) -> Layout:
    layout = Layout(name=name, rows=rows, cols=cols)

    layout.full_clean()
    layout.save()

    return layout


def layout_assign_hold(*, layout_id: int, hold_id: int, index: int, rotation: int):
    layout = layout_get(layout_id)
    hold = hold_get(hold_id)

    if layout is None:
        raise Http404("layout not found")

    if hold is None:
        raise Http404("hold not found")

    LayoutHold.objects.create(layout=layout, hold=hold, index=index, rotation=rotation)
    # layout.holds.create(hold, through_defaults={"index": index, "rotation": rotation})
