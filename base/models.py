from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.utils.timezone import now
from rest_framework.generics import GenericAPIView
from django.core.validators import RegexValidator



class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=300, null=True, blank=True)
    password = models.CharField(max_length=128)  # Adjusting max length to a common value
    groups = models.ManyToManyField(Group, blank=True)  # Default will be handled differently
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Ensure the user is assigned to the default group if not already assigned
        super().save(*args, **kwargs)
        default_group = Group.objects.get(id=6)
        if not self.groups.exists():
            self.groups.add(default_group)
    
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
    contact_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Contact number must be exactly 10 digits.'
    )
    phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[contact_validator],
        help_text="Enter a 10-digit contact number"
    )
    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'),('others','Others')])
    address = models.CharField(max_length=300)
    contact_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Contact number must be exactly 10 digits.'
    )
    phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[contact_validator],
        help_text="Enter a 10-digit contact number"
    )
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
    contact_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Contact number must be exactly 10 digits.'
    )
    phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[contact_validator],
        help_text="Enter a 10-digit contact number"
    )
    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
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
    contact_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Contact number must be exactly 10 digits.'
    )
    contact_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[contact_validator],
        help_text="Enter a 10-digit contact number"
    )
    date = models.DateTimeField(default=nepal_time_default)
    status = models.CharField(max_length=100,choices=[('pending','Pending'),('solved','Solved')], default='pending')
    def __str__(self):
        return self.name