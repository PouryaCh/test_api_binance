from django.shortcuts import render

# binance/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BinancePairsView(APIView):
    def get(self, request):
        url = 'https://api.binance.com/api/v3/ticker/price'
        response = requests.get(url)

        if response.status_code == 200:
            pairs_data = response.json()
            return Response(pairs_data, status=status.HTTP_200_OK)
        return Response({'error': 'Failed to fetch data from Binance'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
