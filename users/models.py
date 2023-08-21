from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class WishList(models.Model):
    class Meta:
        ordering = ("-id",)
        unique_together = ("user", "product")
        db_table = "wishlist"

    # methods
    def __str__(self):
        return f"{self.user_full_name} - {self.product.name}"

    @property
    def user_full_name(self):
        return self.user.get_full_name()

    # fields
    user = models.ForeignKey(
        verbose_name=_("کاربر"),
        related_name="wishlist",
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
    )
    product = models.ForeignKey(
        verbose_name=_("محصول"),
        to="products.Product",
        on_delete=models.CASCADE,
    )


class PurchasedProducts(models.Model):
    class Meta:
        ordering = ("-id",)
        unique_together = ("user", "product")
        verbose_name_plural = "Purchased Products"
        db_table = "purchased_products"

    # methods
    def __str__(self):
        return f"{self.user_full_name} - {self.product.name}"

    @property
    def user_full_name(self):
        return self.user.get_full_name()

    # fields
    user = models.ForeignKey(
        verbose_name=_("کاربر"),
        related_name="purchased_products",
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
    )
    product = models.ForeignKey(
        verbose_name=_("محصول"),
        related_name="sold_items",
        to="products.Product",
        on_delete=models.CASCADE,
    )
