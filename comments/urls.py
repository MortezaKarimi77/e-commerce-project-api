from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    path(
        route="comments/",
        view=views.PrivateCommentListCreate.as_view(),
        name="comment_list_create",
    ),
    path(
        route="comments/<int:comment_id>/",
        view=views.CommentDetailUpdateDelete.as_view(),
        name="comment_detail_update_delete",
    ),
    path(
        route="comments/<int:comment_id>/like/",
        view=views.LikeCreate.as_view(),
        name="like_create",
    ),
    path(
        route="comments/<int:comment_id>/unlike/",
        view=views.LikeDelete.as_view(),
        name="like_delete",
    ),
]
