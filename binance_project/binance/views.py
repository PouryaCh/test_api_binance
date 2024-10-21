import requests
import time
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializer import BinancePairSerializer


# class BinancePairs(APIView):
    
#     # serializer_class = BinancePairSerializer
    
#     def get(self, request):
#         url = 'https://api.binance.com/api/v3/ticker/price'
#         response = requests.get(url)

#         if response.status_code == 200:
#             pairs_data = response.json()
#             return Response(pairs_data, status=status.HTTP_200_OK)
#         return Response({'error': 'Failed to fetch data from Binance'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



import requests
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BinancePairs(APIView):
    
    def get(self, request):
        url = 'https://api.binance.com/api/v3/ticker/price'

        starttime = time.time()

        for _ in range(10):  
            response = requests.get(url)
            if response.status_code != 200:
                return Response({'error': f'Error: {response.status_code}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # return response.json()
            
            
        
        endtime = time.time()
        totaltime = endtime - starttime

        
        return Response({'message': f'Total time for 500 requests: {totaltime:.2f} seconds'}, status=status.HTTP_200_OK)
