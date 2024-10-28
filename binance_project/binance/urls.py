# binance/urls.py

# from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PairsView

# router =DefaultRouter()

# router.register('pairs', views.BinancePairs,)



urlpatterns = [
    
    path('pairs/', PairsView.as_view(), name='binance_pairs')
]
