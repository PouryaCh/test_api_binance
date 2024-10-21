import socket
import threading
import time

# تعریف آدرس و پورت سرور بایننس
HOST = 'api.binance.com'
PORT = 80

# تعداد درخواست‌ها
num_requests = 500
lock = threading.Lock()  # قفل برای جلوگیری از تداخل

# تابع برای ارسال یک درخواست
def send_request(request_number):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        request = f"GET /api/v3/ticker/price HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())
        response = s.recv(4096)  # دریافت پاسخ
        
        with lock:
            print(f"Response {request_number}: {response.decode()}")

# زمان شروع
start_time = time.time()

# ایجاد و راه‌اندازی نخ‌ها
threads = []
for i in range(num_requests):
    thread = threading.Thread(target=send_request, args=(i + 1,))
    threads.append(thread)
    thread.start()

# انتظار برای اتمام همه نخ‌ها
for thread in threads:
    thread.join()

# زمان پایان و محاسبه زمان کل
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total time for {num_requests} requests: {elapsed_time:.2f} seconds")
