from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .viewmixins import (
    AttributeAPIViewMixin,
    AttributeValueAPIViewMixin,
    ProductAPIViewMixin,
    ProductItemAPIViewMixin,
    ProductMediaAPIViewMixin,
)
from .serializers import (
    ProductDetailSerializer,
    ProductItemDetailSerializer,
    ProductItemListSerializer,
    ProductListSerializer,
)


class ProductListCreate(ProductAPIViewMixin, ListCreateAPIView):
    serializer_class = ProductListSerializer
    ordering_fields = ("id", "rating", "cheapest_product_item__selling_price")
    search_fields = ("name", "brand__name", "category__full_name")


class ProductDetailUpdateDelete(ProductAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    http_method_names = ("get", "patch", "delete")

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


class ProductItemListCreate(ProductItemAPIViewMixin, ListCreateAPIView):
    serializer_class = ProductItemListSerializer


class ProductItemDetailUpdateDelete(
    ProductItemAPIViewMixin, RetrieveUpdateDestroyAPIView
):
    lookup_field = "id"
    lookup_url_kwarg = "product_item_id"
    serializer_class = ProductItemDetailSerializer
    http_method_names = ("get", "patch", "delete")


class ProductMediaListCreate(ProductMediaAPIViewMixin, ListCreateAPIView):
    pass


class ProductMediaDetailUpdateDelete(
    ProductMediaAPIViewMixin, RetrieveUpdateDestroyAPIView
):
    lookup_field = "id"
    lookup_url_kwarg = "product_media_id"
    http_method_names = ("get", "patch", "delete")


class AttributeListCreate(AttributeAPIViewMixin, ListCreateAPIView):
    pass


class AttributeDetailUpdateDelete(AttributeAPIViewMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "attribute_id"
    http_method_names = ("get", "patch", "delete")


class AttributeValueListCreate(AttributeValueAPIViewMixin, ListCreateAPIView):
    pass


class AttributeValueDetailUpdateDelete(
    AttributeValueAPIViewMixin, RetrieveUpdateDestroyAPIView
):
    lookup_field = "id"
    lookup_url_kwarg = "attribute_value_id"
    http_method_names = ("get", "patch", "delete")
