#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time

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

    from websocket_client import start_websocket_client

    client = start_websocket_client()  # Initialize the WebSocket client

    def run_websocket_client():
        client.start()
                # Incase you want the websocket connection to go alive for a certain period
    # def stop_websocket_client_after_delay(client, delay):
    #     time.sleep(delay)  # Here is the time.sleep(10) call
    #     print("[main] Calling client.stop()")
    #     client.stop()
    #     print("[main] client.stop() called")

    websocket_thread = threading.Thread(target=run_websocket_client, daemon=True)
    websocket_thread.start()
                #  Change to your specified time, Time=Seconds
    # stop_thread = threading.Thread(target=stop_websocket_client_after_delay, args=(client, 10), daemon=True)
    # stop_thread.start()

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
