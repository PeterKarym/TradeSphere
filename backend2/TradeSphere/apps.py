from django.apps import AppConfig


class TradesphereConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TradeSphere'

    def ready(self):
        print("Loading signals...")  # Debug message to confirm signals are being loaded
        import TradeSphere.signals  # Ensure signals are loaded
