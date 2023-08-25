from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from django_lifecycle import (
    AFTER_CREATE,
    BEFORE_CREATE,
    BEFORE_DELETE,
    LifecycleModelMixin,
    hook,
)

User = get_user_model()


class Comment(LifecycleModelMixin, models.Model):
    class Meta:
        ordering = ("-create_datetime",)
        unique_together = ("user", "product")
        db_table = "comment"

    # methods
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.text:20} ..."

    # hooks
    @hook(BEFORE_CREATE)
    def set_is_buyer(self):
        user_is_buyer = self.user.purchased_products.filter(
            product=self.product
        ).exists()
        if user_is_buyer:
            self.is_buyer = True

    @hook(AFTER_CREATE)
    def increase_comments_count(self):
        self.product.comments_count = F("comments_count") + 1
        self.product.save()

    @hook(BEFORE_DELETE)
    def decrease_comments_count(self):
        self.product.comments_count = F("comments_count") - 1
        self.product.save()

    # fields
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
            validators.MinValueValidator(0),
            validators.MaxValueValidator(5),
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
