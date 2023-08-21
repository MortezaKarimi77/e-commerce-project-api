from django.core.cache import cache
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from products.models import Product
from products.serializers import PublicProductListSerializer

from .mixins import BrandAPIViewMixin
from .serializers import BrandDetailSerializer, BrandListSerializer


class BrandListCreate(BrandAPIViewMixin, ListCreateAPIView):
    serializer_class = BrandListSerializer
    ordering_fields = ("id", "name", "country")
    search_fields = ("name", "country")


class BrandDetailUpdateDelete(BrandAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = BrandDetailSerializer
    http_method_names = ("get", "patch", "delete")
    lookup_field = "url"
    lookup_url_kwarg = "brand_url"

    def get_object(self):
        brand_url = self.kwargs["brand_url"]
        cache_key = f"brand_{brand_url}"
        cached_object = cache.get(key=cache_key)

        if cached_object is None:
            brand = super().get_object()
            cached_object = cache.get_or_set(key=cache_key, default=brand, timeout=None)

        return cached_object


class BrandProductList(ListAPIView):
    serializer_class = PublicProductListSerializer
    search_fields = ("name",)
    # ordering_fields = ("rating", "create_datetime")

    def get_queryset(self):
        brand_url = self.kwargs["brand_url"]
        cache_key = f"{brand_url}_products"
        queryset = Product.objects.get_brand_products(brand_url=brand_url)

        cached_queryset = cache.get_or_set(
            key=cache_key, default=queryset, timeout=None
        )
        return cached_queryset
