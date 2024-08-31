from modeltranslation.translator import TranslationOptions, register, translator

from .models import Product
@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'desc')