from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Doctor_Speciality)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Staff)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Emergency)
