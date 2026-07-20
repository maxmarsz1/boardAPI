from django.urls import include, path

from board.apis import (
    HoldListApi,
    HoldDetailApi,
    HoldCreateApi,
    LayoutRouteListApi,
    RouteListApi,
    RouteDetailApi,
    LayoutListApi,
    LayoutDetailApi,
)

hold_patterns = [
    path("", HoldListApi.as_view(), name="list"),
    path("create/", HoldCreateApi.as_view(), name="create"),
    path("<int:hold_id>/", HoldDetailApi.as_view(), name="detail"),
]

route_patterns = [
    path("", RouteListApi.as_view(), name="list"),
    path("<int:route_id>/", RouteDetailApi.as_view(), name="detail"),
]

layout_patterns = [
    path("", LayoutListApi.as_view(), name="list"),
    path("<int:layout_id>/", LayoutDetailApi.as_view(), name="detail"),
    path("<int:layout_id>/routes/", LayoutRouteListApi.as_view(), name="routes-list"),
]

urlpatterns = [
    path("holds/", include((hold_patterns, "holds"))),
    path("routes/", include((route_patterns, "routes"))),
    path("layouts/", include((layout_patterns, "layouts"))),
]
