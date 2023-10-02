from django.db import IntegrityError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    def get_user_url(self, comment) -> str:
        return reverse(
            viewname="users:user_detail_update_delete",
            kwargs={"username": comment.user.username},
        )

    absolute_url = serializers.CharField(
        source="get_absolute_url",
        read_only=True,
    )
    user_url = serializers.SerializerMethodField(
        method_name="get_user_url",
    )
    product_url = serializers.CharField(
        source="product.get_absolute_url",
        read_only=True,
    )
    full_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )


class CommentListSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "full_name",
            "absolute_url",
            "user",
            "user_url",
            "product",
            "product_url",
            "published",
            "is_buyer",
            "likes_count",
            "create_datetime",
            "update_datetime",
        )

        extra_kwargs = {
            "user": {
                "write_only": True,
            },
            "product": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        try:
            if not validated_data["user"]:
                user = self.context["request"].user
                validated_data["user"] = user
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(_("شما قبلا دیدگاه خود را ثبت کرده‌اید"))


class CommentDetailSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

        extra_kwargs = {
            "user": {
                "write_only": True,
            },
            "product": {
                "write_only": True,
            },
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation.move_to_end("likes_count")
        representation.move_to_end("create_datetime")
        representation.move_to_end("update_datetime")

        return representation
