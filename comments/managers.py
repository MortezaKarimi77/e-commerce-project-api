from django.db import IntegrityError, models
from django.db.models import Exists, OuterRef
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


class CommentManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user", "product", "product__category")
        return queryset

    def all_product_comments(self, user, product):
        queryset = self.filter(product=product)

        if user.is_authenticated:
            from .models import Like

            likes = Like.objects.filter(user=user, comment=OuterRef("id"))
            queryset = queryset.annotate(liked_by_user=Exists(likes))

        return queryset

    def published_product_comments(self, user, product):
        queryset = self.filter(product=product, published=True)

        if user.is_authenticated:
            from .models import Like

            likes = Like.objects.filter(user=user, comment=OuterRef("id"))
            queryset = queryset.annotate(liked_by_user=Exists(likes))

        return queryset

    def user_comments(self, user):
        queryset = self.filter(user=user)
        return queryset


class LikeManager(models.Manager):
    def create_like(self, validated_data):
        try:
            like = self.create(**validated_data)
            return like
        except IntegrityError:
            raise ValidationError(detail=_("شما قبلا این دیدگاه را لایک کرده‌اید"))
