#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
from websocket_client import start_websocket_client
from TradeSphere.demo_client import DemoClient
from TradeSphere.real_client import RealClient, real_client_instance
from django.conf import settings  # Import settings module

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'derivapp.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Create instances of DemoClient and RealClient
    demo_client_instance = DemoClient()
    real_client_instance = RealClient()

    # Start WebSocket clients for demo and real accounts with their respective app_id and api_token
    demo_client = start_websocket_client(app_id=settings.DEMO_APP_ID, api_token=settings.DEMO_API_TOKEN)
    real_client = start_websocket_client(app_id=settings.REAL_APP_ID, api_token=settings.REAL_API_TOKEN)

    # Set WebSocket client for RealClient instance
    real_client_instance.set_websocket_client(real_client)
    print(f"WebSocket client for real_client_instance: {real_client_instance.websocket_client}")

    # Start WebSocket client threads
    if not getattr(demo_client, 'thread', None) or not demo_client.thread.is_alive():  # Use getattr to check for attribute
        demo_client.start()
    if not getattr(real_client, 'thread', None) or not real_client.thread.is_alive():  # Use getattr to check for attribute
        real_client.start()

    # Assign the WebSocket client instances to the class instances
    demo_client_instance.update_balances(demo_client.balances)
    real_client_instance.update_balances(real_client.balances)

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
