from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


class CommentManager(models.Manager):
    def create_comment(self, user, validated_data):
        try:
            if not validated_data["user"]:
                validated_data["user"] = user
            comment = self.create(**validated_data)
            return comment
        except IntegrityError:
            raise ValidationError(detail=_("شما قبلا دیدگاه خود را ثبت کرده‌اید"))
