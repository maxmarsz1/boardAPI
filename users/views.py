from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from django.contrib.auth import get_user_model

from users.serializers import CreateUserSerializer, UserDetailSerializer


@extend_schema(
    description="View used for user registration",
)
class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer


class DetailUserView(ListAPIView):
    model = get_user_model()
    serializer_class = UserDetailSerializer
