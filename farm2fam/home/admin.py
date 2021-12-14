from django.contrib import admin
from home.models import  Farmer
from .models import *
# Register your models here.

admin.site.register(Farmer)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)