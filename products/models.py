from django.contrib.auth import get_user_model
from django.core import validators
from django.core.cache import cache
from django.db import models
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

from .managers import ProductManager

VISIBILITY_CHOICES = (
    (True, _("نمایش داده شود")),
    (False, _("نمایش داده نشود")),
)

AVAILABILITY_CHOICES = (
    (True, _("موجود")),
    (False, _("ناموجود")),
)

MEDIA_TYPE_CHOICES = (
    (1, _("عکس")),
    (2, _("فیلم")),
)

User = get_user_model()


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


class Product(LifecycleModelMixin, TimeStamp):
    class Meta:
        ordering = ("-is_visible", "-is_available", "-id")
        db_table = "product"

    objects = ProductManager()

    # methods
    def __str__(self):
        return self.name

    def get_upload_path(self, filename):
        category = self.category.media_folder_name
        product = self.url.replace("-", " ").strip()
        return f"products/{category}/{product}/{filename}"

    def get_absolute_url(self):
        return reverse(
            viewname="products:product_detail_update_delete",
            kwargs={"category_id": self.category.id, "product_url": self.url},
        )

    # hooks
    @hook(BEFORE_SAVE)
    def set_metadate(self):
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.introduction

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
        cache.delete(key="all_products")
        cache.delete(key="visible_products")
        cache.delete(key="brand_products")
        cache.delete(key=f"product_{self.url}")
        cache.delete(key=f"category_{self.category.id}_products")

    # fields
    category = models.ForeignKey(
        verbose_name=_("دسته‌بندی"),
        related_name="products",
        to="categories.Category",
        on_delete=models.PROTECT,
        db_index=True,
    )
    brand = models.ForeignKey(
        verbose_name=_("برند"),
        related_name="products",
        to="brands.Brand",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True,
    )
    name = models.CharField(
        verbose_name=_("نام"),
        max_length=255,
        unique=True,
    )
    url = models.SlugField(
        verbose_name=_("لینک"),
        max_length=255,
        unique=True,
        allow_unicode=True,
        blank=True,
    )
    introduction = models.TextField(
        verbose_name=_("معرفی"),
        blank=True,
    )
    review = models.TextField(
        verbose_name=_("نقد و بررسی"),
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
        verbose_name=_("تصویر اصلی"),
        upload_to=get_upload_path,
    )
    is_available = models.BooleanField(
        verbose_name=_("وضعیت موجودی"),
        default=False,
        db_index=True,
        choices=AVAILABILITY_CHOICES,
    )
    is_visible = models.BooleanField(
        verbose_name=_("وضعیت نمایش"),
        default=False,
        db_index=True,
        choices=VISIBILITY_CHOICES,
    )
    dimension = models.CharField(
        verbose_name=_("ابعاد"),
        max_length=255,
        blank=True,
    )
    weight = models.CharField(
        verbose_name=_("وزن"),
        max_length=255,
        blank=True,
    )
    included_items = models.TextField(
        verbose_name=_("اقلام همراه"),
        blank=True,
    )
    other_features = models.TextField(
        verbose_name=_("ویژگی‌های دیگر"),
        blank=True,
    )
    other_description = models.TextField(
        verbose_name=_("سایر توضیحات"),
        blank=True,
    )
    rating = models.FloatField(
        verbose_name=_("امتیاز"),
        default=0,
        editable=False,
        validators=(
            validators.MinValueValidator(0),
            validators.MaxValueValidator(5),
        ),
    )
    comments_count = models.IntegerField(
        verbose_name=_("تعداد نظرات"),
        default=0,
        editable=False,
    )
    views_count = models.IntegerField(
        verbose_name=_("تعداد بازدیدها"),
        default=0,
        editable=False,
    )
    sold_count = models.IntegerField(
        verbose_name=_("تعداد فروخته شده"),
        default=0,
        editable=False,
    )


