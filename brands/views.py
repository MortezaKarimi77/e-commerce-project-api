from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from core import cache_key_schema
from core.utils import get_cached_queryset
from products.models import Product
from products.serializers import ProductListSerializer

from .serializers import BrandDetailSerializer, BrandListSerializer
from .viewmixins import BrandAPIViewMixin


class BrandListCreate(BrandAPIViewMixin, ListCreateAPIView):
    serializer_class = BrandListSerializer
    ordering_fields = ("id", "name", "country")
    search_fields = ("name", "country")


class BrandDetailUpdateDelete(BrandAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = BrandDetailSerializer
    lookup_field = "url"
    lookup_url_kwarg = "brand_url"
    http_method_names = ("get", "patch", "delete")


class BrandProductList(ListAPIView):
    serializer_class = ProductListSerializer
    ordering_fields = ("id", "rating", "cheapest_product_item__selling_price")
    search_fields = ("name", "brand__name", "category__full_name")

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
