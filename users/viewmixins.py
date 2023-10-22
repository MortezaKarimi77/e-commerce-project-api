from django.contrib.auth import get_user_model

from core import cache_key_schema
from core.utils import get_cached_object, get_cached_queryset

User = get_user_model()


class UserAPIViewMixin:
    queryset = User.objects.order_by("-id")
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_object(self):
        cache_key = cache_key_schema.single_user(self.kwargs["username"])
        cached_object = get_cached_object(
            get_object_function=super().get_object, cache_key=cache_key
        )
        return cached_object

    def get_queryset(self):
        queryset = super().get_queryset()
        cache_key = cache_key_schema.all_users()
        cached_queryset = get_cached_queryset(queryset=queryset, cache_key=cache_key)
        return cached_queryset
