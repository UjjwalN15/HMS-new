from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Purchase_Products, Product, Purchase
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

@receiver(post_save, sender=Purchase_Products)
def update_product(sender, instance, created, **kwargs):
    try:
        product = Product.objects.get(name=instance.name)
        product.description = instance.details
        product.stock += instance.quantity #For adding quantity if product is purchased
        product.price = instance.price
        product.category = instance.category
        product.supplier = instance.supplier 
        product.department = instance.department  
    except Product.DoesNotExist:
        product = Product.objects.create(
            name=instance.name,
            description=instance.details,
            stock=instance.quantity,
            price=instance.price,
            category=instance.category,
            supplier=instance.supplier,
            department=instance.department,
        )

    product.save()  # Ensure correct handling of ManyToManyField
    
#for subtracting from the quantity if purchased
@receiver(post_save, sender=Purchase)
def update_product(sender, instance, created, **kwargs):
    if created:  # Only update if the purchase was newly created
        product = instance.product
        product.stock -= instance.quantity
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