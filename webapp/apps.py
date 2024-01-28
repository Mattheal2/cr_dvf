from django.apps import AppConfig
from .data import state


class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webapp'
    
    data = state.get_default_data()
    