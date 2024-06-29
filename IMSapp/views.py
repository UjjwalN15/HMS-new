# views.py

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F, Q
from .models import *
from base.models import *
from .serializers import *
from decimal import Decimal

class DepartmentApiView(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_fields = ['name','floor']
    search_fields = ['name']

class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'department']
    search_fields = ['name','description']

class ProductCategoryApiView(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filterset_fields = ['name']
    search_fields = ['name']

class SupplierApiView(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filterset_fields = ['name']
    search_fields = ['name','address']

class ExpensesApiView(ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    search_fields = ['title','description']

class RevenueViewSet(ModelViewSet):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer
    search_fields = ['title','description']
    
class PurchaseProductViewSet(ModelViewSet):
    queryset = Purchase_Products.objects.all()
    serializer_class = PurchaseProductsSerializer
    filterset_fields = ['name', 'supplier']
    search_fields = ['name','details']

class BillingApiView(ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    filterset_fields = ['status','patient']
    search_fields = ['patient__name']

class PurchaseApiView(GenericAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filterset_fields = ['product', 'supplier','patient']
    search_fields = ['patient__name']

    def get(self, request):
        queryset = self.get_queryset()
        filter_queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(filter_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            if product.stock >= quantity:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Stock is less than the requested quantity."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PurchaseDetailApiView(GenericAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get(self, request, pk):
        try:
            queryset = Purchase.objects.get(id=pk)
        except:
            return Response("Purchase Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            queryset = Purchase.objects.get(id=pk)
        except:
            return Response("Purchase Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Data Updated!")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            queryset = Purchase.objects.get(id=pk)
        except:
            return Response("Purchase Not Found", status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response("Data Deleted!")

    def patch(self, request, pk=None):
        queryset = self.get_object()
        serializer = PurchaseSerializer(instance=queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportViewSet(ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer
    search_fields = ['title']

    def list(self, request):
        users_count = User.objects.count()
        patients_count = Patient.objects.count()
        appointments_count = Appointment.objects.count()
        revenue_count_HMS = Revenue.objects.count()
        total_revenue_HMS = Revenue.objects.aggregate(Sum('amount'))['amount__sum']
        revenue_count_IMS = Purchase.objects.count()
        total_revenue_IMS = Purchase.objects.aggregate(total_expense=Sum(F('product__price') * F('quantity')))['total_expense']
        total_products = Product.objects.count()
        total_staffs = Staff.objects.count() 
        total_doctors = Doctor.objects.count()
        expenses_count = Expenses.objects.count()
        purchase_product_count = Purchase_Products.objects.count()
        expenses = Expenses.objects.aggregate(Sum('amount'))['amount__sum']
        purchase_product_expenses = Purchase_Products.objects.aggregate(total_expense=Sum(F('price') * F('quantity')))['total_expense']
        total_doctors = Doctor.objects.count()
        patient_kid = Patient.objects.filter(age__lte=18).count()
        patient_adult = Patient.objects.filter(Q(age__lte=40) & Q(age__gt=18)).count()
        patient_old = Patient.objects.filter(age__gt=40)

        report = {
            'total_system_users': users_count + patients_count + total_staffs + total_doctors,
            'total_patients': patients_count,
            'total_staffs': total_staffs + total_doctors,
            'total_users' : users_count,
            'total_appointments': appointments_count,
            'revenue_count_HMS' : revenue_count_HMS,
            'revenue_HMS': (total_revenue_HMS if total_revenue_HMS else 0),
            'revenue_count_IMS' : revenue_count_IMS,
            'revenue_IMS': (total_revenue_IMS if total_revenue_IMS else 0),
            'total revenue': (total_revenue_HMS if total_revenue_HMS else 0) + (total_revenue_IMS if total_revenue_IMS else 0 ),
            'expenses_count' : expenses_count,
            'expenses': (expenses if expenses else 0),
            'product_purchase_count': purchase_product_count,
            'product_purchase_expenses': (purchase_product_expenses if purchase_product_expenses else 0),
            'total_expenses': (expenses if expenses else Decimal('0.0')) + (purchase_product_expenses if  purchase_product_expenses else Decimal('0.0')),
            'total_products': total_products,
            'total_doctors': total_doctors,
            'kid_patient' : patient_kid,
            'adult_patient' : patient_adult,
            'old_patient' : patient_old,
        }

        return Response(report)