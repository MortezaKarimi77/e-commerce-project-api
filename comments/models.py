from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin

from core.models import TimeStamp

from .managers import CommentManager
from .modelmixins import CommentModelMixin, LikeModelMixin

User = get_user_model()


class Comment(LifecycleModelMixin, CommentModelMixin, TimeStamp):
    user = models.ForeignKey(
        verbose_name=_("کاربر"),
        related_name="comments",
        to=User,
        on_delete=models.CASCADE,
        null=True,
    )
    product = models.ForeignKey(
        verbose_name=_("محصول"),
        related_name="comments",
        to="products.Product",
        on_delete=models.CASCADE,
    )
    likes_count = models.PositiveIntegerField(
        verbose_name=_("تعداد لایک‌ها"),
        default=0,
        editable=False,
    )
    text = models.TextField(
        verbose_name=_("متن دیدگاه"),
        max_length=2000,
    )
    is_buyer = models.BooleanField(
        verbose_name="خریدار",
        default=False,
    )
    published = models.BooleanField(
        verbose_name="وضعیت انتشار",
        default=True,
    )

    objects = CommentManager()

    class Meta:
        ordering = ("-create_datetime",)
        unique_together = ("user", "product")
        db_table = "comment"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.product.name} - {self.text:20} ..."

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="comments:comment_detail_update_delete",
            kwargs={"comment_id": self.id},
        )

    def unique_error_message(self, model_class, unique_check):
        if unique_check == ("user", "product"):
            raise ValidationError(message=_("شما قبلا دیدگاه خود را ثبت کرده‌اید"))
        else:
            return super().unique_error_message(model_class, unique_check)


class Like(LifecycleModelMixin, LikeModelMixin, models.Model):
    comment = models.ForeignKey(
        verbose_name=_("دیدگاه"),
        related_name="likes",
        to=Comment,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name=_("کاربر"),
        to=User,
        on_delete=models.CASCADE,
    )
    create_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان ایجاد"),
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-create_datetime",)
        unique_together = ("user", "comment")
        db_table = "like"

    def __str__(self):
        return f"{self.user.username} liked {self.comment.text:20} ..."

    def unique_error_message(self, model_class, unique_check):
        if unique_check == ("user", "comment"):
            raise ValidationError(message=_("شما قبلا این دیدگاه را لایک کرده‌اید"))
        else:
            return super().unique_error_message(model_class, unique_check)
