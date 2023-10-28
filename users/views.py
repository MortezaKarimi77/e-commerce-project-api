from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from comments.models import Comment
from comments.serializers import CommentListSerializer

from .permissions import IsUserOwner
from .serializers import (
    PrivateUserDetailSerializer,
    PublicUserDetailSerializer,
    UserListSerializer,
)
from .viewmixins import UserAPIViewMixin


class TokenObtainPair(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.pop("refresh")
        response.set_cookie(key="refresh", value=refresh_token, httponly=True)
        return response


class UserListCreate(UserAPIViewMixin, ListCreateAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAdminUser,)
    ordering_fields = ("id", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")


class UserDetailUpdateDelete(UserAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_classes = {
        "private": PrivateUserDetailSerializer,
        "public": PublicUserDetailSerializer,
    }
    permission_classes = {
        "private": (IsAdminUser,),
        "public": (IsAuthenticated, IsUserOwner),
    }
    http_method_names = ("get", "patch", "delete")

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_staff:
            return self.serializer_classes["private"]
        else:
            return self.serializer_classes["public"]

    def get_permissions(self):
        if self.request.user.is_staff:
            return [permission() for permission in self.permission_classes["private"]]
        else:
            return [permission() for permission in self.permission_classes["public"]]


@method_decorator(decorator=cache_page(timeout=60), name="dispatch")
class UserCommentList(ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated,)
    ordering_fields = ("id", "likes_count", "published")
    filterset_fields = ("published",)

    def get_queryset(self):
        user = self.request.user
        queryset = Comment.objects.user_comments(user=user)
        queryset = self.filter_queryset(queryset=queryset)
        return queryset
