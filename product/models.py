from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Product(models.Model):
    title = models.CharField(_('title'), max_length=100)
    desc = models.TextField(_('description'))
    size = models.DecimalField(_('size'), max_digits=5, decimal_places=1, help_text=_('size in liters'))
    image = models.OneToOneField("common.Media", on_delete=models.CASCADE)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, default=0, help_text=_("price in so'm"))
    discount = models.ForeignKey("Discount", on_delete=models.CASCADE, related_name="products", blank=True, null=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="attributes")
    title = models.CharField(_('title'), max_length=255)
    value = models.CharField(_('value'), max_length=255)

    class Meta:
        verbose_name = _('Product Attribute')
        verbose_name_plural = _('Product Attributes')

    def __str__(self):
        return f"{self.product} - {self.title}: {self.value}"


class WebOrder(models.Model):
    full_name = models.CharField(_('full name'), max_length=255)
    phone_number = PhoneNumberField(_('phone number'))

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"

    class Meta:
        verbose_name = _("Web Order")
        verbose_name_plural = _("Web Orders")


class Discount(models.Model):
    title = models.CharField(_('title'), max_length=255)
    desc = models.TextField(_('description'))
    image = models.ForeignKey("common.Media", on_delete=models.CASCADE, related_name="images_discount")
    percentage = models.PositiveIntegerField(_('percentage'), default=0)
