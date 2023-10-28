from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_DELETE, AFTER_SAVE, BEFORE_SAVE, hook

from core.cache_key_schema import categories_pattern


class CategoryModelMixin:
    def validate_unique(self, exclude):
        other_categories = self._meta.model.objects.exclude(id=self.id)
        category = other_categories.filter(parent_category=None, url=self.url)

        if category.exists() and self.parent_category is None:
            raise ValidationError(message=_("لینک این دسته‌بندی قبلا استفاده شده است"))

        return super().validate_unique(exclude)

    def clean(self):
        if self == self.parent_category:
            raise ValidationError(_("یک دسته‌بندی نمی‌تواند زیردسته خودش باشد"))

    @hook(BEFORE_SAVE)
    def set_metadate(self):
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.description

    @hook(BEFORE_SAVE)
    def set_url(self):
        if not self.url:
            self.url = slugify(value=self.name, allow_unicode=True)

    @hook(BEFORE_SAVE)
    def set_full_name(self):
        if self.parent_category:
            self.full_name = f"{self.parent_category.full_name} / {self.name}"
        else:
            self.full_name = self.name

    @hook(AFTER_SAVE, when="full_name", has_changed=True)
    def change_subcategories_full_name(self):
        [subcategory.save() for subcategory in self.subcategories.all()]

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def clear_cache(self):
        cache.delete_pattern(pattern=categories_pattern())
