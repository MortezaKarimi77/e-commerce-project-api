from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    path(
        route="comments/",
        view=views.CommentListCreate.as_view(),
        name="comment_list_create",
    ),
    path(
        route="comments/<comment_id>/",
        view=views.CommentDetailUpdateDelete.as_view(),
        name="comment_detail_update_delete",
    ),
]
