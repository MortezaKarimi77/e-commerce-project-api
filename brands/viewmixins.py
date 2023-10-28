from core.permissions import IsAdminOrReadOnly

from .models import Brand


class BrandAPIViewMixin:
    queryset = Brand.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
