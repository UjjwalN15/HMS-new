from rest_framework import serializers
from .models import *
from decimal import Decimal
from django.utils.timezone import now
from pytz import timezone
import pytz
kathmandu_tz = timezone('Asia/Kathmandu')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department'] = instance.department.name if instance.department else None
        representation['category'] = instance.category.name if instance.category else None
        
        return representation
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

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
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Billing
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        purchases_data = []
        total = Decimal(0)
        # Iterate over related purchases of the instance's patient
        for purchase in instance.patient.purchases.all():
            purchased_date_local = purchase.purchased_date.astimezone(kathmandu_tz)
            purchase_data = {
                'product': purchase.product.name,
                'price': format(purchase.product.price, '.2f'),
                'quantity': format(purchase.quantity,),
                'total': format(purchase.total, '.2f'),
                'purchased_date_time': purchased_date_local.isoformat(),
            }
            purchases_data.append(purchase_data)
            total += Decimal(purchase.total)
        representation['total'] = format(total, '.2f')
        representation['purchases'] = purchases_data
        return representation
    
class PurchaseProductsSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Purchase_Products
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
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