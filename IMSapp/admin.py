from django.contrib import admin
# admin.py
from .models import *

class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    # Ensure that user creation happens here if necessary


admin.site.register(Department)

