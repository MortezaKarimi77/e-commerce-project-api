from core import cache_key_schema
from core.permissions import IsAdminOrReadOnly
from core.utils import get_cached_object, get_cached_queryset

from .models import Brand


class BrandAPIViewMixin:
    queryset = Brand.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self):
        cache_key = cache_key_schema.single_brand(self.kwargs["brand_url"])
        cached_object = get_cached_object(
            get_object_function=super().get_object, cache_key=cache_key
        )
        return cached_object

    def get_queryset(self):
        queryset = super().get_queryset()
        cache_key = cache_key_schema.all_brands()
        cached_queryset = get_cached_queryset(queryset=queryset, cache_key=cache_key)
        return cached_queryset
