# binance/urls.py

# from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BinancePairsView

# router =DefaultRouter()

# router.register('pairs', views.BinancePairs,)



urlpatterns = [
    
    path('pairs/', BinancePairsView.as_view(), name='binance_pairs')
]
