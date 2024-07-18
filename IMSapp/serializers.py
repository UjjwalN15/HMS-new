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
    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Billing
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        purchases_data = []
        total = Decimal(0)
        
        if instance.patient:
            for purchase in instance.patient.purchases.all():
                purchased_date_local = purchase.purchased_date.astimezone(kathmandu_tz)
                purchase_data = {
                    'product': purchase.product.name if purchase.product else None,
                    'price': format(purchase.product.price, '.2f') if purchase.product and purchase.product.price is not None else None,
                    'quantity': format(purchase.quantity) if purchase.quantity is not None else None,
                    'total': format(purchase.total, '.2f') if purchase.total is not None else None,
                    'purchased_date_time': purchased_date_local.isoformat(),
                }
                purchases_data.append(purchase_data)
                total += Decimal(purchase.total) if purchase.total is not None else Decimal(0)
        representation['patient'] = instance.patient.name if instance.patient else None
        representation['total'] = format(total, '.2f')
        representation['purchases'] = purchases_data
        return representation

    def create(self, validated_data):
        patient = validated_data.get('patient')
        billing = Billing.objects.create(patient=patient, status=validated_data.get('status'))

        # Associate purchases with the billing based on the patient
        purchases = Purchase.objects.filter(patient=patient)
        billing.purchases.set(purchases)

        # Calculate the total
        total = purchases.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        billing.total = total
        billing.save()
        return billing

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