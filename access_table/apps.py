from django.apps import AppConfig


class AccessTableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'access_table'
    verbose_name = 'Таблиця контролю доступу'
