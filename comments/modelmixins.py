from django.db.models import F
from django_lifecycle import (
    AFTER_CREATE,
    AFTER_DELETE,
    BEFORE_CREATE,
    BEFORE_DELETE,
    hook,
)


class CommentModelMixin:
    @hook(BEFORE_CREATE)
    def set_is_buyer(self):
        user_is_buyer = self.user.purchased_products.filter(
            product=self.product
        ).exists()
        if user_is_buyer:
            self.is_buyer = True

    @hook(AFTER_CREATE)
    def increase_comments_count(self):
        self.product.comments_count = F("comments_count") + 1
        self.product.save()

    @hook(BEFORE_DELETE)
    def decrease_comments_count(self):
        self.product.comments_count = F("comments_count") - 1
        self.product.save()


class LikeModelMixin:
    @hook(AFTER_CREATE)
    def increase_comment_likes(self):
        self.comment.likes_count = F("likes_count") + 1
        self.comment.save()

    @hook(AFTER_DELETE)
    def decrease_comment_likes(self):
        self.comment.likes_count = F("likes_count") - 1
        self.comment.save()
