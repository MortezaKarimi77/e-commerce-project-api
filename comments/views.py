from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdminOrOwner, IsAdminOrWriteOnly

from .serializers import CommentDetailSerializer, CommentListSerializer
from .viewmixins import CommentAPIViewMixin, LikeAPIViewMixin


class PrivateCommentListCreate(CommentAPIViewMixin, ListCreateAPIView):
    serializer_class = CommentListSerializer
    permission_classes = (IsAdminOrWriteOnly,)
    filterset_fields = ("user__username", "published")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["is_for_admin_panel"] = True
        return context


class CommentDetailUpdateDelete(CommentAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = (IsAdminOrOwner,)
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"
    http_method_names = ("get", "patch", "delete")


class LikeCreate(LikeAPIViewMixin, CreateAPIView):
    permission_classes = (IsAuthenticated,)


class LikeDelete(LikeAPIViewMixin, DestroyAPIView):
    permission_classes = (IsAdminOrOwner,)

    def get_object(self):
        user, comment = self.request.user, super().get_object()
        like = get_object_or_404(klass=self.queryset, comment=comment, user=user)
        return like
