from django.db import models

# Create your models here.
# binance/models.py
from django.db import models

class BinancePair(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return self.symbol
