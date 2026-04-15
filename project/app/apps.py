from django.apps import AppConfig
from django.conf import settings
import sys

class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals

       

    
    


