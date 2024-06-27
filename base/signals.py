# # signals.py for automatic creation of User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Staff, User

# @receiver(post_save, sender=Staff)
# def create_user_for_staff(sender, instance, created, **kwargs):
#     if created:
#         user = User.objects.create(
#             username=instance.user.username,
#             email=instance.user.email,
#             first_name=instance.user.first_name,
#             last_name=instance.user.last_name,
#             # Copy any other necessary fields from Staff to User
#         )
#         instance.user = user
#         instance.save()
