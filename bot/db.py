
from asgiref.sync import sync_to_async, async_to_sync
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
def get_user_db(phone_number):
    try:
        user = CustomUser.objects.get(phone_number=phone_number)
        return user
    except CustomUser.DoesNotExist:
        return None

@sync_to_async
def get_company_contacts():
    contact = Contacts.objects.last()
    return contact

@sync_to_async
def get_my_orders(user):
    print("DB ",user)
    return list(Order.objects.all().filter(user=user))
