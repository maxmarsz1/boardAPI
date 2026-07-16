from rest_framework import generics
from rest_framework.exceptions import NotFound, ValidationError
from board.models import Route, Layout, Hold
from board.serializers import (
    HoldCreateDetailSerializer,
    HoldListSerializer,
    LayoutDetailSerializer,
    LayoutListCreateSerializer,
    RouteCreateSerializer,
    RouteDetailSerializer,
    RouteListSerializer,
)
from board_api.permissions import IsOwnerOrReadOnly


def get_layout(layout_id):
    if layout_id is not None:
        try:
            layout = Layout.objects.get(pk=layout_id)
            return layout
        except Layout.DoesNotExist:
            raise NotFound(f"layout with specified layout_id not found {layout_id}")
    return None


class RouteListCreate(generics.ListCreateAPIView):
    queryset = Route.objects.all()

    def get_queryset(self):
        layout_id = self.kwargs.get("layout_id")
        layout = get_layout(layout_id)
        if layout:
            return layout.layout_routes
        return Route.objects.all()

    def get_serializer_class(self):  # type: ignore
        if self.request.method == "POST":
            return RouteCreateSerializer
        return RouteListSerializer

    def perform_create(self, serializer):
        layout_id = self.kwargs.get("layout_id")
        layout = get_layout(layout_id)

        holds_indexes = [
            hold_type["index"] for hold_type in serializer.validated_data["hold_types"]
        ]
        # layout = serializer.validated_data["layout"]
        layout_max_index = layout.rows * layout.cols - 1

        # checking if holds indexes are in bounds of layout grid
        for hold_index in holds_indexes:
            if hold_index > layout_max_index:
                raise ValidationError(
                    f"hold index out of range: {hold_index}/{layout_max_index}"
                )

        # checking if holds have unique indexes
        if len(set(holds_indexes)) != len(holds_indexes):
            raise ValidationError("holds indexes must be unique within one route")

        # appending route author and layout
        serializer.save(owner=self.request.user, layout=layout)


class RouteDetail(generics.RetrieveDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        layout_id = self.kwargs.get("layout_id")
        layout = Layout.objects.get(pk=layout_id)
        return layout.layout_routes


class LayoutList(generics.ListCreateAPIView):
    queryset = Layout.objects.all()
    serializer_class = LayoutListCreateSerializer


class LayoutDetail(generics.RetrieveAPIView):
    queryset = Layout.objects.all()
    serializer_class = LayoutDetailSerializer


class HoldList(generics.ListCreateAPIView):
    queryset = Hold.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return HoldCreateDetailSerializer
        return HoldListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HoldDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hold.objects.all()
    serializer_class = HoldCreateDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
