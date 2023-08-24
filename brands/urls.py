from django.urls import path

from . import views

app_name = "brands"
urlpatterns = [
    path(
        route="brands/",
        view=views.BrandListCreate.as_view(),
        name="brand_list_create",
    ),
    path(
        route="brands/<brand_url>/",
        view=views.BrandDetailUpdateDelete.as_view(),
        name="brand_detail_update_delete",
    ),
    path(
        route="brands/<brand_url>/products/",
        view=views.BrandProductList.as_view(),
        name="brand_products",
    ),
]
