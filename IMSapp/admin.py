from django.contrib import admin

# Register your models here.
# admin.py
from base.models import Staff, User
from .models import *

class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    # Ensure that user creation happens here if necessary

admin.site.register(Staff)
admin.site.register(Purchase_Products)

