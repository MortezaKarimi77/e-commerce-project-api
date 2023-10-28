from core.permissions import IsAdminOrReadOnly

from .models import Category


class CategoryAPIViewMixin:
    queryset = Category.objects.select_related("parent_category")
    permission_classes = (IsAdminOrReadOnly,)
