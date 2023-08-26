from django.core.cache import cache

from core.permissions import IsAdminOrReadOnly

from .models import Category


class CategoryAPIViewMixin:
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self):
        category_id = self.kwargs["category_id"]
        cache_key = f"category_{category_id}"

        cached_object = cache.get(key=cache_key)
        if cached_object is None:
            category = super().get_object()
            cached_object = cache.get_or_set(
                key=cache_key, default=category, timeout=None
            )

        return cached_object

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("parent_category")
        cache_key = "categories_queryset"

        cached_queryset = cache.get_or_set(
            key=cache_key, default=queryset, timeout=None
        )
        return cached_queryset
