# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TradingSignal
from .views import send_signal  # Import your send_signal view logic
from django.http import HttpRequest  # To simulate a request

@receiver(post_save, sender=TradingSignal)
def trigger_send_signal(sender, instance, created, **kwargs):
    print("Post-save signal triggered!")  # Debug
    if created:
        print(f"Signal triggered for: {instance}")  # Debug
        request = HttpRequest()
        request.method = 'GET'
        send_signal(request)

