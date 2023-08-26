from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin

from .modelmixins import AddressModelMixin, OrderItemModelMixin, OrderModelMixin

User = get_user_model()


class PaymentMethod(models.Model):
    class Meta:
        ordering = ("name",)
        db_table = "payment_method"

    def __str__(self):
        return self.name

    name = models.CharField(
        verbose_name=_("نام"),
        max_length=50,
    )
    provider = models.CharField(
        verbose_name=_("ارائه دهنده"),
        max_length=50,
        blank=True,
    )


class ShippingMethod(models.Model):
    class Meta:
        ordering = ("name",)
        db_table = "shipping_method"

    def __str__(self):
        return self.name

    name = models.CharField(
        verbose_name=_("نام"),
        max_length=50,
    )
    provider = models.CharField(
        verbose_name=_("ارائه دهنده"),
        max_length=50,
        blank=True,
    )
    cost = models.DecimalField(
        verbose_name=_("قیمت"),
        max_digits=10,
        decimal_places=3,
        default=0,
    )


class OrderStatus(models.Model):
    FAILED = 0
    SUCCESSFUL = 1
    PROCESSING = 2
    SENT = 3
    DELIVERED = 4

    ORDER_STATUS_CHOICES = (
        (FAILED, _("پرداخت ناموفق")),
        (SUCCESSFUL, _("پرداخت موفق")),
        (PROCESSING, _("در حال آماده سازی")),
        (SENT, _("ارسال شده")),
        (DELIVERED, _("تحویل داده شده")),
    )

    class Meta:
        ordering = ("status",)
        verbose_name_plural = "Order Statuses"
        db_table = "order_status"

    def __str__(self):
        return self.get_status_display()

    status = models.IntegerField(
        verbose_name=_("وضعیت سفارش"),
        choices=ORDER_STATUS_CHOICES,
    )


class Region(models.Model):
    class Meta:
        ordering = ("name",)
        db_table = "region"

    def __str__(self):
        return self.name

    name = models.CharField(
        verbose_name=_("استان"),
        max_length=50,
        unique=True,
    )


class City(models.Model):
    class Meta:
        ordering = ("name",)
        unique_together = ("region", "name")
        verbose_name_plural = "Cities"
        db_table = "city"

    def __str__(self):
        return f"{self.region}, {self.name}"

    region = models.ForeignKey(
        verbose_name="استان",
        related_name="cities",
        to=Region,
        on_delete=models.CASCADE,
        db_index=True,
    )
    name = models.CharField(
        verbose_name=_("شهر"),
        max_length=50,
        db_index=True,
    )


class Address(LifecycleModelMixin, AddressModelMixin, models.Model):
    class Meta:
        db_table = "address"
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return f"{self.city}, {self.address}"

    user = models.ForeignKey(
        verbose_name=_("کاربر"),
        related_name="addresses",
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
    )
    region = models.ForeignKey(
        verbose_name=_("استان"),
        to="Region",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
    )
    city = models.ForeignKey(
        verbose_name=_("شهر"),
        to="City",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
    )
    address = models.TextField(
        verbose_name=_("نشانی"),
        max_length=1000,
    )
    postal_code = models.CharField(
        verbose_name=_("کد پستی"),
        max_length=100,
    )
    house_number = models.CharField(
        verbose_name=_("شماره پلاک"),
        max_length=50,
        blank=True,
        null=True,
    )
    unit_number = models.CharField(
        verbose_name=_("شماره واحد"),
        max_length=50,
        blank=True,
        null=True,
    )
    receiver_first_name = models.CharField(
        verbose_name=_("نام گیرنده"),
        max_length=50,
        blank=True,
    )
    receiver_last_name = models.CharField(
        verbose_name=_("نام خانوادگی گیرنده"),
        max_length=50,
        blank=True,
    )
    phone_number = models.CharField(
        verbose_name=_("شماه تلفن"),
        max_length=50,
    )
    is_default = models.BooleanField(
        verbose_name="تنظیم به عنوان آدرس پیشفرض",
        default=False,
    )


class Order(LifecycleModelMixin, OrderModelMixin, models.Model):
    class Meta:
        ordering = ("-create_datetime",)
        db_table = "order"

    def __str__(self):
        return f"{self.user} | {self.payment_datetime}"

    order_code = models.BigIntegerField(
        verbose_name=_("کد سفارش"),
        editable=False,
        db_index=True,
    )
    tracking_code = models.CharField(
        verbose_name=_("کد رهگیری مرسوله پستی"),
        max_length=100,
        blank=True,
    )
    user = models.ForeignKey(
        verbose_name=_("کاربر"),
        related_name="orders",
        to=User,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
    )
    status = models.ForeignKey(
        verbose_name=_("وضعیت"),
        to="OrderStatus",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
    )
    address = models.ForeignKey(
        verbose_name=_("نشانی"),
        to="Address",
        on_delete=models.SET_NULL,
        null=True,
    )
    payment_method = models.ForeignKey(
        verbose_name=_("روش پرداخت"),
        to="PaymentMethod",
        on_delete=models.SET_NULL,
        null=True,
    )
    shipping_method = models.ForeignKey(
        verbose_name=_("روش ارسال"),
        to="ShippingMethod",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
    )
    tax_cost = models.DecimalField(
        verbose_name=_("هزینه مالیات"),
        max_digits=15,
        decimal_places=3,
        default=0,
    )
    shipping_cost = models.DecimalField(
        verbose_name=_("هزینه ارسال"),
        max_digits=10,
        decimal_places=3,
    )
    total_cost = models.DecimalField(
        verbose_name=_("مبلغ کل"),
        max_digits=18,
        decimal_places=3,
        default=0,
    )
    create_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان ایجاد"),
        auto_now_add=True,
    )
    payment_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان پرداخت"),
        blank=True,
        null=True,
    )
    delivery_datetime = models.DateTimeField(
        verbose_name=_("تاریخ و زمان تحویل"),
        blank=True,
        null=True,
    )


class OrderItem(LifecycleModelMixin, OrderItemModelMixin, models.Model):
    class Meta:
        unique_together = ("order", "product_item")
        db_table = "order_item"

    def __str__(self):
        return f"{self.name} | {self.order}"

    user = models.ForeignKey(
        verbose_name=_("کاربر"),
        to=User,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
    )
    order = models.ForeignKey(
        verbose_name=_("سفارش"),
        related_name="items",
        to="Order",
        on_delete=models.CASCADE,
        db_index=True,
    )
    product_item = models.ForeignKey(
        verbose_name=_("محصول"),
        to="products.ProductItem",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
    )
    name = models.CharField(
        verbose_name=_("نام"),
        max_length=255,
    )
    price = models.DecimalField(
        verbose_name=_("قیمت"),
        max_digits=15,
        decimal_places=3,
    )
    total_price = models.DecimalField(
        verbose_name=_("قیمت کل"),
        max_digits=18,
        decimal_places=3,
    )
    quantity = models.IntegerField(
        verbose_name=_("تعداد"),
        default=1,
    )
