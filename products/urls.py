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
    path(
        route="product-item-list-create/",
        view=views.ProductItemListCreate.as_view(),
        name="product_item_list_create",
    ),
    path(
        route="product-item-detail-update-delete/<product_item_id>/",
        view=views.ProductItemDetailUpdateDelete.as_view(),
        name="product_item_detail_update_delete",
    ),
    path(
        route="product-media-list-create/",
        view=views.ProductMediaListCreate.as_view(),
        name="product_media_list_create",
    ),
    path(
        route="product-media-detail-update-delete/<product_media_id>/",
        view=views.ProductMediaDetailUpdateDelete.as_view(),
        name="product_media_detail_update_delete",
    ),
]
