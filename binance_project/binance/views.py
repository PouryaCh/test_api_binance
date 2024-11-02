# import requests
# import time
# from concurrent.futures import ThreadPoolExecutor
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import BinancePair

# from .serializer import BinancePairSerializer






# class BinancePairs(APIView):
    
#     def get(self, request):
#         url = 'https://api.binance.com/api/v3/ticker/price'

#         starttime = time.time()
        
#         successful_requests = 0
#         errors = 0
        
#         datas = []

#         for _ in range(20):  
#             response = requests.get(url)
#             if response.status_code == 200:
#                 successful_requests += 1
#                 datas.append(response.json())
#             else:
#                 errors += 1
                
#             time.sleep(1)
            
            
            
        
#         endtime = time.time()
#         totaltime = endtime - starttime

        
#         return Response({
#             'message': f'Total time for 50 requests: {totaltime:.2f} seconds',
#             'successful_requests': successful_requests,
#             'errors': errors,
#             'datas': datas
#         }, status=status.HTTP_200_OK)


# ********************************************************

# def fetch_data(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status() 
#         return response.json()  
#     except requests.exceptions.RequestException as e:
#         return {'error': str(e)} 


# class BinancePairsView(APIView):
    
#     def get(self, request):
#         url = 'https://api.binance.com/api/v3/ticker/price'
#         num_requests = 20
#         num_threads = 10
#         delay_between_batches = 2  
        
#         successful_requests = 0
#         errors = []
#         datas = []

#         starttime = time.time()  

#         with ThreadPoolExecutor(max_workers=num_threads) as executor:
#             for i in range(0, num_requests, num_threads):

#                 futures = [executor.submit(fetch_data, url) for _ in range(num_threads)]
                
                
#                 for future in futures:
#                     result = future.result()
#                     if result and 'error' not in result:
#                         successful_requests += 1
#                         datas.append(result)
                        
#                         for data in result:
#                             serializer = BinancePairSerializer(data={
#                                 'symbol' : data['symbol'],
#                                 'price' : data['price']
#                             })
#                             if serializer.is_valid():
#                                 serializer.save()
#                             else:
#                                 errors.append(serializer.errors) 
                       
#                     else:
#                         errors.append(result.get("error", "Unknown error"))
                    

                
#                 time.sleep(delay_between_batches)

#         endtime = time.time()  
#         totaltime = endtime - starttime  
        
#         return Response({
#             'message': f'Total requests: {num_requests}',
#             'successful_requests': successful_requests,
#             'errors': errors,
#             'total_time': f'{totaltime:.2f} seconds',  
#             'datas': datas
#         }, status=status.HTTP_200_OK)



# **************************************************************

# import requests
# import time
# from concurrent.futures import ThreadPoolExecutor
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# def fetch_data(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return None
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

# class BinancePairs(APIView):
    
#     def get(self, request):
#         url = 'https://api.wallex.ir/v1/markets'
#         num_requests = 50  # تعداد درخواست‌ها
#         num_threads = 20   # تعداد ترد‌های همزمان
#         delay_between_batches = 2  # وقفه بین هر دسته درخواست
        
#         successful_requests = 0
#         errors = 0
#         datas = []

#         starttime = time.time()  # زمان شروع

#         # استفاده از ThreadPoolExecutor برای مالتی‌تردینگ
#         with ThreadPoolExecutor(max_workers=num_threads) as executor:
#             for i in range(0, num_requests, num_threads):
#                 futures = [executor.submit(fetch_data, url) for _ in range(num_threads)]
                
#                 # جمع‌آوری نتایج
#                 for future in futures:
#                     result = future.result()
#                     if result:
#                         successful_requests += 1
#                         datas.append(result)
#                     else:
#                         errors += 1

#                 # اضافه کردن وقفه بین هر دسته از درخواست‌ها
#                 time.sleep(delay_between_batches)

#         endtime = time.time()  # زمان پایان
#         totaltime = endtime - starttime  # زمان کل صرف شده

