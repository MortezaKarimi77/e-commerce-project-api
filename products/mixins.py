from django.core.cache import cache

from utility.permissions import IsAdminOrReadOnly

from .models import Product


class ProductAPIViewMixin:
    queryset = Product.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()

        cached_queryset = cache.get_or_set(
            key="products_queryset", default=queryset, timeout=None
        )
        return cached_queryset
