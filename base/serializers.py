from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password


class Doctor_SpecialitySerializer(ModelSerializer):
    class Meta:
        model = Doctor_Speciality
        fields = '__all__'
class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['specialty'] = instance.specialty.name if instance.specialty else None
        return representation
class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['doctor'] = instance.doctor.name if instance.doctor else None
        return representation
        
class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']
        
class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['role'] = instance.role.name if instance.role else None
        return representation
        
class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = instance.patient.name if instance.patient else None
        representation['doctor'] = instance.doctor.name if instance.doctor else None
        return representation
        
class MedicalRecordSerializer(ModelSerializer):
    pdf_file = serializers.FileField(required=False, allow_null=True)
    class Meta:
        model = MedicalRecord
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = instance.patient.name if instance.patient else None
        representation['doctor'] = instance.doctor.name if instance.doctor else None
        return representation
        
class EmergencySerializer(ModelSerializer):
    class Meta:
        model = Emergency
        fields = '__all__'
        

        
class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email','username','password','groups']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Iterate over related groups if it's a many-to-many relationship
        group_data = []
        for group in instance.groups.all():
            group_data.append({
                'name': group.name,
            })
        representation['groups'] = group_data
        return representation
    
    def validate_password(self, value):
        validate_password(value)
        return value