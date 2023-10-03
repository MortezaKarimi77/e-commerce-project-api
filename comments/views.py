from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from core.permissions import IsAdminOrOwner, IsAdminOrWriteOnly

from .serializers import CommentDetailSerializer, CommentListSerializer
from .viewmixins import CommentAPIViewMixin, LikeAPIViewMixin


class CommentListCreate(CommentAPIViewMixin, ListCreateAPIView):
    serializer_class = CommentListSerializer
    permission_classes = (IsAdminOrWriteOnly,)


class CommentDetailUpdateDelete(CommentAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = (IsAdminOrOwner,)
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"
    http_method_names = ("get", "patch", "delete")


class LikeCreate(LikeAPIViewMixin, CreateAPIView):
    pass


class LikeDelete(LikeAPIViewMixin, DestroyAPIView):
    permission_classes = (IsAdminOrOwner,)

    def get_object(self):
        comment = super().get_object()
        user = self.request.user
        like = get_object_or_404(klass=self.queryset, comment=comment, user=user)
        return like
