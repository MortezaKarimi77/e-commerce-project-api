from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


class LikeManager(models.Manager):
    def create_like(self, validated_data):
        try:
            like = self.create(**validated_data)
            return like
        except IntegrityError:
            raise ValidationError(detail=_("شما قبلا این دیدگاه را لایک کرده‌اید"))
