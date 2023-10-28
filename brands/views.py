from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from core import cache_key_schema
from core.cache_key_schema import brands_key_prefix
from core.utils import get_cached_queryset
from products.models import Product
from products.serializers import ProductListSerializer

from .serializers import BrandDetailSerializer, BrandListSerializer
from .viewmixins import BrandAPIViewMixin


class BrandListCreate(BrandAPIViewMixin, ListCreateAPIView):
    serializer_class = BrandListSerializer
    ordering_fields = ("id", "name", "country")
    search_fields = ("name", "country")

    @method_decorator(
        decorator=cache_page(timeout=None, key_prefix=brands_key_prefix()),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BrandDetailUpdateDelete(BrandAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = BrandDetailSerializer
    lookup_field = "url"
    lookup_url_kwarg = "brand_url"
    http_method_names = ("get", "patch", "delete")

    @method_decorator(
        decorator=cache_page(timeout=None, key_prefix=brands_key_prefix()),
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class BrandProductList(ListAPIView):
    serializer_class = ProductListSerializer
    ordering_fields = ("id", "rating", "cheapest_product_item__selling_price")
    search_fields = ("name", "brand__name", "category__full_name")

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user, brand_url = self.request.user, self.kwargs["brand_url"]

        if user.is_staff:
            queryset = Product.objects.brand_all_products(brand_url)
            queryset = self.filter_queryset(queryset=queryset)
            cache_key = cache_key_schema.brand_all_products(brand_url)
        else:
            queryset = Product.objects.brand_visible_products(brand_url)
            queryset = self.filter_queryset(queryset=queryset)
            cache_key = cache_key_schema.brand_visible_products(brand_url)

        cached_queryset = get_cached_queryset(queryset=queryset, cache_key=cache_key)
        return cached_queryset
