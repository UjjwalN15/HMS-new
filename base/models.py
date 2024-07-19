from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.utils.timezone import now
from .validators import validate_appointment_date, contact_validator, validate_schedule_date, CustomPasswordValidator
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email

class User(AbstractUser):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    age = models.IntegerField()
    username = models.CharField(max_length=300, null=True, blank=True)
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'),('others','Others')])
    phone = models.CharField(max_length=10,validators=[contact_validator],help_text="Enter a 10-digit contact number")
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group,blank=True)
    address = models.CharField(max_length=300)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
        default_group = Group.objects.get(id=6)
        if not self.groups.exists():
            self.groups.add(default_group)
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    
class Doctor_Speciality(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
# class Doctor(models.Model):
#     name = models.CharField(max_length=300)
#     email = models.EmailField(unique=True)
#     age = models.PositiveIntegerField()
#     gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'),('others','Others')])
#     address = models.CharField(max_length=300)
#     specialty = models.ForeignKey(Doctor_Speciality, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=10,unique=True,validators=[contact_validator],help_text="Enter a 10-digit contact number")
#     def __str__(self):
#         return self.name
#     def save(self, *args, **kwargs):
#         # Hash the password before saving the model
#         self.password = make_password(self.password)
#         super().save(*args, **kwargs)
class Doctor(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(unique=True, validators=[validate_email])
    password = models.CharField(max_length=300)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=100, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')])
    address = models.CharField(max_length=300)
    specialty = models.ForeignKey(Doctor_Speciality, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, unique=True, validators=[contact_validator], help_text="Enter a 10-digit contact number")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Apply custom password validation
        CustomPasswordValidator().validate(self.password)
        # Hash the password before saving the model
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Patient(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'),('others','Others')])
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=10,unique=True,validators=[contact_validator],help_text="Enter a 10-digit contact number")
    medical_history = models.TextField(blank=True)
    schedule = models.DateField(validators=[validate_schedule_date])
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Staff_Position(models.Model):
    name = models.CharField(max_length=255)

class Staff(models.Model): 
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'),('others','Others')])
    address = models.CharField(max_length=300)
    role = models.ForeignKey(Group, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,unique=True,validators=[contact_validator],help_text="Enter a 10-digit contact number")
    position = models.ForeignKey(Staff_Position, on_delete=models.CASCADE, default="Unknown Position")
    availability = models.BooleanField()
    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField(validators=[validate_appointment_date])
    status = models.CharField(max_length=100, choices=[('scheduled', 'Scheduled'), ('canceled', 'Canceled'), ('completed', 'Completed')],default='scheduled')
    def __str__(self):
        return self.patient.name

def nepal_time_default():
    return now()

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    diagnosis = models.TextField()
    treatments = models.TextField()
    prescriptions = models.TextField()
    pdf_file = models.FileField(upload_to='medical_record/pdf/', null=True, blank=True)
    def __str__(self):
        return self.patient.name
    
    
class Emergency(models.Model):
    name = models.CharField(max_length=300, default='Unnamed Emergency')
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    contact_number = models.CharField(max_length=10,unique=True,validators=[contact_validator],help_text="Enter a 10-digit contact number")
    date = models.DateTimeField(default=nepal_time_default)
    status = models.CharField(max_length=100,choices=[('pending','Pending'),('solved','Solved')], default='pending')
    def __str__(self):
        return self.name