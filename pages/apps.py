from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        import account.signals


