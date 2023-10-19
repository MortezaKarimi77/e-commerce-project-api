from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Category


class CategoryBaseSerializer(serializers.ModelSerializer):
    absolute_url = serializers.HyperlinkedIdentityField(
        view_name="categories:category_detail_update_delete",
        lookup_url_kwarg="category_id",
        lookup_field="id",
    )
    products_url = serializers.HyperlinkedIdentityField(
        view_name="categories:category_products",
        lookup_url_kwarg="category_id",
        lookup_field="id",
    )

    def validate(self, data):
        category = self.instance
        category_id = category.id if category else None
        input_category_url = data.get("url")
        input_parent_category = data.get("parent_category")
        request = self.context.get("request")

        other_categories = self.Meta.model.objects.filter(
            parent_category=None, url=input_category_url
        ).exclude(id=category_id)

        if request.method in ("PATCH", "PUT"):
            if other_categories.exists() and category.parent_category is None:
                raise ValidationError(
                    detail=_("لینک این دسته‌بندی قبلا استفاده شده است")
                )

        if request.method == "POST":
            if other_categories.exists() and input_parent_category is None:
                raise ValidationError(
                    detail=_("لینک این دسته‌بندی قبلا استفاده شده است")
                )

        if (category is not None) and (category == input_parent_category):
            raise ValidationError(_("یک دسته‌بندی نمی‌تواند زیردسته خودش باشد"))

        return super().validate(data)


class ParentCategorySerializer(CategoryBaseSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "full_name",
            "url",
            "absolute_url",
            "products_url",
        )


class CategoryListSerializer(CategoryBaseSerializer):
    parent_category_info = ParentCategorySerializer(
        source="parent_category",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "full_name",
            "url",
            "absolute_url",
            "products_url",
            "description",
            "meta_title",
            "meta_description",
            "parent_category_info",
            "parent_category",
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
            "parent_category": {
                "write_only": True,
            },
        }


class CategoryDetailSerializer(CategoryBaseSerializer):
    parent_category_info = ParentCategorySerializer(
        source="parent_category",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = "__all__"

        extra_kwargs = {
            "parent_category": {
                "write_only": True,
            },
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.move_to_end(key="parent_category_info")
        return representation


class CategoryInfoSerializer(CategoryBaseSerializer):
    class Meta:
        model = Category
        fields = (
            "full_name",
            "absolute_url",
            "products_url",
        )
