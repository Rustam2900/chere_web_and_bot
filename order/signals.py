from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order
import random
import string


@receiver(post_save, sender=Order)
def generate_order_number(sender, instance, created, **kwargs):
    if created:
        if not instance.order_number:
            # Генерируем уникальный 8-значный номер заказа
            order_number = ''.join(random.choices(string.digits, k=8))

            # Проверяем, что номер заказа уникален
            while Order.objects.filter(order_number=f'#{order_number}').exists():
                order_number = ''.join(random.choices(string.digits, k=8))

            instance.order_number = f'#{order_number}'
            instance.save()
