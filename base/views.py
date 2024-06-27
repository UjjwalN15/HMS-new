from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from IMSapp.models import *
from django.db.models import Sum, Count, Avg
# Create your views here.

class PatientApiView(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    search_fields = ['name']

class Doctor_SpecialityApiView(ModelViewSet):
    queryset = Doctor_Speciality.objects.all()
    serializer_class = Doctor_SpecialitySerializer

class DoctorApiView(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class StaffApiView(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class AppointmentApiView(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class MedicalRecordApiView(ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    
class EmergencyApiView(ModelViewSet):
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializer
    permission_classes = [AllowAny]
    
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
@permission_classes([AllowAny,]) #This permission class should always below the api view
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        hash_password = make_password(password)
        a = serializer.save()
        a.password = hash_password
        a.save()
        return Response('Data Created!', status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny,]) #This permission class should always below the api view
def groups(request):
    groups_obj = Group.objects.all()
    serializer = GroupSerializer(groups_obj, many = True)
    return Response(serializer.data)

class PatientDemographicsReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gender_distribution = Patient.objects.values('patient.gender').annotate(count=Count('gender'))
        age_distribution = Patient.objects.values('patient.age').annotate(count=Count('age'))
        
        return Response({
            'gender_distribution': gender_distribution,
            'age_distribution': age_distribution
        })


class AppointmentsReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_appointments = Appointment.objects.count()
        appointments_by_date = Appointment.objects.values('date').annotate(count=Count('date'))
        
        return Response({
            'total_appointments': total_appointments,
            'appointments_by_date': appointments_by_date
        })

