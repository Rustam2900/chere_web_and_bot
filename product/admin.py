from django.contrib import admin
from product.models import Product, ProductAttribute, WebOrder

class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    extra = 1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeInline]
    list_display = ('title', 'desc', 'size', 'price', 'discount')


admin.site.register(WebOrder)
