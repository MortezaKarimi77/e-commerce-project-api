from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

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
    private_serializer_class = PrivateUserDetailSerializer
    public_serializer_class = PublicUserDetailSerializer
    private_permission_classes = (IsAdminUser,)
    public_permission_classes = (IsAuthenticated, IsUserOwner)
    http_method_names = ("get", "patch", "delete")

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_staff:
            return self.private_serializer_class
        else:
            return self.public_serializer_class

    def get_permissions(self):
        if self.request.user.is_staff:
            return [permission() for permission in self.private_permission_classes]
        else:
            return [permission() for permission in self.public_permission_classes]
