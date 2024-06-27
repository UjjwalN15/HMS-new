from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import Patient
#For total
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
# Create your models here.    
class ProductCategory(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name #returns the name in admin panel
    
    
class Department(models.Model):
    name = models.CharField(max_length = 200,unique=True)
    floor = models.IntegerField()

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    stock = models.IntegerField()
    category = models.ForeignKey(ProductCategory,on_delete = models.CASCADE, null = False)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
    department = models.ManyToManyField(Department)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return self.name
    
    
class Purchase(models.Model):
    patient = models.ForeignKey(Patient, related_name='purchases', on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False, blank=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Ensure total field is added

    def save(self, *args, **kwargs):
        if self.product.stock >= self.quantity:
            self.total = self.quantity * self.product.price
            super(Purchase, self).save(*args, **kwargs)
        else:
            raise ValueError("Stock less than quantity.")
    # Property to calculate total dynamically
    @property
    def total(self):
        return self.quantity * self.product.price

    # Override save method to check stock and save if valid
    def save(self, *args, **kwargs):
        if self.product.stock >= self.quantity:
            super().save(*args, **kwargs)
        else:
            raise ValueError("Stock is less than quantity.")
    
class Purchase_Products(models.Model):
    name = models.CharField(max_length=300)
    quantity = models.IntegerField()
    # product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)  CASCADE removes all the data when the Department is deleted
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
    supplier = models.ForeignKey(Supplier,on_delete = models.CASCADE, null = False, blank=False)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
    @property
    def total(self):
        return self.quantity * self.product.price
    
class Billing(models.Model):
    patient = models.ForeignKey(Patient, related_name='billing', on_delete=models.CASCADE, null=False, blank=False)
    purchases = models.ManyToManyField(Purchase)
    status = models.CharField(max_length=100, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])
    total = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
        
class Revenue(models.Model):
    title = models.CharField(max_length=300)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()

class Expenses(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    amount = models.DecimalField(max_digits=15,decimal_places=2)
    date = models.DateField()
    
class Reports(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()