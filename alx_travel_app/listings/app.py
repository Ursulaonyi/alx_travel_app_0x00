from django.apps import AppConfig

class ListingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listings'
    verbose_name = 'Travel Listings'

    def ready(self):
        # Import signals here if needed
        pass