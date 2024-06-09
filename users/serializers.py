from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"].lower(), username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove the password field from the representation
        representation.pop("password", None)
        return representation


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"
        read_only_fields = ("from_user", "status")
