from django.urls import reverse
from rest_framework import serializers

from .models import Brand


class BrandSerializer(serializers.ModelSerializer):
    def get_products_list_url(self, brand):
        return reverse(
            viewname="brands:brand_product_list",
            kwargs={"brand_url": brand.url},
        )

    absolute_url = serializers.CharField(
        source="get_absolute_url",
        read_only=True,
    )
    products_list_url = serializers.SerializerMethodField(
        method_name="get_products_list_url",
    )


class BrandListSerializer(BrandSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "url",
            "absolute_url",
            "products_list_url",
            "country",
            "description",
            "meta_title",
            "meta_description",
            "main_image",
        )

        extra_kwargs = {
            "description": {
                "write_only": True,
            },
            "meta_title": {
                "write_only": True,
            },
            "meta_description": {
                "write_only": True,
            },
        }


class BrandDetailSerializer(BrandSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context["request"].user

        if not user.is_staff:
            representation.pop("create_datetime", None)
            representation.pop("update_datetime", None)

        return representation
