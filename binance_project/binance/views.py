import requests
import time
from concurrent.futures import ThreadPoolExecutor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status






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

def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
    except Exception as e:
        print(f"Error fetching data from Binance: {e}")
    return None


class BinancePairs(APIView):
    
    def get(self, request):
        url = 'https://api.binance.com/api/v3/ticker/price'
        num_requests = 20  # تعداد درخواست‌ها
        num_threads = 20  # تعداد ترد‌های همزمان
        delay_between_batches = 2  # وقفه بین هر دسته درخواست
        
        successful_requests = 0
        errors = []
        datas = []

        starttime = time.time()  # زمان شروع

        # استفاده از ThreadPoolExecutor برای مالتی‌تردینگ
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for i in range(0, num_requests, num_threads):
                futures = [executor.submit(fetch_data, url) for _ in range(num_threads)]
                
                # جمع‌آوری نتایج
                for future in futures:
                    result = future.result()
                    if result:
                        successful_requests += 1
                        datas.append(result)
                    else:
                        errors.append(result.get("error", "Unknown error"))
                    

                # اضافه کردن وقفه بین هر دسته از درخواست‌ها
                time.sleep(delay_between_batches)

        endtime = time.time()  # زمان پایان
        totaltime = endtime - starttime  # زمان کل صرف شده

        return Response({
            'message': f'Total requests: {num_requests}',
            'successful_requests': successful_requests,
            'errors': errors,
            'total_time': f'{totaltime:.2f} seconds',  # زمان کل
            'datas': datas
        }, status=status.HTTP_200_OK)



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