class ProductItem(LifecycleModelMixin, models.Model):
    class Meta:
        ordering = ("-is_visible", "-is_available", "-id")
        db_table = "product_item"

    # methods
    def __str__(self):
        return f"{self.product} | {self.selling_price}"

    def get_absolute_url(self):
        return reverse(
            "products:product_item_detail_update_delete",
            kwargs={"product_item_id": self.id},
        )

    # hooks
    @hook(BEFORE_SAVE)
    def set_selling_price(self):
        if not self.selling_price:
            self.selling_price = self.original_price

    # fields
    product = models.ForeignKey(
        verbose_name=_("محصول"),
        related_name="items",
        to="Product",
        on_delete=models.CASCADE,
        db_index=True,
    )
    configuration = models.ManyToManyField(
        verbose_name=_("پیکربندی"),
        to="AttributeValue",
        db_table="product_item_configuration",
    )
    sku = models.CharField(
        verbose_name=_("شناسه کالا"),
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )
    original_price = models.DecimalField(
        verbose_name=_("قیمت اصلی"),
        max_digits=15,
        decimal_places=3,
        default=0,
    )
    selling_price = models.DecimalField(
        verbose_name=_("قیمت فروش"),
        max_digits=15,
        decimal_places=3,
        default=0,
    )
    inventory = models.PositiveIntegerField(
        verbose_name=_("موجودی انبار"),
        default=0,
    )
    is_available = models.BooleanField(
        verbose_name=_("وضعیت موجودی"),
        default=False,
        db_index=True,
        choices=AVAILABILITY_CHOICES,
    )
    is_visible = models.BooleanField(
        verbose_name=_("وضعیت نمایش"),
        default=False,
        db_index=True,
        choices=VISIBILITY_CHOICES,
    )


class ProductMedia(LifecycleModelMixin, models.Model):
    class Meta:
        ordering = ("-id",)
        db_table = "product_media"

    # methods
    def __str__(self):
        return f"{self.product} | {self.file}"

    def get_upload_path(self, filename):
        category = self.product.category.media_folder_name
        product = self.product.url.replace("-", " ").strip()
        return f"products/{category}/{product}/{filename}"

    def get_absolute_url(self):
        return reverse(
            "products:product_media_detail_update_delete",
            kwargs={"product_media_id": self.id},
        )

    # hooks
    @hook(BEFORE_UPDATE, when="file", has_changed=True)
    def delete_old_file(self):
        old_file = self._meta.model.objects.get(id=self.id).file
        old_file.delete(save=False)

    # fields
    product = models.ForeignKey(
        verbose_name=_("محصول"),
        related_name="media_files",
        to="Product",
        on_delete=models.CASCADE,
        db_index=True,
    )
    file = models.FileField(
        verbose_name="فایل",
        upload_to=get_upload_path,
    )
    type = models.IntegerField(
        verbose_name=_("نوع فایل"),
        choices=MEDIA_TYPE_CHOICES,
    )
    alternate_text = models.CharField(
        verbose_name=_("متن جایگزین"),
        max_length=255,
        blank=True,
    )


class Attribute(models.Model):
    class Meta:
        ordering = ("name",)
        db_table = "attribute"

    # methods
    def __str__(self):
        return f"{self.category.full_name} - {self.name}"

    def get_absolute_url(self):
        return reverse(
            "products:attribute_detail_update_delete",
            kwargs={"attribute_id": self.id},
        )

    # fields
    category = models.ForeignKey(
        verbose_name=_("دسته‌بندی"),
        related_name="attributes",
        to="categories.Category",
        on_delete=models.PROTECT,
        db_index=True,
    )
    name = models.CharField(
        verbose_name=_("نام"),
        max_length=50,
        unique=True,
    )


class AttributeValue(models.Model):
    class Meta:
        ordering = ("attribute",)
        db_table = "attribute_value"

    # methods
    def __str__(self):
        model_fields = self._meta.get_fields()

        for field in model_fields:
            if not field.is_relation:
                field_name = field.name
                field_value = getattr(self, field_name)
                if field_value and field_name != "id":
                    break

        return f"{self.attribute}: {field_value}"

    def get_absolute_url(self):
        return reverse(
            "products:attribute_value_detail_update_delete",
            kwargs={"attribute_value_id": self.id},
        )

    # fields
    attribute = models.ForeignKey(
        verbose_name=_("ویژگی"),
        related_name="values",
        to="Attribute",
        on_delete=models.PROTECT,
        db_index=True,
    )
    char_value = models.CharField(
        verbose_name=_("متن کوتاه (حداکثر ۲۵۵ کاراکتر)"),
        max_length=255,
        blank=True,
        null=True,
    )
    text_value = models.TextField(
        verbose_name=_("متن بلند"),
        blank=True,
        null=True,
    )
    int_value = models.IntegerField(
        verbose_name=_("عدد صحیح"),
        blank=True,
        null=True,
    )
    decimal_value = models.DecimalField(
        verbose_name=_("عدد اعشاری"),
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
    )
    date_value = models.DateField(
        verbose_name=_("تاریخ"),
        blank=True,
        null=True,
    )
    time_value = models.TimeField(
        verbose_name=_("زمان"),
        blank=True,
        null=True,
    )
