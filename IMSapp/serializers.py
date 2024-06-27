from rest_framework import serializers
from .models import *
from base.serializers import PatientSerializer
from decimal import Decimal

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
    patient = PatientSerializer()

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
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price', read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Billing
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total = Decimal(0)
        for purchase in instance.purchases.all():
            total += purchase.quantity * purchase.product.price
        representation['total'] = total
        return representation
        
class PurchaseProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase_Products
        fields = '__all__'
        
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
        
