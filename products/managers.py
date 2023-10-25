from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("brand", "category", "cheapest_product_item")
        return queryset

    def visible_products(self):
        queryset = self.filter(is_visible=True)
        return queryset

    def brand_all_products(self, brand_url):
        queryset = self.filter(brand__url=brand_url)
        return queryset

    def brand_visible_products(self, brand_url):
        queryset = self.filter(brand__url=brand_url, is_visible=True)
        return queryset

    def category_all_products(self, category_id):
        queryset = self.filter(category=category_id)
        return queryset

    def category_visible_products(self, category_id):
        queryset = self.filter(category=category_id, is_visible=True)
        return queryset
