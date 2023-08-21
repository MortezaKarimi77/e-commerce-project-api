from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .mixins import ProductAPIViewMixin
from .serializers import ProductDetailSerializer, ProductListSerializer


class ProductListCreate(ProductAPIViewMixin, ListCreateAPIView):
    serializer_class = ProductListSerializer
    # ordering_fields = ("id", "name", "country")
    # search_fields = ("name", "country")


class ProductDetailUpdateDelete(ProductAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    # http_method_names = ("get", "patch", "delete")

    def get_object(self):
        category_id = self.kwargs["category_id"]
        product_url = self.kwargs["product_url"]

        cache_key = f"product_{product_url}"
        cached_object = cache.get(key=cache_key)

        if cached_object is None:
            queryset = self.get_queryset()
            product = get_object_or_404(
                klass=queryset, category__id=category_id, url=product_url
            )
            cached_object = cache.get_or_set(
                key=cache_key, default=product, timeout=None
            )

        return cached_object
