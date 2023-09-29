from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class WishList(models.Model):
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

    class Meta:
        ordering = ("-id",)
        unique_together = ("user", "product")
        db_table = "wishlist"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.product.name}"


class PurchasedProducts(models.Model):
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

    class Meta:
        ordering = ("-id",)
        unique_together = ("user", "product")
        verbose_name_plural = "Purchased Products"
        db_table = "purchased_products"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.product.name}"
