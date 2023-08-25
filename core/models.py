from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStamp(models.Model):
    class Meta:
        abstract = True

    create_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان ایجاد"),
        auto_now_add=True,
    )
    update_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان آخرین ویرایش"),
        auto_now=True,
    )
