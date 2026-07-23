from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView, status

from board.selectors.hold import hold_get, hold_list
from board.selectors.route import route_list, route_get, route_get_by_layout_id
from board.selectors.layout import layout_list, layout_get
from board.services.hold import hold_create
from board.services.layout import layout_assign_hold, layout_create


class HoldListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        image = serializers.CharField()

    def get(self, request):
        holds = hold_list()

        data = self.OutputSerializer(holds, many=True).data

        return Response(data)


class HoldDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        image = serializers.CharField()
        owner = serializers.CharField()
        model_file = serializers.CharField()

    def get(self, request, hold_id):
        hold = hold_get(pk=hold_id)
        print(hold_id)
        print(hold)

        serializer = self.OutputSerializer(hold)

        return Response(serializer.data)


class HoldCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        model_file = serializers.FileField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hold_create(owner=request.user, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class RouteListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        grade = serializers.CharField()
        owner = serializers.CharField()
        layout = serializers.CharField()

    def get(self, request):
        routes = route_list()

        data = self.OutputSerializer(routes, many=True).data

        return Response(data)


class RouteDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        grade = serializers.CharField()
        owner = serializers.CharField()
        layout = serializers.CharField()

    def get(self, request, route_id):
        route = route_get(pk=route_id)

        serializer = self.OutputSerializer(route)

        return Response(serializer.data)


class LayoutListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        rows = serializers.CharField()
        cols = serializers.CharField()
        preview_image = serializers.CharField()

    def get(self, request):
        layouts = layout_list()

        data = self.OutputSerializer(layouts, many=True).data

        return Response(data)


class LayoutDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        rows = serializers.CharField()
        cols = serializers.CharField()
        preview_image = serializers.CharField()

    def get(self, request, layout_id):
        layout = layout_get(pk=layout_id)

        serializer = self.OutputSerializer(layout)

        return Response(serializer.data)


class LayoutCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        rows = serializers.CharField()
        cols = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        layout = layout_create(**input_serializer.data)

        output_serializer = self.OutputSerializer(layout)
        return Response(output_serializer.data)


class LayoutRouteListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        grade = serializers.CharField()
        owner = serializers.CharField()
        layout = serializers.CharField()

    def get(self, request, layout_id):
        routes = route_get_by_layout_id(layout_id)

        data = self.OutputSerializer(routes, many=True).data

        return Response(data)


class LayoutHoldAssignApi(APIView):
    class InputSerializer(serializers.Serializer):
        hold_id = serializers.CharField()
        index = serializers.CharField()
        rotation = serializers.IntegerField()

    def post(self, request, layout_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        layout_assign_hold(layout_id=layout_id, **serializer.data)

        return Response(status=status.HTTP_201_CREATED)
