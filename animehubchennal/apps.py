from django.apps import AppConfig


class AnimehubchennalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'animehubchennal'

    def ready(self):
        from .auto_call import start_auto_call
        start_auto_call()
