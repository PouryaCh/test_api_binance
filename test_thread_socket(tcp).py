import socket
import threading
import time

# Define the Binance server address and port
HOST = 'api.binance.com'
PORT = 80

# Number of requests
num_requests = 500
lock = threading.Lock()  # Lock to prevent interference between threads

# Function to send a single request
def send_request(request_number):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        request = f"GET /api/v3/ticker/price HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())
        response = s.recv(4096)  # Receive response
        
        with lock:
            print(f"Response {request_number}: {response.decode()}")

# Start time
start_time = time.time()

# Create and start threads
threads = []
for i in range(num_requests):
    thread = threading.Thread(target=send_request, args=(i + 1,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# End time and total time calculation
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total time for {num_requests} requests: {elapsed_time:.2f} seconds")
