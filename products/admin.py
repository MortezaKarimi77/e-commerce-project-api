from django.contrib import admin

from . import models

admin.site.register(
    model_or_iterable=(
        models.Product,
        models.ProductMedia,
        models.ProductItem,
        models.Attribute,
        models.AttributeValue,
    )
)
