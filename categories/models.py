from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Index
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_lifecycle import (
    AFTER_DELETE,
    AFTER_SAVE,
    BEFORE_SAVE,
    LifecycleModelMixin,
    hook,
)


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


class Category(LifecycleModelMixin, TimeStamp):
    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"
        db_table = "category"

        unique_together = (
            ("parent_category", "name"),
            ("parent_category", "url"),
        )

        indexes = (Index(Lower("name"), name="lower_category_name_idx"),)

    # methods
    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse(
            viewname="categories:category_detail_update_delete",
            kwargs={"category_id": self.pk},
        )

    def validate_unique(self, exclude):
        other_categories = self._meta.model.objects.exclude(id=self.id)
        category = other_categories.filter(parent_category=None, url=self.url)

        if category.exists() and self.parent_category is None:
            raise ValidationError(message=_("لینک این دسته‌بندی قبلا استفاده شده است"))

        return super().validate_unique(exclude)

    def clean(self, serializer_parent_category=None):
        if (self == self.parent_category) or (self == serializer_parent_category):
            raise ValidationError(_("یک دسته‌بندی نمی‌تواند زیردسته خودش باشد"))

    # hooks
    @hook(BEFORE_SAVE)
    def set_metadate(self):
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.description

    @hook(BEFORE_SAVE)
    def set_url(self):
        if not self.url:
            self.url = slugify(value=self.name, allow_unicode=True)

    @hook(BEFORE_SAVE)
    def set_full_name(self):
        if self.parent_category:
            self.full_name = f"{self.parent_category.full_name} / {self.name}"
        else:
            self.full_name = self.name

    @hook(AFTER_SAVE, when="full_name", has_changed=True)
    def change_subcategories_full_name(self):
        [subcategory.save() for subcategory in self.subcategories.all()]

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def clear_cache(self):
        cache.delete(key=f"category_{self.id}")
        cache.delete(key="categories_queryset")

    # fields
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
