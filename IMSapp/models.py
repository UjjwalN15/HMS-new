from django.db import models
from base.models import Patient
#For total
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from decimal import Decimal
from django.utils.timezone import now
from django.db.models import Sum, F
from django.db.models.signals import post_save, post_delete
from django.core.validators import RegexValidator
# Create your models here.    
class ProductCategory(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name #returns the name in admin panel
    
    
class Department(models.Model):
    name = models.CharField(max_length = 200,unique=True)
    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Contact number must be exactly 10 digits.'
    )
    contact = models.CharField(
        max_length=10,
        unique=True,
        validators=[contact_validator],
        help_text="Enter a 10-digit contact number"
    )
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    description = models.TextField()
    stock = models.IntegerField()
    category = models.ForeignKey(ProductCategory,on_delete = models.CASCADE, null = False)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Purchase(models.Model):
    patient = models.ForeignKey(Patient, related_name='purchases', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchased_date = models.DateTimeField(default=now)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def save(self, *args, **kwargs):
        self.price = Decimal(self.product.price)
        self.total = Decimal(self.quantity) * self.product.price
        super(Purchase, self).save(*args, **kwargs)
    def __str__(self):
        return self.product.name

class Purchase_Products(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super(Purchase_Products, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    
# class Billing(models.Model):
#     patient = models.ForeignKey(Patient, related_name='billing', on_delete=models.CASCADE, null=False, blank=False)
#     purchases = models.ManyToManyField(Purchase)
#     status = models.CharField(max_length=100, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])
#     def __str__(self):
#         return self.patient.name
class Billing(models.Model):
    patient = models.ForeignKey(Patient, related_name='billing', on_delete=models.CASCADE, null=False, blank=False)
    purchases = models.ManyToManyField(Purchase)
    status = models.CharField(max_length=100, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.patient.name

        
class Revenue(models.Model):
    title = models.CharField(max_length=300)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    def __str__(self):
        return self.title

class Expenses(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    amount = models.DecimalField(max_digits=15,decimal_places=2)
    date = models.DateField()
    def __str__(self):
        return self.title
    
class Reports(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()