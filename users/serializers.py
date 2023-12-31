from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as SimpleJwtTokenObtainPairSerializer,
)

User = get_user_model()


class TokenObtainPairSerializer(SimpleJwtTokenObtainPairSerializer):
    def validate(self, data):
        data = super().validate(data)
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["full_name"] = self.user.get_full_name()
        return data


class UserBaseSerializer(serializers.ModelSerializer):
    absolute_url = serializers.HyperlinkedIdentityField(
        view_name="users:user_detail_update_delete",
        lookup_url_kwarg="username",
        lookup_field="username",
    )

    def update(self, instance, validated_data):
        password = validated_data.get("password")
        if password:
            validated_data["password"] = make_password(password=password)
        return super().update(instance, validated_data)


class UserListSerializer(UserBaseSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "full_name",
            "first_name",
            "last_name",
            "is_superuser",
            "is_staff",
            "is_active",
            "absolute_url",
        )

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "full_name": {
                "read_only": True,
                "source": "get_full_name",
            },
            "first_name": {
                "write_only": True,
            },
            "last_name": {
                "write_only": True,
            },
            "is_superuser": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class PrivateUserDetailSerializer(UserBaseSerializer):
    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.move_to_end("absolute_url")
        return representation


class PublicUserDetailSerializer(UserBaseSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "full_name",
            "first_name",
            "last_name",
            "absolute_url",
        )

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "full_name": {
                "read_only": True,
                "source": "get_full_name",
            },
            "first_name": {
                "write_only": True,
            },
            "last_name": {
                "write_only": True,
            },
        }
