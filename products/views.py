from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from comments.models import Comment
from comments.serializers import CommentListSerializer

from .models import Product
from .serializers import (
    ProductDetailSerializer,
    ProductItemDetailSerializer,
    ProductItemListSerializer,
    ProductListSerializer,
)
from .viewmixins import (
    AttributeAPIViewMixin,
    AttributeValueAPIViewMixin,
    ProductAPIViewMixin,
    ProductItemAPIViewMixin,
    ProductMediaAPIViewMixin,
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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            "items",
            "media_files",
            "items__configuration__attribute",
        )
        return queryset


class ProductCommentList(ListAPIView):
    serializer_class = CommentListSerializer

    def get_object(self):
        category_id = self.kwargs["category_id"]
        product_url = self.kwargs["product_url"]
        cache_key = f"product_{product_url}"

        cached_object = cache.get(key=cache_key)
        if cached_object is None:
            product = get_object_or_404(
                klass=Product, category__id=category_id, url=product_url
            )
            cached_object = cache.get_or_set(
                key=cache_key, default=product, timeout=None
            )

        return cached_object

    def get_queryset(self):
        product = self.get_object()
        user = self.request.user
        queryset = Comment.objects.product_comments(user=user, product=product)
        return queryset


class ProductItemListCreate(ProductItemAPIViewMixin, ListCreateAPIView):
    serializer_class = ProductItemListSerializer


class ProductItemDetailUpdateDelete(
    ProductItemAPIViewMixin, RetrieveUpdateDestroyAPIView
):
    lookup_field = "id"
    lookup_url_kwarg = "product_item_id"
    serializer_class = ProductItemDetailSerializer
    http_method_names = ("get", "patch", "delete")

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("configuration__attribute")
        return queryset


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
