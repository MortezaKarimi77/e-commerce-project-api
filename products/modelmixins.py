from django.core.cache import cache
from django.utils.text import slugify
from django_lifecycle import (
    AFTER_CREATE,
    AFTER_DELETE,
    AFTER_SAVE,
    BEFORE_SAVE,
    BEFORE_UPDATE,
    hook,
)

from core import cache_key_schema


class ProductModelMixin:
    @hook(BEFORE_SAVE)
    def find_cheapest_product_item(self):
        cheapest_product_item = (
            self.items.filter(
                inventory__gt=0,
                is_visible=True,
                is_available=True,
            )
            .order_by("selling_price")
            .first()
        )
        if cheapest_product_item:
            self.cheapest_product_item = cheapest_product_item
        else:
            self.cheapest_product_item = None

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
        category, brand = self.category, self.brand
        cache.delete_many(
            keys=(
                cache_key_schema.all_products(),
                cache_key_schema.visible_products(),
                cache_key_schema.single_product(self.url),
                cache_key_schema.category_all_products(category.id),
                cache_key_schema.category_visible_products(category.id),
                cache_key_schema.brand_all_products(brand.url if brand else None),
                cache_key_schema.brand_visible_products(brand.url if brand else None),
            )
        )


class ProductItemModelMixin:
    @hook(AFTER_CREATE)
    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def update_cheapest_product_item(self):
        self.product.save()

    @hook(BEFORE_SAVE)
    def set_selling_price(self):
        if not self.selling_price:
            self.selling_price = self.original_price

    @hook(BEFORE_SAVE)
    def set_availability(self):
        if self.inventory == 0:
            self.is_available = False

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def clear_cache(self):
        product = self.product
        cache.delete_many(
            keys=(
                cache_key_schema.all_product_items(),
                cache_key_schema.single_product_item(self.id),
                cache_key_schema.all_products(),
                cache_key_schema.visible_products(),
                cache_key_schema.single_product(product.url),
            )
        )


class ProductMediaModelMixin:
    @hook(BEFORE_UPDATE, when="file", has_changed=True)
    def delete_old_file(self):
        old_file = self._meta.model.objects.get(id=self.id).file
        old_file.delete(save=False)
