from modeltranslation.translator import TranslationOptions, register

from .models import AboutUs, Banner, Contacts


@register(AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = ('desc',)

@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle')

@register(Contacts)
class ContactsTranslationOptions(TranslationOptions):
    fields = ('address',)