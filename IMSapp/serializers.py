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
    # department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), many=True)
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Iterate over related departments if it's a many-to-many relationship
        # department_data = []
        # for department in instance.department.all():
        #     department_data.append({
        #         'name': department.name,
        #     })
        
        representation['department'] = instance.department.name if instance.department else None
        representation['category'] = instance.category.name if instance.category else None
        representation['supplier'] = instance.supplier.name if instance.supplier else None
        
        return representation




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
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    
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
        representation['patient'] = instance.patient.name 
        representation['supplier'] = instance.supplier.name 
        representation['product'] = instance.product.name 
        return representation


class BillingSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Billing
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total = Decimal(0)
        purchases_data = []
        for purchase in instance.purchases.all():
            purchase_data = {
            'product': (purchase.product.name),
            'price': format(Decimal(purchase.product.price), '.2f'),
            'quantity': format(Decimal(purchase.quantity), '.2f'),
            'total': format(Decimal(purchase.total), '.2f'),
            }
            purchases_data.append(purchase_data)
            total += Decimal(purchase.quantity) * Decimal(purchase.product.price)
        representation['total'] = format(total, '.2f')
        representation['purchases'] = purchases_data
        representation['patient'] = instance.patient.name 
        return representation
    
class PurchaseProductsSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Purchase_Products
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # department_data = []
        # for department in instance.department.all():
        #     department_data.append({
        #         'name': department.name,
        #     })
        
        representation['department'] = instance.department.name if instance.department else None
        representation['category'] = instance.category.name if instance.category else None
        representation['supplier'] = instance.supplier.name if instance.supplier else None
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
        
