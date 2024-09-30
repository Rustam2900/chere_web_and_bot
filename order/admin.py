from django.contrib import admin
from order.models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderMinSum)
admin.site.register(CartItem)