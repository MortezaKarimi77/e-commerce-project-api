from django.core.cache import cache
from django.urls import reverse
from django.utils.text import slugify
from django_lifecycle import AFTER_DELETE, AFTER_SAVE, BEFORE_SAVE, BEFORE_UPDATE, hook


class BrandModelMixin:
    # methods
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="brands:brand_detail_update_delete",
            kwargs={"brand_url": self.url},
        )

    # hooks
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

    @hook(BEFORE_UPDATE, when="main_image", has_changed=True)
    def delete_old_image(self):
        old_image = self._meta.model.objects.get(id=self.id).main_image
        old_image.delete(save=False)

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def clear_cache(self):
        cache.delete(key=f"brand_{self.url}")
        cache.delete(key="brands_queryset")
