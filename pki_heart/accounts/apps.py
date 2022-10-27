from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # workaround to customize REDIRECT_FIELD_NAME
    def ready(self):
        from django.conf import settings
        from django.contrib import auth
        auth.REDIRECT_FIELD_NAME = settings.REDIRECT_FIELD_NAME
