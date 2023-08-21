from django.urls import path

from . import views

app_name = "categories"
urlpatterns = [
    path(
        route="category-list-create/",
        view=views.CategoryListCreate.as_view(),
        name="category_list_create",
    ),
    path(
        route="category-detail-update-delete/<category_id>/",
        view=views.CategoryDetailUpdateDelete.as_view(),
        name="category_detail_update_delete",
    ),
    path(
        route="category-product-list/<category_id>/",
        view=views.CategoryProductList.as_view(),
        name="category_product_list",
    ),
]
