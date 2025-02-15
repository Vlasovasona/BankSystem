from django.apps import AppConfig

# содержит основную конфигурацию приложения

class BankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bank'
