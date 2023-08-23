from django.core.cache import cache
from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("brand", "category")
        return queryset

    def products_list(self, user):
        if user.is_staff:
            products = self.get_queryset()
            cache_key = "all_products"
        else:
            products = self.filter(is_visible=True)
            cache_key = "visible_products"

        cached_queryset = cache.get_or_set(
            key=cache_key, default=products, timeout=None
        )
        return cached_queryset

    def brand_products(self, brand_url, user):
        if user.is_staff:
            brand_products = self.filter(brand__url=brand_url)
            cache_key = f"brand_{brand_url}_all_products"
        else:
            brand_products = self.filter(brand__url=brand_url, is_visible=True)
            cache_key = f"brand_{brand_url}_visible_products"

        cached_queryset = cache.get_or_set(
            key=cache_key, default=brand_products, timeout=None
        )
        return cached_queryset

    def category_products(self, category_id, user):
        if user.is_staff:
            category_products = self.filter(category=category_id)
            cache_key = f"category_{category_id}_all_products"
        else:
            category_products = self.filter(category=category_id, is_visible=True)
            cache_key = f"category_{category_id}_visible_products"

        cached_queryset = cache.get_or_set(
            key=cache_key, default=category_products, timeout=None
        )
        return cached_queryset
