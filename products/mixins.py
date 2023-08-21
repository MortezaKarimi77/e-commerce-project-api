from django.core.cache import cache

from utility.permissions import IsAdminOrReadOnly

from .models import Product


class ProductAPIViewMixin:
    model = Product
    queryset = Product.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            queryset = super().get_queryset()
            cache_key = "all_products_queryset"
        else:
            queryset = self.model.objects.get_visible_products()
            cache_key = "visible_products_queryset"

        cached_queryset = cache.get_or_set(
            key=cache_key, default=queryset, timeout=None
        )
        return cached_queryset
