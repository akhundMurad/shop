from django.contrib import admin

from products.models import Product, Order

admin.site.register(Product)
admin.site.register(Order)
