from django.utils.translation import gettext_lazy as _
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Banner(models.Model):
    title = models.CharField(_('title'), max_length=255)
    subtitle = models.CharField(_('subtitle'), max_length=255)
    bg_image = models.OneToOneField('common.Media', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('banner')
        verbose_name_plural = _('banner')


class AboutUs(models.Model):
    desc = models.CharField(_('description'), max_length=255)
    video = models.OneToOneField('common.Media', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('About Us')
        verbose_name_plural = _('About Us')

    def __str__(self):
        return f"{self.id} - {self.desc}"


class AboutUsGallery(models.Model):
    image = models.OneToOneField("common.Media", blank=True, null=True, on_delete=models.SET_NULL)
    about_us = models.OneToOneField(AboutUs, on_delete=models.CASCADE, related_name='about_us')

    def __str__(self):
        return f"{self.about_us}-{self.image.file.url}"

    class Meta:
        verbose_name = _('About Us Gallery')
        verbose_name_plural = _('About Us Galleries')


class Contacts(models.Model):
    address = models.TextField(_('address'))
    phone_number1 = PhoneNumberField(_('phone number1'), max_length=20)
    phone_number2 = PhoneNumberField(_('phone number2'), max_length=20)
    work_time = models.CharField(_('work time'), max_length=255)

    def __str__(self):
        return f"{self.id}-{self.address}"

    class Meta:
        verbose_name = _('contacts')
        verbose_name_plural = _('contacts')


class ContactWithUs(models.Model):
    full_name = models.CharField(_('full name'), max_length=255)
    phone_number = PhoneNumberField(_('phone number'))
    subject = models.CharField(_('subject'), max_length=255)
    message = models.TextField(_('message'))

    class Meta:
        verbose_name = _('Contact With Us')
        verbose_name_plural = _('Contact with Us')


class SocialMedia(models.Model):
    link = models.URLField(_('link'))
    icon = models.CharField(_('icon'), max_length=255, help_text=_('write icon code'))

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = _('Social Media')
        verbose_name_plural = _('Social Medias')
