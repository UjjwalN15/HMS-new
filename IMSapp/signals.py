from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Purchase_Products, Product, Purchase
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

@receiver(post_save, sender=Purchase_Products)
def update_product(sender, instance, created, **kwargs):
    product_name_capitalized = instance.name.capitalize()  # Convert the product name to capitalized
    product_description_capitalized = instance.details.capitalize()  # Convert the product name to capitalized

    try:
        # Perform the lookup using the lowercase product name
        product = Product.objects.get(name__iexact=product_name_capitalized)
        product.description = instance.details
        product.stock += instance.quantity  # For adding quantity if product is purchased
        product.price = instance.price
        product.category = instance.category
        product.supplier = instance.supplier
        product.department = instance.department
    except Product.DoesNotExist:
        # Create a new product using the lowercase product name
        product = Product.objects.create(
            name=product_name_capitalized,
            description=product_description_capitalized,
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