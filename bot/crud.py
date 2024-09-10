
from asgiref.sync import sync_to_async
from django.db import IntegrityError

from users.models import CustomUser

@sync_to_async
def create_user(user_data):
    try:
        new_user = CustomUser.objects.create(**user_data)
        return new_user
    except IntegrityError:
        raise Exception("User already exists")
