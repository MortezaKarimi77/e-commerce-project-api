from django.db import models
from django.utils.translation import gettext_lazy as _


class Promotion(models.Model):
    class Meta:
        ordering = ("-end_datetime",)
        db_table = "promotion"

    def __str__(self):
        return f"{self.name} - {self.discount_rate}%"

    category = models.ManyToManyField(
        verbose_name=_("دسته‌بندی"),
        to="categories.Category",
    )
    name = models.CharField(
        verbose_name=_("نام"),
        max_length=100,
        unique=True,
    )
    description = models.CharField(
        verbose_name=_("توضیحات"),
        max_length=255,
        blank=True,
    )
    discount_rate = models.IntegerField(
        verbose_name=_("درصد تخفیف"),
        default=0,
    )
    create_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان ایجاد"),
        auto_now_add=True,
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان آغاز"),
    )
    end_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان پایان"),
    )
