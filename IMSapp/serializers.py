from rest_framework import serializers
from .models import *
from base.serializers import PatientSerializer
from decimal import Decimal
from django.db.models import Sum, F

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
# class PurchaseSerializer(serializers.ModelSerializer):
#     price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price', read_only=True)
#     total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     patient = PatientSerializer
#     class Meta:
#         model = Purchase
#         fields = '__all__'
class PurchaseSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price', read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Purchase
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        price = representation.get('price')
        quantity = representation.get('quantity')
        if price is not None and quantity is not None:
            total = Decimal(price) * Decimal(quantity)
            representation['total'] = str(total)
        return representation

class BillingSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    patient = PatientSerializer(read_only=True)
    # purchases = serializers.PrimaryKeyRelatedField(many=True, queryset=Purchase.objects.all())
    purchases = PurchaseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Billing  # Ensure you have imported the Billing model
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total = Decimal(0)
        for purchase in instance.purchases.all():
            total += Decimal(purchase.quantity) * Decimal(purchase.product.price)
        representation['total'] = format(total, '.2f')  # Ensures total has 2 decimal places
        return representation
        
class PurchaseProductsSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Purchase_Products
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        price = instance.price
        quantity = instance.quantity
        total = price * quantity
        representation['total'] = format(total, '.2f')  # Ensures the total has 2 decimal places
        return representation
        
class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'
        
class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = '__all__'
        
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'
        
