from django.core.cache import cache
from rest_framework.permissions import IsAdminUser

from utility.permissions import IsAdminOrReadOnly

from .models import Product, ProductMedia
from .serializers import ProductMediaSerializer


class ProductAPIViewMixin:
    model = Product
    queryset = Product.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            queryset = super().get_queryset()
            cache_key = "all_products"
        else:
            queryset = self.model.objects.get_visible_products()
            cache_key = "visible_products"

        cached_queryset = cache.get_or_set(
            key=cache_key, default=queryset, timeout=None
        )
        return cached_queryset


class ProductMediaAPIViewMixin:
    queryset = ProductMedia.objects.select_related("product")
    serializer_class = ProductMediaSerializer
    permission_classes = (IsAdminUser,)
