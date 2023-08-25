from django.db.models import F
from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, BEFORE_DELETE, hook


class CommentModelMixin:
    # methods
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.text:20} ..."

    # hooks
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
