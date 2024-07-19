from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import  AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from IMSapp.models import *
from django.core.exceptions import ValidationError
from .validators import CustomPasswordValidator
from rest_framework.exceptions import PermissionDenied
# Create your views here.


class PatientApiView(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filterset_fields = ['name','phone','email']
    search_fields = ['name']
class UserApiView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Doctor_SpecialityApiView(ModelViewSet):
    queryset = Doctor_Speciality.objects.all()
    serializer_class = Doctor_SpecialitySerializer
    filterset_fields = ['name']
    search_fields = ['name']

class DoctorApiView(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filterset_fields = ['name','phone','email']
    search_fields = ['name','specialty','address']
    
class Staff_PositionApiView(ModelViewSet):
    queryset = Staff_Position.objects.all()
    serializer_class = Staff_PositionSerializer
    filterset_fields = ['name']
    search_fields = ['name']


class StaffApiView(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filterset_fields = ['name','phone','email']
    search_fields = ['name','role','address']
    def get_queryset(self):
        # Restrict queryset to the current staff member
        return Staff.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        # Ensure only the current staff member can update their own information
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to update other staff members' information.")

class AppointmentApiView(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['status']
    search_fields = ['patient__name','doctor__name','status']

class MedicalRecordApiView(ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    parser_classes = (MultiPartParser, FormParser)
    filterset_fields = ['date']
    search_fields = ['diagnosis','treatments','doctor__name','patient__name']
    

class EmergencyApiView(ModelViewSet):
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializer
    permission_classes = [AllowAny]
    filterset_fields = ['name','contact_number','email']
    search_fields = ['title','description']
    
@permission_classes([AllowAny,])
class LogoutView(APIView):
    def post(self, request, format=None):
        # Simply delete the token to force a logout
        request.user.auth_token.delete()
        return Response("Logout Successful",status=status.HTTP_200_OK)

    
@api_view(['POST'])
@permission_classes([AllowAny,]) #This permission class should always below the api view
def Login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=email, password=password)
    if user == None:
        return Response("Invalid Credentials",status=status.HTTP_404_NOT_FOUND)
    else:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(token.key)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        phone = request.data.get('phone')
        if User.objects.filter(phone=phone).exists():
            return Response({'phone': ['Phone number already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Validate the password
            CustomPasswordValidator().validate(password)
            # If valid, hash the password
            hash_password = make_password(password)
            
            # Save the user instance
            user = serializer.save()
            user.password = hash_password
            user.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # If password validation fails, return the errors
            return Response({'password': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny,]) #This permission class should always below the api view
def groups(request):
    groups_obj = Group.objects.all()
    serializer = GroupSerializer(groups_obj, many = True)
    return Response(serializer.data)