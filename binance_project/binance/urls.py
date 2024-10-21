# binance/urls.py
from django.urls import path
from .views import BinancePairsView

urlpatterns = [
    path('pairs/', BinancePairsView.as_view(), name='binance_pairs'),
]
