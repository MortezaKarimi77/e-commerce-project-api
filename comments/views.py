from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from core.permissions import IsAdminOrOwner, IsAdminOrWriteOnly

from .serializers import CommentDetailSerializer, CommentListSerializer
from .viewmixins import CommentAPIViewMixin


class CommentListCreate(CommentAPIViewMixin, ListCreateAPIView):
    serializer_class = CommentListSerializer
    permission_classes = (IsAdminOrWriteOnly,)


class CommentDetailUpdateDelete(CommentAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = (IsAdminOrOwner,)
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"
    http_method_names = ("get", "patch", "delete")
