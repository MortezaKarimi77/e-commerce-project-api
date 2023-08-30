from django.contrib.auth import get_user_model

from core.utils import get_cached_object, get_cached_queryset

User = get_user_model()


class UserAPIViewMixin:
    queryset = User.objects.all()
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_object(self):
        username = self.kwargs["username"]
        cache_key = f"user_{username}"
        cached_object = get_cached_object(
            get_object_function=super().get_object, cache_key=cache_key
        )
        return cached_object

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-id")
        cache_key = "users_queryset"
        cached_queryset = get_cached_queryset(queryset=queryset, cache_key=cache_key)
        return cached_queryset
