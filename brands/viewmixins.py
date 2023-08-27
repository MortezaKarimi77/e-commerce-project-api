from django.core.cache import cache

from core.permissions import IsAdminOrReadOnly

from .models import Brand


class BrandAPIViewMixin:
    queryset = Brand.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self):
        brand_url = self.kwargs["brand_url"]
        cache_key = f"brand_{brand_url}"

        cached_object = cache.get(key=cache_key)
        if cached_object is None:
            brand = super().get_object()
            cached_object = cache.get_or_set(key=cache_key, default=brand, timeout=None)

        return cached_object

    def get_queryset(self):
        queryset = super().get_queryset()
        cache_key = "brands_queryset"

        cached_queryset = cache.get_or_set(
            key=cache_key, default=queryset, timeout=None
        )
        return cached_queryset
