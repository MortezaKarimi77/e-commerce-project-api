from rest_framework import serializers
from rest_framework.reverse import reverse

from brands.serializers import BrandInfoSerializer
from categories.serializers import CategoryInfoSerializer

from .models import Attribute, AttributeValue, Product, ProductItem, ProductMedia


class AttributeSerializer(serializers.ModelSerializer):
    category_full_name = serializers.CharField(
        source="category.full_name",
        read_only=True,
    )
    category_url = serializers.SerializerMethodField(
        method_name="get_category_url",
    )
    absolute_url = serializers.HyperlinkedIdentityField(
        view_name="products:attribute_detail_update_delete",
        lookup_url_kwarg="attribute_id",
        lookup_field="id",
    )

    class Meta:
        model = Attribute
        fields = "__all__"

        extra_kwargs = {
            "category": {
                "write_only": True,
            },
        }

    def get_category_url(self, attribute) -> str:
        return reverse(
            viewname="categories:category_detail_update_delete",
            request=self.context.get("request"),
            kwargs={"category_id": attribute.category.id},
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.move_to_end("absolute_url")
        representation.move_to_end("category_url")
        return representation


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(
        source="attribute.name",
        read_only=True,
    )
    attribute_category = serializers.CharField(
        source="attribute.category.full_name",
        read_only=True,
    )
    attribute_url = serializers.SerializerMethodField(
        method_name="get_attribute_url",
    )
    absolute_url = serializers.HyperlinkedIdentityField(
        view_name="products:attribute_value_detail_update_delete",
        lookup_url_kwarg="attribute_value_id",
        lookup_field="id",
    )

    class Meta:
        model = AttributeValue
        fields = "__all__"

        extra_kwargs = {
            "attribute": {
                "write_only": True,
            },
        }

    def get_attribute_url(self, attribute_value) -> str:
        return reverse(
            viewname="products:attribute_detail_update_delete",
            request=self.context.get("request"),
            kwargs={"attribute_id": attribute_value.attribute.id},
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.move_to_end("absolute_url")
        representation.move_to_end("attribute_url")
        return representation


class ConfigurationSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(
        source="attribute.name",
        read_only=True,
    )

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


class ProductItemBaseSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )
    product_url = serializers.SerializerMethodField(
        method_name="get_product_url",
    )
    absolute_url = serializers.HyperlinkedIdentityField(
        view_name="products:product_item_detail_update_delete",
        lookup_url_kwarg="product_item_id",
        lookup_field="id",
    )

    def get_product_url(self, product_item) -> str:
        return reverse(
            viewname="products:product_detail_update_delete",
            request=self.context.get("request"),
            kwargs={
                "category_id": product_item.product.category.id,
                "product_url": product_item.product.url,
            },
        )


class ProductItemListSerializer(ProductItemBaseSerializer):
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


class ProductItemDetailSerializer(ProductItemBaseSerializer):
    product_item_configuration = ConfigurationSerializer(
        source="configuration",
        many=True,
        read_only=True,
    )

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.move_to_end("product_item_configuration")
        return representation


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
    type_name = serializers.CharField(
        source="get_type_display",
        read_only=True,
    )
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )
    absolute_url = serializers.HyperlinkedIdentityField(
        view_name="products:product_media_detail_update_delete",
        lookup_url_kwarg="product_media_id",
        lookup_field="id",
    )

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


class ProductBaseSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField(
        method_name="get_absolute_url",
    )
    comments_url = serializers.SerializerMethodField(
        method_name="get_comments_url",
    )
    original_price = serializers.CharField(
        source="cheapest_product_item.original_price",
        default=None,
        read_only=True,
    )
    selling_price = serializers.CharField(
        source="cheapest_product_item.selling_price",
        default=None,
        read_only=True,
    )

    def get_absolute_url(self, product) -> str:
        return reverse(
            viewname="products:product_detail_update_delete",
            request=self.context.get("request"),
            kwargs={"category_id": product.category.id, "product_url": product.url},
        )

    def get_comments_url(self, product) -> str:
        return reverse(
            viewname="products:product_comments",
            request=self.context.get("request"),
            kwargs={"category_id": product.category.id, "product_url": product.url},
        )


class ProductListSerializer(ProductBaseSerializer):
    category_full_name = serializers.CharField(
        source="category.full_name",
        read_only=True,
    )
    brand_name = serializers.CharField(
        source="brand.name",
        read_only=True,
    )

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
            "comments_url",
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


class ProductDetailSerializer(ProductBaseSerializer):
    brand_info = BrandInfoSerializer(
        source="brand",
        read_only=True,
    )
    category_info = CategoryInfoSerializer(
        source="category",
        read_only=True,
    )
    media_files = ProductMediaSerializer(
        many=True,
        read_only=True,
    )
    items = ProductItemInProductSerializer(
        many=True,
        read_only=True,
    )

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
            "cheapest_product_item": {
                "read_only": True,
            },
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context["request"].user

        representation.move_to_end("create_datetime")
        representation.move_to_end("update_datetime")
        representation.move_to_end("main_image")
        representation.move_to_end("absolute_url")
        representation.move_to_end("comments_url")
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
