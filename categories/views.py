from django.core.cache import cache
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from products.models import Product
from products.serializers import PublicProductListSerializer

from .mixins import CategoryAPIViewMixin
from .serializers import CategoryDetailSerializer, CategoryListSerializer


class CategoryListCreate(CategoryAPIViewMixin, ListCreateAPIView):
    serializer_class = CategoryListSerializer
    pagination_class = None
    ordering_fields = ("id", "name")
    search_fields = ("name",)


class CategoryDetailUpdateDelete(CategoryAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    http_method_names = ("get", "patch", "delete")
    lookup_field = "id"
    lookup_url_kwarg = "category_id"

    def get_object(self):
        category_id = self.kwargs["category_id"]
        cache_key = f"category_{category_id}"
        cached_object = cache.get(key=cache_key)

        if cached_object is None:
            category = super().get_object()
            cached_object = cache.get_or_set(
                key=cache_key, default=category, timeout=None
            )

        return cached_object


class CategoryProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = PublicProductListSerializer

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        cache_key = f"category_{category_id}_products"
        queryset = Product.objects.get_category_products(category_id=category_id)

        cached_queryset = cache.get_or_set(
            key=cache_key, default=queryset, timeout=None
        )
        return cached_queryset
