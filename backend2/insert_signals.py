import time
import json
import logging
import os
import django
from datetime import datetime
from django.utils.timezone import make_aware

# Set up Django to use your settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'derivapp.settings')
django.setup()

from TradeSphere.models import TradingSignal  # Use your Django model

# File where MT5 writes the signals (e.g., signals.json)
SIGNAL_FILE = r'C:\Users\hp\AppData\Roaming\MetaQuotes\Terminal\Common\Files\signals.json'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Insert a signal using Django ORM instead of psycopg2 ---
def insert_signal(symbol, signal_type, price, timestamp):
    """Insert a trading signal into the database using Django's ORM."""
    try:
        # Match the timestamp format in your signal data
        ts = datetime.strptime(timestamp, '%Y.%m.%d %H:%M:%S')
        ts_aware = make_aware(ts)  # Make timezone-aware
        TradingSignal.objects.create(
            symbol=symbol,
            signal_type=signal_type,
            price=price,
            timestamp=ts_aware
        )
        logging.info(f"Signal inserted: {symbol}, {signal_type}, {price}, {timestamp}")
    except Exception as e:
        logging.error(f"Error inserting signal: {e}")



# --- Monitor the file and process signals ---
def monitor_signal_file():
    """Monitor the signals.json file and insert new signals into the database."""
    try:
        while True:
            try:
                # Open the file with 'utf-16-le' encoding (consistent with your file format)
                with open(SIGNAL_FILE, 'r', encoding='utf-16-le') as file:
                    raw = file.read().strip()
                
                # Attempt to parse the JSON content
                try:
                    signals = json.loads(raw)
                except json.JSONDecodeError as e:
                    logging.error(f"JSONDecodeError: {e}")
                    logging.error("Content of signals.json is invalid.")
                    logging.error("Raw content of signals.json: " + repr(raw))
                    time.sleep(5)  # Wait before retrying
                    continue

                # List to store unprocessed signals
                unprocessed_signals = []

                # Process each signal in the JSON array
                for signal in signals:
                    symbol = signal.get('symbol')
                    signal_type = signal.get('signalType')
                    price = signal.get('price')
                    timestamp = signal.get('timestamp')

                    # Validate the signal's fields
                    if not (symbol and signal_type and price and timestamp):
                        logging.error(f"Invalid signal format: {signal}")
                        unprocessed_signals.append(signal)
                        continue

                    # Try inserting the signal into the database via Django ORM
                    try:
                        insert_signal(symbol, signal_type, price, timestamp)
                    except Exception as e:
                        logging.error(f"Error inserting signal {signal}: {e}")
                        unprocessed_signals.append(signal)
                    else:
                        logging.info(f"Successfully processed signal: {symbol}, {signal_type}, {price}, {timestamp}")

                # Log a summary of processed vs unprocessed signals
                logging.info(f"Processed {len(signals) - len(unprocessed_signals)} signals. Remaining unprocessed: {len(unprocessed_signals)}")

                # Rewrite the signals.json file with only unprocessed signals
                with open(SIGNAL_FILE, 'w', encoding='utf-16-le') as file:
                    json.dump(unprocessed_signals, file, indent=4)

                if unprocessed_signals:
                    logging.info("Unprocessed signals retained in signals.json.")
                else:
                    logging.info("All signals have been processed. Waiting for new signals.")

                time.sleep(5)  # Check for new signals every 5 seconds

            except FileNotFoundError:
                logging.warning(f"Signal file {SIGNAL_FILE} not found. Waiting for it to be created...")
                time.sleep(5)
    except KeyboardInterrupt:
        logging.info("File monitoring stopped.")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

if __name__ == '__main__':
    monitor_signal_file()
