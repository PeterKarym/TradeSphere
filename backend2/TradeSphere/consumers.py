import json
import logging
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

logger = logging.getLogger('trading')

class TradingConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            'trading_group',
            self.channel_name
        )
        logger.info(f"WebSocket connection accepted and client added to trading_group: {self.channel_name}")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'trading_group',
            self.channel_name
        )
        logger.info(f"WebSocket connection closed and client removed from trading_group: {self.channel_name}")

    def receive(self, text_data):
        logger.info(f"WebSocket message received: {text_data}")
        try:
            data = json.loads(text_data)
            signal_type = data['signalType']
            price = data['price']
            timestamp = data['timestamp']
            symbol = data['symbol']
            formatted_message = data['formatted_message']
            logger.info(f"Processed WebSocket message: {formatted_message}")
            self.send(text_data=json.dumps({'status': 'Signal processed', 'message': formatted_message}))
            logger.info(f"Response sent to client")

            async_to_sync(self.channel_layer.group_send)(
                'trading_group',
                {
                    'type': 'trading_message',
                    'message': {
                        'signalType': signal_type,
                        'price': price,
                        'timestamp': timestamp,
                        'symbol': symbol,
                        'formatted_message': formatted_message
                    }
                }
            )
            logger.info(f"Broadcast message sent to trading_group: {formatted_message}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def trading_message(self, event):
        logger.info(f"Trading message received: {event}")
        try:
            message = event['message']
            formatted_message = message['formatted_message']
            logger.info(f"Received trading message: {formatted_message}")
            self.send(text_data=json.dumps({'message': formatted_message}))
            logger.info(f"Trading message sent to client")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
