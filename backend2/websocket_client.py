import asyncio
import websockets
import json
import threading
import atexit

class WebSocketClient:
    def __init__(self, app_id):
        self.app_id = app_id
        self.uri = f"wss://ws.derivws.com/websockets/v3?app_id={self.app_id}"
        self.loop = asyncio.new_event_loop()
        self.stop_event = threading.Event()

        # Register a shutdown handler
        atexit.register(self.shutdown_handler)

    async def connect(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                self.websocket = websocket
                print("[open] Connection established")
                
                     # Subscribing to Ticks for a Different Symbol
                subscribe_message = json.dumps({
                    "ticks": "R_100",  # Replace with your desired symbol
                    "subscribe": 1
                })
                await self.websocket.send(subscribe_message)
                
                # Requesting Historical Data
                historical_data_request = json.dumps({
                    "ticks_history": "R_50",  # Replace with your desired symbol
                    "end": "latest",
                    "count": 10,  # Number of data points
                    "subscribe": 1
                })
                await self.websocket.send(historical_data_request)

                # Handling Responses that were requested above
                while not self.stop_event.is_set():
                    try:
                        response = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                        data = json.loads(response)
                        print(f"[message] Data received from server: {data}")
                        # Handle specific types of responses
                        if data.get("msg_type") == "tick":
                            # Process tick data
                            pass
                        elif data.get("msg_type") == "history":
                            # Process historical data
                            print(f"[history] Historical data received: {data['history']}")
                            pass
                        elif data.get("msg_type") == "buy":
                            # Process trade confirmation
                            pass
                    except asyncio.TimeoutError:
                        continue

        except websockets.ConnectionClosedError as e:
            print(f"[close] Connection closed with error, code={e.code}, reason={e.reason}")
        except Exception as e:
            print(f"[error] {str(e)}")
        finally:
            if self.websocket:
                await self.websocket.close()
                print("[finally] Connection closed in finally block")
                print("[notification] WebSocket connection closed")

    async def close(self):
        if self.websocket:
            print("[close] Closing connection...")
            await self.websocket.close()
            print("[close] Connection closed by client")
            print("[notification] WebSocket connection closed")

    def start(self):
        print("[start] Starting WebSocket client...")
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())

    def stop(self):
        print("[stop] Stopping WebSocket client...")
        self.stop_event.set()
        asyncio.run_coroutine_threadsafe(self.close(), self.loop).result()
        self.loop.stop()
        self.loop.close()
        self.thread.join()
        print("[stop] WebSocket client stopped")

    def shutdown_handler(self):
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.close(), self.loop).result()

def start_websocket_client():
    client = WebSocketClient(app_id=1089)  # Replace with your app_id
    return client






# Example usage:
# client = start_websocket_client()
# client.start()
# client.stop()




'''
Instructions to run this code:

1. Ensure Python 3 is installed on your machine. You can download it from https://www.python.org/.
2. Install the `websockets` library by running:
   pip install websockets
3. Save this code to a file, e.g., `websocket_client.py`.
4. Open a terminal and navigate to the directory where you saved the file.
5. Run the code using the following command:
   python websocket_client.py

Replace `app_id` with your own application ID if needed.
'''
