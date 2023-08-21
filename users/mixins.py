from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()


class UserAPIViewMixin:
    queryset = User.objects.all()
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-id")

        cached_queryset = cache.get_or_set(
            key="users_queryset", default=queryset, timeout=None
        )
        return cached_queryset
