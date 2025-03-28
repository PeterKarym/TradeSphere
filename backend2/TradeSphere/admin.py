from django.contrib import admin
from .models import TradingSignal

@admin.register(TradingSignal)
class TradingSignalAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'signal_type', 'price', 'timestamp')
    list_filter = ('symbol', 'signal_type', 'timestamp')
    search_fields = ('symbol', 'signal_type', 'timestamp')
