from django.urls import path

from . import views

app_name = "brands"
urlpatterns = [
    path(
        route="brand-list-create/",
        view=views.BrandListCreate.as_view(),
        name="brand_list_create",
    ),
    path(
        route="brand-detail-update-delete/<brand_url>/",
        view=views.BrandDetailUpdateDelete.as_view(),
        name="brand_detail_update_delete",
    ),
    path(
        route="brand-product-list/<brand_url>/",
        view=views.BrandProductList.as_view(),
        name="brand_product_list",
    ),
]
