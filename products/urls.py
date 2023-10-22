from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path(
        route="products/",
        view=views.ProductListCreate.as_view(),
        name="product_list_create",
    ),
    path(
        route="products/<int:category_id>/<slug:product_url>/",
        view=views.ProductDetailUpdateDelete.as_view(),
        name="product_detail_update_delete",
    ),
    path(
        route="products/<int:category_id>/<slug:product_url>/comments/",
        view=views.ProductCommentList.as_view(),
        name="product_comments",
    ),
    path(
        route="product-items/",
        view=views.ProductItemListCreate.as_view(),
        name="product_item_list_create",
    ),
    path(
        route="product-items/<int:product_item_id>/",
        view=views.ProductItemDetailUpdateDelete.as_view(),
        name="product_item_detail_update_delete",
    ),
    path(
        route="product-medias/",
        view=views.ProductMediaListCreate.as_view(),
        name="product_media_list_create",
    ),
    path(
        route="product-medias/<int:product_media_id>/",
        view=views.ProductMediaDetailUpdateDelete.as_view(),
        name="product_media_detail_update_delete",
    ),
    path(
        route="attributes/",
        view=views.AttributeListCreate.as_view(),
        name="attribute_list_create",
    ),
    path(
        route="attributes/<int:attribute_id>/",
        view=views.AttributeDetailUpdateDelete.as_view(),
        name="attribute_detail_update_delete",
    ),
    path(
        route="attribute-values/",
        view=views.AttributeValueListCreate.as_view(),
        name="attribute_value_list_create",
    ),
    path(
        route="attribute-values/<int:attribute_value_id>/",
        view=views.AttributeValueDetailUpdateDelete.as_view(),
        name="attribute_value_detail_update_delete",
    ),
]
