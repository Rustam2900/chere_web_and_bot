from __future__ import absolute_import, unicode_literals
import requests
from celery import shared_task
from django.conf import settings

@shared_task(name="send_message_for_reminder")
def send_message_for_notify(telegram_id, message):
    api_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage?chat_id={telegram_id}&text={message}"
    response = requests.post(api_url)
    print(response.status_code)