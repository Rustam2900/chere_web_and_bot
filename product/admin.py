from django.contrib import admin
from product.models import Product, ProductAttribute, WebOrder

admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(WebOrder)
