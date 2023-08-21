from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    # methods
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

    def get_products_list_url(self, category):
        return reverse(
            viewname="categories:category_product_list",
            kwargs={"category_id": category.id},
        )

    # fields
    absolute_url = serializers.CharField(
        source="get_absolute_url",
        read_only=True,
    )
    products_list_url = serializers.SerializerMethodField(
        method_name="get_products_list_url",
    )


class ParentCategorySerializer(CategorySerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "full_name",
            "url",
            "absolute_url",
            "products_list_url",
        )


class CategoryListSerializer(CategorySerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "full_name",
            "url",
            "absolute_url",
            "products_list_url",
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

    parent_category_info = ParentCategorySerializer(
        source="parent_category",
        read_only=True,
    )


class CategoryDetailSerializer(CategorySerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        parent_category_info = representation.get("parent_category_info")

        if parent_category_info:
            representation.move_to_end(key="parent_category_info")
        return representation
