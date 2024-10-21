import requests
import time
import threading

# Binance API URL
url = 'https://api.binance.com/api/v3/ticker/price'

# Number of requests
num_requests = 500

# Lock for preventing print interference
print_lock = threading.Lock()

# Function to send a request to the API and display time
def fetch(attempt):
    start_time = time.time()  # Start time
    try:
        response = requests.get(url)
        elapsed_time = time.time() - start_time  # Time taken
        
        with print_lock:
            print(f"Request number {attempt} with status code: {response.status_code} and time: {elapsed_time:.2f} seconds")  # Print status code and time
        
        if response.status_code == 451:
            with print_lock:
                print(f"Access to the resource is unavailable for legal reasons in request number {attempt}.")
            return None
        
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        with print_lock:
            print(f"HTTP error in request number {attempt}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        with print_lock:
            print(f"Connection error in request number {attempt}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        with print_lock:
            print(f"Timeout error in request number {attempt}: {timeout_err}")
    except Exception as err:
        with print_lock:
            print(f"General error in request number {attempt}: {err}")
    return None

# Measure the overall start time
start_time = time.time()

# List to store threads
threads = []

# Create and start threads
for i in range(1, num_requests + 1):
    thread = threading.Thread(target=fetch, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Measure the end time
end_time = time.time()

# Calculate total time
elapsed_time = end_time - start_time
print(f"Total time for 500 requests: {elapsed_time:.2f} seconds")
