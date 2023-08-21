from django.urls import reverse
from rest_framework import serializers

from . import models
from .models import Product


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductItem
        fields = "__all__"


class PrivateProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = (
            "name",
            "category",
            "category_url",
            "main_image",
            "rating",
            "get_absolute_url",
            "is_available",
        )

    category = serializers.CharField(
        source="category.name",
    )
    category_url = serializers.CharField(
        source="category.get_absolute_url",
    )


class PublicProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = (
            "name",
            "category",
            "category_url",
            "price",
            "main_image",
            "rating",
            "get_absolute_url",
            "items",
        )

    def get_price(self, product):
        cheapest_product_item = (
            product.items.filter(
                is_visible=True,
                is_available=True,
            )
            .order_by("selling_price")
            .only(
                "product_id",
                "selling_price",
                "original_price",
            )
            .first()
        )

        if product.is_available and cheapest_product_item:
            return {
                "original_price": cheapest_product_item.original_price,
                "selling_price": cheapest_product_item.selling_price,
            }

    def get_category(self, product):
        product_subcategory = product.category.parent_category
        product_category = product.category

        if product_subcategory:
            return product_subcategory.__str__() + " | " + product_category.name
        else:
            return product_category.__str__()

    category = serializers.SerializerMethodField(
        source="get_category",
    )
    category_url = serializers.CharField(
        source="category.get_absolute_url",
    )
    price = serializers.SerializerMethodField(
        method_name="get_price",
    )
    items = ProductItemSerializer(many=True)


class ProductSerializer(serializers.ModelSerializer):
    absolute_url = serializers.CharField(
        source="get_absolute_url",
        read_only=True,
    )


class ProductListSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "url",
            "category",
            "category_full_name",
            "brand",
            "introduction",
            "review",
            "meta_title",
            "meta_description",
            "is_available",
            "is_visible",
            "dimension",
            "weight",
            "included_items",
            "other_features",
            "other_description",
            "rating",
            "absolute_url",
            "main_image",
        )

        extra_kwargs = {
            "category": {
                "write_only": True,
            },
            "brand": {
                "write_only": True,
            },
            "introduction": {
                "write_only": True,
            },
            "review": {
                "write_only": True,
            },
            "meta_title": {
                "write_only": True,
            },
            "meta_description": {
                "write_only": True,
            },
            "dimension": {
                "write_only": True,
            },
            "weight": {
                "write_only": True,
            },
            "included_items": {
                "write_only": True,
            },
            "other_features": {
                "write_only": True,
            },
            "other_description": {
                "write_only": True,
            },
        }

    # methods
    category_full_name = serializers.CharField(
        source="category.full_name",
        read_only=True,
    )


class ProductDetailSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = "__all__"

        extra_kwargs = {
            "category": {
                "write_only": True,
            },
            "brand": {
                "write_only": True,
            },
        }

    # methods
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context["request"].user

        representation.move_to_end("main_image")
        representation.move_to_end("absolute_url")
        representation.move_to_end("brand_info")
        representation.move_to_end("category_info")

        if not user.is_staff:
            representation.pop("create_datetime", None)
            representation.pop("update_datetime", None)
            representation.pop("is_visible", None)
            representation.pop("views_count", None)
            representation.pop("sold_count", None)

        return representation

    def get_brand_info(self, product):
        brand = product.brand
        products_list_url = reverse(
            viewname="brands:brand_product_list",
            kwargs={"brand_url": brand.url},
        )
        return {
            "name": brand.name,
            "absolute_url": brand.get_absolute_url(),
            "products_list_url": products_list_url,
        }

    def get_category_info(self, product):
        category = product.category
        products_list_url = reverse(
            viewname="categories:category_product_list",
            kwargs={"category_id": category.id},
        )
        return {
            "full_name": category.full_name,
            "absolute_url": category.get_absolute_url(),
            "products_list_url": products_list_url,
        }

    # fields
    brand_info = serializers.SerializerMethodField(
        method_name="get_brand_info",
    )
    category_info = serializers.SerializerMethodField(
        method_name="get_category_info",
    )
