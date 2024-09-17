from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CartItem(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='cart_items')
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='cart_items', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_visible = models.BooleanField(_('is visible'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELLED = 'CANCELLED', _('Cancelled')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(_("status"), max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    address = models.CharField(_('address'), max_length=255)
    latitude = models.DecimalField(_('latitude'), max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(_('longitude'), max_digits=11, decimal_places=8, blank=True, null=True)
    phone_number = PhoneNumberField(_('Phone number'), max_length=20)
    total_price = models.DecimalField(_("total price"), decimal_places=2, max_digits=10)
    order_number = models.CharField(_("order number"),max_length=25, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderMinSum(models.Model):
    min_order_sum = models.CharField(_("order minimum sum"), max_length=255)

    class Meta:
        verbose_name = _("Order minimum sum")
        verbose_name_plural = _("Order minimum sum")


class NotificationOrder(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='notification_orders')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='notification_orders')
    employee_count = models.PositiveIntegerField(_('employee count'), default=0)
    durations_days = models.PositiveIntegerField(_('durations days'), default=0)
    box_count = models.PositiveIntegerField(_('box count'), default=0)

    def __str__(self):
        return f"{self.order.id} {self.employee_count} {self.durations_days} {self.box_count}"

    class Meta:
        verbose_name = _("Notification order")
        verbose_name_plural = _("Notification orders")
