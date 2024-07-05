from django.apps import AppConfig

class ImsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IMSapp'

    def ready(self):
        import IMSapp.signals  # Ensure this points to your actual signals module