#         return Response({
#             'message': f'Total requests: {num_requests}',
#             'successful_requests': successful_requests,
#             'errors': errors,
#             'total_time': f'{totaltime:.2f} seconds',  # زمان کل
#             'datas': datas
#         }, status=status.HTTP_200_OK)

# **************************************************************************************

import requests
import time
import logging
from django.db import transaction
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pairs, PairsKlines
from rest_framework.pagination import PageNumberPagination
from .serializer import PairsSerializer
from concurrent.futures import ThreadPoolExecutor, as_completed

class PairsView(APIView, PageNumberPagination):
    
    def get(self, request):
        url = 'https://api.binance.com/api/v3/ticker/price'
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            pairs_data = response.json()
            
            saved_pairs = []
            for pair in pairs_data:
                pair_obj, created = Pairs.objects.update_or_create(
                    symbol=pair['symbol'],
                    defaults={'price': pair['price']}
                )
                saved_pairs.append({
                    'symbol': pair_obj.symbol,
                    'price': str(pair_obj.price),
                })
                
            result = self.paginate_queryset(saved_pairs, request, view=self)
            serializer = PairsSerializer(result, many=True)
            
            return Response({
                'message': 'Pairs data fetched and saved successfully',
                'count': len(saved_pairs), 
                'next': self.get_next_link(),  
                'previous': self.get_previous_link(),  
                'current_page': request.query_params.get('page', 1),  
                'total_pages': (len(saved_pairs) + self.page_size - 1) // self.page_size,  
                'pairs': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class KlinesView(APIView):
    def get(self, request):
        # Get market information from Binance
        url = 'https://api.binance.com/api/v3/ticker/24hr'
        try:
            response = requests.get(url)
            response.raise_for_status()
            market_data = response.json()
        except Exception as e:
            return Response({"message": f"Error fetching market data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Sort data based on transaction volume
        def get_volume(item):
            return float(item['volume'])

        sorted_market_data = sorted(market_data, key=get_volume, reverse=True)
        top_100_symbols = [data['symbol'] for data in sorted_market_data[:50]]

        # Disable all symbols and enable top 100 icons
        with transaction.atomic():
            Pairs.objects.update(is_active=False)
            Pairs.objects.filter(symbol__in=top_100_symbols).update(is_active=True)

        # Get and save keylines for 100 active sybols
        active_pairs = Pairs.objects.filter(is_active=True)
        klines_url = 'https://api.binance.com/api/v3/klines'
        all_klines_data = []

        for pair in active_pairs:
            params = {'symbol': pair.symbol, 'interval': '1h', 'limit': 5}
            try:
                response = requests.get(klines_url, params=params)
                response.raise_for_status()
                klines_data = response.json()

                pair_klines = []
                for kline in klines_data:
                    kline_obj, created = PairsKlines.objects.update_or_create(
                        pair=pair,
                        open_time=datetime.fromtimestamp(kline[0] / 1000),
                        defaults={
                            'open_price': kline[1],
                            'high_price': kline[2],
                            'low_price': kline[3],
                            'close_price': kline[4],
                            'volume': kline[5],
                            'close_time': datetime.fromtimestamp(kline[6] / 1000),
                            'trades_count': kline[8]
                        }
                    )
                    pair_klines.append({
                        'open_time': kline_obj.open_time,
                        'open_price': str(kline_obj.open_price),
                        'high_price': str(kline_obj.high_price),
                        'low_price': str(kline_obj.low_price),
                        'close_price': str(kline_obj.close_price),
                        'volume': str(kline_obj.volume),
                        'close_time': kline_obj.close_time,
                        'trades_count': kline_obj.trades_count,
                        'is_new': created
                    })
                
                all_klines_data.append({'symbol': pair.symbol, 'klines': pair_klines})
            except Exception as e:
                continue  

        return Response({
            'message': 'Klines data fetched and saved successfully for top 100 pairs',
            'data': all_klines_data
        }, status=status.HTTP_200_OK)
