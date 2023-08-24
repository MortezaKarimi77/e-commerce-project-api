from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

app_name = "users"
urlpatterns = [
    path(
        route="auth/token/obtain/",
        view=views.TokenObtainPair.as_view(),
        name="token_obtain",
    ),
    path(
        route="auth/token/refresh/",
        view=TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        route="auth/token/verify/",
        view=TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path(
        route="users/",
        view=views.UserListCreate.as_view(),
        name="user_list_create",
    ),
    path(
        route="users/<username>/",
        view=views.UserDetailUpdateDelete.as_view(),
        name="user_detail_update_delete",
    ),
]
