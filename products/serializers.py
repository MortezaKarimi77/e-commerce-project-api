from django.urls import reverse
from rest_framework import serializers

from .models import Attribute, AttributeValue, Product, ProductItem, ProductMedia


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"

        extra_kwargs = {
            "category": {
                "write_only": True,
            },
        }

    # methods
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.move_to_end("absolute_url")
        representation.move_to_end("category_url")
        return representation

    # fields
    category_full_name = serializers.CharField(
        source="category.full_name",
        read_only=True,
    )
    category_url = serializers.CharField(
        source="category.get_absolute_url",
        read_only=True,
    )
    absolute_url = serializers.CharField(
        source="get_absolute_url",
        read_only=True,
    )


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = "__all__"

        extra_kwargs = {
            "attribute": {
                "write_only": True,
            },
        }

    # methods
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.move_to_end("absolute_url")
        representation.move_to_end("attribute_url")
        return representation

    # fields
    attribute_name = serializers.CharField(
        source="attribute.name",
        read_only=True,
    )
    attribute_url = serializers.CharField(
        source="attribute.get_absolute_url",
        read_only=True,
    )
    attribute_category = serializers.CharField(
        source="attribute.category.full_name",
        read_only=True,
    )
    absolute_url = serializers.CharField(
        source="get_absolute_url",
        read_only=True,
    )


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = (
            "attribute_name",
            "char_value",
            "text_value",
            "int_value",
            "decimal_value",
            "date_value",
            "time_value",
        )

    # fields
    attribute_name = serializers.CharField(
        source="attribute.name",
        read_only=True,
    )


class ProductItemSerializer(serializers.ModelSerializer):
    # fields
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )
    product_url = serializers.CharField(
        source="product.get_absolute_url",
        read_only=True,
    )
    absolute_url = serializers.CharField(
        source="get_absolute_url",
        read_only=True,
    )


class ProductItemListSerializer(ProductItemSerializer):
    class Meta:
        model = ProductItem
        fields = (
            "id",
            "sku",
            "product",
            "product_name",
            "product_url",
            "original_price",
            "selling_price",
            "inventory",
            "is_available",
            "is_visible",
            "absolute_url",
            "configuration",
        )
        extra_kwargs = {
            "product": {
                "write_only": True,
            },
            "original_price": {
                "write_only": True,
            },
            "inventory": {
                "write_only": True,
            },
            "configuration": {
                "write_only": True,
            },
        }


class ProductItemDetailSerializer(ProductItemSerializer):
    class Meta:
        model = ProductItem
        fields = "__all__"

        extra_kwargs = {
            "product": {
                "write_only": True,
            },
            "configuration": {
                "write_only": True,
            },
        }

    # methods
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.move_to_end("product_item_configuration")
        return representation

    def get_product_item_configuration(self, product_item):
        product_items = product_item.configuration.select_related("attribute")
        return ConfigurationSerializer(instance=product_items, many=True).data

    # fields
    product_item_configuration = serializers.SerializerMethodField(
        method_name="get_product_item_configuration",
    )


class ProductItemInProductSerializer(ProductItemDetailSerializer):
    class Meta:
        model = ProductItem
        fields = (
            "id",
            "original_price",
            "selling_price",
            "inventory",
            "is_available",
            "is_visible",
            "absolute_url",
            "product_item_configuration",
        )


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = "__all__"

        extra_kwargs = {
            "product": {
                "write_only": True,
            },
            "type": {
                "write_only": True,
            },
        }

    # methods
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context["request"].user

        if not user.is_staff:
            representation.pop("id", None)
            representation.pop("product_name", None)
            representation.pop("absolute_url", None)

        return representation

    # fields
    type_name = serializers.CharField(
        source="get_type_display",
        read_only=True,
    )
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )
    absolute_url = serializers.CharField(
        source="get_absolute_url",
        read_only=True,
    )


class ProductSerializer(serializers.ModelSerializer):
    # fields
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
            "brand_name",
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
            "original_price",
            "selling_price",
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

    # fields
    category_full_name = serializers.CharField(
        source="category.full_name",
        read_only=True,
    )
    brand_name = serializers.CharField(
        source="brand.name",
        read_only=True,
    )
    original_price = serializers.CharField(
        source="cheapest_product_item.original_price",
        read_only=True,
    )
    selling_price = serializers.CharField(
        source="cheapest_product_item.selling_price",
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

        representation.move_to_end("create_datetime")
        representation.move_to_end("update_datetime")
        representation.move_to_end("main_image")
        representation.move_to_end("absolute_url")
        representation.move_to_end("brand_info")
        representation.move_to_end("category_info")
        representation.move_to_end("media_files")
        representation.move_to_end("items")

        if not user.is_staff:
            representation.pop("create_datetime", None)
            representation.pop("update_datetime", None)
            representation.pop("views_count", None)
            representation.pop("sold_count", None)

        return representation

    def get_brand_info(self, product):
        brand = product.brand

        if brand:
            products_list_url = reverse(
                viewname="brands:brand_product_list",
                kwargs={"brand_url": brand.url},
            )
            return {
                "name": brand.name,
                "absolute_url": brand.get_absolute_url(),
                "products_list_url": products_list_url,
            }
        else:
            return None

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
    media_files = ProductMediaSerializer(
        many=True,
        read_only=True,
    )
    items = ProductItemInProductSerializer(
        many=True,
        read_only=True,
    )
