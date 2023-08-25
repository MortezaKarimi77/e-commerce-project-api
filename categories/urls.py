from django.urls import path

from . import views

app_name = "categories"
urlpatterns = [
    path(
        route="categories/",
        view=views.CategoryListCreate.as_view(),
        name="category_list_create",
    ),
    path(
        route="categories/<category_id>/",
        view=views.CategoryDetailUpdateDelete.as_view(),
        name="category_detail_update_delete",
    ),
    path(
        route="categories/<category_id>/products/",
        view=views.CategoryProductList.as_view(),
        name="category_products",
    ),
]
