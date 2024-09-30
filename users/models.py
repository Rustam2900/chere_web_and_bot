from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from users.validators import phone_number_validator

class CustomUserManager(UserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        LEGAL = 'legal', _('Legal')
        PRIVATE = 'private', _('Private')

    full_name = models.CharField(_("full name"), blank=True, max_length=255)
    username = models.CharField(_("username"), blank=True, max_length=255, null=True)
    email = models.EmailField(_("email address"), blank=True, null=True)
    phone_number = models.CharField(_("phone number"), blank=True, unique=True, validators=[phone_number_validator], max_length=20)
    password = models.CharField(_("password"), blank=True, max_length=255)
    reminder_days = models.PositiveIntegerField(_("reminder days"), blank=True, null=True)
    user_type = models.CharField(
        _("user type"), choices=UserType.choices, default=UserType.PRIVATE, blank=True, max_length=255)
    user_lang = models.CharField(_("user language"), blank=True, null=True, max_length=10)
    telegram_id = models.CharField(_("telegram id"), blank=True, null=True, max_length=255, unique=True)
    tg_username = models.CharField(
        _("telegram username"), blank=True, null=True, max_length=255, unique=True)
    company_name = models.CharField(_("company name"), blank=True, null=True, max_length=255)



    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    USERNAME_FIELD = "phone_number"
    objects = CustomUserManager()