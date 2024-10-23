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
        url = 'https://api.wallex.ir/v1/markets'

        starttime = time.time()
        
        successful_requests = 0
        errors = 0
        
        datas = []

        for _ in range(10):  
            response = requests.get(url)
            if response.status_code == 200:
                successful_requests += 1
                datas.append(response.json())
            else:
                errors += 1
                
            time.sleep(1)
            
            
            
        
        endtime = time.time()
        totaltime = endtime - starttime

        
        return Response({
            'message': f'Total time for 50 requests: {totaltime:.2f} seconds',
            'successful_requests': successful_requests,
            'errors': errors,
            'datas': datas
        }, status=status.HTTP_200_OK)

