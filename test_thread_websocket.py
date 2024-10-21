import websocket
import json
import threading
import time

# تعداد درخواست‌ها
num_requests = 500
received_messages = 0
lock = threading.Lock()  # قفل برای جلوگیری از تداخل

# تابع برای پردازش پیام‌ها
def on_message(ws, message):
    global received_messages
    with lock:
        received_messages += 1  # افزایش شمارش پیام‌های دریافتی
        print(f"Received message {received_messages}: {message}")

# تابع برای مدیریت خطاها
def on_error(ws, error):
    print(f"Error: {error}")

# تابع برای بستن ارتباط
def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

# تابع برای شروع ارتباط
def on_open(ws):
    print("Connection opened")
    # ارسال پیام اشتراک برای دریافت داده‌های معاملاتی
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@trade",  # نمونه‌ای از جفت ارز
        ],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))

# آدرس وب‌سوکت بایننس
socket_url = "wss://stream.binance.com:9443/ws"

# زمان شروع
start_time = time.time()

# ایجاد وب‌سوکت
ws = websocket.WebSocketApp(socket_url,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# شروع ارتباط
ws.on_open = on_open

# اجرای وب‌سوکت در یک رشته جداگانه
ws_thread = threading.Thread(target=ws.run_forever)
ws_thread.start()

# صبر کنید تا تعداد درخواست‌ها دریافت شود
while received_messages < num_requests:
    time.sleep(0.1)  # مدت زمان کوتاه برای چک کردن شمارش

# بستن وب‌سوکت
ws.close()

# زمان پایان و محاسبه زمان کل
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total time for {num_requests} messages: {elapsed_time:.2f} seconds")
