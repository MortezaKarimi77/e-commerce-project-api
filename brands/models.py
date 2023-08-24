from django.core.cache import cache
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
    BEFORE_UPDATE,
    LifecycleModelMixin,
    hook,
)


class Brand(LifecycleModelMixin, models.Model):
    class Meta:
        ordering = ("name",)
        db_table = "brand"

        indexes = (
            Index(Lower("name"), name="lower_brand_name_idx"),
            Index(Lower("country"), name="lower_brand_country_idx"),
        )

    # methods
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="brands:brand_detail_update_delete",
            kwargs={"brand_url": self.url},
        )

    def get_upload_path(self, filename) -> str:
        brand_name = self.url.replace("-", " ").strip()
        return f"brands/{brand_name}/{filename}"

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

    @hook(BEFORE_UPDATE, when="main_image", has_changed=True)
    def delete_old_image(self):
        old_image = self._meta.model.objects.get(id=self.id).main_image
        old_image.delete(save=False)

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def clear_cache(self):
        cache.delete(key=f"brand_{self.url}")
        cache.delete(key="brands_queryset")

    # fields
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
        upload_to=get_upload_path,
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
