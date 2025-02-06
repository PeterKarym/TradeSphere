import asyncio
import websockets
import json
import threading
import atexit
from threading import Lock
from TradeSphere.demo_client import demo_client_instance
from TradeSphere.real_client import real_client_instance
import re
from django.conf import settings  # Import Django settings

class WebSocketClient:
    def __init__(self, app_id, api_token):
        self.app_id = app_id
        self.api_token = api_token
        self.uri = f"wss://ws.derivws.com/websockets/v3?app_id={self.app_id}"
        self.loop = None
        self.stop_event = threading.Event()
        self.balance_lock = Lock()
        self.balances = {}  # Store balances for primary and MT5 accounts
        self.cashier_url = None  # Store the cashier URL
        self.websocket = None  # Ensure WebSocket instance is tracked
        atexit.register(self.shutdown_handler)
    

    # Establish WebSocket connection
    async def connect(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                self.websocket = websocket
                print("[open] Connection established")
                await self.authorize_session()
                
                while not self.stop_event.is_set():
                    try:
                        response = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                        data = json.loads(response)
                        print(f"[message] Data received from server: {data}")
                        
                        # Handle balance responses (Balance API)
                        if data.get("msg_type") == "balance":
                            self.handle_account_balance(data)
                            self.update_clients(data)
                        
                        # Handle cashier responses (Cashier API)
                        if data.get("msg_type") == "cashier":
                            self.handle_cashier_response(data)
                    except asyncio.TimeoutError:
                        continue
        except websockets.ConnectionClosedError as e:
            print(f"[close] Connection closed unexpectedly, code={e.code}, reason={e.reason}")
            self.websocket = None
        except Exception as e:
            print(f"[error] {str(e)}")
            self.websocket = None
        finally:
            if self.websocket:
                await self.websocket.close()
                print("[finally] Connection closed")
            self.websocket = None

    # Authorize session (Authorize API)
    async def authorize_session(self):
        if not self.websocket:
            print("[error] WebSocket is not connected!")
            return
        
        authorize_message = json.dumps({"authorize": settings.REAL_API_TOKEN})
        print(f"[debug] Sending authorization message: {authorize_message}")
        await self.websocket.send(authorize_message)
        response = await self.websocket.recv()
        data = json.loads(response)
        print(f"[debug] Authorization response received: {data}")
        
        if data.get("msg_type") == "authorize":
            print("Authorization successful!")
            self.process_account_list(data['authorize']['account_list'])
            await self.request_account_balance()
            await asyncio.sleep(1)  # Add a delay to ensure balances are received
            await self.request_cashier_info("deposit", "doughflow", "my_verification_code")
        else:
            print("Authorization failed:", data.get("error"))

    def process_account_list(self, account_list):
        self.real_account_id = None
        self.virtual_account_id = None
        
        # Process specific real and virtual accounts
        for account in account_list:
            if account['loginid'] == "CR4609348":
                self.real_account_id = account['loginid']
                print(f"[info] Real account found: {self.real_account_id}")
            elif account['loginid'] == "VRTC6703856":
                self.virtual_account_id = account['loginid']
                print(f"[info] Virtual account found: {self.virtual_account_id}")
        
        if not self.real_account_id:
            print("[error] Real account CR4609348 not found.")
        
        if not self.virtual_account_id:
            print("[error] Virtual account VRTC6703856 not found.")
    
    # Request account balance (Balance API)
    async def request_account_balance(self):
        if not self.websocket:
            print("[error] Cannot request balance: WebSocket is not connected!")
            return
        
        if self.real_account_id:
            balance_message = json.dumps({"balance": 1, "account": self.real_account_id})
            await self.websocket.send(balance_message)
            print(f"[balance] Account balance request sent for real account: {self.real_account_id}")

        if self.virtual_account_id:
            balance_message = json.dumps({"balance": 1, "account": self.virtual_account_id})
            await self.websocket.send(balance_message)
            print(f"[balance] Account balance request sent for virtual account: {self.virtual_account_id}")

    def handle_account_balance(self, data):
        balance_info = data.get("balance", {})
        loginid = balance_info.get("loginid")
        balance = balance_info.get("balance")
        
        with self.balance_lock:
            self.balances[loginid] = balance
            print(f"Account Balance for {loginid}: {balance}")

    def update_clients(self, data):
        loginid = data.get("balance", {}).get("loginid")
        balance = {loginid: data.get("balance", {}).get("balance")}
        
        if "VRTC" in loginid:
            demo_client_instance.update_balances(balance)
            print(f"[debug] Demo account balance updated for {loginid}: {balance}")
        else:
            real_client_instance.update_balances(balance)
            print(f"[debug] Real account balance updated for {loginid}: {balance}")

    # Request cashier information (Cashier API)
    async def request_cashier_info(self, cashier, provider, verification_code):
        if not self.websocket:
            print("[error] Cannot request cashier info: WebSocket is not connected!")
            return
        
        if self.real_account_id:
            print(f"[info] Requesting cashier info for real account: {self.real_account_id}")
            cashier_message = json.dumps({
                "cashier": cashier,
                "provider": provider,
                "verification_code": verification_code,
                
            })
            await self.websocket.send(cashier_message)
            print("[cashier] Cashier info request sent")
        else:
            print("[error] Real account is not set!")

    def handle_cashier_response(self, data):
        if not self.websocket:
            print("[error] WebSocket client is not set in handle_cashier_response")
        if "error" in data:
            self.notify_user(data['error'].get('message', 'Unknown error'))
        else:
            cashier_url = data.get("cashier")
            if self.is_valid_cashier_url(cashier_url):
                self.cashier_url = cashier_url
                real_client_instance.update_cashier_url(cashier_url)  # Call update_cashier_url
                print(f"Cashier URL: {self.cashier_url}")
            else:
                self.notify_user("Invalid Cashier URL.")

    def notify_user(self, message):
        print(f"[notification] {message}")

    # Security check: Ensure cashier URL is valid
    def is_valid_cashier_url(self, url):
        pattern = r"^https:\/\/cashier\.deriv\.com\/login\.asp\?.*"
        return re.match(pattern, url) is not None

    # Close WebSocket connection
    async def close(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    # Start WebSocket client
    def start(self):
        print("[start] Starting WebSocket client...")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        self.loop.run_until_complete(self.connect())

    # Stop WebSocket client
    def stop(self):
        print("[stop] Stopping WebSocket client...")
        self.stop_event.set()
        asyncio.run_coroutine_threadsafe(self.close(), self.loop).result()
        self.loop.stop()
        self.loop.close()
        self.thread.join()
        print("[stop] WebSocket client stopped")

    # Handle application shutdown
    def shutdown_handler(self):
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.close(), self.loop).result()

# Start WebSocket client function
client_instance = None

def start_websocket_client(app_id, api_token):
    global client_instance

    if client_instance is None:
        client_instance = WebSocketClient(app_id, api_token)
    
    return client_instance
