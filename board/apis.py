from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from board.selectors.hold import hold_get, hold_list
from board.selectors.route import route_list, route_get, route_get_by_layout_id
from board.selectors.layout import layout_list, layout_get


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
