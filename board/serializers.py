from rest_framework import serializers

from board.models import Layout, LayoutHold, Route, Hold, RouteHold
from users.serializers import UserDetailSerializer


class RouteHoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteHold
        fields = ["index", "type"]


class RouteDetailSerializer(serializers.ModelSerializer):
    hold_types = RouteHoldSerializer(many=True)
    owner = UserDetailSerializer(read_only=True)

    class Meta:
        model = Route
        fields = ["id", "name", "grade", "owner", "tilt", "hold_types"]


class RouteCreateSerializer(serializers.ModelSerializer):
    hold_types = RouteHoldSerializer(many=True)

    class Meta:
        model = Route
        fields = ["id", "name", "grade", "tilt", "hold_types"]

    def create(self, validated_data):
        holds_data = validated_data.pop("hold_types")
        route = Route.objects.create(**validated_data)
        for hold_data in holds_data:
            RouteHold.objects.create(route=route, **hold_data)
        return route


class RouteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ["id", "name", "grade"]


class LayoutListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layout
        fields = ["id", "name", "rows", "cols"]


class LayoutHoldSerializer(serializers.ModelSerializer):
    image = serializers.FilePathField(path="assets/holds/images", source="hold.image")

    class Meta:
        model = LayoutHold
        fields = ["id", "index", "rotation", "image"]


class LayoutDetailSerializer(serializers.ModelSerializer):
    holds = LayoutHoldSerializer(source="layout_holds", many=True, read_only=True)

    class Meta:
        model = Layout
        fields = ["id", "name", "rows", "cols", "holds"]


class HoldListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hold
        fields = ["id", "name", "image"]


class HoldCreateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hold
        fields = ["id", "name", "model_file", "owner", "image"]
        read_only_fields = ["image", "owner"]
