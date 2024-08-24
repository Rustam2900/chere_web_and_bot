from random import choices

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):

    class UserType(models.TextChoices):
        LEGAL = 'Legal', _('Legal')
        PRIVATE = 'Private', _('Private')


    full_name = models.CharField(_("full name"), blank=True, max_length=255)
    username = models.CharField(_("username"), blank=True, max_length=255, unique=True)
    email = models.EmailField(_("email address"),blank=True, null=True, unique=True)
    phone_number = PhoneNumberField(_("phone number"), blank=True, null=True, unique=True)
    password = models.CharField(_("password"), blank=True, max_length=255)
    user_type = models.CharField(
        _("user type"), choices=UserType.choices, default=UserType.PRIVATE , blank=True, max_length=255)
    telegram_id = models.CharField(_("telegram id"), blank=True, null=True, max_length=255, unique=True)
    tg_username = models.CharField(
        _("telegram username"), blank=True, null=True, max_length=255, unique=True)

    def __str__(self):
        return self.username

