from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

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
        user = self.request.user
        brand_url = self.kwargs["brand_url"]

        queryset = Product.objects.brand_products(brand_url=brand_url, user=user)
        return queryset
