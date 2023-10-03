from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path(
        route="admin/",
        view=admin.site.urls,
    ),
    path(
        route="api/v1/browseable-api-auth/",
        view=include("rest_framework.urls"),
    ),
    path(
        route="api/v1/schema/",
        view=SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        route="api/v1/schema/redoc/",
        view=SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        route="api/v1/schema/swagger-ui/",
        view=SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        route="__debug__/",
        view=include("debug_toolbar.urls"),
    ),
    path(
        route="api/v1/",
        view=include("products.urls"),
    ),
    path(
        route="api/v1/",
        view=include("categories.urls"),
    ),
    path(
        route="api/v1/",
        view=include("brands.urls"),
    ),
    path(
        route="api/v1/",
        view=include("users.urls"),
    ),
    path(
        route="api/v1/",
        view=include("comments.urls"),
    ),
] + static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
