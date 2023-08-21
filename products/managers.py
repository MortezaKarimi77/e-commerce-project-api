from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("brand", "category")
        return queryset

    def get_visible_products(self):
        visible_products = self.filter(is_visible=True)
        return visible_products

    def get_brand_products(self, brand_url):
        brand_products = self.filter(brand__url=brand_url)
        return brand_products

    def get_category_products(self, category_id):
        category_products = self.filter(category=category_id)
        return category_products

    # def get_brand_products(self, brand_url):
    #     brand_products = self.select_related("category")
    #     brand_products = brand_products.filter(brand__url=brand_url)
    #     return brand_products

    # def get_category_products(self, category_id):
    #     category_products = self.select_related("category")
    #     category_products = category_products.filter(category=category_id)
    #     return category_products
