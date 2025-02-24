import threading
import logging
from django.conf import settings  # Import Django settings

class RealClient:
    def __init__(self):
        self.balance_lock = threading.Lock()
        self.balances = {}
        self.cashier_url = None  # Initialize cashier_url attribute
        self.logger = logging.getLogger(__name__)
        self.websocket_client = None  # Add a WebSocket client reference

    def update_balances(self, balances):
        with self.balance_lock:
            self.balances.update(balances)
            self.logger.info(f"Updated Real Balances: {self.balances}")

    def set_websocket_client(self, websocket_client):
        self.websocket_client = websocket_client
        self.logger.info(f"WebSocket client set: {self.websocket_client}")

    async def request_cashier_info(self, cashier, provider, verification_code):
        if not self.websocket_client or self.websocket_client.websocket is None:
            # Reinitialize the WebSocket client if not connected
            self.logger.info("Reinitializing WebSocket client...")
            from websocket_client import WebSocketClient  # Delayed import to avoid circular imports
            new_websocket_client = WebSocketClient(settings.REAL_APP_ID, settings.REAL_API_TOKEN)  # Use settings for app_id and api_token
            self.set_websocket_client(new_websocket_client)
            await new_websocket_client.connect()

        if self.websocket_client:
            self.logger.info(f"Requesting cashier info with WebSocket client: {self.websocket_client}")
            await self.websocket_client.request_cashier_info(cashier, provider, verification_code)
        else:
            self.logger.error("WebSocket client is not set!")

    async def request_deposit(self, amount):
        if not self.websocket_client or self.websocket_client.websocket is None:
            # Reinitialize the WebSocket client if not connected
            self.logger.info("Reinitializing WebSocket client...")
            from websocket_client import WebSocketClient  # Delayed import to avoid circular imports
            new_websocket_client = WebSocketClient(settings.REAL_APP_ID, settings.REAL_API_TOKEN)  # Use settings for app_id and api_token
            self.set_websocket_client(new_websocket_client)
            await new_websocket_client.connect()

        if self.websocket_client:
            self.logger.info(f"Requesting deposit with WebSocket client: {self.websocket_client}")
            await self.websocket_client.request_deposit(amount)
        else:
            self.logger.error("WebSocket client is not set!")

    async def request_withdrawal(self, amount, email):
        if not self.websocket_client or self.websocket_client.websocket is None:
            # Reinitialize the WebSocket client if not connected
            self.logger.info("Reinitializing WebSocket client...")
            from websocket_client import WebSocketClient  # Delayed import to avoid circular imports
            new_websocket_client = WebSocketClient(settings.REAL_APP_ID, settings.REAL_API_TOKEN)  # Use settings for app_id and api_token
            self.set_websocket_client(new_websocket_client)
            await new_websocket_client.connect()

        if self.websocket_client:
            self.logger.info(f"Requesting withdrawal with WebSocket client: {self.websocket_client}")
            await self.websocket_client.request_withdrawal(amount, email)
        else:
            self.logger.error("WebSocket client is not set!")
    
    async def confirm_email_verification_code(self, verification_code):
        if not self.websocket_client or self.websocket_client.websocket is None:
            self.logger.info("Reinitializing WebSocket client...")
            from websocket_client import WebSocketClient
            new_websocket_client = WebSocketClient(settings.REAL_APP_ID, settings.REAL_API_TOKEN)
            self.set_websocket_client(new_websocket_client)
            await new_websocket_client.connect()

        if self.websocket_client:
            self.logger.info(f"Confirming email verification code with WebSocket client: {self.websocket_client}")
            await self.websocket_client.confirm_email_verification_code(verification_code)
        else:
            self.logger.error("WebSocket client is not set!")
    
    async def handle_confirm_email_response(self, data):
        if not self.websocket_client:
            return {"error": "WebSocket client is not connected."}
        response = await self.websocket_client.handle_confirm_email_response(data)
        return response 

    def update_cashier_url(self, cashier_url):
        self.cashier_url = cashier_url
        self.logger.info(f"Updated Cashier URL: {self.cashier_url}")

# Create an instance of RealClient
real_client_instance = RealClient()
