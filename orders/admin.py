from django.contrib import admin

from . import models

admin.site.register(
    model_or_iterable=(
        models.Order,
        models.OrderItem,
        models.Address,
        models.Region,
        models.City,
        models.OrderStatus,
        models.PaymentMethod,
        models.ShippingMethod,
    )
)
