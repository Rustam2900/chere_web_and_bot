import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CartItem(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='cart_items')
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='cart_items', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELLED = 'CANCELLED', _('Cancelled')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(_("status"), max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    address = models.CharField(_('Address'))
    location = models.IntegerField(_("location"), null=True, blank=True)
    phone_number = PhoneNumberField(_('Phone number'), max_length=20)
    total_price = models.DecimalField(_("total price"), decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderMinSum(models.Model):
    min_order_sum = models.CharField(max_length=255)
