from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        
class Doctor_SpecialitySerializer(ModelSerializer):
    class Meta:
        model = Doctor_Speciality
        fields = '__all__'
        
class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        
        
class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        
class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        
class MedicalRecordSerializer(ModelSerializer):
    pdf_file = serializers.FileField(required=False, allow_null=True)
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        
class EmergencySerializer(ModelSerializer):
    class Meta:
        model = Emergency
        fields = '__all__'
        

        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','groups']
        
class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']   