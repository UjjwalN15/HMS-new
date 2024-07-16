from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.utils.timezone import now
from base.validators import CustomPasswordValidator
from .validators import validate_appointment_date, contact_validator


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=300, null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        default_group = Group.objects.get(id=6)
        if not self.groups.exists():
            self.groups.add(default_group)

    def set_password(self, raw_password):
        # Perform Django's built-in password validation
        CustomPasswordValidator(raw_password, self)
        
        # Set password using Django's built-in method
        super().set_password(raw_password)
        
        # Ensure validation is triggered
        self.full_clean()
    
class Doctor_Speciality(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'),('others','Others')])
    address = models.CharField(max_length=300)
    specialty = models.ForeignKey(Doctor_Speciality, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,unique=True,validators=[contact_validator],help_text="Enter a 10-digit contact number")
    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'),('others','Others')])
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=10,unique=True,validators=[contact_validator],help_text="Enter a 10-digit contact number")
    medical_history = models.TextField(blank=True)
    schedule = models.DateTimeField(default=now)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return self.name




class Staff(models.Model): 
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'),('others','Others')])
    address = models.CharField(max_length=300)
    role = models.ForeignKey(Group, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,unique=True,validators=[contact_validator],help_text="Enter a 10-digit contact number")
    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField(validators=[validate_appointment_date])
    status = models.CharField(max_length=100, choices=[('scheduled', 'Scheduled'), ('canceled', 'Canceled'), ('completed', 'Completed')],default='scheduled')
    def __str__(self):
        return self.patient.name

def nepal_time_default():
    return now()

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    diagnosis = models.TextField()
    treatments = models.TextField()
    prescriptions = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='medical_record/pdf/', null=True, blank=True)
    def __str__(self):
        return self.patient.name
    
    
class Emergency(models.Model):
    name = models.CharField(max_length=300, blank=False, null=False, default='Unnamed Emergency')
    email = models.EmailField(unique=True, null=False, blank=False)
    title = models.CharField(max_length=300)
    description = models.TextField()
    contact_number = models.CharField(max_length=10,unique=True,validators=[contact_validator],help_text="Enter a 10-digit contact number")
    date = models.DateTimeField(default=nepal_time_default)
    status = models.CharField(max_length=100,choices=[('pending','Pending'),('solved','Solved')], default='pending')
    def __str__(self):
        return self.name