from django.contrib import admin
from .models import Product, Order, OrderDetail

# from simple_history.admin import SimpleHistoyAdmin

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)