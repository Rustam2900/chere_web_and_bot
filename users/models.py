from random import choices

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        LEGAL = 'legal', _('Legal')
        PRIVATE = 'private', _('Private')

    full_name = models.CharField(_("full name"), blank=True, max_length=255)
    username = models.CharField(_("username"), blank=True, max_length=255, unique=True)
    email = models.EmailField(_("email address"), blank=True, null=True )
    phone_number = PhoneNumberField(_("phone number"), blank=True, null=True, unique=True)
    password = models.CharField(_("password"), blank=True, max_length=255)
    user_type = models.CharField(
        _("user type"), choices=UserType.choices, default=UserType.PRIVATE, blank=True, max_length=255)
    telegram_id = models.CharField(_("telegram id"), blank=True, null=True, max_length=255, unique=True)
    tg_username = models.CharField(
        _("telegram username"), blank=True, null=True, max_length=255, unique=True)
    company_name = models.CharField(_("company name"), blank=True, null=True, max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
