from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin

from core.models import TimeStamp
from core.utils import product_directory_path

from .managers import ProductManager
from .modelmixins import ProductItemModelMixin, ProductModelMixin

User = get_user_model()


class Product(LifecycleModelMixin, ProductModelMixin, TimeStamp):
    VISIBLE, AVAILABLE = True, True
    INVISIBLE, UNAVAILABLE = False, False

    VISIBILITY_CHOICES = (
        (VISIBLE, _("نمایش داده شود")),
        (INVISIBLE, _("نمایش داده نشود")),
    )
    AVAILABILITY_CHOICES = (
        (AVAILABLE, _("موجود")),
        (UNAVAILABLE, _("ناموجود")),
    )

    class Meta:
        ordering = ("-is_visible", "-is_available", "-id")
        db_table = "product"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            viewname="products:product_detail_update_delete",
            kwargs={"category_id": self.category.id, "product_url": self.url},
        )

    objects = ProductManager()

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
    cheapest_product_item = models.OneToOneField(
        verbose_name=_("ارزان‌ترین محصول"),
        related_name="cheapest_product",
        to="ProductItem",
        on_delete=models.SET_NULL,
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
        upload_to=product_directory_path,
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
            MinValueValidator(0),
            MaxValueValidator(5),
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


class ProductItem(LifecycleModelMixin, ProductItemModelMixin, models.Model):
    VISIBLE, AVAILABLE = True, True
    INVISIBLE, UNAVAILABLE = False, False

    VISIBILITY_CHOICES = (
        (VISIBLE, _("نمایش داده شود")),
        (INVISIBLE, _("نمایش داده نشود")),
    )
    AVAILABILITY_CHOICES = (
        (AVAILABLE, _("موجود")),
        (UNAVAILABLE, _("ناموجود")),
    )

    class Meta:
        ordering = ("-is_visible", "-is_available", "-id")
        db_table = "product_item"

    def __str__(self):
        return f"{self.product} | {self.selling_price}"

    def get_absolute_url(self):
        return reverse(
            "products:product_item_detail_update_delete",
            kwargs={"product_item_id": self.id},
        )

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
    IMAGE = 1
    VIDEO = 2

    MEDIA_TYPE_CHOICES = (
        (IMAGE, _("عکس")),
        (VIDEO, _("فیلم")),
    )

    class Meta:
        ordering = ("-id",)
        db_table = "product_media"

    def __str__(self):
        return f"{self.product} | {self.file}"

    def get_absolute_url(self):
        return reverse(
            "products:product_media_detail_update_delete",
            kwargs={"product_media_id": self.id},
        )

    product = models.ForeignKey(
        verbose_name=_("محصول"),
        related_name="media_files",
        to="Product",
        on_delete=models.CASCADE,
        db_index=True,
    )
    file = models.FileField(
        verbose_name="فایل",
        upload_to=product_directory_path,
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

    def __str__(self):
        return f"{self.category.full_name} - {self.name}"

    def get_absolute_url(self):
        return reverse(
            "products:attribute_detail_update_delete",
            kwargs={"attribute_id": self.id},
        )

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
