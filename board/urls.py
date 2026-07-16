from django.urls import path
from board.views import (
    HoldDetail,
    HoldList,
    LayoutDetail,
    LayoutList,
    RouteDetail,
    RouteListCreate,
)

urlpatterns = [
    # path("routes/", RouteListCreate.as_view(), name="route-list"),
    # path("routes/<int:pk>/", RouteDetail.as_view(), name="route-detail"),
    path("layouts/", LayoutList.as_view(), name="layout-list"),
    path("layouts/<int:pk>/", LayoutDetail.as_view(), name="layout-detail"),
    path("layouts/<int:layout_id>/routes/", RouteListCreate.as_view()),
    path("layouts/<int:layout_id>/routes/<int:pk>/", RouteDetail.as_view()),
    path("holds/", HoldList.as_view(), name="hold-list"),
    path("holds/<int:pk>/", HoldDetail.as_view(), name="hold-detail"),
]
