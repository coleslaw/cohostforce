from django.apps import AppConfig


class OnlineSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'online_site'
    def ready(self):
        from online_site import models
