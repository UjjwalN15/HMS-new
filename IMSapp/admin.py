from django.contrib import admin
# admin.py
from .models import *


admin.site.register(Department)
admin.site.register(ProductCategory)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Purchase_Products)
admin.site.register(Billing)
admin.site.register(Revenue)
admin.site.register(Expenses)
admin.site.register(Reports)

