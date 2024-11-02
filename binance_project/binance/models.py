# from django.db import models

# # Create your models here.
# # binance/models.py
# from django.db import models

# class BinancePair(models.Model):
#     symbol = models.CharField(max_length=10, unique=True)
#     price = models.DecimalField(max_digits=20, decimal_places=8)

#     def __str__(self):
#         return self.symbol


# from django.db import models

# class BinancePair(models.Model):
#     symbol = models.CharField(max_length=20)
#     price = models.DecimalField(max_digits=20, decimal_places=8)
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self) :
#         return f"{sead lf.symbol} : {self.price}"

from django.db import models



class Pairs(models.Model):
    
    symbol = models.CharField(max_length=20)
    price =  models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=30, decimal_places=10, default=0)  
    is_active = models.BooleanField(default=True)
    
    def __str__(self) :
        return f"{self.symbol} : {self.price}"


class PairsKlines(models.Model):
    pair = models.ForeignKey(Pairs, on_delete=models.CASCADE, related_name='klines')
    open_time = models.DateTimeField()
    open_price = models.DecimalField(max_digits=20, decimal_places=8)
    high_price = models.DecimalField(max_digits=20, decimal_places=8)
    low_price = models.DecimalField(max_digits=20, decimal_places=8)
    close_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=8)
    close_time = models.DateTimeField()
    trades_count = models.IntegerField()

    def __str__(self):
        return f"{self.pair.symbol} - {self.close_time}"

