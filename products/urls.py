from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path(
        route="product-list-create/",
        view=views.ProductListCreate.as_view(),
        name="product_list_create",
    ),
    path(
        route="product-detail-update-delete/<category_id>/<product_url>/",
        view=views.ProductDetailUpdateDelete.as_view(),
        name="product_detail_update_delete",
    ),
]
