from django.shortcuts import get_object_or_404

from core.utils import get_cached_object, get_cached_queryset

from .models import Comment, Like
from .serializers import LikeSerializer


class CommentAPIViewMixin:
    queryset = Comment.objects.all()

    def get_object(self):
        comment_id = self.kwargs["comment_id"]
        cache_key = f"comment_{comment_id}"

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


class LikeAPIViewMixin:
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_object(self):
        comment = get_object_or_404(klass=Comment, pk=self.kwargs.get("comment_id"))
        return comment

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        context["comment"] = self.get_object()
        return context
