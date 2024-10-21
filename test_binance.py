import requests
import time

# Binance API URL
url = 'https://api.binance.com/api/v3/ticker/price'

# Function to send a request to the API and display the status code
def fetch(url, attempt=1):
    try:
        response = requests.get(url)
        print(f"Request number {attempt} with status code: {response.status_code}")  # Print status code
        response.raise_for_status()  # Raise an error for HTTP status codes that indicate an error
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

# Measure start time
start_time = time.time()

# Send 500 requests sequentially
results = []
for i in range(500):
    result = fetch(url, i+1)  # Send request and display status code
    if result:
        results.append(result)
    else:
        print(f"Error in request number {i+1}")

# Measure end time
end_time = time.time()

# Calculate total time
elapsed_time = end_time - start_time
print(f"Total time for 500 requests: {elapsed_time} seconds")
