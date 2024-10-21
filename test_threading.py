import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Binance API URL
url = 'https://api.binance.com/api/v3/ticker/price'

# Function to send a request to the API and display the time
def fetch(url, attempt):
    start_time = time.time()  # Start time
    try:
        response = requests.get(url)
        elapsed_time = time.time() - start_time  # Time taken
        print(f"Request number {attempt} with status code: {response.status_code} and time: {elapsed_time:.2f} seconds")  # Print status code and time
        if response.status_code == 451:
            print(f"Access to the resource is not available for legal reasons in request number {attempt}.")
            return None
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error in request number {attempt}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error in request number {attempt}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error in request number {attempt}: {timeout_err}")
    except Exception as err:
        print(f"General error in request number {attempt}: {err}")
    return None

# Measure the total start time
start_time = time.time()

# Number of requests
num_requests = 500

# Use ThreadPoolExecutor to manage threads
with ThreadPoolExecutor(max_workers=20) as executor:  # Set maximum number of threads
    futures = {executor.submit(fetch, url, i + 1): i + 1 for i in range(num_requests)}
    
    for future in as_completed(futures):
        attempt = futures[future]
        try:
            result = future.result()
            if result:
                print(f"Result of request number {attempt}: {result}")
            else:
                print(f"Error in request number {attempt}")
        except Exception as exc:
            print(f"Request number {attempt} encountered an error: {exc}")

# Measure the end time
end_time = time.time()

# Calculate total elapsed time
elapsed_time = end_time - start_time
print(f"Total time for 500 requests: {elapsed_time:.2f} seconds")
