from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from core import cache_key_schema
from core.cache_key_schema import categories_key_prefix
from core.utils import get_cached_queryset
from products.models import Product
from products.serializers import ProductListSerializer

from .serializers import CategoryDetailSerializer, CategoryListSerializer
from .viewmixins import CategoryAPIViewMixin


class CategoryListCreate(CategoryAPIViewMixin, ListCreateAPIView):
    serializer_class = CategoryListSerializer
    pagination_class = None
    ordering_fields = ("id", "name")
    search_fields = ("name",)

    @method_decorator(
        decorator=cache_page(timeout=None, key_prefix=categories_key_prefix()),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CategoryDetailUpdateDelete(CategoryAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    lookup_field = "id"
    lookup_url_kwarg = "category_id"
    http_method_names = ("get", "patch", "delete")

    @method_decorator(
        decorator=cache_page(timeout=None, key_prefix=categories_key_prefix()),
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CategoryProductList(ListAPIView):
    serializer_class = ProductListSerializer
    ordering_fields = ("id", "rating", "cheapest_product_item__selling_price")
    search_fields = ("name", "brand__name", "category__full_name")

    def get_queryset(self):
        user, category_id = self.request.user, self.kwargs["category_id"]

        if user.is_staff:
            queryset = Product.objects.category_all_products(category_id)
            queryset = self.filter_queryset(queryset=queryset)
            cache_key = cache_key_schema.category_all_products(category_id)
        else:
            queryset = Product.objects.category_visible_products(category_id)
            queryset = self.filter_queryset(queryset=queryset)
            cache_key = cache_key_schema.category_visible_products(category_id)

        cached_queryset = get_cached_queryset(queryset=queryset, cache_key=cache_key)
        return cached_queryset
