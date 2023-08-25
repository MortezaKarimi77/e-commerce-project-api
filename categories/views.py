from django.core.cache import cache
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from products.models import Product
from products.serializers import ProductListSerializer

from .serializers import CategoryDetailSerializer, CategoryListSerializer
from .viewmixins import CategoryAPIViewMixin


class CategoryListCreate(CategoryAPIViewMixin, ListCreateAPIView):
    serializer_class = CategoryListSerializer
    pagination_class = None
    ordering_fields = ("id", "name")
    search_fields = ("name",)


class CategoryDetailUpdateDelete(CategoryAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    lookup_field = "id"
    lookup_url_kwarg = "category_id"
    http_method_names = ("get", "patch", "delete")

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
    serializer_class = ProductListSerializer
    ordering_fields = ("id", "rating", "cheapest_product_item__selling_price")
    search_fields = ("name", "brand__name", "category__full_name")

    def get_queryset(self):
        user = self.request.user
        category_id = self.kwargs["category_id"]

        queryset = Product.objects.category_products(category_id=category_id, user=user)
        return queryset
