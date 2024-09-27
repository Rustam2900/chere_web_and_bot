from django.contrib.auth.hashers import check_password

from asgiref.sync import sync_to_async
from django.db import IntegrityError
from company.models import Contacts
from order.models import Order
from users.models import CustomUser


@sync_to_async
def create_user_db(user_data):
    try:
        new_user = CustomUser.objects.create(**user_data)
        return new_user
    except IntegrityError:
        raise Exception("User already exists")


@sync_to_async
def login_user(phone, password, tg_id, tg_u, user_lang):
    user = CustomUser.objects.filter(phone_number=phone).last()
    if user and check_password(password, user.password):
        user.telegram_id = tg_id
        user.tg_username = f"https://t.me/{tg_u}"
        user.user_lang = user_lang
        user.save()
        return user
    else:
        return None


@sync_to_async
def get_user_db(telegram_id):
    try:
        user = CustomUser.objects.get()
        return user
    except CustomUser.DoesNotExist:
        return None


@sync_to_async
def get_company_contacts():
    contact = Contacts.objects.last()
    return contact


@sync_to_async
def get_my_orders(phone_number):
    return list(Order.objects.all().filter(phone_number=phone_number))
