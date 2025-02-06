#Perform Deriv API calls related to demo accounts.
import threading
import logging

class DemoClient:
    def __init__(self):
        self.balance_lock = threading.Lock()
        self.balances = {}
        self.logger = logging.getLogger(__name__)

    def update_balances(self, balances):
        with self.balance_lock:
            self.balances.update(balances)
            self.logger.info(f"Updated Demo Balances: {self.balances}")

demo_client_instance = DemoClient()
