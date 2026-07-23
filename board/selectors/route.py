from typing import Iterable
from django.db.models import Q

from common.utils import get_object
from board.models import Route


def route_list() -> Iterable[Route]:
    return Route.objects.all()


def route_get_by_layout_id(pk: int) -> Iterable[Route]:
    query = Q(layout__id=pk)

    return Route.objects.filter(query)


def route_get(pk: int) -> Route | None:
    route = get_object(Route, pk=pk)
    return route
