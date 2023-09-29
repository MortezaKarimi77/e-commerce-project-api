from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin

from .modelmixins import CommentModelMixin

User = get_user_model()


class Comment(LifecycleModelMixin, CommentModelMixin, models.Model):
    user = models.ForeignKey(
        verbose_name=_("کاربر"),
        related_name="comments",
        to=User,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        verbose_name=_("محصول"),
        related_name="comments",
        to="products.Product",
        on_delete=models.CASCADE,
    )
    like = models.IntegerField(
        verbose_name=_("تعداد لایک"),
        default=0,
        editable=False,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(5),
        ),
    )
    text = models.TextField(
        verbose_name=_("متن دیدگاه"),
        max_length=2000,
    )
    is_buyer = models.BooleanField(
        verbose_name="خریدار",
        default=False,
    )
    create_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان ایجاد"),
        auto_now_add=True,
    )
    update_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان آخرین ویرایش"),
        auto_now=True,
    )

    class Meta:
        ordering = ("-create_datetime",)
        unique_together = ("user", "product")
        db_table = "comment"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.text:20} ..."
