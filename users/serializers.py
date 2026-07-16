from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}

    def create(self, validated_data):
        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email"]
