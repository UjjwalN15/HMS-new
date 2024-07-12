from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import Sum, F
from .models import Purchase_Products, Product, Purchase
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

@receiver(post_save, sender=Purchase_Products)
def update_or_create_product(sender, instance, created, **kwargs):
    product_name = instance.name.capitalize()  # Capitalize the product name
    product_description = instance.details.capitalize()  # Capitalize the product description

    try:
        # Try to find an existing product with a case-insensitive match on the name
        product = Product.objects.get(name__iexact=product_name)
        product.description = product_description
        product.stock += instance.quantity  # Increase stock if the product is purchased again
        product.price = instance.price
        product.category = instance.category
        product.department = instance.department
    except Product.DoesNotExist:
        # Create a new product if it doesn't exist
        product = Product.objects.create(
            name=product_name,
            description=product_description,
            stock=instance.quantity,
            price=instance.price,
            category=instance.category,
            department=instance.department,
        )

    product.save()  # Save the product instance

@receiver(post_save, sender=Purchase)
def adjust_product_stock(sender, instance, created, **kwargs):
    if created:  # Only adjust stock if the purchase was newly created
        product = instance.product
        product.stock -= instance.quantity  # Decrease stock based on the purchase quantity
        product.save()
        

#For sending mail dynamically
@receiver(post_save, sender=Product)
def send_stock_alert(sender, instance, **kwargs):
    if instance.stock <= 50:
        subject = f'Stock Alert for Product: {instance.name}'
        message = f'The stock for product "{instance.name}" is below 50. Current stock: {instance.stock}.Please contact the supplier to purchase the product.Thank you. HMS TEAM'
        recipients = ['spaceandnature98@gmail.com', 'itsmeujjwal725@gmail.com', 'boysfuny2020@gmail.com']
        
        send_mail(
            subject,
            message,
            'sajilokheti54@gmail.com',  # From email
            recipients,
            fail_silently=False,  # Set to True to avoid errors if email sending fails
        )