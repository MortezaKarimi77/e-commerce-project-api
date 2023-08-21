from django.core.cache import cache

from utility.permissions import IsAdminOrReadOnly

from .models import Category


class CategoryAPIViewMixin:
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("parent_category")

        cached_queryset = cache.get_or_set(
            key="categories_queryset", default=queryset, timeout=None
        )
        return cached_queryset
