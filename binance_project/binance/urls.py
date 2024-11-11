# binance/urls.py

# from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ExchangeView, PairsView, KlinesView

# router =DefaultRouter()

# router.register('pairs', views.BinancePairs,)



urlpatterns = [
    
    path('exchanges/', ExchangeView.as_view(), name='exchange-list'),
    path('<str:exchange_name>/pairs/', PairsView.as_view(), name='pairs-list'),
    path('<str:exchange_name>/klines', KlinesView.as_view(), name='klines_list'),
]
