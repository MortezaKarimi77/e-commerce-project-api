from django.db import models
from django.db.models import Index
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin

from core.models import TimeStamp

from .modelmixins import CategoryModelMixin


class Category(LifecycleModelMixin, CategoryModelMixin, TimeStamp):
    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"
        db_table = "category"

        unique_together = (
            ("parent_category", "name"),
            ("parent_category", "url"),
        )

        indexes = (Index(Lower("name"), name="lower_category_name_idx"),)

    parent_category = models.ForeignKey(
        verbose_name="دسته‌بندی والد",
        related_name="subcategories",
        to="Category",
        on_delete=models.PROTECT,
        db_index=True,
        blank=True,
        null=True,
    )
    name = models.CharField(
        verbose_name=_("نام"),
        max_length=100,
    )
    full_name = models.CharField(
        verbose_name=_("نام کامل"),
        max_length=255,
        editable=False,
        blank=True,
    )
    url = models.SlugField(
        verbose_name=_("لینک"),
        max_length=100,
        allow_unicode=True,
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
    media_folder_name = models.CharField(
        verbose_name=_("نام پوشه مدیا"),
        max_length=100,
    )
