from core.permissions import IsAdminOrReadOnly
from core.utils import get_cached_object, get_cached_queryset

from .models import Category


class CategoryAPIViewMixin:
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self):
        category_id = self.kwargs["category_id"]
        cache_key = f"category_{category_id}"

        cached_object = get_cached_object(
            get_object_function=super().get_object, cache_key=cache_key
        )
        return cached_object

    def get_queryset(self):
        queryset = super().get_queryset().select_related("parent_category")
        cache_key = "categories_queryset"
        cached_queryset = get_cached_queryset(queryset=queryset, cache_key=cache_key)
        return cached_queryset
