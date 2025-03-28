from django.apps import AppConfig
from pathlib import Path


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    path = Path(__file__).resolve().parent 