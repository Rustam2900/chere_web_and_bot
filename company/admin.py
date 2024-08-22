from django.contrib import admin

from company.models import Banner, AboutUsGallery, AboutUs, ContactWithUs, SocialMedia, Contacts

admin.site.register(Banner)
admin.site.register(AboutUsGallery)
admin.site.register(ContactWithUs)
admin.site.register(Contacts)
admin.site.register(SocialMedia)

class AboutUsGalleryInline(admin.StackedInline):
    model = AboutUsGallery
    extra = 1

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    inlines = [AboutUsGalleryInline]


    

