from django.db import models

class TradingSignal(models.Model):
    symbol = models.CharField(max_length=50)
    signal_type = models.CharField(max_length=10)  # BUY or SELL
    price = models.DecimalField(max_digits=10, decimal_places=5)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'trading_signals'  # Use the existing table name

