from django.db import models
from django.db.models import Index
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin

from core.utils import brand_directory_path

from .modelmixins import BrandModelMixin


class Brand(LifecycleModelMixin, BrandModelMixin, models.Model):
    class Meta:
        ordering = ("name",)
        db_table = "brand"

        indexes = (
            Index(Lower("name"), name="lower_brand_name_idx"),
            Index(Lower("country"), name="lower_brand_country_idx"),
        )

    name = models.CharField(
        verbose_name=_("نام"),
        max_length=100,
        unique=True,
    )
    url = models.SlugField(
        verbose_name=_("لینک"),
        max_length=100,
        unique=True,
        blank=True,
    )
    country = models.CharField(
        verbose_name=_("کشور"),
        max_length=30,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("توضیحات"),
        blank=True,
    )
    meta_title = models.CharField(
        verbose_name=_("عنوان متا"),
        max_length=255,
        blank=True,
    )
    meta_description = models.TextField(
        verbose_name=_("توضیحات متا"),
        blank=True,
    )
    main_image = models.ImageField(
        verbose_name=_("تصویر"),
        upload_to=brand_directory_path,
        blank=True,
    )
    create_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان ایجاد"),
        auto_now_add=True,
    )
    update_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان آخرین ویرایش"),
        auto_now=True,
    )
