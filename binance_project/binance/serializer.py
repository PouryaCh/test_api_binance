# binance/serializers.py
from rest_framework import serializers
from .models import BinancePair

class BinancePairSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinancePair
        fields = ['symbol', 'price']
