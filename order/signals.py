from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from django_celery_beat.models import ClockedSchedule, PeriodicTask, CrontabSchedule
import random
import string
import json
from django.utils import timezone


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
        clocked_schedule = CrontabSchedule.objects.create(
            # hour=instance.user.reminder_days * 24,
            minute=instance.user.reminder_days,
            # day_of_week=0
        )
        cart_items = instance.cart_items.all()
        text = "Products: "
        for cart_item in cart_items:
            text += f"{cart_item.product.title} - {cart_item.quantity}\n"

        text += f"Total price: {instance.total_price}"
        print("timezone: ", timezone.now())
        PeriodicTask.objects.create(
            name=f"Message is sending to Telegram Bot: {timezone.now().strftime('%Y-%m-%d %H:%M')}",
            crontab=clocked_schedule,
            task="order.tasks.send_message_for_notify",
            enabled=True,
            one_off=True,
            kwargs=json.dumps({"telegram_id": str(instance.user.telegram_id), "message": str(text)}),
        )
        instance.save()
