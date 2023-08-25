from rest_framework.permissions import IsAdminUser

from core.permissions import IsAdminOrReadOnly

from .models import Attribute, AttributeValue, Product, ProductItem, ProductMedia
from .serializers import (
    AttributeSerializer,
    AttributeValueSerializer,
    ProductMediaSerializer,
)


class ProductAPIViewMixin:
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.products_list(user=user)
        return queryset


class ProductItemAPIViewMixin:
    queryset = ProductItem.objects.select_related("product", "product__category")
    permission_classes = (IsAdminUser,)


class ProductMediaAPIViewMixin:
    queryset = ProductMedia.objects.select_related("product")
    serializer_class = ProductMediaSerializer
    permission_classes = (IsAdminUser,)


class AttributeAPIViewMixin:
    queryset = Attribute.objects.select_related("category")
    serializer_class = AttributeSerializer
    permission_classes = (IsAdminUser,)


class AttributeValueAPIViewMixin:
    queryset = AttributeValue.objects.select_related("attribute", "attribute__category")
    serializer_class = AttributeValueSerializer
    permission_classes = (IsAdminUser,)
