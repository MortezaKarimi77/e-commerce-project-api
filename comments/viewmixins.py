from core.utils import get_cached_object, get_cached_queryset

from .models import Comment


class CommentAPIViewMixin:
    queryset = Comment.objects.all()

    def get_object(self):
        comment_url = self.kwargs["comment_id"]
        cache_key = f"comment_{comment_url}"

        cached_object = get_cached_object(
            get_object_function=super().get_object, cache_key=cache_key
        )
        return cached_object

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user", "product", "product__category")
        cache_key = "comments_queryset"

        cached_queryset = get_cached_queryset(queryset=queryset, cache_key=cache_key)
        return cached_queryset
