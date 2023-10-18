from rest_framework import serializers

from .models import Brand


class BrandSerializer(serializers.ModelSerializer):
    absolute_url = serializers.HyperlinkedIdentityField(
        view_name="brands:brand_detail_update_delete",
        lookup_url_kwarg="brand_url",
        lookup_field="url",
    )
    products_url = serializers.HyperlinkedIdentityField(
        view_name="brands:brand_products",
        lookup_url_kwarg="brand_url",
        lookup_field="url",
    )


class BrandListSerializer(BrandSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "url",
            "absolute_url",
            "products_url",
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


class BrandInfoSerializer(BrandSerializer):
    class Meta:
        model = Brand
        fields = (
            "name",
            "absolute_url",
            "products_url",
        )
