from django.db import models

from core.utils import get_cached_queryset


class ProductManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("brand", "category", "cheapest_product_item")
        return queryset

    def products_list(self, user):
        if user.is_staff:
            products = self.get_queryset()
            cache_key = "all_products"
        else:
            products = self.filter(is_visible=True)
            cache_key = "visible_products"

        cached_queryset = get_cached_queryset(queryset=products, cache_key=cache_key)
        return cached_queryset

    def brand_products(self, brand_url, user):
        if user.is_staff:
            brand_products = self.filter(brand__url=brand_url)
            cache_key = f"brand_{brand_url}_all_products"
        else:
            brand_products = self.filter(brand__url=brand_url, is_visible=True)
            cache_key = f"brand_{brand_url}_visible_products"

        cached_queryset = get_cached_queryset(
            queryset=brand_products, cache_key=cache_key
        )
        return cached_queryset

    def category_products(self, category_id, user):
        if user.is_staff:
            category_products = self.filter(category=category_id)
            cache_key = f"category_{category_id}_all_products"
        else:
            category_products = self.filter(category=category_id, is_visible=True)
            cache_key = f"category_{category_id}_visible_products"

        cached_queryset = get_cached_queryset(
            queryset=category_products, cache_key=cache_key
        )
        return cached_queryset
