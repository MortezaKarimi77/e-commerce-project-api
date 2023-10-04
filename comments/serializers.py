from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )
    absolute_url = serializers.SerializerMethodField(
        method_name="get_absolute_url",
    )
    user_url = serializers.SerializerMethodField(
        method_name="get_user_url",
    )
    product_url = serializers.SerializerMethodField(
        source="get_product_url",
    )

    def get_absolute_url(self, comment) -> str:
        return reverse(
            viewname="comments:comment_detail_update_delete",
            request=self.context.get("request"),
            kwargs={"comment_id": comment.id},
        )

    def get_user_url(self, comment) -> str:
        return reverse(
            viewname="users:user_detail_update_delete",
            request=self.context.get("request"),
            kwargs={"username": comment.user.username},
        )

    def get_product_url(self, comment) -> str:
        return reverse(
            viewname="products:product_detail_update_delete",
            request=self.context.get("request"),
            kwargs={
                "category_id": comment.product.category.id,
                "product_url": comment.product.url,
            },
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
            raise serializers.ValidationError(
                detail=_("شما قبلا دیدگاه خود را ثبت کرده‌اید")
            )


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


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

        extra_kwargs = {
            "user": {
                "read_only": True,
            },
            "comment": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        try:
            validated_data["user"] = self.context.get("user")
            validated_data["comment"] = self.context.get("comment")
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                detail=_("شما قبلا این دیدگاه را لایک کرده‌اید")
            )
