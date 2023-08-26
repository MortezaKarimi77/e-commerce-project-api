from django_lifecycle import BEFORE_CREATE, BEFORE_SAVE, BEFORE_UPDATE, hook


class AddressModelMixin:
    @hook(BEFORE_SAVE)
    def set_receiver_name(self):
        if not self.receiver_first_name:
            self.receiver_first_name = self.user.first_name
        if not self.receiver_last_name:
            self.receiver_last_name = self.user.last_name

    @hook(BEFORE_SAVE, when="is_default", was=False, is_now=True)
    def set_default_address(self):
        previous_default_address = self.user.addresses.exclude(
            id=self.id,
        ).exclude(
            is_default=False,
        )
        previous_default_address.update(is_default=False)


class OrderModelMixin:
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="order_code", has_changed=True)
    def set_order_code(self):
        self.order_code = self.id

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="shipping_cost", has_changed=True)
    def set_shipping_cost(self):
        self.shipping_cost = self.shipping_method.cost


class OrderItemModelMixin:
    @hook(BEFORE_CREATE)
    def set_price(self):
        selling_price = self.product_item.selling_price
        self.price = selling_price
        self.total_price = selling_price * self.quantity

    @hook(BEFORE_CREATE)
    def set_name(self):
        self.name = self.product_item.product.name
